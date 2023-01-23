"""
JavaScript object datatype in Python

(c) tankalxat34 - 2023
License: MIT

"""


def var2str(variable):
    return [global_var for global_var in globals() if id(variable) == id(globals()[global_var])]


class Object:
    """
    Implementing object such as in JavaScipt
    """
    def __init__(self, *args, **kwargs):
        if args:
            for arg in args:
                if type(arg) == dict:
                    self._parse(arg)
                else:
                    raise ValueError("First argument must be 'dict'")
        else:
            for kwarg in kwargs.keys():
                self._parse_by_key_value(kwargs, kwarg)

    # local methods
    def _parse_by_key_value(self, arg, key):
        if type(arg[key]) == dict:
            self.__setattr__(key, ObjectNotation(arg[key]))

        elif type(arg[key]) == list:
            to_dict = {}
            for i in range(len(arg[key])):
                to_dict[str(i)] = arg[key][i]
            self.__setattr__(key, ObjectNotation(to_dict))

        else:
            self.__setattr__(key, arg[key])

    def _parse(self, arg):
        for key in arg.keys():
            self._parse_by_key_value(arg, key)
    
    # common methods
    def keys(self):
        """
        Return `tuple` of keys from object
        """
        return tuple(self.__dict__.keys())
    
    def values(self):
        """
        Return `tuple` of values from object
        """
        return tuple(self.__dict__.values())
    
    def raw(self, key):
        """
        Return raw value by specified key
        """
        return self.__dict__[key]
    
    def has(self, __attr_name) -> bool:
        """
        Return `True` if object has this attribute
        """
        return __attr_name in self
    
    # properties    
    @property
    def length(self) -> int:
        """
        Return count of keys in this object
        """
        return int(len(self.keys()))
    
    # magic methods
    def __str__(self) -> str:
        result = ""
        for attr in self.__dict__.keys():
            result += f"{attr}: '{self.__dict__[attr]}', " if type(self.__dict__[attr]) == str \
                else f"{attr}: {self.__dict__[attr]}, "
        return f"JSObject({result[:-2]})"
    
    def __len__(self) -> int:
        return self.length
    
    def __contains__(self, __o: any):
        return __o in self.keys()
    
    def __iter__(self):
        return iter(tuple(self.keys()))
    
    def __setitem__(self, key, value):
        setattr(self, str(key), value)
    
    def __getitem__(self, key):
        try:
            return getattr(self, self.keys()[key])
        except Exception:
            return getattr(self, str(key))

    def __delitem__(self, __key):
        try:
            return delattr(self, self.keys()[__key])
        except AttributeError:
            return delattr(self, str(__key))

    

class ObjectNotation(Object):
    """
    Implementing access to keys by `obj.path.to.your.key` notation as in JavaScript

    #### Creating new object

    Using dictionary:
        >>> obj = ObjectNotation({"key1": "value1", "key2": "value2", "key3": {"a": "b", "lst": [14, 5, 6, 12]}})
    
    Using arguments:
        >>> obj = ObjectNotation(key1="value1", key2="value2", key3={"a": "b", "lst": [14, 5, 6, 12]})
    
    #### Getting values by keys or indexes
        >>> obj[0]
        value1
        >>> obj.key2
        value2
        >>> obj["key3"]
        [14, 5, 6, 12]
    
    #### Creating new keys in object
        >>> obj.year = 2023

        or:

        >>> obj.set("year", 2023)
        
        or:

        >>> year = 2023
        >>> obj.set(year)

        or:
        
        >>> obj["year"] = 2023
    
    #### Saving functions in object
        >>> obj.fibonachi = lambda n: 1 if n <= 2 else obj.fibonachi(n - 1) + obj.fibonachi(n - 2)
        >>> obj.fibonachi(7)
        13

    #### Removing keys by string-names or indexes
        >>> del obj.year

        or:
        
        >>> del obj[-1]

        or:

        >>> del obj["year"]
    
    #### Changing value by key
        >>> obj.key1 = 123

        or:

        >>> obj["key1"] = 123

    #### Cycle `for` by object

    Indexes:
        >>> for i in range(len(obj)):
        ...     print(i)
        0
        1
        2
    
    Keys:
        >>> for k in obj:
        ...     print(k)
        key1
        key2
        key3
        fibonachi

    Values:
        >>> for v in obj.values():
        ...     print(v)
        123
        value2
        JSObject(a: 'b', lst: JSObject(0: 14, 1: 5, 2: 6, 3: 12))
        <function <lambda> at 0x0000020189F19480>
    
    #### Boolean statements
        >>> "key3" in obj
        True
        >>> "fake_key" in obj
        False

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set(self, __name, __value = None):
        """
        Setting new value in object
        """
        if __value:
            self.__setattr__(__name, ObjectNotation({__name: __value}).raw(__name))
        else:
            self.__setattr__(var2str(__name)[0], ObjectNotation({var2str(__name)[0]: __name}).raw(var2str(__name)[0]))
    
    def copy(self):
        """
        Get a new copy of object
        """
        return ObjectNotation(self.__dict__)


