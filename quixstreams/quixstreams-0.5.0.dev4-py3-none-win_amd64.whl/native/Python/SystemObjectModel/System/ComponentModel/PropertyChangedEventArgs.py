# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ....InteropHelpers.InteropUtils import InteropUtils


class PropertyChangedEventArgs(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type PropertyChangedEventArgs
        
        Returns
        ----------
        
        PropertyChangedEventArgs:
            Instance wrapping the .net type PropertyChangedEventArgs
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = PropertyChangedEventArgs._PropertyChangedEventArgs__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(PropertyChangedEventArgs, cls).__new__(cls)
            PropertyChangedEventArgs._PropertyChangedEventArgs__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type PropertyChangedEventArgs
        
        Returns
        ----------
        
        PropertyChangedEventArgs:
            Instance wrapping the .net type PropertyChangedEventArgs
        """
        if '_PropertyChangedEventArgs__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del PropertyChangedEventArgs._PropertyChangedEventArgs__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("propertychangedeventargs_constructor")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor(propertyName: str) -> c_void_p:
        """
        Parameters
        ----------
        
        propertyName: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type PropertyChangedEventArgs
        """
        propertyName_ptr = InteropUtils.utf8_to_ptr(propertyName)
        
        result = InteropUtils.invoke("propertychangedeventargs_constructor", propertyName_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("propertychangedeventargs_get_propertyname")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_PropertyName(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("propertychangedeventargs_get_propertyname", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
