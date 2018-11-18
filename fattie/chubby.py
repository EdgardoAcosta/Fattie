from fattie.cube import Cube
from fattie.belly.types import Types
from fattie.belly.quadruple import Operator, SpecialFunction
from fattie.belly.exceptions import BigError
from fattie.belly.quadruple import QuadruplePack, QuadrupleStack, match_operators
from fattie.belly.heavyfunction import HeavyFunction, ActiveFunction
from fattie.belly.fluffyvariable import FluffyVariable, AddressLocation

cube = Cube()
cube.insert_values()
address = AddressLocation()


class Switch:

    def __init__(self, option):
        self.option = option
        self.cases = {}

    def __call__(self, option, fn):
        self.cases[option] = fn

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cases[self.option]()


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

        self._array_op = []
        self._dim_stack = []
        self._dimension = 0

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
        self.function_validate(instance.id_function)

        self.active_function.start_position = self._quadruple.index

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

            result = FluffyVariable(None, type_var=check_types, addr=val_result)
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
    def fill_jumps_if(self, line=0):
        self._fill(line)

    def make_goto_if(self):
        self._jump()

    # </editor-fold>

    # <editor-fold desc="WHILE condition">
    def fill_jumps_while(self):
        self._fill()

    # </editor-fold>

    # <editor-fold desc="Functions">

    def _top_era(self):
        if len(self._era) == 0:
            return None
        return self._era[-1]

    def function_validate(self, fn_name):
        self.active_function.clear()
        self._count_params = 0
        find = self.find_function(fn_name)

        if find is None:
            raise BigError.undefined_function(
                "The Function in the assignation doesn't see to be declared -> {} <-".format(fn_name))
        self.active_function.id = find.id_function
        self.active_function.params_size = len(find.params)
        self.active_function.return_type = self.text_to_type(find.return_type)
        self.active_function.size = find.size

    def function_return(self):

        return_value = self._operand.pop()

        if return_value is None:
            raise BigError("Error on retrun data")

        check_data = cube.compare_types(Operator.RETURN, return_value.type_var, self.active_function.return_type)

        if check_data:
            result = FluffyVariable(None, type_var=self.active_function.return_type,
                                    addr=address.set_addr(kind=self.active_function.return_type))

            quadruple = QuadruplePack(Operator.RETURN, l_value=return_value, r_value=None, result=result)

            self._quadruple.add(quadruple)
        else:
            raise BigError.mismatch_operator(
                "Return type {} does't correspond to the return type of function {} ".format(return_value.type_var,
                                                                                             self.active_function.return_type))

    def function_end(self):
        self._quadruple.add(QuadruplePack(Operator.ENDPROC, None, None))

    def function_create_era(self):
        size_era = FluffyVariable(None, None, addr=address.calculate_era())
        self._quadruple.add(QuadruplePack(Operator.ERA, None, None, size_era))

    def function_validate_params(self, empty_params=False):
        fun = self.find_function(self.active_function.id)

        if empty_params:
            if self.active_function.params_size != 0:
                raise BigError.no_empty_params(
                    "The function {} required {} parameters, {} given".format(fun.id_function,
                                                                              self.active_function.params_size,
                                                                              self._count_params + 1))

        argument = self._operand.pop()

        if self._count_params + 1 > self.active_function.params_size:
            raise BigError.no_empty_params(
                "The function {} required {} parameters, {} given".format(fun.id_function,
                                                                          self.active_function.params_size,
                                                                          self._count_params + 1))

        if argument.type_var != fun.params[self._count_params].type_var:
            raise BigError.mismatch_params(
                "The parameter {} doesn't  match the type of parameter in function".format(self._count_params))
        param = FluffyVariable(None, None, addr=self._count_params)
        self._quadruple.add(QuadruplePack(Operator.PARAM, fun.params[self._count_params], None, param))
        self._count_params += 1

    # </editor-fold>

    # <editor-fold desc="Arrays">
    def _top_dim(self):
        return self._dim_stack[-1]

    def push_dim(self, var, dim):

        if dim == 0:
            print(var.array.parse())
            self._dim_stack.append(var.array)
        else:
            d = self._top_dim()
            self._dim_stack.append(d.next)

        # with Switch(1) as case:
        #     case(1, lambda: print("one"))

    def eval_dim(self):
        exp = self._operand.pop()
        dim = self._top_dim()
        # print(exp.parse())
        # print(dim.parse())
        if exp is not None:

            dimS = FluffyVariable(None, Types.INT, addr=dim.size)
            dimM = FluffyVariable(None, Types.INT, addr=dim.m)
            tem = FluffyVariable(None, exp.type_var, addr=address.set_addr(exp.type_var))
            #  Validate dim and generate VER
            self._quadruple.add(QuadruplePack(Operator.VER, exp, 0, dimS))
            self._quadruple.add(QuadruplePack(Operator.TIMES, dimM, exp, tem))
            self._operand.append(tem)
        else:
            raise BigError("Error in array expression")

    def eval_array(self):

        dim = self._dim_stack.pop()

        while self._top_dim().var == dim.var:
            _ = self._dim_stack.pop()
            op = self._operand.pop()
            op2 = self._operand.pop()
            temp = FluffyVariable(None, None, addr=address.set_addr(op.type_var))
            q = QuadruplePack(Operator.PLUS, op, op2, temp)
            self._quadruple.add(q)
            self._operand.append(temp)

        var = self.find_variable(dim.var)
        base = FluffyVariable(None, var.type_var, addr=var.addr)
        dim = self._operand.pop()
        temp = FluffyVariable(None, Types.INT, addr=address.set_addr(Types.INT))

        # TODO: marcar temp como accesso directo
        self._quadruple.add(QuadruplePack(Operator.PLUS, base, dim, temp))
        self._operand.append(temp)

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

    def _jump(self):
        self._jumps.append(self._quadruple.index)
        self._quadruple.add(QuadruplePack(Operator.GOTO, None, None))

    # Fill jumps
    def _fill(self, line=0):
        actual_quadruple = self._jumps.pop()
        if actual_quadruple is None:
            raise BigError("Error, pending quadruples")
        else:
            available_quadruple = self._quadruple.index + line
            address_quadruple = FluffyVariable(None, None, addr=available_quadruple)
            self._quadruple.fill(actual_quadruple, address_quadruple)

    # Make GOSUB
    def gosub(self):
        self._era.append(self._quadruple.index)
        function_dir = FluffyVariable(None, None, addr=self.active_function.start_position)
        self._quadruple.add(QuadruplePack(Operator.GOSUB, None, None, function_dir))

        if self.active_function.return_type is not None:
            temp = FluffyVariable(None, self.active_function.return_type
                                  , addr=address.set_addr(self.active_function.return_type))
            self._operand.append(temp)
            self._quadruple.add(QuadruplePack(Operator.GETRET, None, None, temp))

    # </editor-fold>

    # <editor-fold desc="Constants">
    def add_constants(self, value, var_type):
        if value not in self._constants:
            self._constants[value] = self._next_const_addr
            self._next_const_addr += 1
            const = FluffyVariable(None, type_var=var_type, addr=self._constants[value])
            quadruple = QuadruplePack(operation=Operator.CONST, l_value=FluffyVariable(None, None, addr=value),
                                      r_value=None,
                                      result=const)

            self.add_operand(const)
            self._quadruple.add(quadruple)

        return self._constants[value]

    # </editor-fold>

    # <editor-fold desc="Static Methods">
    @staticmethod
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
    def text_to_special_operator(op):
        for e in list(SpecialFunction):
            if op.upper() == e.name:
                return e
        raise BigError("Operator {} is not a valid one".format(op))

    @staticmethod
    def text_to_type(tp):
        for t in list(Types):
            if tp.upper() == t.name:
                return t
        raise BigError("Type {} is not a valid one".format(tp))

    # </editor-fold>

    # <editor-fold desc="Special Functions">
    def make_special_function(self, action_name):
        action_name = self.text_to_special_operator(action_name)
        exp = self._operand.pop()

        if exp is None:
            raise BigError("ERROR")
        q = QuadruplePack(action_name, None, None, exp)
        self._quadruple.add(q)

    # </editor-fold>

    def make_output(self):
        file = open("fat.ft", "w")
        self._quadruple.write_to_file(file)

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
