import sys
import ast
import re
import turtle
import time
from fattie.belly.fluffyvariable import local_addr, global_addr
from fattie.belly.exceptions import BigError
from fattie.belly.types import Types

regex_int = '^[0-9]+$'
regex_float = '[0-9]*\.[0-9]+|[0-9]+'
regex_boolean = '(^True$|^False$)'
regex_color = '#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
types = [Types.INT, Types.FLOAT, Types.CHAR, Types.BOOLEAN]


# definition of the globalmemory for variables
# Global memory slots for ints 0 - 100000,floats 100000 - 200000,chars 200000 - 300000, bools 300000 - 400000,
# const 500000 - 600000
class FatMemory:

    def __init__(self, _int=0, _float=0, _char=0, _boo=0):
        self.fat_memory = {
            1: [None] * _int,
            2: [None] * _float,
            3: [None] * _char,
            4: [None] * _boo

        }


# virtual machine
class BigMachine:
    """
     Function to start the VM, will initialize the necessary memory,allocate the variables and
     read the self._quadruples generated from the compiler
     :return: None
     """

    def __init__(self, filename):
        # stack with the self._quadrupless
        self._quadruples = list()

        # <editor-fold desc="Memory initialization">

        # definition of the stack where we are going to store the memory necesary for the functions
        # this memories are fat memories with variables in them
        self._bigMemory = list()

        # definition of the globalmemory for variables
        # Global memory slots for ints 0 - 100000,floats 100000 - 200000,chars 200000 - 300000, bools 300000 - 400000,
        # const 500000 - 600000
        self._fatGlobalMemory = 20 * [None]

        # definition of the memory for the constants
        # it stores the constants values
        self._heavyConstants = 600000 * [None]
        # definition of the virtualmemory
        # this memory save the memory requirements for functions
        self._memorySizes = list()

        # Retorn to quadruple
        self._saved_quadruple = []

        self._return_values = []

        self._settable_memory = None

        self._params = []
        # </editor-fold>

        # <editor-fold desc="Turtle default settings">
        self._screen_dim = True

        self._screen = turtle.Screen()
        self._turtle = turtle.Turtle()
        self._start_x = self._turtle.setx(0)
        self._start_y = self._turtle.sety(0)
        self._turtle.pensize(2)
        self._turtle.speed()
        self._screen.screensize(400, 400)
        # </editor-fold>

        # <editor-fold desc="Read file">
        with open(filename) as fp:
            line = fp.readline()
            count = 1
            while line:
                self._quadruples.append(ast.literal_eval(line))
                line = fp.readline()
            count += 1
        # </editor-fold>

    # <editor-fold desc="Set, get">

    def _get_value_heavy_constants(self, position):
        position = position - 500000
        result = self._heavyConstants[position]
        return result

    def _check_for_constant_direction(self, address):
        if address >= 500000:
            return True
        else:
            return False

    def _check_type_local(self, addr):
        if isinstance(addr, str):
            for t in list(Types):
                if addr == t.name:
                    return t.value
        return types[addr // 100000].value

    def _check_type_global(self, addr):
        if isinstance(addr, str):
            for t in list(Types):
                if addr == t.name:
                    return t.value
        return types[addr // 100000].value

    def insert(self, addr, value):
        if addr // 1000000 >= 1:
            position = (addr - 1000000)
            # addr = addr - 1000000

            self._fatGlobalMemory[position] = value
        else:
            self._bigMemory[-1].fat_memory[self._check_type_local(addr)][addr % 100000] = value

    def get_value(self, position, referenced=False):
        if position >= 1000000:

            position = (position - 1000000)
            value = self._fatGlobalMemory[position]
        elif position >= 500000:
            position = position - 500000
            result = self._heavyConstants[position]
            value = result
        else:
            value = self._bigMemory[-1].fat_memory[self._check_type_global(position)][position % 100000]

        if referenced:

            value = self.get_value(value)
            if value >= 500000:
                return self.get_value(value)

        return value

    def _access_type(self, quadruple):
        return quadruple['access'] == 'Indirect'

    @staticmethod
    def parse(quadruple):
        return quadruple['l_value'], quadruple['r_value'], quadruple['result']

    def _get_real_value(self, quadruple):
        if quadruple['access'] == 'Indirect':
            position = quadruple['addr']
            return self.get_value(self._bigMemory[-1][self._check_type_local(quadruple['type_var'])][position])

        return quadruple['addr']

    @staticmethod
    def _fibonacci(n):
        fib = []
        a, b = 0, 1
        while a < n:
            a, b = b, a + b
            fib.append(a)

        return fib

    def _draw_fib(self, fib, factor):
        num_sqr = len(fib)
        self._turtle.pensize(0)
        self._turtle.penup()
        self._turtle.goto(50, 50)
        self._turtle.pendown()

        for i in range(num_sqr):
            self._draw_square(factor * fib[i])  # Draw square
            self._turtle.penup()  # Move to new corner as starting point
            self._turtle.forward(factor * fib[i])
            self._turtle.right(90)
            self._turtle.forward(factor * fib[i])
            self._turtle.pendown()
        self._turtle.penup()
        self._turtle.goto(50, 50)  # Move to starting point
        self._turtle.setheading(0)  # Face the turtle to the right
        self._turtle.pencolor('red')
        self._turtle.pensize(3)
        self._turtle.pendown()
        # Draw quartercircles with fibonacci numbers as radius
        for i in range(num_sqr):
            self._turtle.circle(-factor * fib[i], 90)  # minus sign to draw clockwise

    def _draw_square(self, side_length):  # Function for drawing a square
        for i in range(4):
            self._turtle.forward(side_length)
            self._turtle.right(90)

    # </editor-fold>

    def get_consts(self):
        for i in range(1, len(self._quadruples)):
            # assignation of constants
            if self._quadruples[i]['operator'] == 'CONST':
                l_val = self._quadruples[i]['l_value']['addr']
                result = self._quadruples[i]['result']['addr']
                result = result - 500000
                self._heavyConstants[result] = l_val

    def process_quadruples(self):

        # print(self._quadruples[0])
        i = 0
        endFlag = False
        self.get_consts()
        while not endFlag:
            # print("i -> ", i)
            # assignation of any variable
            if self._quadruples[i]['operator'] == 'EQUAL':
                l_val = self._quadruples[i]['l_value']['addr']
                result = self._quadruples[i]['result']['addr']

                if self._quadruples[i]['result']['access'] == "Indirect":
                    result = self._bigMemory[-1].fat_memory[self._check_type_local(self._quadruples[i]['result']['type_var'])][self._quadruples[i]['result']['addr']]
                    value = l_val
                    if value < 500000:
                        value = self._bigMemory[-1].fat_memory[self._check_type_local(self._quadruples[i]['result']['type_var'])][value]

                else:
                    # check if the l_val is a constant
                    if self._check_for_constant_direction(l_val):
                        value = self._get_value_heavy_constants(l_val)
                    else:
                        # verify if l_val is a global or local direction
                        value = self.get_value(l_val)

                    # verify if is going to assign to a global variable
                self.insert(result, value)



            # add of two variables
            elif self._quadruples[i]['operator'] == 'PLUS':
                l_val = self._quadruples[i]['l_value']['addr']
                r_val = self._quadruples[i]['r_value']['addr']
                result = self._quadruples[i]['result']['addr']
                # verify if is going to subtract l_val from a global variable
                l_operand = self.get_value(l_val, self._access_type(self._quadruples[i]['l_value']))
                # print("10 ? ", self._access_type(self._quadruples[i]['l_value']))

                # verify if is going to stract r_val from a global variable
                r_operand = self.get_value(r_val, self._access_type(self._quadruples[i]['r_value']))

                # verify if si going to assign to a global variable
                evaluation = l_operand + r_operand

                self.insert(result, evaluation)


            # subtract of two variables
            elif self._quadruples[i]['operator'] == 'MINUS':
                l_val = self._quadruples[i]['l_value']['addr']
                r_val = self._quadruples[i]['r_value']['addr']
                result = self._quadruples[i]['result']['addr']

                # verify if is going to subtract l_val from a global variable
                l_operand = self.get_value(l_val, self._access_type(self._quadruples[i]['l_value']))

                # verify if is going to stract r_val from a global variable
                r_operand = self.get_value(r_val, self._access_type(self._quadruples[i]['r_value']))

                # verify if si going to assign to a global variable
                evaluation = l_operand - r_operand

                self.insert(result, evaluation)

            # multiply two variables
            elif self._quadruples[i]['operator'] == 'TIMES':
                l_val = self._quadruples[i]['l_value']['addr']
                r_val = self._quadruples[i]['r_value']['addr']
                result = self._quadruples[i]['result']['addr']

                # verify if is going to subtract l_val from a global variable
                l_operand = self.get_value(l_val, self._access_type(self._quadruples[i]['l_value']))

                # verify if is going to stract r_val from a global variable
                r_operand = self.get_value(r_val, self._access_type(self._quadruples[i]['r_value']))

                # verify if si going to assign to a global variable
                evaluation = l_operand * r_operand

                self.insert(result, evaluation)

            # divide two variables
            elif self._quadruples[i]['operator'] == 'DIVIDE':

                l_val = self._quadruples[i]['l_value']['addr']
                r_val = self._quadruples[i]['r_value']['addr']
                result = self._quadruples[i]['result']['addr']
                access = self._quadruples[i]['result']['access'] == 'Indirect'

                # verify if is going to subtract l_val from a global variable
                l_operand = self.get_value(l_val, self._access_type(self._quadruples[i]['l_value']))

                # verify if is going to stract r_val from a global variable
                r_operand = self.get_value(r_val, self._access_type(self._quadruples[i]['r_value']))

                # verify if si going to assign to a global variable

                evaluation = l_operand / r_operand

                self.insert(result, evaluation)


            # <editor-fold desc="Logical operator">
            elif self._quadruples[i]['operator'] == 'LESS':
                l_val = self.get_value(self._quadruples[i]['l_value']['addr'])
                r_val = self.get_value(self._quadruples[i]['r_value']['addr'])
                result = self._quadruples[i]['result']  # ['addr']

                self.insert(result['addr'], (l_val < r_val))

            elif self._quadruples[i]['operator'] == 'GREATER':
                l_val = self.get_value(self._quadruples[i]['l_value']['addr'])
                r_val = self.get_value(self._quadruples[i]['r_value']['addr'])
                result = self._quadruples[i]['result']
                self.insert(result['addr'], (l_val > r_val))

            elif self._quadruples[i]['operator'] == 'NOTEQUAL':
                l_val = self.get_value(self._quadruples[i]['l_value']['addr'])
                r_val = self.get_value(self._quadruples[i]['r_value']['addr'])
                result = self._quadruples[i]['result']['addr']

                self.insert(result, (l_val != r_val))

            elif self._quadruples[i]['operator'] == 'EQUALS':
                l_val = self.get_value(self._quadruples[i]['l_value']['addr'])
                r_val = self.get_value(self._quadruples[i]['r_value']['addr'])
                result = self._quadruples[i]['result']['addr']

                self.insert(result, (l_val == r_val))

            elif self._quadruples[i]['operator'] == 'UMINUS':
                l_val = self._quadruples[i]['l_value']
                r_val = self._quadruples[i]['r_value']
                result = self._quadruples[i]['result']
            # </editor-fold>

            # <editor-fold desc="GOTO'S">
            elif self._quadruples[i]['operator'] == 'GOTO':

                i = self._quadruples[i]['result']['addr']
                continue

            elif self._quadruples[i]['operator'] == 'GOTOF':
                expression = self.get_value(self._quadruples[i]['l_value']['addr'])
                if expression:
                    pass
                else:
                    i = self._quadruples[i]['result']['addr']
                    continue
            # </editor-fold>

            # <editor-fold desc="Function">
            elif self._quadruples[i]['operator'] == 'GOSUB':
                # Save point to retorn afect execution
                self._saved_quadruple.append(i + 1)
                # Goto addres of GOSUB
                i = self._quadruples[i]['result']['addr']
                memory = self._settable_memory
                # TODO: Fix this
                self._bigMemory.append(FatMemory(memory['INT'], memory['FLOAT'], memory['CHAR'], memory['BOOLEAN']))
                if len(self._params) > 0:
                    for param in self._params:
                        for key in param:
                            self.insert(key, param[key])

                self._settable_memory = None

                continue

            elif self._quadruples[i]['operator'] == 'ENDPROC':
                # Return to las position of execution
                i = self._saved_quadruple.pop()
                continue

            elif self._quadruples[i]['operator'] == 'RETURN':

                value = self.get_value(self._quadruples[i]['l_value']['addr'])
                self._return_values.append(value)
                result = self._quadruples[i]['result']['addr']
                i = self._saved_quadruple.pop()
                continue

                pass

                # self.insert(result, value)

            elif self._quadruples[i]['operator'] == 'PARAM':
                value = self.get_value(self._quadruples[i]['l_value']['addr'])

                if value is None:
                    print("Tha variable {} don't have a value ".format(self._quadruples[i]['l_value']['id_var']))
                    sys.exit(0)

                self._params.append({self._quadruples[i]['result']['addr']: value})

            # implementation of the era for functions
            elif self._quadruples[i]['operator'] == 'ERA':
                self._settable_memory = self._quadruples[i]['result']['addr']

            elif self._quadruples[i]['operator'] == 'GETRET':
                result = self._quadruples[i]['result']['addr']
                self._bigMemory.pop()
                self.insert(result, self._return_values.pop())

            elif self._quadruples[i]['operator'] == 'END':
                endFlag = True
            # </editor-fold>

            # <editor-fold desc="ARRAYS">
            elif self._quadruples[i]['operator'] == 'VER':
                exp = self.get_value(self._quadruples[i]['l_value']['addr'])
                # print("---\nQ {} \nVER {}\n--- ".format(self._quadruples[i], exp))
                if exp >= 500000:
                    exp = self.get_value(exp)
                dim = int(self._quadruples[i]['result']['addr']) - 1
                if 0 <= exp <= dim:
                    pass
                else:
                    print("The dimensions of the array dont match")
                    # sys.exit(0)

            # </editor-fold>

            # <editor-fold desc="IO">

            # Read value from user
            elif self._quadruples[i]['operator'] == 'INPUT':

                result = self._quadruples[i]['result']
                addr = result['addr']

                _input = input("<- ").strip()
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

                self.insert(addr, _input)

            # Show value in terminal
            elif self._quadruples[i]['operator'] == 'PRINT':

                aux = self.get_value(self._quadruples[i]['result']['addr'],
                                     self._access_type(self._quadruples[i]['result']))

                print("-> {} ".format(aux))
            # </editor-fold>

            # <editor-fold desc="MOVE">
            elif self._quadruples[i]['operator'] == 'MOVEUP':

                up = self.get_value(self._quadruples[i]['result']['addr'])
                self._turtle.setheading(90)
                self._turtle.forward(up)

            elif self._quadruples[i]['operator'] == 'MOVEDOWN':

                move = self.get_value(self._quadruples[i]['result']['addr'])
                self._turtle.setheading(270)
                self._turtle.forward(move)

            elif self._quadruples[i]['operator'] == 'MOVERIGHT':

                move = self.get_value(self._quadruples[i]['result']['addr'])
                self._turtle.setheading(0)
                self._turtle.forward(move)

            elif self._quadruples[i]['operator'] == 'MOVELEFT':

                move = self.get_value(self._quadruples[i]['result']['addr'])
                self._turtle.setheading(180)
                self._turtle.forward(move)
            # </editor-fold>

            # <editor-fold desc="PEN">
            elif self._quadruples[i]['operator'] == 'COLOR':

                color = self.get_value(self._quadruples[i]['result']['addr']).strip()

                if re.match(regex_color, color):
                    self._turtle.pencolor(color)
                else:
                    print("Invalid Hex color")
                    sys.exit(1)

            elif self._quadruples[i]['operator'] == 'PENSIZE':
                # TODO: Function not implemented on compiler only on VM
                size = self.get_value(self._quadruples[i]['result']['addr'])
                self._turtle.pensize(size)

            elif self._quadruples[i]['operator'] == 'DRAW':

                action = self.get_value(self._quadruples[i]['result']['addr'])

                if action:
                    self._turtle.pendown()
                else:
                    self._turtle.penup()

            elif self._quadruples[i]['operator'] == 'STARTPOSITION':
                x = self.get_value(self._quadruples[i]['r_value']['addr'])
                y = self.get_value(self._quadruples[i]['result']['addr'])

                self._turtle.setx(x)
                self._turtle.sety(y)

            elif self._quadruples[i]['operator'] == 'SCREENSIZES':
                result = self._quadruples[i]['result']
                addr = result['addr']
                self.insert(addr, self._screen.screensize()[int(self._screen_dim)])
                self._screen_dim = not self._screen_dim

            elif self._quadruples[i]['operator'] == 'GO':

                x = self.get_value(self._quadruples[i]['r_value']['addr'])
                y = self.get_value(self._quadruples[i]['result']['addr'])

                self._turtle.penup()
                self._turtle.goto(x, y)
                self._turtle.pendown()


            # </editor-fold>

            # <editor-fold desc="DRAW">
            elif self._quadruples[i]['operator'] == 'SQUARE':
                angle = self.get_value(self._quadruples[i]['r_value']['addr'])
                length = self.get_value(self._quadruples[i]['result']['addr'])

                for i in range(4):
                    self._turtle.forward(length)
                    self._turtle.right(angle)

            elif self._quadruples[i]['operator'] == 'CIRCLE':
                radius = self.get_value(self._quadruples[i]['r_value']['addr'])
                angle = self.get_value(self._quadruples[i]['result']['addr'])
                self._turtle.circle(radius, angle)

            elif self._quadruples[i]['operator'] == 'CLEAN':
                self._turtle.clear()


            # </editor-fold>

            # <editor-fold desc="Special Functions">
            elif self._quadruples[i]['operator'] == 'FIBONACCI':

                n = self.get_value(self._quadruples[i]['result']['addr'])
                fib = self._fibonacci(n)
                self._turtle.setx(0)
                self._turtle.sety(0)
                self._draw_fib(fib, 6)

            elif self._quadruples[i]['operator'] == 'SLEEP':
                ms = self.get_value(self._quadruples[i]['result']['addr'])
                print("...zzz")
                time.sleep(float(ms))
            # </editor-fold>

            else:
                pass
            i += 1


if __name__ == '__main__':
    big_machine = BigMachine("fat.txt")
    big_machine.process_quadruples()
