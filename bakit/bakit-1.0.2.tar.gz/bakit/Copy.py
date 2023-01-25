from typing import Any
from pickle import loads, dumps

# def copy(obj:object) -> Any:   
#    try:
#       return obj.copy() # (list, dict, set, frozenset, bytearray) + numpy array
#    except AttributeError:
#       cls = type(obj)

#       copier = getattr(cls, "__copy__", None)
#       if copier:
#          return copier(obj)

#       if isinstance(obj, str):
#          return obj[::-1][::-1]
#       if isinstance(obj, (int, float, complex, bool)):
#          return obj
#       else:
#          pass
         

#    raise TypeError(f"uncopyable object of type {type(obj)}")

def copy(obj:object) -> Any:
   try:
      return loads(dumps(obj))
   except:
      raise TypeError(f"uncopyable object of type {type(obj)}")