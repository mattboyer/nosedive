import inspect
import logging
import sys
import types

from nose.plugins import Plugin

log = logging.getLogger('nose.plugins.depth')

def _depth_tracer(frame, event, arg):
    if 'call' != event:
        return _depth_tracer

    # We need to find out what the test module is to determine whether or not
    # we're being called from it (however indirectly) or not.
    previous_frames = inspect.getouterframes(frame)

    # NOTE We have frame == previous_frames[0][0]
    this_frame_called_from_test = False
    for caller_frame_info in previous_frames[1:]:
        if caller_frame_info[1] == '/home/mboyer/Hacks/StackDepthTracer/test/tests.py':
            this_frame_called_from_test = True
            break

    if not this_frame_called_from_test:
        return None

    testcase_frame = caller_frame_info[0]

    modules_in_test_frame_globals = [
        obj for obj in testcase_frame.f_globals.values() if type(obj) is types.ModuleType
    ]

    this_frame_module = inspect.getmodule(frame)
    if not this_frame_module in modules_in_test_frame_globals:
        return None

    log.info('Entering %s from module %s', frame, this_frame_module)
    log.info('Test entry point %s', testcase_frame)

class DepthPlugin(Plugin):
    # This is the name that will appear in the output of 'nosetests -p'
    name='nosedive'

    def prepareTestCase(self, test):
        # TODO Test this for module-level tests
        log.info('Tracing calls from %s', test)

        # Let's assume that this Python interpreter *does* implement
        # sys.gettrace/settrace
        try:
            sys.gettrace()
        except AttributeError:
            raise SystemError('NoseDive requires sys.settrace')
        sys.settrace(_depth_tracer)

    def stopTest(self, test):
        sys.settrace(None)
