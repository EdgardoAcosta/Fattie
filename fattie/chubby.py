from fattie.cube import Cube
from fattie.belly.types import Types
from fattie.belly.quadruple import Operator
from fattie.belly.exceptions import BigError
from fattie.belly.quadruple import QuadruplePack, QuadrupleStack
from fattie.belly.heavyfunction import HeavyFunction, ActiveFunction
from fattie.belly.fluffyvariable import FluffyVariable, AddressLocation

cube = Cube()
cube.insert_values()
address = AddressLocation()


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
        self._jumps = []
        self._cont = 0

        self._era = []
        self.active_function = ActiveFunction()

        self._next_const_addr = 500000

    # <editor-fold desc="Variable and Function tables">
    def add_global_variable(self, instance):
        if instance.id_var in self._global_variable:
            raise BigError.redefined_variable(instance.id_var)
        instance.addr = address.set_addr(instance.type_var, True)
        self._global_variable[instance.id_var] = instance

    def add_local_variable(self, instance):

        if instance.id_var in self._global_variable:
            raise BigError.redefined_variable(instance.id_var)

        if instance.id_var in self._local_variable:
            raise BigError.redefined_variable(instance.id_var)

        instance.addr = address.set_addr(instance.type_var)
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
            raise BigError.redefined_function(' This one -> {} <- '.format(instance.id_function))
        self._functions[instance.id_function] = instance

    def find_function(self, id_fun):
        if id_fun not in self._functions:
            raise BigError.undefined_function(id_fun)

        return self._functions[id_fun]

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

        if len(self._operator)> 0 and self._top_operator() in [Operator.PLUS, Operator.MINUS, Operator.TIMES, Operator.DIVIDE]:
            r_operand = self._operand.pop()
            r_type = r_operand.type_var
            l_operand = self._operand.pop()
            l_type = l_operand.type_var
            oper = self._operator.pop()

            check_types = cube.compare_types(oper, l_type, r_type)

            if check_types:
                val_result = address.set_addr(check_types)

                result = FluffyVariable(None, check_types, val_result)
                # Generate Quadruple
                quadruple = QuadruplePack(oper, l_operand, r_operand, result)
                # Push quadruple to list
                self.quadruple.add(quadruple)

                # Add result position of quadruple to the operand list
                self._operand.append(result)

            else:
                raise BigError.mismatch_operator("{} {} {} ".format(l_type.name, oper.name, r_type.name))
        else:
            # TODO: Validate the boolean variables
            # for i in self._operand:
            #     print(i.parse())
            pass

    def create_assignation(self):
        expression = self._operand.pop()
        variable = self._operand.pop()

        if variable is None or expression is None:
            raise BigError('None Value to assign')

        comparison = cube.compare_types(Operator.EQUAL, expression.type_var, variable.type_var)
        if comparison:
            q = QuadruplePack(Operator.EQUAL, expression, None, variable)
            self.quadruple.add(q)

        else:
            raise BigError.mismatch_assignation(
                "The expression has type {} and expression has type {} they're incompatible".format(
                    expression.type_var.name,
                    variable.type_var.name))

    # </editor-fold>

    # <editor-fold desc="MAIN">
    # Generate GOTO MAIN
    def jump_main(self):
        self._jump()

    def jump_fill_main(self):
        self._fill()

    def end_main(self):
        self.quadruple.add(QuadruplePack(Operator.END, None, None))

    # </editor-fold>

    # <editor-fold desc="IF conditional">

    # Fill jumps for if
    def fill_jumps_if(self):
        self._fill()

    # </editor-fold>

    # <editor-fold desc="WHILE condition">
    def fill_jumps_while(self):
        self._fill()

    # </editor-fold>

    # <editor-fold desc="Functions">
    def set_active_function(self, fun):
        # Saved as a ActiveFunction
        self.active_function.id = fun.id_function
        self.active_function.return_type = fun.return_type

    def function_return(self):

        return_value = self._operand.pop()

        if return_value is None:
            raise BigError("Error on retrun dara")

        check_data = cube.compare_types(Operator.RETURN, return_value.type_var, self.active_function.return_type)

        quadruple = QuadruplePack(Operator.RETURN, l_value=return_value, r_value=None, result=self.active_function)

        self.quadruple.add(quadruple)

    # </editor-fold>

    # <editor-fold desc="Jumps">
    # Generate GOTOF
    def jump_false(self):

        if len(self._operand) == 0:
            raise BigError("The stack is empty")

        self._jumps.append(self.quadruple.index)
        result = self._operand.pop()

        if result.type_var != Types.BOOLEAN:
            raise BigError.mismatch_operator("The operation doesn't return a boolean value")

        # Generate GotoFalse, return to fill the address
        self.quadruple.add(QuadruplePack(Operator.GOTOF, result, None, None))

        # self.print_quadruple()

    def _jump(self):
        self._jumps.append(self.quadruple.index)
        self.quadruple.add(QuadruplePack(Operator.GOTO, None, None))

    # Fill jumps
    def _fill(self):
        actual_quadruple = self._jumps.pop()
        if actual_quadruple is None:
            raise BigError("Error, pending quadruples")
        else:
            available_quadruple = self.quadruple.index
            address_quadruple = FluffyVariable(None, None, addr=available_quadruple)
            self.quadruple.fill(actual_quadruple, address_quadruple)

    # Make GOSUB
    def gosub(self):
        # TODO: Create function for gosub
        self._era.append(self.quadruple.index)
        pass

    # </editor-fold>

    # <editor-fold desc="Constants">
    def add_constants(self, value):
        if value not in self._constants:
            self._constants[value] = self._next_const_addr
            self._next_const_addr += 1

            quadruple = QuadruplePack(operation=Operator.CONST, l_value=FluffyVariable(None, None, value), r_value=None,
                                      result=FluffyVariable(None, None, self._constants[value]))

            self.quadruple.add(quadruple)

        return self._constants[value]

    # </editor-fold>

    @staticmethod
    # TODO: make this method
    def reset_addr():
        address.reset_addr()

    def set_function_size(self):
        pass

    # <editor-fold desc="Prints for test">

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

    def print_quadruple(self):
        print("\nPrint quadruple \n")
        self.quadruple.print()

    def print_all(self):
        print("\nGlobal variables \n")
        for key, value in self._global_variable.items():
            print("{} : {}".format(key, value.parse()))

        print("\nLocal variables - Main \n")
        for key, value in self._local_variable.items():
            print("{} : {}".format(key, value.parse()))

        print("\nFunction table \n")
        for key, value in self._functions.items():
            print("{} : {}".format(key, value.parse()))

        print("\nPrint quadruple \n")
        self.quadruple.print()

    def print_test(self, value=""):
        print("TEST : {}".format(value))

    # </editor-fold>
