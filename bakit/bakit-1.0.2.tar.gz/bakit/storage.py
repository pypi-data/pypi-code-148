from typing import Any, Union
from typing_validation import validate, can_validate
from os import environ

class Storage:
   def __init__(self, data: dict = {}, *, keytype: Any = Any, valuetype: Any = Any, ignore_validation: bool = False):
      if not isinstance(data, dict):
         raise TypeError(f"data must be a dict not {type(data)}")
      if (not ignore_validation) and (not can_validate(keytype)):
         raise ValueError(f"unsupported validation for {repr(keytype)}")
      if (not ignore_validation) and (not can_validate(valuetype)):
         raise ValueError(f"unsupported validation for {repr(valuetype)}")
      
      self.keytype = keytype
      self.valuetype = valuetype
      self._data = data

      self.__ignore_validation = ignore_validation

   @property
   def ignore_validation(self):
      return self.__ignore_validation

   def encodekey(self, key):
      return key

   def decodekey(self, key):
      return key
   
   def encodevalue(self, value):
      return value

   def decodevalue(self, value):
      return value

   def __getitem__(self, key):
      return self.decodevalue(self._data[self.encodevalue(key)])
   
   def __setitem__(self, key, value):
      if not self.__ignore_validation:
         validate(key, self.keytype)
         validate(value, self.valuetype)

      self._data[self.encodevalue(key)] = self.encodekey(value)

   def __delitem__(self, key):
      del self._data[self.encodekey(key)]
   
   def __iter__(self):
      keys = list(self._data)
      for key in keys:
         yield self.decodekey(key)
      
   def __len__(self):
      return len(self._data)

   def __repr__(self):
      return f"Storage({self._data})"

   def copy(self):
      return self._data.copy()
   
   def __ior__(self, other):
        self._data.update(other)
        return self
      
   def __or__(self, other):
      new = other.copy()
      new.update(self._data)

      return new

   def new(self, data: dict = {}, *, keytype: Any = Any, valuetype: Any = Any, ignore_validation: bool = False):
      self.__init__(data, keytype=keytype, valuetype=valuetype, ignore_validation=ignore_validation)
      
class Config(Storage):
   def __init__(self, data: dict = {}):
      super().__init__(data, keytype=str, valuetype=Union[str, int, bool])

   def new(self, *args, **kwargs):
      raise TypeError("can not reinitialize a Config storage")

class Environ(Storage):
   def __init__(self):
      super().__init__(environ.copy(), keytype=str, valuetype=str)

   def new(self, *args, **kwargs):
      raise TypeError("can not reinitialize a Config storage")
