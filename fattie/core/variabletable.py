# Class to check if a variable exist on the variable table and add new variable if not exit to table
class VariableTable:
    # Init variables of class
    def __init__(self, parent = None):
        self.parent = parent  # Parent of a variable
        self.variable = {}  # Dictionary of variables

    # Check if variable is on dictionary of if is in parent
    def find_variable(self, id):
        if self.parent:
            # If variable not in dictionary return the father
            return self.variable.get(id, self.parent.find_variable(id=id))
        return self.variable.get(id)

    def add_variable(self, id, value):
        if id not in self.variable:
            # Save de variable if not in dictionary
            self.variable[id] = value
            return True
        # Return false if already exist variable
        return False
