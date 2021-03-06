from enum import IntEnum
from fattie.belly.fluffyvariable import FluffyVariable

match_operators = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "TIMES",
    "/": "DIVIDE",
    "equals": "EQUALS",
    "less": "LESS",
    "greater": "GREATER",
    "notequal": "NOTEQUAL",
    "return": "RETURN"
}


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

    ERA = 24
    RETURN = 25
    ENDPROC = 26
    END = 27
    PARAM = 28
    GETRET = 29
    VER = 30


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
    SCREENSIZES = 114

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

    # For test proposes only
    def parse(self):
        r_v = self.r_value
        if self.r_value is not None:
            r_v = self.r_value.parse() if isinstance(self.r_value, FluffyVariable) else self.r_value

        return {
            "operator": self.operator.name,
            "l_value": self.l_value.parse() if self.l_value is not None else self.l_value,
            "r_value": r_v,
            "result": self.result.parse() if self.result is not None else self.result
        }


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

    def fill(self, position, value):
        self.stack[position].result = value

    def write_to_file(self, file):
        for i in self.stack:
            file.write(str(i.parse()) + "\n")

    # For test proposes only
    def print(self):
        i = 0
        for value in self.stack:
            print(str(i) + " ->", value.parse())
            i += 1
