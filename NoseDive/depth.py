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


class TestTracer(object):
    def __init__(self, test_module_path):
        self.test_module_path = test_module_path
        self.test_module_call_seen = False
        self.modules_in_test_frame_globals = None
        self.call_stacks = []

    def __call__(self, frame, event, arg):
        if 'call' != event:
            return None

        if not self.test_module_call_seen:
            # We need to determine whether or not we're being called from the
            # test module (however indirectly).
            previous_frames = inspect.getouterframes(frame)

            # NOTE We have frame == previous_frames[0][0]
            if len(previous_frames) <= 1:
                return None

            for caller_frame_info in previous_frames[1:]:
                if caller_frame_info[1] == self.test_module_path:
                    self.test_module_call_seen = True
                    self.modules_in_test_frame_globals = [
                        obj for obj in caller_frame_info[0].f_globals.values() if
                        isinstance(obj, types.ModuleType)
                    ]
                    break

        # Still not found
        if not self.test_module_call_seen:
            return None

        this_frame_module = inspect.getmodule(frame)
        if this_frame_module not in self.modules_in_test_frame_globals:
            return None

        self.call_stacks.append(frame)
        #log.info('Entering %s', print_frame(frame))


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

        tracer = TestTracer(inspect.getmodule(test.test).__file__)
        sys.settrace(tracer)


    def stopTest(self, test):
        tracer = sys.gettrace()
        sys.settrace(None)
        for product_frame in tracer.call_stacks:
            log.info('%s', print_frame(product_frame))
