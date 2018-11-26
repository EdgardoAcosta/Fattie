import sys


class BigError(SyntaxError):
    def __init__(self, msg):
        self.msg = msg
        self.err_name = 'Syntax error'

    def print(self, lineno):
        print('{} at line -> {} <-: {}'.format(self.err_name, lineno, self.msg), file=sys.stderr)
        sys.exit(0)

    @staticmethod
    def undefined_function(msg):
        err = BigError(msg)
        err.err_name = 'Undefined function'
        return err

    @staticmethod
    def redefined_function(msg):
        err = BigError(msg)
        err.err_name = 'Redefined function'
        return err

    @staticmethod
    def no_empty_params(msg):
        err = BigError(msg)
        err.err_name = 'Function required params'
        return err

    @staticmethod
    def mismatch_params(msg):
        err = BigError(msg)
        err.err_name = 'Mismatch parameter'
        return err

    @staticmethod
    def redefined_variable(msg):
        err = BigError(msg)
        err.err_name = 'Redefined variable'
        return err

    @staticmethod
    def undefined_variable(msg):
        err = BigError(msg)
        err.err_name = 'Undefined variable'
        return err

    @staticmethod
    def mismatch_operator(msg):
        err = BigError(msg)
        err.err_name = 'Mismatch operator'
        return err

    @staticmethod
    def mismatch_assignation(msg):
        err = BigError(msg)
        err.err_name = 'Mismatch assignation'
        return err

    @staticmethod
    def invalid_operator(msg):
        err = BigError(msg)
        err.err_name = 'Invalid operator'
        return err

    @staticmethod
    def invalid_array(msg):
        err = BigError(msg)
        err.err_name = 'Variable is not Array type'
        return err

    @staticmethod
    def invalid_type(msg):
        err = BigError(msg)
        err.err_name = 'Invali type in expression'
        return err

    @staticmethod
    def invalid_value(msg):
        err = BigError(msg)
        err.err_name = 'Invali value'
        return err


