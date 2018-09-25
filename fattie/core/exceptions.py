import sys


class FattieError(SyntaxError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Syntax error'

    def print(self, lineno):
        print(self.err_name + ' at line {}: '.format(lineno) + self.msg, file=sys.stderr)


class UndefinedVariable(FattieError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Undefined variable'
