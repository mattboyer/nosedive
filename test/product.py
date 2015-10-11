import random

class MainClass(object):
    def dispatcher(self, input):
        doer = Doer()
        doer.do(input)

class Doer(object):
    def do(self, input):
        tester = Tester()
        if tester.test(input):
            # These two calls to str and int's respective __init__()'s may
            # raise exceptions
            int_as_string = str(input)
            print(int(int_as_string, 8))

class Tester(object):
    def test(self, input):
        if 42 == input:
            return True
        # This is a deliberate bug!
        return 'False'
