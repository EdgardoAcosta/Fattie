from fattie.belly.quadruple import Operator, SpecialFunction
from fattie.belly.types import Types
from fattie.belly.exceptions import BigError


class Cube:

    def __init__(self):
        self.cube = {}

    def set_cube(self, op, value_l, value_r, result):

        if op not in self.cube:
            self.cube[op] = dict()
        if value_l not in self.cube[op]:
            self.cube[op][value_l] = dict()

        self.cube[op][value_l][value_r] = result

    def compare_types(self, oper, value_l, value_r):
        # print("Op {} , L {} , R {}".format(oper, value_l, value_r))
        if oper in self.cube:
            if value_l in self.cube[oper]:
                try:
                    if self.cube[oper][value_l][value_r]:
                        return self.cube[oper][value_l][value_r]
                except KeyError as e:
                    return False

        return False

    # For test proposes only

    def insert_values(self):
        # Sums
        self.set_cube(Operator.PLUS, Types.INT, Types.INT, Types.INT)
        self.set_cube(Operator.PLUS, Types.INT, Types.FLOAT, Types.FLOAT)
        self.set_cube(Operator.PLUS, Types.FLOAT, Types.INT, Types.FLOAT)
        self.set_cube(Operator.PLUS, Types.FLOAT, Types.FLOAT, Types.FLOAT)
        self.set_cube(Operator.PLUS, Types.CHAR, Types.CHAR, Types.CHAR)
        #  Rests
        self.set_cube(Operator.MINUS, Types.INT, Types.INT, Types.INT)
        self.set_cube(Operator.MINUS, Types.INT, Types.FLOAT, Types.FLOAT)
        self.set_cube(Operator.MINUS, Types.FLOAT, Types.INT, Types.FLOAT)
        self.set_cube(Operator.MINUS, Types.FLOAT, Types.FLOAT, Types.FLOAT)
        # Multiplications
        self.set_cube(Operator.TIMES, Types.INT, Types.INT, Types.INT)
        self.set_cube(Operator.TIMES, Types.INT, Types.FLOAT, Types.FLOAT)
        self.set_cube(Operator.TIMES, Types.FLOAT, Types.INT, Types.FLOAT)
        self.set_cube(Operator.TIMES, Types.FLOAT, Types.FLOAT, Types.FLOAT)
        # Divisions
        self.set_cube(Operator.DIVIDE, Types.INT, Types.INT, Types.FLOAT)
        self.set_cube(Operator.DIVIDE, Types.INT, Types.FLOAT, Types.FLOAT)
        self.set_cube(Operator.DIVIDE, Types.FLOAT, Types.INT, Types.FLOAT)
        self.set_cube(Operator.DIVIDE, Types.FLOAT, Types.FLOAT, Types.FLOAT)
        # Comparison if its the same
        self.set_cube(Operator.EQUALS, Types.INT, Types.INT, Types.BOOLEAN)
        self.set_cube(Operator.EQUALS, Types.FLOAT, Types.FLOAT, Types.BOOLEAN)
        self.set_cube(Operator.EQUALS, Types.BOOLEAN, Types.BOOLEAN, Types.BOOLEAN)
        self.set_cube(Operator.EQUALS, Types.CHAR, Types.CHAR, Types.CHAR)
        # Less than
        self.set_cube(Operator.LESS, Types.INT, Types.INT, Types.BOOLEAN)
        self.set_cube(Operator.LESS, Types.INT, Types.FLOAT, Types.BOOLEAN)
        self.set_cube(Operator.LESS, Types.FLOAT, Types.INT, Types.BOOLEAN)
        self.set_cube(Operator.LESS, Types.FLOAT, Types.FLOAT, Types.BOOLEAN)
        # Greater than
        self.set_cube(Operator.GREATER, Types.INT, Types.INT, Types.BOOLEAN)
        self.set_cube(Operator.GREATER, Types.INT, Types.FLOAT, Types.BOOLEAN)
        self.set_cube(Operator.GREATER, Types.FLOAT, Types.INT, Types.BOOLEAN)
        self.set_cube(Operator.GREATER, Types.FLOAT, Types.FLOAT, Types.BOOLEAN)
        # Different than
        self.set_cube(Operator.NOTEQUAL, Types.INT, Types.INT, Types.BOOLEAN)
        self.set_cube(Operator.NOTEQUAL, Types.INT, Types.FLOAT, Types.BOOLEAN)
        self.set_cube(Operator.NOTEQUAL, Types.FLOAT, Types.INT, Types.BOOLEAN)
        self.set_cube(Operator.NOTEQUAL, Types.FLOAT, Types.FLOAT, Types.BOOLEAN)
        self.set_cube(Operator.NOTEQUAL, Types.BOOLEAN, Types.BOOLEAN, Types.BOOLEAN)
        # Boolean comparison
        self.set_cube(Operator.AND, Types.BOOLEAN, Types.BOOLEAN, Types.BOOLEAN)
        self.set_cube(Operator.OR, Types.BOOLEAN, Types.BOOLEAN, Types.BOOLEAN)
        self.set_cube(Operator.NOT, Types.BOOLEAN, None, Types.BOOLEAN)
        # Assignation
        self.set_cube(Operator.EQUAL, Types.INT, Types.INT, Types.INT)
        self.set_cube(Operator.EQUAL, Types.INT, Types.FLOAT, Types.INT)
        self.set_cube(Operator.EQUAL, Types.FLOAT, Types.FLOAT, Types.FLOAT)
        self.set_cube(Operator.EQUAL, Types.FLOAT, Types.INT, Types.FLOAT)
        self.set_cube(Operator.EQUAL, Types.BOOLEAN, Types.BOOLEAN, Types.BOOLEAN)
        self.set_cube(Operator.EQUAL, Types.CHAR, Types.CHAR, Types.CHAR)

        # SpecialFunctions

        # Input
        self.set_cube(SpecialFunction.INPUT, Types.CHAR, None, Types.CHAR)
        self.set_cube(SpecialFunction.INPUT, Types.INT, None, Types.INT)
        self.set_cube(SpecialFunction.INPUT, Types.FLOAT, None, Types.FLOAT)
        # Print
        self.set_cube(SpecialFunction.PRINT, Types.INT, None, None)
        self.set_cube(SpecialFunction.PRINT, Types.CHAR, None, None)
        self.set_cube(SpecialFunction.PRINT, Types.FLOAT, None, None)
        # MoveUp
        self.set_cube(SpecialFunction.MOVEUP, Types.INT, None, None)
        self.set_cube(SpecialFunction.MOVEUP, Types.CHAR, None, None)
        self.set_cube(SpecialFunction.MOVEUP, Types.FLOAT, None, None)
        # MoveDown
        self.set_cube(SpecialFunction.MOVEDOWN, Types.INT, None, None)
        self.set_cube(SpecialFunction.MOVEDOWN, Types.CHAR, None, None)
        self.set_cube(SpecialFunction.MOVEDOWN, Types.FLOAT, None, None)
        # MoveRight
        self.set_cube(SpecialFunction.MOVERIGHT, Types.INT, None, None)
        self.set_cube(SpecialFunction.MOVERIGHT, Types.CHAR, None, None)
        self.set_cube(SpecialFunction.MOVERIGHT, Types.FLOAT, None, None)
        # MoveLeft
        self.set_cube(SpecialFunction.MOVELEFT, Types.INT, None, None)
        self.set_cube(SpecialFunction.MOVELEFT, Types.CHAR, None, None)
        self.set_cube(SpecialFunction.MOVELEFT, Types.FLOAT, None, None)
        # Angle
        self.set_cube(SpecialFunction.ANGLE, Types.INT, None, None)
        # Color
        self.set_cube(SpecialFunction.COLOR, Types.INT, None, Types.CHAR)
        # Circle
        self.set_cube(SpecialFunction.CIRCLE, Types.INT, None, None)
        # Square
        self.set_cube(SpecialFunction.SQUARE, Types.INT, None, None)
        # Clean
        self.set_cube(SpecialFunction.CLEAN, Types.INT, None, None)
        self.set_cube(SpecialFunction.CLEAN, Types.FLOAT, None, None)
        # Draw
        self.set_cube(SpecialFunction.DRAW, Types.INT, None, None)
        self.set_cube(SpecialFunction.DRAW, Types.FLOAT, None, None)
        # StartPosition<--------------- Checar lo de la doble atributo de la funcion
        self.set_cube(SpecialFunction.STARTPOSITION, Types.INT, Types.INT, None)
        self.set_cube(SpecialFunction.STARTPOSITION, Types.FLOAT, Types.FLOAT, None)
        # ScreenSizeX
        self.set_cube(SpecialFunction.SCREENSIZESX, Types.INT, None, Types.INT)
        # ScreenSizeY
        self.set_cube(SpecialFunction.SCREENSIZESY, Types.INT, None, Types.INT)
        # GO change of position with out painting
        self.set_cube(SpecialFunction.GO, Types.INT, None, None)
        # Fibonacci
        self.set_cube(SpecialFunction.FIBONACCI, Types.INT, None, None)
        # Factorial
        self.set_cube(SpecialFunction.FACTORIAL, Types.INT, None, None)
        # Sleep sleep de funcition N miliseconds
        self.set_cube(SpecialFunction.SLEEP, Types.INT, None, None)

        # self.print()

    def print(self):
        print(self.cube)


# Create semantic cube

cube = Cube()
