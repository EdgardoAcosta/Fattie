import ast
import re
import turtle
import time

regex_int = '^[0-9]+$'
regex_float = '[0-9]*\.[0-9]+|[0-9]+'
regex_boolean = '(^True$|^False$)'


class BigMachine:
    """
     Function to start the VM, will initialize the necessary memory,allocate the variables and
     read the quadruple generated from the compiler
     :return: None
     """

    def __init__(self, filename):
        # stack with the quadruples
        self._quadruples = list()

        # definition of the memory
        # Memory slots for ints 0 - 100000,floats 100000 - 200000,chars 200000 - 300000, bools 300000 - 400000,
        # const 500000 - 600000
        self._fatMemory = 600000 * [""]

        # definition of the globalmemory
        # Global memory slots for ints 0 - 100000,floats 100000 - 200000,chars 200000 - 300000, bools 300000 - 400000,
        # const 500000 - 600000
        self._fatGlobalMemory = 600000 * [""]

        self._screen = turtle.Screen()
        self._turtle = turtle.Turtle()
        self._start_x = self._turtle.setx(0)
        self._start_y = self._turtle.sety(0)

        with open(filename) as fp:
            line = fp.readline()
            count = 1
            while line:
                self._quadruples.append(ast.literal_eval(line))
                line = fp.readline()
                count += 1

    # <editor-fold desc="Set, get">
    def _insert_in_fat_memory(self, position, value):
        self._fatMemory[position] = value

    def _get_value_fat_memory(self, position):
        result = self._fatMemory[position]
        return result

    def _insert_in_fat_global_memory(self, position, value):
        self._fatGlobalMemory[position] = value

    def _get_value_fat_global_memory(self, position):
        result = self._fatGlobalMemory[position]
        return result

    def inset(self, addr, value):
        if addr / 1000000 >= 1:
            addr = addr - 1000000
            self._insert_in_fat_global_memory(addr, value)
        else:
            self._insert_in_fat_memory(addr, value)

    def get_value(self, add):
        if add >= 1000000:
            add = add - 1000000
            return self._get_value_fat_global_memory(add)
        else:
            return self._get_value_fat_memory(add)

    # </editor-fold>

    def process_quadruple(self):
        for quadruple in self._quadruples:

            # assignation of constants
            if quadruple['operator'] == 'CONST':
                l_val = quadruple['l_value']['addr']
                result = quadruple['result']['addr']

                self._insert_in_fat_memory(result, l_val)

            # assignation of any variable
            elif quadruple['operator'] == 'EQUAL':
                l_val = quadruple['l_value']['addr']
                result = quadruple['result']['addr']

                # verify if l_val is a global or local direction
                if l_val >= 1000000:
                    l_val = l_val - 1000000
                    value = self._get_value_fat_global_memory(l_val)
                else:
                    value = self._get_value_fat_memory(l_val)

                # verify if is going to assign to a global variable
                if result / 1000000 >= 1:
                    result = result - 1000000
                    self._insert_in_fat_global_memory(result, value)
                else:
                    self._insert_in_fat_memory(result, value)

            # add of two variables
            elif quadruple['operator'] == 'PLUS':

                l_val = quadruple['l_value']['addr']
                r_val = quadruple['r_value']['addr']
                result = quadruple['result']['addr']

                # verify if is going to subtract l_val from a global variable
                if l_val / 1000000 >= 1:
                    l_val = l_val - 1000000

                    # verify if l_val is indirect o direct reference
                    if self._get_value_fat_global_memory(l_val) >= 500000:
                        l_operand = self._get_value_fat_memory(self._get_value_fat_global_memory(l_val))
                    else:
                        l_operand = self._get_value_fat_global_memory(l_val)

                else:
                    # verify if l_val is indirect o direct reference
                    if self._get_value_fat_memory(l_val) >= 500000:
                        l_operand = self._get_value_fat_memory(self._get_value_fat_memory(l_val))
                    else:
                        l_operand = self._get_value_fat_memory(l_val)

                # verify if is going to stract r_val from a global variable
                if r_val / 1000000 >= 1:
                    r_val = r_val - 1000000

                    # verify if l_val is indirect o direct reference
                    if self._get_value_fat_global_memory(r_val) >= 500000:
                        r_operand = self._get_value_fat_memory(self._get_value_fat_global_memory(r_val))
                    else:
                        r_operand = self._get_value_fat_global_memory(r_val)

                else:
                    # verify if l_val is indirect o direct reference
                    if self._get_value_fat_memory(r_val) >= 500000:
                        r_operand = self._get_value_fat_memory(self._get_value_fat_memory(r_val))
                    else:
                        r_operand = self._get_value_fat_memory(r_val)

                # verify if si going to assign to a global variable
                if result / 1000000 >= 1:
                    result = result - 1000000
                    evaluation = l_operand + r_operand
                    self._insert_in_fat_global_memory(result, evaluation)

                else:
                    evaluation = l_operand + r_operand
                    self._insert_in_fat_memory(result, evaluation)

                # TODO: Checar el UMINUS PORQUE NO SABES QUE PEDO
                # TODO: Checar la concatenacion de CHARS

            # subtract of two variables
            elif quadruple['operator'] == 'MINUS':
                l_val = quadruple['l_value']['addr']
                r_val = quadruple['r_value']['addr']
                result = quadruple['result']['addr']

                # verify if is going to stract l_val from a global variable
                if l_val / 1000000 >= 1:
                    l_val = l_val - 1000000

                    # verify if l_val is indirect o direct reference
                    if self._get_value_fat_global_memory(l_val) >= 500000:
                        l_operand = self._get_value_fat_memory(self._get_value_fat_global_memory(l_val))
                    else:
                        l_operand = self._get_value_fat_global_memory(l_val)

                else:
                    # verify if l_val is indirect o direct reference
                    if self._get_value_fat_memory(l_val) >= 500000:
                        l_operand = self._get_value_fat_memory(self._get_value_fat_memory(l_val))
                    else:
                        l_operand = self._get_value_fat_memory(l_val)

                # verify if is going to stract r_val from a global variable
                if r_val / 1000000 >= 1:
                    r_val = r_val - 1000000

                    # verify if l_val is indirect o direct reference
                    if self._get_value_fat_global_memory(r_val) >= 500000:
                        r_operand = self._get_value_fat_memory(self._get_value_fat_global_memory(r_val))
                    else:
                        r_operand = self._get_value_fat_global_memory(r_val)

                else:
                    # verify if l_val is indirect o direct reference
                    if self._get_value_fat_memory(r_val) >= 500000:
                        r_operand = self._get_value_fat_memory(self._get_value_fat_memory(r_val))
                    else:
                        r_operand = self._get_value_fat_memory(r_val)

                # verify if si goign to assign to a global variable
                if result / 1000000 >= 1:
                    result = result - 1000000
                    evaluation = l_operand + r_operand
                    self._insert_in_fat_global_memory(result, evaluation)

                else:
                    evaluation = l_operand - r_operand
                    self._insert_in_fat_memory(result, evaluation)

            # multiply two variables
            elif quadruple['operator'] == 'TIMES':
                l_val = quadruple['l_value']['addr']
                r_val = quadruple['r_value']['addr']
                result = quadruple['result']['addr']

                # verify if is going to stract l_val from a global variable
                if l_val / 1000000 >= 1:
                    l_val = l_val - 1000000

                    # verify if l_val is indirect o direct reference
                    if self._get_value_fat_global_memory(l_val) >= 500000:
                        l_operand = self._get_value_fat_memory(self._get_value_fat_global_memory(l_val))
                    else:
                        l_operand = self._get_value_fat_global_memory(l_val)

                else:
                    # verify if l_val is indirect o direct reference
                    if self._get_value_fat_memory(l_val) >= 500000:
                        l_operand = self._get_value_fat_memory(self._get_value_fat_memory(l_val))
                    else:
                        l_operand = self._get_value_fat_memory(l_val)

                # verify if is going to stract r_val from a global variable
                if r_val / 1000000 >= 1:
                    r_val = r_val - 1000000

                    # verify if l_val is indirect o direct reference
                    if self._get_value_fat_global_memory(r_val) >= 500000:
                        r_operand = self._get_value_fat_memory(self._get_value_fat_global_memory(r_val))
                    else:
                        r_operand = self._get_value_fat_global_memory(r_val)

                else:
                    # verify if l_val is indirect o direct reference
                    if self._get_value_fat_memory(r_val) >= 500000:
                        r_operand = self._get_value_fat_memory(self._get_value_fat_memory(r_val))
                    else:
                        r_operand = self._get_value_fat_memory(r_val)

                # verify if si going to assign to a global variable
                if result / 1000000 >= 1:
                    result = result - 1000000
                    evaluation = l_operand + r_operand
                    self._insert_in_fat_global_memory(result, evaluation)

                else:
                    evaluation = l_operand * r_operand
                    self._insert_in_fat_memory(result, evaluation)

            # divide two variables
            elif quadruple['operator'] == 'DIVIDE':
                l_val = quadruple['l_value']['addr']
                r_val = quadruple['r_value']['addr']
                result = quadruple['result']['addr']

                # verify if is going to stract l_val from a global variable
                if l_val / 1000000 >= 1:
                    l_val = l_val - 1000000

                    # verify if l_val is indirect o direct reference
                    if self._get_value_fat_global_memory(l_val) >= 500000:
                        l_operand = self._get_value_fat_memory(self._get_value_fat_global_memory(l_val))
                    else:
                        l_operand = self._get_value_fat_global_memory(l_val)

                else:
                    # verify if l_val is indirect o direct reference
                    if self._get_value_fat_memory(l_val) >= 500000:
                        l_operand = self._get_value_fat_memory(self._get_value_fat_memory(l_val))
                    else:
                        l_operand = self._get_value_fat_memory(l_val)

                # verify if is going to stract r_val from a global variable
                if r_val / 1000000 >= 1:
                    r_val = r_val - 1000000

                    # verify if l_val is indirect o direct reference
                    if self._get_value_fat_global_memory(r_val) >= 500000:
                        r_operand = self._get_value_fat_memory(self._get_value_fat_global_memory(r_val))
                    else:
                        r_operand = self._get_value_fat_global_memory(r_val)

                else:
                    # verify if l_val is indirect o direct reference
                    if self._get_value_fat_memory(r_val) >= 500000:
                        r_operand = self._get_value_fat_memory(self._get_value_fat_memory(r_val))
                    else:
                        r_operand = self._get_value_fat_memory(r_val)

                # verify if si going to assign to a global variable
                if result / 1000000 >= 1:
                    result = result - 1000000
                    evaluation = l_operand + r_operand
                    self._insert_in_fat_global_memory(result, evaluation)

                else:
                    evaluation = l_operand / r_operand
                    self._insert_in_fat_memory(result, evaluation)

            # elif quadruple['operator'] == 'LESS':
            #     l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'GREATER':
            #      l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'NOTEQUAL':
            #     l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'AND':
            #     l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'OR':
            #     l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'NOT':
            #     l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'TRUE':
            #     l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'FALSE':
            #     l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'EQUALS':
            #     l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'GOTO':
            #     l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'GOTOF':
            #     l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'GOSUB':
            #     l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'UMINUS':
            #     l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'CONST':
            #     l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'ERA':
            #      l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'RETURN':
            #    l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'ENPROC':
            #      l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'END':
            #      l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'PARAM':
            #     l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']
            #
            # elif quadruple['operator'] == 'GETRET':
            #     l_val = quadruple['l_value']['addr']
            #     r_val = quadruple['r_value']['addr']
            #     result = quadruple['result']['addr']

            # Read value from user
            elif quadruple['operator'] == 'INPUT':

                result = quadruple['result']
                addr = result['addr']

                _input = input("<- ")
                # Variable is of type int
                if result['type_var'] == 'INT':
                    if re.match(regex_boolean, _input):
                        _input = int(_input == 'True')
                    elif re.match(regex_int, _input):
                        _input = int(_input)
                    elif re.match(regex_float, _input):
                        _input = int(float(_input))
                    else:
                        # if string value, will return the sum of all the ascii characters
                        _input = sum([ord(i) for i in _input])
                # Variable id of type float
                if result['type_var'] == 'FLOAT':
                    if re.match(regex_boolean, _input):
                        _input = float(_input == 'True')
                    elif re.match(regex_int, _input) or re.match(regex_float, _input):
                        _input = float(_input)
                    else:
                        # if string value, will return the sum of all the ascii characters
                        _input = float(sum([ord(i) for i in _input]))

                if result['type_var'] == 'CHAR':
                    _input = str(_input)

                if result['type_var'] == 'BOOLEAN':

                    if re.match(regex_boolean, _input):
                        _input = (_input == 'True')
                    elif re.match(regex_int, _input):
                        _input = (int(_input) == 1)
                    elif re.match(regex_float, _input):
                        _input = (int(float(_input)) == 1)
                    else:
                        # if string value, will return the sum of all the ascii characters
                        _input = 0

                self.inset(addr, _input)

            # Show value in terminal
            elif quadruple['operator'] == 'PRINT':

                result = quadruple['result']
                if result['addr'] / 1000000 >= 1:
                    result = result - 1000000
                    aux = self._get_value_fat_global_memory(result)
                else:
                    aux = self._get_value_fat_memory(result['addr'])

                print("-> {} ".format(aux))

            elif quadruple['operator'] == 'SQUARE':
                angle = self.get_value(quadruple['r_value']['addr'])
                length = self.get_value(quadruple['result']['addr'])

                for i in range(4):
                    self._turtle.forward(length)
                    self._turtle.right(angle)

            elif quadruple['operator'] == 'CLEAN':
                self._turtle.clear()

            elif quadruple['operator'] == 'SLEEP':
                ms = self.get_value(quadruple['result']['addr'])
                time.sleep(float(ms))

    # <editor-fold desc="Prints for test">
    def _print_local_value(self, position):
        print("local:{}=>{}".format(position, self._fatMemory[position]))

    def _print_global_value(self, position):
        print("global:{}=>{}".format(position, self._fatGlobalMemory[position]))
    # </editor-fold>


if __name__ == '__main__':
    big_machine = BigMachine("fat.txt")
    big_machine.process_quadruple()
