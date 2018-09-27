from fattie.belly.fluffyvariabletable import FluffyVariableTable


# Class to create the tables for the functions
class HeavyFunctionTable:
    # Constructor
    def __init__(self, id_function=None, return_type=None, params=None):
        self.id_function = id_function
        self.return_type = return_type
        self.params = params
        self.function = {}

    # Find a function on the table
    def find_function(self, id):
        return self.function.get(id)

    # Add a new function to the table
    def add_function(self, id_function, return_type, params):
        if id_function not in self.function:  # If the function don't exist on the table
            self.function[id_function] = {
                "type": return_type,
                "params": params
            }

            # Add parameter to the Variable Table
            if params:
                variable = FluffyVariableTable(scope=id_function)
                # For each item on the array of params
                for item in params:
                    variable.add_variable(item.get("id"), item.get("type"), None)

            return True
        return False
