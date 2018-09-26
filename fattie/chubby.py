from fattie.belly.fluffyvariabletable import FluffyVariableTable
from fattie.belly.heavyfunctiontable import HeavyFunctionTable
from fattie.belly.exceptions import BigError


class Chubby:
    # Constructor of class
    def __init__(self):
        self._global_variable = FluffyVariableTable('global')
        self._local_variable = FluffyVariableTable()
        self._functions = HeavyFunctionTable()

    def add_global_variable(self, id, value):
        self._global_variable.add_variable(id, value)

    def add_local_variable(self, id, value):
        self._local_variable.add_variable(id, value)

    def find_variable(self, id):
        local_variable = self._local_variable.find_variable(id)
        global_variable = self._local_variable.find_variable(id)

        if local_variable is not None:
            return local_variable
        elif global_variable is not None:
            return global_variable
        else:
            raise BigError.undefined_variable('Variable not defined')

    def add_function(self, id, type, params):
        self._functions.add_function(id, type, params)

    def find_function(self, id):
        function = self._functions.find_function(id)

        if function is None:
            return function
        else:
            raise BigError.undefined_function('Function Undefined')
