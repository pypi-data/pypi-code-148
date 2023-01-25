# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ....SystemPrivateCoreLib.System.DateTime import DateTime
from .ParameterDataBuilder import ParameterDataBuilder
from ....InteropHelpers.InteropUtils import InteropUtils


class ParametersBufferWriter(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParametersBufferWriter
        
        Returns
        ----------
        
        ParametersBufferWriter:
            Instance wrapping the .net type ParametersBufferWriter
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = ParametersBufferWriter._ParametersBufferWriter__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(ParametersBufferWriter, cls).__new__(cls)
            ParametersBufferWriter._ParametersBufferWriter__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParametersBufferWriter
        
        Returns
        ----------
        
        ParametersBufferWriter:
            Instance wrapping the .net type ParametersBufferWriter
        """
        if '_ParametersBufferWriter__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del ParametersBufferWriter._ParametersBufferWriter__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("parametersbufferwriter_get_epoch")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Epoch(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("parametersbufferwriter_get_epoch", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferwriter_set_epoch")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Epoch(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("parametersbufferwriter_set_epoch", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferwriter_addtimestamp")
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
            GC Handle Pointer to .Net type ParameterDataBuilder
        """
        result = InteropUtils.invoke("parametersbufferwriter_addtimestamp", self.__pointer, dateTime)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferwriter_addtimestamp2")
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
            GC Handle Pointer to .Net type ParameterDataBuilder
        """
        result = InteropUtils.invoke("parametersbufferwriter_addtimestamp2", self.__pointer, timeSpan)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferwriter_addtimestampmilliseconds")
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
            GC Handle Pointer to .Net type ParameterDataBuilder
        """
        timeMilliseconds_long = ctypes.c_longlong(timeMilliseconds)
        
        result = InteropUtils.invoke("parametersbufferwriter_addtimestampmilliseconds", self.__pointer, timeMilliseconds_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferwriter_addtimestampnanoseconds")
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
            GC Handle Pointer to .Net type ParameterDataBuilder
        """
        timeNanoseconds_long = ctypes.c_longlong(timeNanoseconds)
        
        result = InteropUtils.invoke("parametersbufferwriter_addtimestampnanoseconds", self.__pointer, timeNanoseconds_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferwriter_write")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Write(self, data: c_void_p) -> None:
        """
        Parameters
        ----------
        
        data: c_void_p
            GC Handle Pointer to .Net type ParameterData
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("parametersbufferwriter_write", self.__pointer, data)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferwriter_get_defaulttags")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_DefaultTags(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Dictionary<string, string>
        """
        result = InteropUtils.invoke("parametersbufferwriter_get_defaulttags", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferwriter_set_defaulttags")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_DefaultTags(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, string>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("parametersbufferwriter_set_defaulttags", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferwriter_flush")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p]
    def Flush(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("parametersbufferwriter_flush", self.__pointer)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferwriter_dispose")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p]
    def Dispose(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("parametersbufferwriter_dispose", self.__pointer)
