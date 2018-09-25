from fattie.core.variabletable import VariableTable
from fattie.core.exceptions import *


class Chubby:
    # Constructor of class
    def __init__(self):
        self._global_variable = VariableTable()
        self._local_variable = VariableTable()

    def add_global_variable(self, id, value):
        self._global_variable.add_variable(id, value)

    def add_local_variable(self, id, value):
        self._local_variable.add_variable(id, value)

    def find_variable(self, id):
        local_variable = self._local_variable.find_variable(id)
        global_variable = self._local_variable.find_variable(id)

        if global_variable is None and global_variable is None:
            raise UndefinedVariable(id)

        return local_variable
