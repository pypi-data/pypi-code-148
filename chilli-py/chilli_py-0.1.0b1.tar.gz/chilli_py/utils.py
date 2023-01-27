from time import time 

""" Utility functions """

def myprint(**kwargs):
    """
        myprint 
        Print key - value pairs. 
        For debugging.

        Call, e.g., 

            myprint(etot=-1.75)
    """
    for key,val in kwargs.items():
        print(f"{key} : {val}")

def slice_dct(dct,l):
    """
        slice_dct 
        Get a slice of a dict (dct) 
        according the keys in list l. 
    """
    return dict([(key, value) for key,value in dct.items() if key in l])

def timeit(f):
    """
        timeit
        Decorator write to stdout

        Input
            - f : function
    """
    def f0(*args, **kwargs):
        before = time()
        res = f(*args, **kwargs)
        after = time()
        print('elapsed time ({}) = {:+.15f} [s]'.format(f.__qualname__, after - before))
        return res
    return f0

def tictoc(f):
    """
        timeit
        Decorator write to stdout

        Note
            - maybe should only be used by experts 

        Input
            - f : function
    """
    def f0(*args, **kwargs):
        before = time()
        res = f(*args, **kwargs)
        after = time()
        dt = after - before
        print('elapsed time ({}) = {:+.15f} [s]'.format(f.__qualname__, dt))
        return res, dt 
    return f0


class history():
    """
        history
        Magically transforms a function
        to a class instance
        and collects function return values (RV)
        and timings (T). 
    """
    def __init__(self,f):
        self.f = f
        # Current values
        self.rv = None
        self.t = None
        # History of values
        self.RV = []
        self.T = []
        self.count = 0

    def __call__(self,*args,**kwargs):
        """
            __call__
            Make a class instance callable.
        """
        self._callme(self.f,*args,**kwargs)
        self._log(self.f,*args,**kwargs)
        return self.rv

    def _callme(self,f,*args,**kwargs):
        """
            _callme
            Perform the actual functional call
            plus timing and counting.
        """
        self.count += 1
        before = time()
        self.rv = f(*args,**kwargs)
        after = time()
        self.t = after - before
        self.RV.append(self.rv)
        self.T.append(self.t)

    def _log(self,f,*args,**kwargs):
        """
            _log
            Log the all information.
        """
        print('Function name: {}'.format(self.f.__qualname__))
        print('Doc string: {}'.format(self.f.__doc__))
        print('Function calls: {}'.format(self.count))
        #print('Input: {} {}'.format(*args,**kwargs))
        print('elapsed time ({}) = {:+.15f} [s]'.format(self.f.__qualname__, self.t))
        print('Output: {}'.format(self.rv))
        print(self.RV,self.T)

