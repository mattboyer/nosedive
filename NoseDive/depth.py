from __future__ import print_function

import inspect
import logging
import sys
import types

from nose.plugins import Plugin


log = logging.getLogger('nose.plugins.depth')


class TestTracer(object):
    def __init__(self, test_module_path):
        self.test_module_path = test_module_path
        # This is the index of the first frame in the stack that originates in
        # the test module
        self.test_frame_idx = None
        self.modules_in_test_frame_globals = None
        self.call_stacks = []

    def __call__(self, frame, event, arg):
        if 'call' != event:
            return None

        previous_frames = inspect.getouterframes(frame)
        if not self.test_frame_idx:
            # We need to determine whether or not we're being called from the
            # test module (however indirectly).

            # NOTE We have frame == previous_frames[0][0]
            if len(previous_frames) <= 1:
                return None

            for frame_idx, caller_frame_info in enumerate(previous_frames):
                if caller_frame_info[1] != self.test_module_path:
                    continue

                self.modules_in_test_frame_globals = [
                    obj for obj in caller_frame_info[0].f_globals.values() if
                    isinstance(obj, types.ModuleType)
                ]
                # What if we've found a frame that belongs to a test fixture
                # (eg. setUp) which doesn't call any product code?
                this_frame_module = inspect.getmodule(frame)
                if this_frame_module in self.modules_in_test_frame_globals:
                    self.test_frame_idx = len(previous_frames) - frame_idx - 1
                    break

        # Still not found
        if not self.test_frame_idx:
            return None

        this_frame_module = inspect.getmodule(frame)
        if this_frame_module not in self.modules_in_test_frame_globals:
            return None

        self.call_stacks.append(
            (frame, len(previous_frames) - 1 - self.test_frame_idx)
        )


class DepthPlugin(Plugin):
    # This is the name that will appear in the output of 'nosetests -p'
    # TODO Dynamically derive this from the package path
    name = 'nosedive'

    def __init__(self):
        super(DepthPlugin, self).__init__()
        self.stacks = {}

    def prepareTestCase(self, test):
        # TODO Test this for module-level tests
        log.info('Tracing calls from %s', test)

        # Let's assume that this Python interpreter *does* implement
        # sys.gettrace/settrace
        try:
            sys.gettrace()
        except RuntimeError:
            raise SystemError('NoseDive requires sys.settrace')

        tracer = TestTracer(inspect.getmodule(test.test).__file__)
        sys.settrace(tracer)

    def stopTest(self, test):
        tracer = sys.gettrace()
        sys.settrace(None)
        self.stacks[test.test] = tracer.call_stacks

    def report(self, output_stream):
        for test in self.stacks:
            print("Stacks seen in test: %s" % test, file=output_stream)
            for stack, depth in self.stacks[test]:
                print("\t%s: %d" % (
                        self._print_frame(stack), depth
                    ), file=output_stream)

    def _print_frame(self, frame):
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
                    try:
                        qualname = class_attr.__func__.__qualname__
                    except AttributeError:
                        qualname = '.'.join((
                            class_attr.im_class.__name__,
                            class_attr.im_func.__name__
                        ))
                    call_desc = "{module}.{callable}".format(
                        module=module_name,
                        callable=qualname
                    )

        return "{call}() [{file}:{line}]".format(
            call=call_desc,
            file=frame.f_code.co_filename,
            line=frame.f_lineno,
        )
