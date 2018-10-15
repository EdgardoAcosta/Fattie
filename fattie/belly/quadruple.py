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


class QuadruplePack:
    def __init__(self):
        pass
