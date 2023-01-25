import weakref

def __dummy(*args, **kwargs):
    pass

def nativedecorator(cls):
    orig_init = cls.__init__
    orig_classname = cls.__name__
    orig_finalizer = getattr(cls, "_" + orig_classname + "__finalizerfunc", __dummy)
    orig_enter = getattr(cls, "__enter__", __dummy)
    orig_exit = getattr(cls, "__exit__", __dummy)
    orig_dispose = getattr(cls, "dispose", __dummy)

    def new_init(self, *args, **kwargs):
        orig_init(self, *args, **kwargs)
        self.__nativedecorator__finalizer = weakref.finalize(self, new_finalizerfunc, self)

    def new_finalizerfunc(self):
        orig_finalizer(self)
        getattr(self, "_" + orig_classname + "__interop")._dispose_ptr()
        self.__nativedecorator__finalizer.detach()

    def new_enter(self):
        orig_enter(self)

    def new_exit(self, exc_type, exc_val, exc_tb):
        orig_exit(self, exc_type, exc_val, exc_tb)
        new_dispose(self)

    def new_dispose(self, *args, **kwargs):
        if not self.__nativedecorator__finalizer.alive:
            return
        orig_dispose(self, *args, **kwargs)
        self.__nativedecorator__finalizer()


    cls.__init__ = new_init
    cls.__finalizerfunc = new_finalizerfunc
    cls.__enter__ = new_enter
    cls.__exit__ = new_exit
    cls.dispose = new_dispose
    return cls