from fattie.belly.types import Types
from fattie.belly.exceptions import BigError


class AddressLocation:
    def __init__(self):
        self.address = {
            Types.INT: 000000,
            Types.FLOAT: 100000,
            Types.CHAR: 200000,
            Types.BOOLEAN: 300000
        }
        self.other_type = 400000

    def get_addr(self, kind):
        if kind not in self.address:
            raise BigError("Error type not defined")

        return self.address[kind]

    def update_addr(self, kind):
        if kind not in self.address:
            raise BigError("Error type not defined")

        self.address[kind] += 1


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
            "addr ": self.addr if self.addr is not None else ''
        })
