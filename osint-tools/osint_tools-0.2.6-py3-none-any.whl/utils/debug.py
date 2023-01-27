
from functools import wraps, partial

def debug(func=None, *, prefix=''):
    '''
    DEBUGS FUNCTIONS:
    - debugs functions by printing out nice error repr
    '''
    if func is None:
        return partial(debug, prefix=prefix)
        
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__qualname__)
        return func(*args, **kwargs)
    return wrapper

def debugmethods(cls):
    '''
    DEBUGS CLASSES (just methods, not @classmethods or @staticmethods)

    Example:

        @debugmethods
        class Spam:
            def a(self):
                pass

            def b(self):
                pass
    '''
    for key, val in vars(cls).items():
        if callable(val):
            setattr(cls, key, debug(val))
    return cls


class debugmeta(type):

    '''
    Meta Class that propogates through entire class hierarchy.
    Can think of it almost as a genetic mutation.

    Example:
            class Base(metaclass=debugmeta):
                pass
            
            class Ham(Base):
            
                def a(self):
                    pass
    '''
    def __new__(cls, clsname, bases, clsdict):
        clsobj = super().__new__(cls, clsname, bases, clsdict)
        clsobj = debugmethods(clsobj)
        return clsobj
