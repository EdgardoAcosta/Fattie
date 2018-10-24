from enum import IntEnum


class Operator(IntEnum):
    PLUS = 1
    MINUS = 2
    TIMES = 3
    DIVIDE = 4
    EQUALS = 5
    LESS = 6
    GREATER = 7
    NOTEQUAL = 8

    AND = 9
    OR = 10
    NOT = 11

    TRUE = 16
    FALSE = 17

    EQUAL = 18

    GOTO = 19
    GOTOF = 20
    GOSUB = 21

    UMINUS = 22

    CONST = 23


class SpecialFunction(IntEnum):
    INPUT = 101
    PRINT = 102
    MOVEUP = 103
    MOVEDOWN = 104
    MOVERIGHT = 105
    MOVELEFT = 106
    ANGLE = 107
    COLOR = 108
    CIRCLE = 109
    SQUARE = 110
    CLEAN = 111
    DRAW = 112
    STARTPOSITION = 113
    SCREENSIZESX = 114
    SCREENSIZESY = 115
    GO = 116
    FIBONACCI = 117
    FACTORIAL = 118
    SLEEP = 119


# Structures for quadruples
class QuadruplePack:
    def __init__(self, operation, l_value=None, r_value=None, result=None):
        self.operator = operation
        self.l_value = l_value
        self.r_value = r_value
        self.result = result


# Structure to manage quadruples stack
class QuadrupleStack:
    def __init__(self):
        self.stack = []
        self.index = 0

    def add(self, quadruple):
        self.stack.append(quadruple)
        self.index += 1

    def delete(self):
        self.stack.pop()
        self.index -= 1

    def print(self):
        print(self.stack)
