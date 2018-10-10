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
    INPUT = 1
    PRINT = 2
    MOVEUP = 3
    MOVEDOWN = 4
    MOVERIGHT = 5
    MOVELEFT = 6
    ANGLE = 7
    COLOR = 8
    CIRCLE = 9
    SQUARE = 10
    CLEAN = 11
    DRAW = 12
    STARTPOSITION = 13
    SCREENSIZESX = 14
    SCREENSIZESY = 15
    GO = 16
    FIBONACCI = 17
    FACTORIAL = 18
    SLEEP = 19


class QuadruplePack:
    def __init__(self):
        pass
