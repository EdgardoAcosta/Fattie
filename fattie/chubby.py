from fattie.belly.fluffyvariable import FluffyVariable
from fattie.belly.heavyfunction import HeavyFunction
from fattie.belly.exceptions import BigError
from fattie.belly.quadruple import Operator
from fattie.cube import Cube
from fattie.belly.quadruple import QuadruplePack, QuadrupleStack

cube = Cube()


class Chubby:
    # Constructor of class
    def __init__(self):
        self._global_variable = {}
        self._local_variable = {}
        self._functions = {}

        self._operand = []
        self._operator = []
        self._constants = {}
        self.quadruple = QuadrupleStack()

        self._next_const_addr = 500000

    # <editor-fold desc="Variable and Function tables">
    def add_global_variable(self, instance):
        if instance.id_var in self._global_variable:
            raise BigError.redefined_variable(instance.id_var)
        self._global_variable[instance.id_var] = instance

    def add_local_variable(self, instance):

        if instance.id_var in self._global_variable:
            raise BigError.redefined_variable(instance.id_var)

        if instance.id_var in self._local_variable:
            raise BigError.redefined_variable(instance.id_var)

        self._local_variable[instance.id_var] = instance

    def find_variable(self, id_var):

        if id_var in self._local_variable:
            return self._local_variable.get(id_var)
        elif id_var in self._global_variable:
            return self._global_variable.get(id_var)
        else:
            raise BigError.undefined_variable('{}'.format(id_var))

    def clean_variables_from_function(self):
        self._local_variable.clear()

    def add_function(self, instance):
        if instance.id_function in self._functions:
            raise BigError.redefined_funtion(' This one -> {} <- '.format(instance.id_function))
        self._functions[instance.id_function] = instance

    def find_function(self, id_fun):
        if id_fun not in self._functions:
            raise BigError.undefined_function(id_fun)

        return self._functions[id_fun]

    # For test proposes only
    def print_global_variables(self):
        print("\nGlobal variables \n")
        for key, value in self._global_variable.items():
            print("{} : {}".format(key, value.parse()))

    def print_local_variables(self):
        print("\nLocal variables \n")
        for key, value in self._local_variable.items():
            print("{} : {}".format(key, value.parse()))

    def print_function_table(self):
        print("\nFunction table \n")
        for key, value in self._functions.items():
            print("{} : {}".format(key, value.parse()))

    def print_all(self):
        print("\nGlobal variables \n")
        for key, value in self._global_variable.items():
            print("{} : {}".format(key, value.parse()))

        print("\nLocal variables \n")
        for key, value in self._local_variable.items():
            print("{} : {}".format(key, value.parse()))

        print("\nFunction table \n")
        for key, value in self._functions.items():
            print("{} : {}".format(key, value.parse()))

    # </editor-fold>

    # <editor-fold desc="Arithmetical expressions">
    def add_operand(self, operand):
        self._operand.append(operand)

    def add_operator(self, operator):
        self._operator.append(operator)

    def _top_operator(self):
        return self._operator[-1]

    def _top_operand(self):
        return self._operand[-1]

    def check_top(self):

        if self._top_operator() in [Operator.PLUS, Operator.MINUS, Operator.TIMES, Operator.DIVIDE]:
            r_operand = self._operand.pop()
            r_type = r_operand.type_var
            l_operand = self._operand.pop()

            l_type = l_operand.type_var
            oper = self._operator.pop()

            check_types = cube.compare_types(oper, l_type, r_type)
            print("{} {} {} ".format(l_type, oper, r_type))

            if check_types:
                # TODO: Check what is result
                result = ""  # AVAIL.next()
                quadruple = QuadruplePack(oper, l_operand, r_operand, result)
                self.quadruple.add(quadruple)

            else:
                raise BigError.mismatch_operator("{} {} {} ".format(l_type, oper.name, r_type))

    # </editor-fold>

    def add_constants(self, value):
        if value not in self._constants:
            self._constants[value] = self._next_const_addr
            self._next_const_addr += 1

            quadruple = QuadruplePack(operation=Operator.CONST, l_value=FluffyVariable(None, None, value), r_value=None,
                                      result=FluffyVariable(None, None, self._constants[value]))
            self.quadruple.add(quadruple)

        return self._constants[value]

    @staticmethod
    def print_test(value=""):
        print("ENTRO {}".format(value))
