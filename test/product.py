import random

class MainClass(object):
    def dispatcher(self, input):
        doer = Doer()
        return doer.do(input)

class Doer(object):
    def do(self, input):
        delegate_instance = Delegate()
        if delegate_instance.business_logic(input):
            # These two calls to str and int's respective __init__()'s may
            # raise exceptions
            int_as_string = str(input)
            return (int(int_as_string, 8))

class Delegate(object):
    def business_logic(self, input):
        if 42 == input:
            return True
        # This is a deliberate bug!
        return 'False'
