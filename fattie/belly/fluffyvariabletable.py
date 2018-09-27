# Class to check if a variable exist on the variable table and add new variable if not exit to table
class FluffyVariableTable:
    # Init variables of class
    def __init__(self, scope=None):
        self.scope = scope  # Parent of a variable
        self.variable = {}  # Dictionary of variables

    # Check if variable is on dictionary of if is in parent
    def find_variable(self, id_var):
        return self.variable.get(id_var)

    def add_variable(self, id_var, type_variable, value):
        if id_var not in self.variable:
            # Save de variable if not in dictionary
            self.variable[id_var] = {
                "value": value,
                "type": type_variable
            }
            print(self.variable)
            return True
        # Return false if already exist variable
        return False
