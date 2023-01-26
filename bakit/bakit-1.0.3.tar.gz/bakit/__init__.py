'''
# BAKit
Built-in Alternative Kit

'''

from .storage import Storage, Config, Environ

__version__ = "1.0.3"
__all__ = ["Storage", "Config", "Environ"
           "storage", "config", "environ"]

storage = Storage()
config = Config()
environ = Environ()