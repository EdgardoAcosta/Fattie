# Class to check if a variable exist on the variable table and add new variable if not exit to table
class FluffyVariable:
    # Init variables of class
    def __init__(self, id_var, type_var, addr=None):
        self.id_var = id_var
        self.type_var = type_var
        self.addr = addr

    # For test proposes only
    def parse(self):
        return({
            "id_var": self.id_var,
            "type_var ": self.type_var,
            "addr ": self.addr
        })
