from fattie.cube import Cube
from fattie.belly.types import Types
from fattie.belly.quadruple import Operator
from fattie.belly.exceptions import BigError
from fattie.belly.quadruple import QuadruplePack, QuadrupleStack, match_operators
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
        self._quadruple = QuadrupleStack()
        self._jumps = []
        self._cont = 0

        self._era = []
        self.active_function = ActiveFunction()
        self._count_params = 0

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
        if len(self._operator) == 0:
            return None
        return self._operator[-1]

    def _top_operand(self):
        return self._operand[-1]

    def check_operator_stack(self, list_operators):
        if self._top_operator() in list_operators:
            self._check_top()

    def _check_top(self):
        # len(self._operator)> 0
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
            # Push _quadruple to list
            self._quadruple.add(quadruple)

            # Add result position of _quadruple to the operand list
            self._operand.append(result)

        else:
            raise BigError.mismatch_operator("{} {} {} ".format(l_type.name, oper.name, r_type.name))

    def create_assignation(self):
        expression = self._operand.pop()
        variable = self._operand.pop()

        if variable is None or expression is None:
            raise BigError('None Value to assign')

        comparison = cube.compare_types(Operator.EQUAL, expression.type_var, variable.type_var)
        if comparison:
            q = QuadruplePack(Operator.EQUAL, expression, None, variable)
            self._quadruple.add(q)

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
        self._quadruple.add(QuadruplePack(Operator.END, None, None))

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

    def function_call_find(self, fn_name):
        self.active_function.clear()
        find = self.find_function(fn_name)

        if find is None:
            raise BigError.undefined_function(
                "The Function in the assignation doesn't see to be declared -> {} <-".format(fn_name))

        print(find.parse())
        self.active_function.id = find.id_function
        self.active_function.params_size = len(find.params)
        self.active_function.return_type = find.return_type

    def function_return(self):

        return_value = self._operand.pop()

        if return_value is None:
            raise BigError("Error on retrun dara")

        check_data = cube.compare_types(Operator.RETURN, return_value.type_var, self.active_function.return_type)

        quadruple = QuadruplePack(Operator.RETURN, l_value=return_value, r_value=None, result=self.active_function)

        self._quadruple.add(quadruple)

    def function_end(self):
        self._quadruple.add(QuadruplePack(Operator.ENDPROC, None, None))

    def function_create_era(self):
        # TODO: Generate ERA size
        self._quadruple.add(QuadruplePack(Operator.ERA, None, 5))

    def function_validate_params(self, empty_params=False):
        fun = self.find_function(self.active_function.id)

        if empty_params:
            if self.active_function.params_size != 0:
                raise BigError.no_empty_params(
                    "The function {} required {} parameters".format(fun.id_function, self._count_params))
        else:

            argument = self._operand.pop()

            if argument.type_var != fun.type_var:
                raise BigError.mismatch_params(
                    "The parameter {} doesn't  match the type of parameter in function".format(self._count_params))

            self._quadruple.add(QuadruplePack(Operator.PARAM, None, fun.params[self._count_params]))
            self._count_params += 1

    # </editor-fold>

    # <editor-fold desc="Jumps">
    # Generate GOTOF
    def jump_false(self):
        # if len(self._operand) == 0:

        self._jumps.append(self._quadruple.index)

        result = self._operand.pop()

        if result is None:
            print(self._operand)
            raise BigError("The stack is empty")

        if result.type_var != Types.BOOLEAN:
            raise BigError.mismatch_operator("The operation doesn't return a boolean value")

        # Generate GotoFalse, return to fill the address
        self._quadruple.add(QuadruplePack(Operator.GOTOF, result, None, None))

        # self.print_quadruple()

    def _jump(self):
        self._jumps.append(self._quadruple.index)
        self._quadruple.add(QuadruplePack(Operator.GOTO, None, None))

    # Fill jumps
    def _fill(self):
        actual_quadruple = self._jumps.pop()
        if actual_quadruple is None:
            raise BigError("Error, pending quadruples")
        else:
            available_quadruple = self._quadruple.index
            address_quadruple = FluffyVariable(None, None, addr=available_quadruple)
            self._quadruple.fill(actual_quadruple, address_quadruple)

    # Make GOSUB
    def gosub(self):
        # TODO: Create function for gosub
        self._era.append(self._quadruple.index)
        pass

    # </editor-fold>

    # <editor-fold desc="Constants">
    def add_constants(self, value, type):
        if value not in self._constants:
            self._constants[value] = self._next_const_addr
            self._next_const_addr += 1
            const = FluffyVariable(None, type_var=type, addr=self._constants[value])
            quadruple = QuadruplePack(operation=Operator.CONST, l_value=FluffyVariable(None, None, value), r_value=None,
                                      result=const)

            print(quadruple.parse())
            self.add_operand(const)
            self._quadruple.add(quadruple)

        return self._constants[value]

    # </editor-fold>

    # <editor-fold desc="Static Methods">
    @staticmethod
    # TODO: make this method
    def reset_addr():
        address.reset_addr()

    @staticmethod
    def text_to_operator(op):
        op = match_operators.get(op)
        for e in list(Operator):
            if op == e.name:
                return e
        raise BigError("Operator {} is not a valid one".format(op))

    @staticmethod
    def text_to_type(tp):
        for t in list(Types):
            if tp.upper() == t.name:
                return t
        raise BigError("Type {} is not a valid one".format(tp))

    # </editor-fold>

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
        print("\nPrint _quadruple \n")
        self._quadruple.print()

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

        print("\nPrint _quadruple \n")
        self._quadruple.print()

    @staticmethod
    def print_test(value=""):
        print("***** TEST *****: {}".format(value))

    # </editor-fold>
