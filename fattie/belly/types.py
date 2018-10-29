from enum import IntEnum, Enum
from fattie.belly.exceptions import BigError


class Types(Enum):
    INT = 1
    FLOAT = 2
    CHAR = 3
    BOOLEAN = 4

    ARRAY = 5
    MATRIX = 6
