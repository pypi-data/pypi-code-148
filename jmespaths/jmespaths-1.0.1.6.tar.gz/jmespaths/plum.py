class Plum():
    @property
    def __class__(self):
        return type(self.data[self.expression])

    def __init__(self, expression, data) -> None:
        self.expression = expression
        self.data = data.peach() if isinstance(data, Plum) else data

    def __get__(self, instance, owner=None):
        return self.data[self.expression][instance]

    def __len__(self):
        return len(self.data[self.expression])

    def __getitem__(self, index):
        len_of_peach = len(self.data[self.expression])
        if 0-len_of_peach <= index < len_of_peach:
            return Plum(index, self.data[self.expression])
        else:
            raise IndexError()

    def get(self, instance, owner=None):
        try:
            return self.__get__(instance, owner)
        except TypeError:
            return owner
        except KeyError:
            return owner

    def plum(self, value):
        if isinstance(self.data, dict):
            if self.expression not in self.data:
                return
        self.data[self.expression] = value

    def peach(self):
        return self.data[self.expression]

    def keys(self):
        return self.data[self.expression].keys()

    def values(self):
        return self.data[self.expression].values()
