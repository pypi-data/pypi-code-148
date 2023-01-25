# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ..Utils.ParameterDataTimestamps import ParameterDataTimestamps
from .ParameterDataTimestamp import ParameterDataTimestamp
from ...InteropHelpers.InteropUtils import InteropUtils


class ParameterData(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterData
        
        Returns
        ----------
        
        ParameterData:
            Instance wrapping the .net type ParameterData
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = ParameterData._ParameterData__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(ParameterData, cls).__new__(cls)
            ParameterData._ParameterData__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterData
        
        Returns
        ----------
        
        ParameterData:
            Instance wrapping the .net type ParameterData
        """
        if '_ParameterData__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del ParameterData._ParameterData__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("parameterdata_constructor")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor(capacity: int = None) -> c_void_p:
        """
        Parameters
        ----------
        
        capacity: int
            (Optional) Underlying .Net type is int. Defaults to 10
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterData
        """
        result = InteropUtils.invoke("parameterdata_constructor", capacity)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdata_constructor2")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_ubyte, ctypes.c_ubyte]
    @staticmethod
    def Constructor2(rawData: c_void_p, parametersFilter: c_void_p = None, merge: bool = True, clean: bool = True) -> c_void_p:
        """
        Parameters
        ----------
        
        rawData: c_void_p
            GC Handle Pointer to .Net type ParameterDataRaw
        
        parametersFilter: c_void_p
            (Optional) GC Handle Pointer to .Net type string[]. Defaults to None
        
        merge: bool
            (Optional) Underlying .Net type is Boolean. Defaults to True
        
        clean: bool
            (Optional) Underlying .Net type is Boolean. Defaults to True
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterData
        """
        merge_bool = 1 if merge else 0
        clean_bool = 1 if clean else 0
        
        result = InteropUtils.invoke("parameterdata_constructor2", rawData, parametersFilter, merge_bool, clean_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdata_constructor3")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_ubyte, ctypes.c_ubyte]
    @staticmethod
    def Constructor3(timestamps: c_void_p, merge: bool = True, clean: bool = True) -> c_void_p:
        """
        Parameters
        ----------
        
        timestamps: c_void_p
            GC Handle Pointer to .Net type List<ParameterDataTimestamp>
        
        merge: bool
            (Optional) Underlying .Net type is Boolean. Defaults to True
        
        clean: bool
            (Optional) Underlying .Net type is Boolean. Defaults to True
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterData
        """
        merge_bool = 1 if merge else 0
        clean_bool = 1 if clean else 0
        
        result = InteropUtils.invoke("parameterdata_constructor3", timestamps, merge_bool, clean_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdata_clone")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Clone(self, parametersFilter: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        parametersFilter: c_void_p
            GC Handle Pointer to .Net type string[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterData
        """
        result = InteropUtils.invoke("parameterdata_clone", self.__pointer, parametersFilter)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdata_get_timestamps")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Timestamps(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataTimestamps
        """
        result = InteropUtils.invoke("parameterdata_get_timestamps", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdata_addtimestamp")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def AddTimestamp(self, dateTime: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        dateTime: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataTimestamp
        """
        result = InteropUtils.invoke("parameterdata_addtimestamp", self.__pointer, dateTime)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdata_addtimestamp2")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def AddTimestamp2(self, timeSpan: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        timeSpan: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataTimestamp
        """
        result = InteropUtils.invoke("parameterdata_addtimestamp2", self.__pointer, timeSpan)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdata_addtimestampmilliseconds")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_longlong]
    def AddTimestampMilliseconds(self, timeMilliseconds: int) -> c_void_p:
        """
        Parameters
        ----------
        
        timeMilliseconds: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataTimestamp
        """
        timeMilliseconds_long = ctypes.c_longlong(timeMilliseconds)
        
        result = InteropUtils.invoke("parameterdata_addtimestampmilliseconds", self.__pointer, timeMilliseconds_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdata_addtimestampnanoseconds")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_longlong]
    def AddTimestampNanoseconds(self, timeNanoseconds: int) -> c_void_p:
        """
        Parameters
        ----------
        
        timeNanoseconds: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataTimestamp
        """
        timeNanoseconds_long = ctypes.c_longlong(timeNanoseconds)
        
        result = InteropUtils.invoke("parameterdata_addtimestampnanoseconds", self.__pointer, timeNanoseconds_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdata_equals")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Equals(self, obj: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        obj: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("parameterdata_equals", self.__pointer, obj)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdata_gethashcode")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def GetHashCode(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("parameterdata_gethashcode", self.__pointer)
        return result
