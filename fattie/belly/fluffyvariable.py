from enum import Enum
from fattie.belly.types import Types
from fattie.belly.exceptions import BigError

local_addr = {
    Types.INT: 000000,
    Types.FLOAT: 100000,
    Types.CHAR: 200000,
    Types.BOOLEAN: 300000
}

global_addr = {
    Types.INT: 1000000,
    Types.FLOAT: 1100000,
    Types.CHAR: 1200000,
    Types.BOOLEAN: 1300000
}


class AddressLocation:
    def __init__(self):
        self.local_address = local_addr.copy()
        self.global_address = global_addr.copy()
        self.other_type = 400000

    def get_addr(self, kind, g_var=False):
        if kind not in self.local_address:
            raise BigError("Error type not defined")
        if g_var:
            return self.global_address[kind]
        return self.local_address[kind]

    def set_addr(self, kind, g_var=False):
        if kind not in self.local_address:
            raise BigError("Error type not defined")
        # Global variable
        if g_var:
            actual_value = self.global_address[kind]
            self.global_address[kind] += 1
        # Local variables
        else:
            actual_value = self.local_address[kind]
            self.local_address[kind] += 1

        return actual_value

    def calculate_era(self):
        result = {}
        for e in self.local_address:
            result[e.name] = self.local_address[e] % local_addr[e] if local_addr[e] != 0 else self.local_address[e] - \
                                                                                              local_addr[e] + 1
            #  Because the array start on 0 it has to add 1 to all different of zero
            result[e.name] += 10  # (result[e.name] + 10) if result[e.name] != 0 else result[e.name]
        return result

    def reset_addr(self):
        self.local_address = local_addr.copy()


class Access(Enum):
    Direct = 1
    Indirect = 2
    Test = 3


# Class to check if a variable exist on the variable table and add new variable if not exit to table
class FluffyVariable:
    # Init variables of class
    def __init__(self, id_var, type_var, array=None, access=Access.Direct, addr=None):
        self.id_var = id_var
        self.type_var = type_var
        self.addr = addr
        self.array = array
        self.access = access

        if self.array is not None:
            temp = self.array
            while temp is not None:
                temp.var = self
                temp = temp.next

    def __setitem__(self, instance, value):
        self.instance = value

    def parse(self):
        # print(self.array.parse() if self.array is not None else [])
        return ({
            "id_var": self.id_var,
            "type_var": self.type_var.name if self.type_var is not None else '',
            "access": self.access.name,
            "array": self.array.parse() if self.array is not None else [],
            "addr": self.addr,  # if self.addr is not None else '',

        })

    # For test proposes only
    def print(self):
        print({
            "id_var": self.id_var,
            "type_var": self.type_var.name if self.type_var is not None else '',
            "addr": self.addr,  # if self.addr is not None else '',
            "array": self.array.parse() if self.array is not None else [],
        })


class Dimension:
    def __init__(self, size, m=None, var=None):
        self.size = size
        self.m = m
        self.var = var
        self.next = None

    def print(self):
        print({
            "size": self.size,
            "m": self.m,
            "var": self.var.parse() if self.var is not None else self.var
        })

    def parse(self):
        return ({
            "size": self.size,
            "m": self.m,
            "var": {
                "id_var": self.var.id_var,
                "type_var": self.var.type_var.name if self.var.type_var is not None else '',
                "addr": self.var.addr
            }
        })
