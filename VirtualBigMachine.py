import sys
import ast
import re
import turtle
import time

regex_int = '^[0-9]+$'
regex_float = '[0-9]*\.[0-9]+|[0-9]+'
regex_boolean = '(^True$|^False$)'
regex_color = '#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'


class BigMachine:
    """
     Function to start the VM, will initialize the necessary memory,allocate the variables and
     read the self._quadruples generated from the compiler
     :return: None
     """

    def __init__(self, filename):
        # stack with the self._quadrupless
        self._quadruples = list()

        # definition of the memory
        # Memory slots for ints 0 - 100000,floats 100000 - 200000,chars 200000 - 300000, bools 300000 - 400000,
        # const 500000 - 600000
        self._fatMemory = 600000 * [None]

        # definition of the globalmemory
        # Global memory slots for ints 0 - 100000,floats 100000 - 200000,chars 200000 - 300000, bools 300000 - 400000,
        # const 500000 - 600000
        self._fatGlobalMemory = 600000 * [None]

        self._screen_dim = True

        self._screen = turtle.Screen()
        self._turtle = turtle.Turtle()
        self._start_x = self._turtle.setx(0)
        self._start_y = self._turtle.sety(0)
        self._turtle.pensize(2)
        self._turtle.speed()
        self._screen.screensize(400, 400)

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

    def insert(self, addr, value):
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

    def process_quadruples(self):
        i = 0
        endFlag = False
        while not endFlag:
            # print("i -> ", i)

            # assignation of constants
            if self._quadruples[i]['operator'] == 'CONST':
                l_val = self._quadruples[i]['l_value']['addr']
                result = self._quadruples[i]['result']['addr']

                self._insert_in_fat_memory(result, l_val)
                # self._print_global_value(result)result)

            # assignation of any variable
            elif self._quadruples[i]['operator'] == 'EQUAL':
                l_val = self._quadruples[i]['l_value']['addr']
                result = self._quadruples[i]['result']['addr']

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
                    # self._print_global_value(result)

                else:
                    self._insert_in_fat_memory(result, value)
                    # self._print_global_value(result)result)

            # add of two variables
            elif self._quadruples[i]['operator'] == 'PLUS':

                l_val = self._quadruples[i]['l_value']['addr']
                r_val = self._quadruples[i]['r_value']['addr']
                result = self._quadruples[i]['result']['addr']

                # verify if is going to subtract l_val from a global variable
                if l_val / 1000000 >= 1:
                    l_val = l_val - 1000000
                    l_operand = self._get_value_fat_global_memory(l_val)

                else:
                    l_operand = self._get_value_fat_memory(l_val)

                # verify if is going to stract r_val from a global variable
                if r_val / 1000000 >= 1:
                    r_val = r_val - 1000000

                    r_operand = self._get_value_fat_global_memory(r_val)

                else:
                    r_operand = self._get_value_fat_memory(r_val)

                # verify if si going to assign to a global variable
                if result / 1000000 >= 1:
                    result = result - 1000000
                    evaluation = l_operand + r_operand
                    self._insert_in_fat_global_memory(result, evaluation)
                    # self._print_global_value(result)

                else:

                    evaluation = l_operand + r_operand
                    self._insert_in_fat_memory(result, evaluation)
                    # self._print_global_value(result)result)

                # TODO: Checar el UMINUS PORQUE NO SABES QUE PEDO

            # subtract of two variables
            elif self._quadruples[i]['operator'] == 'MINUS':
                l_val = self._quadruples[i]['l_value']['addr']
                r_val = self._quadruples[i]['r_value']['addr']
                result = self._quadruples[i]['result']['addr']

                # verify if is going to subtract l_val from a global variable
                if l_val / 1000000 >= 1:
                    l_val = l_val - 1000000
                    l_operand = self._get_value_fat_global_memory(l_val)

                else:
                    l_operand = self._get_value_fat_memory(l_val)

                # verify if is going to stract r_val from a global variable
                if r_val / 1000000 >= 1:
                    r_val = r_val - 1000000

                    r_operand = self._get_value_fat_global_memory(r_val)

                else:
                    r_operand = self._get_value_fat_memory(r_val)

                # verify if si going to assign to a global variable
                if result / 1000000 >= 1:
                    result = result - 1000000
                    evaluation = l_operand - r_operand
                    self._insert_in_fat_global_memory(result, evaluation)
                    # self._print_global_value(result)

                else:

                    evaluation = l_operand - r_operand
                    self._insert_in_fat_memory(result, evaluation)
                    # # self._print_global_value(result)result)

            # multiply two variables
            elif self._quadruples[i]['operator'] == 'TIMES':
                l_val = self._quadruples[i]['l_value']['addr']
                r_val = self._quadruples[i]['r_value']['addr']
                result = self._quadruples[i]['result']['addr']

                # verify if is going to subtract l_val from a global variable
                if l_val / 1000000 >= 1:
                    l_val = l_val - 1000000
                    l_operand = self._get_value_fat_global_memory(l_val)

                else:
                    l_operand = self._get_value_fat_memory(l_val)

                # verify if is going to stract r_val from a global variable
                if r_val / 1000000 >= 1:
                    r_val = r_val - 1000000

                    r_operand = self._get_value_fat_global_memory(r_val)

                else:
                    r_operand = self._get_value_fat_memory(r_val)

                # verify if si going to assign to a global variable
                if result / 1000000 >= 1:
                    result = result - 1000000
                    evaluation = l_operand * r_operand
                    self._insert_in_fat_global_memory(result, evaluation)
                    # self._print_global_value(result)

                else:

                    evaluation = l_operand * r_operand
                    self._insert_in_fat_memory(result, evaluation)
                    # self._print_global_value(result)result)

            # divide two variables
            elif self._quadruples[i]['operator'] == 'DIVIDE':

                l_val = self._quadruples[i]['l_value']['addr']
                r_val = self._quadruples[i]['r_value']['addr']
                result = self._quadruples[i]['result']['addr']

                # verify if is going to subtract l_val from a global variable
                l_operand = self.get_value(l_val)

                # verify if is going to stract r_val from a global variable
                r_operand = self.get_value(r_val)

                # verify if si going to assign to a global variable
                if result / 1000000 >= 1:
                    result = result - 1000000
                    evaluation = l_operand / r_operand
                    self._insert_in_fat_global_memory(result, evaluation)
                    # self._print_global_value(result)

                else:
                    evaluation = l_operand / r_operand
                    self._insert_in_fat_memory(result, evaluation)
                    # self._print_global_value(result)result)

            # <editor-fold desc="Logical operator">
            elif self._quadruples[i]['operator'] == 'LESS':
                l_val = self.get_value(self._quadruples[i]['l_value']['addr'])
                r_val = self.get_value(self._quadruples[i]['r_value']['addr'])
                result = self._quadruples[i]['result']['addr']

                self.insert(result, (l_val < r_val))

            elif self._quadruples[i]['operator'] == 'GREATER':
                l_val = self.get_value(self._quadruples[i]['l_value']['addr'])
                r_val = self.get_value(self._quadruples[i]['r_value']['addr'])
                result = self._quadruples[i]['result']['addr']

                self.insert(result, (l_val > r_val))

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

                if not expression:
                    i = self._quadruples[i]['result']['addr']
                    continue
            # </editor-fold>

            # <editor-fold desc="Function">
            elif self._quadruples[i]['operator'] == 'GOSUB':
                l_val = self._quadruples[i]['l_value']
                r_val = self._quadruples[i]['r_value']
                result = self._quadruples[i]['result']

            elif self._quadruples[i]['operator'] == 'ENPROC':
                l_val = self._quadruples[i]['l_value']
                r_val = self._quadruples[i]['r_value']
                result = self._quadruples[i]['result']

            elif self._quadruples[i]['operator'] == 'RETURN':
                l_val = self._quadruples[i]['l_value']
                r_val = self._quadruples[i]['r_value']
                result = self._quadruples[i]['result']

            elif self._quadruples[i]['operator'] == 'PARAM':
                l_val = self._quadruples[i]['l_value']
                r_val = self._quadruples[i]['r_value']
                result = self._quadruples[i]['result']

            elif self._quadruples[i]['operator'] == 'GETRET':
                l_val = self._quadruples[i]['l_value']
                r_val = self._quadruples[i]['r_value']
                result = self._quadruples[i]['result']

            elif self._quadruples[i]['operator'] == 'END':
                endFlag = True
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

                result = self._quadruples[i]['result']
                if result['addr'] / 1000000 >= 1:
                    result = result - 1000000
                    aux = self._get_value_fat_global_memory(result)
                else:
                    aux = self._get_value_fat_memory(result['addr'])

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

                color = self.get_value(self._quadruples[i]['result']['addr'])

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

            # elif self._quadruples[i]['operator'] == 'AND':
            #     l_val = self._quadruples[i]['l_value']['addr']
            #     r_val = self._quadruples[i]['r_value']['addr']
            #     result = self._quadruples[i]['result']['addr']
            #
            # elif self._quadruples[i]['operator'] == 'OR':
            #     l_val = self._quadruples[i]['l_value']['addr']
            #     r_val = self._quadruples[i]['r_value']['addr']
            #     result = self._quadruples[i]['result']['addr']
            #
            # elif self._quadruples[i]['operator'] == 'NOT':
            #     l_val = self._quadruples[i]['l_value']['addr']
            #     r_val = self._quadruples[i]['r_value']['addr']
            #     result = self._quadruples[i]['result']['addr']

            else:
                # print(self._quadruples[i])
                # print("Error self._quadruples[i] not found")
                # sys.exit(0)
                pass
            i += 1

    # <editor-fold desc="Prints for test">
    def _print_local_value(self, position):
        print("local:{}=>{}".format(position, self._fatMemory[position]))

    def _print_global_value(self, position):
        print("global:{}=>{}".format(position, self._fatGlobalMemory[position]))
    # </editor-fold>


if __name__ == '__main__':
    big_machine = BigMachine("fat.txt")
    big_machine.process_quadruples()
