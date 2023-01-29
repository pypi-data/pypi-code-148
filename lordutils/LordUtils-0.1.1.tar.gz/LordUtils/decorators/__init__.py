

class callCounter:
    """
    Count how many times a function called
    """

    def __init__(self, func):
        self.func = func
        self.counter = 0
        self.initCounter = 0

    def __call__(self, *args, **kwargs):
        self.counter = self.counter + 1
        self.initCounter = self.initCounter + 1
        return self.func(*args, **kwargs)

    def reset(self):
        self.counter = 0

    def setCounter(self, num):
        self.counter = num

    def get(self):
        return self.counter

    def getFullCount(self):
        return self.initCounter


class return_bool_counter(object):
    """
    Count how many times a function return true and false
    """
    def __init__(self, func):
        self.func = func
        self.true_counter = 0
        self.false_counter = 0

    def __call__(self, *args, **kwargs):
        r = self.func(*args, **kwargs)
        if isinstance(r, bool):
            if r:
                self.true_counter += 1
            else:
                self.false_counter += 1
        elif isinstance(r, list | tuple):
            if True in r:
                self.true_counter += 1
            else:
                self.false_counter += 1
        return r

    def reset(self):
        self.true_counter = 0
        self.false_counter = 0

    def get_true(self):
        return self.true_counter

    def get_false(self):
        return self.false_counter


class CachedProperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = instance.__dict__[self.func.__name__] = self.func(instance)
        return value

