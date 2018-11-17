from fattie.belly.fluffyvariable import FluffyVariable


# Class to create the tables for the functions
class HeavyFunction:
    # Constructor
    def __init__(self, id_function=None, return_type=None, params=None, size=None):
        self.id_function = id_function
        self.return_type = return_type
        self.params = params
        self.size = size

    def parse(self):
        return ({
            "id_function": self.id_function,
            "return_type ": self.return_type,
            "params": [param.parse() for param in self.params],  # self.params
            "size": self.size
        })


class ActiveFunction:

    # Constructor
    def __init__(self, _id=None, start_position=None, size=None, params_size=None, return_type=None):
        self.id = _id
        self.start_position = start_position
        self.params_size = params_size
        self.size = size
        self.return_type = return_type

    def clear(self):
        self.id = None
        self.params_size = None
        self.size = None
        self.return_type = None

    def parse(self):
        return ({
            "id": self.id,
            "start_position ": self.start_position,
            "params_size": self.params_size,
            "size": self.size,
            "return_type": self.return_type
        })