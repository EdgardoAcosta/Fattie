from fattie.belly.types import Types
from fattie.belly.exceptions import BigError

addr = {
    Types.INT: 0x0000000,
    Types.FLOAT: 0x0100000,
    Types.CHAR: 0x0200000,
    Types.BOOLEAN: 0x0300000
}


class AddressLocation:
    def __init__(self):
        self.address = addr
        self.other_type = 0x400000

    def get_addr(self, kind):
        if kind not in self.address:
            raise BigError("Error type not defined")

        return self.address[kind]

    def set_addr(self, kind, g_var=False):
        if kind not in self.address:
            raise BigError("Error type not defined")
        # Global variable
        actual_value = self.address[kind]
        if g_var:
            return 0x1000000 | actual_value + 1

        self.address[kind] += 1
        return actual_value

    def reset_addr(self):
        self.address = addr


# Class to check if a variable exist on the variable table and add new variable if not exit to table
class FluffyVariable:
    # Init variables of class
    def __init__(self, id_var, type_var, addr=None):
        self.id_var = id_var
        self.type_var = type_var
        self.addr = addr

    # For test proposes only
    def parse(self):
        return ({
            "id_var": self.id_var,
            "type_var": self.type_var.name if self.type_var is not None else '',
            "addr": self.addr if self.addr is not None else ''
        })
