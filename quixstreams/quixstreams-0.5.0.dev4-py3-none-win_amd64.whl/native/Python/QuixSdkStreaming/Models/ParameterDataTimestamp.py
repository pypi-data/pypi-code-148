# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ..ParameterDataTimestampValues import ParameterDataTimestampValues
from ..Utils.ParameterDataTimestampTags import ParameterDataTimestampTags
from ...SystemPrivateCoreLib.System.DateTime import DateTime
from ...SystemPrivateCoreLib.System.TimeSpan import TimeSpan
from ...InteropHelpers.InteropUtils import InteropUtils


class ParameterDataTimestamp(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterDataTimestamp
        
        Returns
        ----------
        
        ParameterDataTimestamp:
            Instance wrapping the .net type ParameterDataTimestamp
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = ParameterDataTimestamp._ParameterDataTimestamp__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(ParameterDataTimestamp, cls).__new__(cls)
            ParameterDataTimestamp._ParameterDataTimestamp__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterDataTimestamp
        
        Returns
        ----------
        
        ParameterDataTimestamp:
            Instance wrapping the .net type ParameterDataTimestamp
        """
        if '_ParameterDataTimestamp__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del ParameterDataTimestamp._ParameterDataTimestamp__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("parameterdatatimestamp_get_parameters")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Parameters(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataTimestampValues
        """
        result = InteropUtils.invoke("parameterdatatimestamp_get_parameters", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamp_get_tags")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Tags(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataTimestampTags
        """
        result = InteropUtils.invoke("parameterdatatimestamp_get_tags", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamp_get_timestampnanoseconds")
    __interop_func.restype = ctypes.c_longlong
    __interop_func.argtypes = [c_void_p]
    def get_TimestampNanoseconds(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("parameterdatatimestamp_get_timestampnanoseconds", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamp_set_timestampnanoseconds")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, ctypes.c_longlong]
    def set_TimestampNanoseconds(self, value: int) -> None:
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
        
        InteropUtils.invoke("parameterdatatimestamp_set_timestampnanoseconds", self.__pointer, value_long)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamp_get_timestampmilliseconds")
    __interop_func.restype = ctypes.c_longlong
    __interop_func.argtypes = [c_void_p]
    def get_TimestampMilliseconds(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("parameterdatatimestamp_get_timestampmilliseconds", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamp_get_timestamp")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Timestamp(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("parameterdatatimestamp_get_timestamp", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamp_get_timestampastimespan")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_TimestampAsTimeSpan(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("parameterdatatimestamp_get_timestampastimespan", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamp_addvalue")
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
            GC Handle Pointer to .Net type ParameterDataTimestamp
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        
        result = InteropUtils.invoke("parameterdatatimestamp_addvalue", self.__pointer, parameterId_ptr, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamp_addvalue2")
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
            GC Handle Pointer to .Net type ParameterDataTimestamp
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        result = InteropUtils.invoke("parameterdatatimestamp_addvalue2", self.__pointer, parameterId_ptr, value_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamp_addvalue3")
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
            GC Handle Pointer to .Net type ParameterDataTimestamp
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        
        result = InteropUtils.invoke("parameterdatatimestamp_addvalue3", self.__pointer, parameterId_ptr, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamp_addvalue4")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def AddValue4(self, parameterId: str, value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        parameterId: str
            Underlying .Net type is string
        
        value: c_void_p
            GC Handle Pointer to .Net type ParameterValue
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataTimestamp
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        
        result = InteropUtils.invoke("parameterdatatimestamp_addvalue4", self.__pointer, parameterId_ptr, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamp_removevalue")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def RemoveValue(self, parameterId: str) -> c_void_p:
        """
        Parameters
        ----------
        
        parameterId: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataTimestamp
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        
        result = InteropUtils.invoke("parameterdatatimestamp_removevalue", self.__pointer, parameterId_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamp_addtag")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def AddTag(self, tagId: str, tagValue: str) -> c_void_p:
        """
        Parameters
        ----------
        
        tagId: str
            Underlying .Net type is string
        
        tagValue: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataTimestamp
        """
        tagId_ptr = InteropUtils.utf8_to_ptr(tagId)
        tagValue_ptr = InteropUtils.utf8_to_ptr(tagValue)
        
        result = InteropUtils.invoke("parameterdatatimestamp_addtag", self.__pointer, tagId_ptr, tagValue_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamp_addtags")
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
            GC Handle Pointer to .Net type ParameterDataTimestamp
        """
        result = InteropUtils.invoke("parameterdatatimestamp_addtags", self.__pointer, tags)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdatatimestamp_removetag")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def RemoveTag(self, tagId: str) -> c_void_p:
        """
        Parameters
        ----------
        
        tagId: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDataTimestamp
        """
        tagId_ptr = InteropUtils.utf8_to_ptr(tagId)
        
        result = InteropUtils.invoke("parameterdatatimestamp_removetag", self.__pointer, tagId_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
