from fattie.belly.fluffyvariable import FluffyVariable
from fattie.belly.heavyfunction import HeavyFunction
from fattie.belly.exceptions import BigError


class Chubby:
    # Constructor of class
    def __init__(self):
        self._global_variable = {}
        self._local_variable = {}
        self._functions = {}

    def add_global_variable(self, instance):
        if instance.id_var in self._global_variable:
            raise BigError.redefined_variable(instance.id_var)
        self._global_variable[instance.id_var] = instance

    def add_local_variable(self, instance):
        if instance.id_var in self._local_variable:
            raise BigError.redefined_variable(instance.id_var)

        self._local_variable[instance.id_var] = instance

    def find_variable(self, id_var):
        local_variable = self._local_variable.find_variable(id_var)
        global_variable = self._local_variable.find_variable(id_var)

        if local_variable is not None:
            return local_variable
        elif global_variable is not None:
            return global_variable
        else:
            raise BigError.undefined_variable('Variable not defined ')

    def add_function(self, instance):
        if instance.id_function in self._functions:
            raise BigError.redefined_funtion('Function \{}\ already defined'.format(instance.id_function))

        self._functions[instance.id_function] = instance

    def find_function(self, id_fun):
        if id_fun not in self._functions:
            raise BigError.undefined_function(id_fun)

        return self._functions[id_fun]
