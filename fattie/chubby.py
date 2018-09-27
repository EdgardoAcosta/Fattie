from fattie.belly.fluffyvariabletable import FluffyVariableTable
from fattie.belly.heavyfunctiontable import HeavyFunctionTable
from fattie.belly.exceptions import BigError


class Chubby:
    # Constructor of class
    def __init__(self):
        self._global_variable = FluffyVariableTable('global')
        self._local_variable = FluffyVariableTable()
        self._functions = HeavyFunctionTable()

    def add_global_variable(self, id_var, type_variable, value=None):
        self._global_variable.add_variable(id_var, type_variable, value)

    def add_local_variable(self, id_var, type_variable, value=None):
        self._local_variable.add_variable(id_var, type_variable, value)

    def find_variable(self, id_var):
        local_variable = self._local_variable.find_variable(id_var)
        global_variable = self._local_variable.find_variable(id_var)

        if local_variable is not None:
            return local_variable
        elif global_variable is not None:
            return global_variable
        else:
            raise BigError.undefined_variable('Variable not defined')

    def add_function(self, id_fun, return_type=None, params = None):
        self._functions.add_function(id_fun, return_type, params)

    def find_function(self, id_fun):
        func = self._functions.find_function(id_fun)

        if func is None:
            return func
        else:
            raise BigError.undefined_function('Function Undefined')
