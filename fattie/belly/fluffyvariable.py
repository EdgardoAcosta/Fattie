from fattie.belly.types import Types
from fattie.belly.exceptions import BigError

local_addr = {
    Types.INT: 000000,
    Types.FLOAT: 100000,
    Types.CHAR: 200000,
    Types.BOOLEAN: 300000
}
equivalent = {
    Types.ARRAY_INT: Types.INT,
    Types.ARRAY_FLOAT: Types.FLOAT,
    Types.ARRAY_CHAR: Types.CHAR,
    Types.ARRAY_BOOLEAN: Types.BOOLEAN,
    Types.MATRIX_INT: Types.INT,
    Types.MATRIX_FLOAT: Types.FLOAT,
    Types.MATRIX_CHAR: Types.CHAR,
    Types.MATRIX_BOOLEAN: Types.BOOLEAN

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
        kind = equivalent.get(kind,kind)
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
            result[e] = self.local_address[e] % local_addr[e] if local_addr[e] != 0 else self.local_address[e] - \
                                                                                         local_addr[e]
        return result

    def reset_addr(self):
        self.local_address = local_addr.copy()


# Class to check if a variable exist on the variable table and add new variable if not exit to table
class FluffyVariable:
    # Init variables of class
    def __init__(self, id_var, type_var, addr=None):
        self.id_var = id_var
        self.type_var = type_var
        self.addr = addr

    def __setitem__(self, instance, value):
        self.instance = value

    def print(self):
        print({
            "id_var": self.id_var,
            "type_var": self.type_var.name if self.type_var is not None else '',
            "addr": self.addr,  # if self.addr is not None else '',
        })

    # For test proposes only
    def parse(self):
        return ({
            "id_var": self.id_var,
            "type_var": self.type_var.name if self.type_var is not None else '',
            "addr": self.addr,  # if self.addr is not None else '',
        })
