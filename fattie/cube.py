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

# cube.set_cube(SpecialFunction.INPUT, Types.CHAR, Types.CHAR, Types.CHAR)

cube.set_cube(SpecialFunction.MOVEUP, Types.INT, None, None)
cube.set_cube(SpecialFunction.MOVEUP, Types.FLOAT, None, None)

# cube.print()
