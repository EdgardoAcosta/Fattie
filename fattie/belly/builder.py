from fattie.belly.fluffyvariabletable import FluffyVariableTable
from inspect import signature


class Builder:
    def __init__(self, target):
        sig = signature(target)
        self._attrs = {}
        self._required = [param.name for param in sig.parameters]
        self._target = target

    def build(self):
        params = []
        for key in self._required:
            if key not in self._attrs:
                raise ValueError()

            params.append(self._attrs[key])

        return self._target(*params)

    def put(self, name, var):
        self._attrs[name] = var
        return self

    def clear(self):
        self._attrs.clear()


var_builder = Builder(FluffyVariableTable)


fn_builder = Builder(FluffyVariableTable)

fn_builder.put('id', 'name').put('type', 'Int')

var = fn_builder.build()