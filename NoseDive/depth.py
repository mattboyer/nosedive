import inspect
import logging
import sys
import types

from nose.plugins import Plugin

log = logging.getLogger('nose.plugins.depth')


def print_frame(frame):
    module_name = inspect.getmodule(frame).__name__

    call_desc = "{module}::{call}".format(
        module=module_name,
        call=frame.f_code.co_name,
    )

    # This is unreliable, there's no particular requirement for the 1st
    # argument of instance method calls to be called 'self'
    if 'self' in frame.f_locals:
        calling_object = frame.f_locals.get('self')
        if calling_object and \
                hasattr(calling_object, frame.f_code.co_name):
            class_attr = getattr(calling_object, frame.f_code.co_name)
            if isinstance(class_attr, types.MethodType):
                call_desc = "{module}.{callable}".format(
                    module=module_name,
                    callable=class_attr.__func__.__qualname__,
                )

    return "{call}() [{file}:{line}]".format(
        call=call_desc,
        file=frame.f_code.co_filename,
        line=frame.f_lineno,
    )


def tracer_factory(test_module_path):

    def _depth_tracer(frame, event, arg):
        if 'call' != event:
            return _depth_tracer

        # We need to find out what the test module is to determine whether or
        # not we're being called from it (however indirectly) or not.
        previous_frames = inspect.getouterframes(frame)

        # NOTE We have frame == previous_frames[0][0]
        if len(previous_frames) <= 1:
            return None

        this_frame_called_from_test = False
        for caller_frame_info in previous_frames[1:]:
            if caller_frame_info[1] == test_module_path:
                this_frame_called_from_test = True
                break

        if not this_frame_called_from_test:
            return None

        testcase_frame = caller_frame_info[0]

        modules_in_test_frame_globals = [
            obj for obj in testcase_frame.f_globals.values() if
            isinstance(obj, types.ModuleType)
        ]

        this_frame_module = inspect.getmodule(frame)
        if this_frame_module not in modules_in_test_frame_globals:
            return None

        log.info('Entering %s', print_frame(frame))

        log.info('Test entry point %s', print_frame(testcase_frame))

    return _depth_tracer


class DepthPlugin(Plugin):
    # This is the name that will appear in the output of 'nosetests -p'
    name = 'nosedive'

    def prepareTestCase(self, test):
        # TODO Test this for module-level tests
        log.info('Tracing calls from %s', test)

        # Let's assume that this Python interpreter *does* implement
        # sys.gettrace/settrace
        try:
            sys.gettrace()
        except Exception as e:
            raise SystemError('NoseDive requires sys.settrace')
        sys.settrace(tracer_factory(inspect.getmodule(test.test).__file__))

    def stopTest(self, test):
        sys.settrace(None)
