# Class to check if a variable exist on the variable table and add new variable if not exit to table
class FluffyVariable:
    # Init variables of class
    def __init__(self, id_var, type_var):
        self.id_var = id_var
        self.type_var = type_var
        self.addr = None

# test = {
#            "main": {
#                "test_var": {
#                    "value": 12,
#                    "type": "Int"
#                },
#                "test_var2": {
#                    "value": 'Hola',
#                    "type": "String"
#                }
#            },
#            "fun1": {
#                "test_var3": {
#                    "value": 'adios',
#                    "type": "String"
#                }
#            }
#
#        }
