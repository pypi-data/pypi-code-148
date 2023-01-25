# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...InteropHelpers.InteropUtils import InteropUtils


class ParameterDataTimestampTags(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterDataTimestampTags
        
        Returns
        ----------
        
        ParameterDataTimestampTags:
            Instance wrapping the .net type ParameterDataTimestampTags
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = ParameterDataTimestampTags._ParameterDataTimestampTags__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(ParameterDataTimestampTags, cls).__new__(cls)
            ParameterDataTimestampTags._ParameterDataTimestampTags__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterDataTimestampTags
        
        Returns
        ----------
        
        ParameterDataTimestampTags:
            Instance wrapping the .net type ParameterDataTimestampTags
        """
        if '_ParameterDataTimestampTags__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del ParameterDataTimestampTags._ParameterDataTimestampTags__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("parameterdatatimestamptags_getenumerator")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def GetEnumerator(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IEnumerator<KeyValuePair<string, string>>
        """
        result = InteropUtils.invoke("parameterdatatimestamptags_getenumerator", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamptags_get_item")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def get_Item(self, key: str) -> str:
        """
        Parameters
        ----------
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("parameterdatatimestamptags_get_item", self.__pointer, key_ptr)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamptags_get_keys")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Keys(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IEnumerable<string>
        """
        result = InteropUtils.invoke("parameterdatatimestamptags_get_keys", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamptags_get_values")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Values(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IEnumerable<string>
        """
        result = InteropUtils.invoke("parameterdatatimestamptags_get_values", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamptags_get_count")
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
        result = InteropUtils.invoke("parameterdatatimestamptags_get_count", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamptags_containskey")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    def ContainsKey(self, key: str) -> bool:
        """
        Parameters
        ----------
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("parameterdatatimestamptags_containskey", self.__pointer, key_ptr)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamptags_trygetvalue")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def TryGetValue(self, key: str, value: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        key: str
            Underlying .Net type is string
        
        value: c_void_p
            GC Handle Pointer to .Net type String&
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("parameterdatatimestamptags_trygetvalue", self.__pointer, key_ptr, valueOut)
        return result
