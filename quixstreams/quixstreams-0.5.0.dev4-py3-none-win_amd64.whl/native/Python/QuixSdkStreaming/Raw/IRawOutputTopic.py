# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from typing import Callable
from ...InteropHelpers.InteropUtils import InteropUtils


class IRawOutputTopic(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type IRawOutputTopic
        
        Returns
        ----------
        
        IRawOutputTopic:
            Instance wrapping the .net type IRawOutputTopic
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = IRawOutputTopic._IRawOutputTopic__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(IRawOutputTopic, cls).__new__(cls)
            IRawOutputTopic._IRawOutputTopic__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type IRawOutputTopic
        
        Returns
        ----------
        
        IRawOutputTopic:
            Instance wrapping the .net type IRawOutputTopic
        """
        if '_IRawOutputTopic__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del IRawOutputTopic._IRawOutputTopic__weakrefs[self.__pointer.value]
        InteropUtils.free_hptr(self.__pointer)
        self.__finalizer.detach()
    
    def _get_interop_ptr(self) -> c_void_p:
        return self.__pointer
    
    def _dispose_ptr(self):
        self.__finalizer()
    
    def __enter__(self):
        pass
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__finalizer()
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("irawoutputtopic_write")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Write(self, data: c_void_p) -> None:
        """
        Parameters
        ----------
        
        data: c_void_p
            GC Handle Pointer to .Net type RawMessage
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("irawoutputtopic_write", self.__pointer, data)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("irawoutputtopic_add_ondisposed")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnDisposed(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0, p1: value(c_void_p(p0), c_void_p(p1))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in irawoutputtopic_add_ondisposed, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO IRawOutputTopic.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in irawoutputtopic_add_ondisposed, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("irawoutputtopic_add_ondisposed", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("irawoutputtopic_remove_ondisposed")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnDisposed(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0, p1: value(c_void_p(p0), c_void_p(p1))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in irawoutputtopic_remove_ondisposed, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO IRawOutputTopic.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in irawoutputtopic_remove_ondisposed, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("irawoutputtopic_remove_ondisposed", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
