# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ....InteropHelpers.InteropUtils import InteropUtils


class ParameterDataBuilder(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterDataBuilder
        
        Returns
        ----------
        
        ParameterDataBuilder:
            Instance wrapping the .net type ParameterDataBuilder
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = ParameterDataBuilder._ParameterDataBuilder__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(ParameterDataBuilder, cls).__new__(cls)
            ParameterDataBuilder._ParameterDataBuilder__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterDataBuilder
        
        Returns
        ----------
        
        ParameterDataBuilder:
            Instance wrapping the .net type ParameterDataBuilder
        """
        if '_ParameterDataBuilder__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del ParameterDataBuilder._ParameterDataBuilder__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("parameterdatabuilder_constructor")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Constructor(buffer: c_void_p, data: c_void_p, timestamp: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        buffer: c_void_p
            GC Handle Pointer to .Net type ParametersBufferWriter
        
        data: c_void_p
            GC Handle Pointer to .Net type ParameterData
        
        timestamp: c_void_p
            GC Handle Pointer to .Net type ParameterDataTimestamp
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataBuilder
        """
        result = InteropUtils.invoke("parameterdatabuilder_constructor", buffer, data, timestamp)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatabuilder_addvalue")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_double]
    def AddValue(self, parameterId: str, value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        parameterId: str
            Underlying .Net type is string
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataBuilder
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        
        result = InteropUtils.invoke("parameterdatabuilder_addvalue", self.__pointer, parameterId_ptr, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatabuilder_addvalue2")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def AddValue2(self, parameterId: str, value: str) -> c_void_p:
        """
        Parameters
        ----------
        
        parameterId: str
            Underlying .Net type is string
        
        value: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataBuilder
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        result = InteropUtils.invoke("parameterdatabuilder_addvalue2", self.__pointer, parameterId_ptr, value_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatabuilder_addvalue3")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def AddValue3(self, parameterId: str, value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        parameterId: str
            Underlying .Net type is string
        
        value: c_void_p
            GC Handle Pointer to .Net type byte[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataBuilder
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        
        result = InteropUtils.invoke("parameterdatabuilder_addvalue3", self.__pointer, parameterId_ptr, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatabuilder_addtag")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def AddTag(self, tagId: str, value: str) -> c_void_p:
        """
        Parameters
        ----------
        
        tagId: str
            Underlying .Net type is string
        
        value: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataBuilder
        """
        tagId_ptr = InteropUtils.utf8_to_ptr(tagId)
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        result = InteropUtils.invoke("parameterdatabuilder_addtag", self.__pointer, tagId_ptr, value_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatabuilder_addtags")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def AddTags(self, tags: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        tags: c_void_p
            GC Handle Pointer to .Net type IEnumerable<KeyValuePair<string, string>>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataBuilder
        """
        result = InteropUtils.invoke("parameterdatabuilder_addtags", self.__pointer, tags)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatabuilder_write")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p]
    def Write(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("parameterdatabuilder_write", self.__pointer)
