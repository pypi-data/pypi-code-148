# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ..Models.ParameterDataTimestamp import ParameterDataTimestamp
from ...InteropHelpers.InteropUtils import InteropUtils


class ParameterDataTimestamps(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterDataTimestamps
        
        Returns
        ----------
        
        ParameterDataTimestamps:
            Instance wrapping the .net type ParameterDataTimestamps
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = ParameterDataTimestamps._ParameterDataTimestamps__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(ParameterDataTimestamps, cls).__new__(cls)
            ParameterDataTimestamps._ParameterDataTimestamps__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterDataTimestamps
        
        Returns
        ----------
        
        ParameterDataTimestamps:
            Instance wrapping the .net type ParameterDataTimestamps
        """
        if '_ParameterDataTimestamps__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del ParameterDataTimestamps._ParameterDataTimestamps__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("parameterdatatimestamps_getenumerator")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def GetEnumerator(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IEnumerator<ParameterDataTimestamp>
        """
        result = InteropUtils.invoke("parameterdatatimestamps_getenumerator", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamps_get_item")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_int]
    def get_Item(self, index: int) -> c_void_p:
        """
        Parameters
        ----------
        
        index: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataTimestamp
        """
        result = InteropUtils.invoke("parameterdatatimestamps_get_item", self.__pointer, index)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamps_get_count")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_Count(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("parameterdatatimestamps_get_count", self.__pointer)
        return result
