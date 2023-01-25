# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...InteropHelpers.InteropUtils import InteropUtils


class ParameterDataRaw(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterDataRaw
        
        Returns
        ----------
        
        ParameterDataRaw:
            Instance wrapping the .net type ParameterDataRaw
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = ParameterDataRaw._ParameterDataRaw__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(ParameterDataRaw, cls).__new__(cls)
            ParameterDataRaw._ParameterDataRaw__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterDataRaw
        
        Returns
        ----------
        
        ParameterDataRaw:
            Instance wrapping the .net type ParameterDataRaw
        """
        if '_ParameterDataRaw__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del ParameterDataRaw._ParameterDataRaw__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("parameterdataraw_constructor")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataRaw
        """
        result = InteropUtils.invoke("parameterdataraw_constructor")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdataraw_constructor2")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [ctypes.c_longlong, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Constructor2(epoch: int, timestamps: c_void_p, numericValues: c_void_p, stringValues: c_void_p, binaryValues: c_void_p, tagValues: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        epoch: int
            Underlying .Net type is long
        
        timestamps: c_void_p
            GC Handle Pointer to .Net type long[]
        
        numericValues: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, double?[]>
        
        stringValues: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, string[]>
        
        binaryValues: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, byte[][]>
        
        tagValues: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, string[]>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataRaw
        """
        epoch_long = ctypes.c_longlong(epoch)
        
        result = InteropUtils.invoke("parameterdataraw_constructor2", epoch_long, timestamps, numericValues, stringValues, binaryValues, tagValues)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdataraw_tojson")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def ToJson(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("parameterdataraw_tojson", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdataraw_get_epoch")
    __interop_func.restype = ctypes.c_longlong
    __interop_func.argtypes = [c_void_p]
    def get_Epoch(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("parameterdataraw_get_epoch", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdataraw_set_epoch")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, ctypes.c_longlong]
    def set_Epoch(self, value: int) -> None:
        """
        Parameters
        ----------
        
        value: int
            Underlying .Net type is long
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_long = ctypes.c_longlong(value)
        
        InteropUtils.invoke("parameterdataraw_set_epoch", self.__pointer, value_long)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdataraw_get_timestamps")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Timestamps(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type long[]
        """
        result = InteropUtils.invoke("parameterdataraw_get_timestamps", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdataraw_set_timestamps")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Timestamps(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type long[]
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("parameterdataraw_set_timestamps", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdataraw_get_numericvalues")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_NumericValues(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Dictionary<string, double?[]>
        """
        result = InteropUtils.invoke("parameterdataraw_get_numericvalues", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdataraw_set_numericvalues")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_NumericValues(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, double?[]>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("parameterdataraw_set_numericvalues", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdataraw_get_stringvalues")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_StringValues(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Dictionary<string, string[]>
        """
        result = InteropUtils.invoke("parameterdataraw_get_stringvalues", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdataraw_set_stringvalues")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_StringValues(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, string[]>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("parameterdataraw_set_stringvalues", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdataraw_get_binaryvalues")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_BinaryValues(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Dictionary<string, byte[][]>
        """
        result = InteropUtils.invoke("parameterdataraw_get_binaryvalues", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdataraw_set_binaryvalues")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_BinaryValues(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, byte[][]>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("parameterdataraw_set_binaryvalues", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdataraw_get_tagvalues")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_TagValues(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Dictionary<string, string[]>
        """
        result = InteropUtils.invoke("parameterdataraw_get_tagvalues", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdataraw_set_tagvalues")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_TagValues(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, string[]>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("parameterdataraw_set_tagvalues", self.__pointer, value)
