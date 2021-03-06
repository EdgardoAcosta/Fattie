from inspect import signature, Parameter


class Builder:
    def __init__(self, target):
        sig = signature(target)
        self._attrs = {}
        self._params = sig.parameters
        self._target = target

    def build(self):
        params = []

        for key in self._params:
            if key in self._attrs:
                params.append(self._attrs[key])
            elif self._params[key].default is Parameter.empty:
                raise AttributeError("No Value {} in {}".format(key, self._target))

        return self._target(*params)

    def put(self, name, value):
        if name not in self._params:
            raise AttributeError("Wrong values for the function")
        self._attrs[name] = value
        return self

    def parse(self):
        print({
            "_attrs": self._attrs,
            "_target": self._target
        })

    def clear(self):
        self._attrs.clear()



