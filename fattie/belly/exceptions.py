import sys


class BigError(SyntaxError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Syntax error'

    def print(self, lineno):
        print('{} at line -> {} <-: {}'.format(self.err_name, lineno, self.msg), file=sys.stderr)

    @staticmethod
    def undefined_variable(msg):
        err = BigError(msg)
        err.err_name = 'Undefined variable'
        return err

    @staticmethod
    def undefined_function(msg):
        err = BigError(msg)
        err.err_name = 'Undefined function'
        return err

    @staticmethod
    def redefined_funtion(msg):
        err = BigError(msg)
        err.err_name = 'Redefined function'
        return err

    @staticmethod
    def redefined_variable(msg):
        err = BigError(msg)
        err.err_name = 'Redefined variable'
        return err

    @staticmethod
    def mismatch_operator(msg):
        err = BigError(msg)
        err.err_name = 'Mismatch operator'
        return err

    @staticmethod
    def invalid_operator(msg):
        err = BigError(msg)
        err.err_name = 'Invalid operator'
        return err
