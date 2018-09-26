from fattie.belly.fluffyvariabletable import FluffyVariableTable


class HeavyFunctionTable():
    def __init__(self):
        self.function = {}

    def find_function(self, id):
        return self.function.get(id)

    def add_function(self, id, type, params=[]):
        if id not in self.function:
            self.function[id] = {
                "type": type,
                "params": params
            }

            if params:
                variable = FluffyVariableTable(scope=id)
                for item in params:
                    variable.add_variable(item.id, item.value)

            return True
        return False
