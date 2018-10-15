from fattie.belly.quadruple import Operator, SpecialFunction
from fattie.belly.types import Types


class Cube:

    def __init__(self):
        self.cube = {}

    def set_cube(self, op, value_l, value_r, result):

        if op not in self.cube:
            self.cube[op] = dict()
        if value_l not in self.cube[op]:
            self.cube[op][value_l] = dict()

        self.cube[op][value_l][value_r] = result

    # For test proposes only
    def print(self):
        print(self.cube)


# Create semantic cube

cube = Cube()
# Sums
cube.set_cube(Operator.PLUS, Types.INT, Types.INT, Types.INT)
cube.set_cube(Operator.PLUS, Types.INT, Types.FLOAT, Types.FLOAT)
cube.set_cube(Operator.PLUS, Types.FLOAT, Types.INT, Types.FLOAT)
cube.set_cube(Operator.PLUS, Types.FLOAT, Types.FLOAT, Types.FLOAT)
cube.set_cube(Operator.PLUS, Types.CHAR, Types.CHAR, Types.CHAR)
#  Rests
cube.set_cube(Operator.MINUS, Types.INT, Types.INT, Types.INT)
cube.set_cube(Operator.MINUS, Types.INT, Types.FLOAT, Types.FLOAT)
cube.set_cube(Operator.MINUS, Types.FLOAT, Types.INT, Types.FLOAT)
cube.set_cube(Operator.MINUS, Types.FLOAT, Types.FLOAT, Types.FLOAT)
# Multiplications
cube.set_cube(Operator.TIMES, Types.INT, Types.INT, Types.INT)
cube.set_cube(Operator.TIMES, Types.INT, Types.FLOAT, Types.FLOAT)
cube.set_cube(Operator.TIMES, Types.FLOAT, Types.INT, Types.FLOAT)
cube.set_cube(Operator.TIMES, Types.FLOAT, Types.FLOAT, Types.FLOAT)
# Divisions
cube.set_cube(Operator.DIVIDE, Types.INT, Types.INT, Types.FLOAT)
cube.set_cube(Operator.DIVIDE, Types.INT, Types.FLOAT, Types.FLOAT)
cube.set_cube(Operator.DIVIDE, Types.FLOAT, Types.INT, Types.FLOAT)
cube.set_cube(Operator.DIVIDE, Types.FLOAT, Types.FLOAT, Types.FLOAT)
# Comparison if its the same
cube.set_cube(Operator.EQUALS, Types.INT, Types.INT, Types.BOOLEAN)
cube.set_cube(Operator.EQUALS, Types.FLOAT, Types.FLOAT, Types.BOOLEAN)
cube.set_cube(Operator.EQUALS, Types.BOOLEAN, Types.BOOLEAN, Types.BOOLEAN)
cube.set_cube(Operator.EQUALS, Types.CHAR, Types.CHAR, Types.CHAR)
# Less than
cube.set_cube(Operator.LESS, Types.INT, Types.INT, Types.BOOLEAN)
cube.set_cube(Operator.LESS, Types.INT, Types.FLOAT, Types.BOOLEAN)
cube.set_cube(Operator.LESS, Types.FLOAT, Types.INT, Types.BOOLEAN)
cube.set_cube(Operator.LESS, Types.FLOAT, Types.FLOAT, Types.BOOLEAN)
# Greater than
cube.set_cube(Operator.GREATER, Types.INT, Types.INT, Types.BOOLEAN)
cube.set_cube(Operator.GREATER, Types.INT, Types.FLOAT, Types.BOOLEAN)
cube.set_cube(Operator.GREATER, Types.FLOAT, Types.INT, Types.BOOLEAN)
cube.set_cube(Operator.GREATER, Types.FLOAT, Types.FLOAT, Types.BOOLEAN)
# Different than
cube.set_cube(Operator.NOTEQUAL, Types.INT, Types.INT, Types.BOOLEAN)
cube.set_cube(Operator.NOTEQUAL, Types.INT, Types.FLOAT, Types.BOOLEAN)
cube.set_cube(Operator.NOTEQUAL, Types.FLOAT, Types.INT, Types.BOOLEAN)
cube.set_cube(Operator.NOTEQUAL, Types.FLOAT, Types.FLOAT, Types.BOOLEAN)
cube.set_cube(Operator.NOTEQUAL, Types.BOOLEAN, Types.BOOLEAN, Types.BOOLEAN)
# Boolean comparison
cube.set_cube(Operator.AND, Types.BOOLEAN, Types.BOOLEAN, Types.BOOLEAN)
cube.set_cube(Operator.OR, Types.BOOLEAN, Types.BOOLEAN, Types.BOOLEAN)
cube.set_cube(Operator.NOT, Types.BOOLEAN, None, Types.BOOLEAN)
# Assignation
cube.set_cube(Operator.EQUAL, Types.INT, Types.INT, Types.INT)
cube.set_cube(Operator.EQUAL, Types.FLOAT, Types.FLOAT, Types.FLOAT)
cube.set_cube(Operator.EQUAL, Types.BOOLEAN, Types.BOOLEAN, Types.BOOLEAN)
cube.set_cube(Operator.EQUAL, Types.CHAR, Types.CHAR, Types.CHAR)

# SpecialFunctions

# Input
cube.set_cube(SpecialFunction.INPUT, Types.CHAR, None, Types.CHAR)
cube.set_cube(SpecialFunction.INPUT, Types.INT, None, Types.INT)
cube.set_cube(SpecialFunction.INPUT, Types.FLOAT, None, Types.FLOAT)
# Print
cube.set_cube(SpecialFunction.PRINT, Types.INT, None, None)
cube.set_cube(SpecialFunction.PRINT, Types.CHAR, None, None)
cube.set_cube(SpecialFunction.PRINT, Types.FLOAT, None, None)
# MoveUp
cube.set_cube(SpecialFunction.MOVEUP, Types.INT, None, None)
cube.set_cube(SpecialFunction.MOVEUP, Types.CHAR, None, None)
cube.set_cube(SpecialFunction.MOVEUP, Types.FLOAT, None, None)
# MoveDown
cube.set_cube(SpecialFunction.MOVEDOWN, Types.INT, None, None)
cube.set_cube(SpecialFunction.MOVEDOWN, Types.CHAR, None, None)
cube.set_cube(SpecialFunction.MOVEDOWN, Types.FLOAT, None, None)
# MoveRight
cube.set_cube(SpecialFunction.MOVERIGHT, Types.INT, None, None)
cube.set_cube(SpecialFunction.MOVERIGHT, Types.CHAR, None, None)
cube.set_cube(SpecialFunction.MOVERIGHT, Types.FLOAT, None, None)
# MoveLeft
cube.set_cube(SpecialFunction.MOVELEFT, Types.INT, None, None)
cube.set_cube(SpecialFunction.MOVELEFT, Types.CHAR, None, None)
cube.set_cube(SpecialFunction.MOVELEFT, Types.FLOAT, None, None)
# Angle
cube.set_cube(SpecialFunction.ANGLE, Types.INT, None, None)
# Color
cube.set_cube(SpecialFunction.COLOR, Types.INT, None, Types.CHAR)
# Circle
cube.set_cube(SpecialFunction.CIRCLE, Types.INT, None, None)
# Square
cube.set_cube(SpecialFunction.SQUARE, Types.INT, None, None)
# Clean
cube.set_cube(SpecialFunction.CLEAN, Types.INT, None, None)
cube.set_cube(SpecialFunction.CLEAN, Types.FLOAT, None, None)
# Draw
cube.set_cube(SpecialFunction.DRAW, Types.INT, None, None)
cube.set_cube(SpecialFunction.DRAW, Types.FLOAT, None, None)
# StartPosition<--------------- Checar lo de la doble atributo de la funcion
cube.set_cube(SpecialFunction.STARTPOSITION, Types.INT, Types.INT, None)
cube.set_cube(SpecialFunction.STARTPOSITION, Types.FLOAT, Types.FLOAT, None)
# ScreenSizeX
cube.set_cube(SpecialFunction.SCREENSIZESX, Types.INT, None, Types.INT)
# ScreenSizeY
cube.set_cube(SpecialFunction.SCREENSIZESY, Types.INT, None, Types.INT)
# GO change of position with out painting
cube.set_cube(SpecialFunction.GO, Types.INT, None, None)
# Fibonacci
cube.set_cube(SpecialFunction.FIBONACCI, Types.INT, None, None)
# Factorial
cube.set_cube(SpecialFunction.FACTORIAL, Types.INT, None, None)
# Sleep sleep de funcition N miliseconds
cube.set_cube(SpecialFunction.SLEEP, Types.INT, None, None)

print(cube.__dict__)
