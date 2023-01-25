# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...InteropHelpers.InteropUtils import InteropUtils


class TransportContext(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TransportContext
        
        Returns
        ----------
        
        TransportContext:
            Instance wrapping the .net type TransportContext
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = TransportContext._TransportContext__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(TransportContext, cls).__new__(cls)
            TransportContext._TransportContext__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TransportContext
        
        Returns
        ----------
        
        TransportContext:
            Instance wrapping the .net type TransportContext
        """
        if '_TransportContext__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del TransportContext._TransportContext__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("transportcontext_constructor")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    @staticmethod
    def Constructor(dictionary: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        dictionary: c_void_p
            GC Handle Pointer to .Net type IDictionary<string, Object>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TransportContext
        """
        result = InteropUtils.invoke("transportcontext_constructor", dictionary)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("transportcontext_constructor2")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor2() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TransportContext
        """
        result = InteropUtils.invoke("transportcontext_constructor2")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
