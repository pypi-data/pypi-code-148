# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .....InteropHelpers.InteropUtils import InteropUtils


class NotifyCollectionChangedEventArgs(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type NotifyCollectionChangedEventArgs
        
        Returns
        ----------
        
        NotifyCollectionChangedEventArgs:
            Instance wrapping the .net type NotifyCollectionChangedEventArgs
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = NotifyCollectionChangedEventArgs._NotifyCollectionChangedEventArgs__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(NotifyCollectionChangedEventArgs, cls).__new__(cls)
            NotifyCollectionChangedEventArgs._NotifyCollectionChangedEventArgs__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type NotifyCollectionChangedEventArgs
        
        Returns
        ----------
        
        NotifyCollectionChangedEventArgs:
            Instance wrapping the .net type NotifyCollectionChangedEventArgs
        """
        if '_NotifyCollectionChangedEventArgs__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del NotifyCollectionChangedEventArgs._NotifyCollectionChangedEventArgs__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("notifycollectionchangedeventargs_get_newstartingindex")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_NewStartingIndex(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("notifycollectionchangedeventargs_get_newstartingindex", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("notifycollectionchangedeventargs_get_oldstartingindex")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_OldStartingIndex(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("notifycollectionchangedeventargs_get_oldstartingindex", self.__pointer)
        return result
