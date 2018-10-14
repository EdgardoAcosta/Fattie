from fattie.belly.fluffyvariable import FluffyVariable


# Class to create the tables for the functions
class HeavyFunction:
    # Constructor
    def __init__(self, id_function=None, return_type=None, params=None):
        self.id_function = id_function
        self.return_type = return_type
        self.params = params

    def parse(self):
        return ({
            "id_function": self.id_function,
            "return_type ": self.return_type,
            "params ": self.params
        })
