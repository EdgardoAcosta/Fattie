from inspect import signature


class Builder:
    def __init__(self, target):
        sig = signature(target)
        self._attrs = {}
        self._required = [param for param in sig.parameters]
        self._target = target

    def build(self):
        params = []
        for key in self._required:
            if key not in self._attrs:
                raise AttributeError("No Value {} in {}".format(key, self._target))

            params.append(self._attrs[key])

        return self._target(*params)

    def put(self, name, var):
        if name not in self._required:
            raise AttributeError("Wrong values for the function")
        self._attrs[name] = var
        return self

    def clear(self):
        self._attrs.clear()
