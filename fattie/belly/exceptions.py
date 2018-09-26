import sys


class BigError(SyntaxError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Syntax error'

    def print(self, lineno):
        print(self.err_name + ' at line {}: '.format(lineno) + self.msg, file=sys.stderr)

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
