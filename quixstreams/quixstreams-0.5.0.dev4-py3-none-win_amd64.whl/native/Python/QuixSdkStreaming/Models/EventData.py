# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...SystemPrivateCoreLib.System.DateTime import DateTime
from ...SystemPrivateCoreLib.System.TimeSpan import TimeSpan
from ...InteropHelpers.InteropUtils import InteropUtils


class EventData(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type EventData
        
        Returns
        ----------
        
        EventData:
            Instance wrapping the .net type EventData
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = EventData._EventData__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(EventData, cls).__new__(cls)
            EventData._EventData__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type EventData
        
        Returns
        ----------
        
        EventData:
            Instance wrapping the .net type EventData
        """
        if '_EventData__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del EventData._EventData__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("eventdata_constructor")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor(eventId: str, timestampNanoseconds: int, eventValue: str) -> c_void_p:
        """
        Parameters
        ----------
        
        eventId: str
            Underlying .Net type is string
        
        timestampNanoseconds: int
            Underlying .Net type is long
        
        eventValue: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventData
        """
        eventId_ptr = InteropUtils.utf8_to_ptr(eventId)
        timestampNanoseconds_long = ctypes.c_longlong(timestampNanoseconds)
        eventValue_ptr = InteropUtils.utf8_to_ptr(eventValue)
        
        result = InteropUtils.invoke("eventdata_constructor", eventId_ptr, timestampNanoseconds_long, eventValue_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdata_constructor2")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Constructor2(eventId: str, timestamp: c_void_p, eventValue: str) -> c_void_p:
        """
        Parameters
        ----------
        
        eventId: str
            Underlying .Net type is string
        
        timestamp: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        eventValue: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventData
        """
        eventId_ptr = InteropUtils.utf8_to_ptr(eventId)
        eventValue_ptr = InteropUtils.utf8_to_ptr(eventValue)
        
        result = InteropUtils.invoke("eventdata_constructor2", eventId_ptr, timestamp, eventValue_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdata_constructor3")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Constructor3(eventId: str, timestamp: c_void_p, eventValue: str) -> c_void_p:
        """
        Parameters
        ----------
        
        eventId: str
            Underlying .Net type is string
        
        timestamp: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        eventValue: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventData
        """
        eventId_ptr = InteropUtils.utf8_to_ptr(eventId)
        eventValue_ptr = InteropUtils.utf8_to_ptr(eventValue)
        
        result = InteropUtils.invoke("eventdata_constructor3", eventId_ptr, timestamp, eventValue_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdata_clone")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def Clone(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventData
        """
        result = InteropUtils.invoke("eventdata_clone", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdata_get_id")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Id(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("eventdata_get_id", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdata_set_id")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Id(self, value: str) -> None:
        """
        Parameters
        ----------
        
        value: str
            Underlying .Net type is string
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        InteropUtils.invoke("eventdata_set_id", self.__pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdata_get_value")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Value(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("eventdata_get_value", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdata_set_value")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Value(self, value: str) -> None:
        """
        Parameters
        ----------
        
        value: str
            Underlying .Net type is string
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        InteropUtils.invoke("eventdata_set_value", self.__pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdata_get_tags")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Tags(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IDictionary<string, string>
        """
        result = InteropUtils.invoke("eventdata_get_tags", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdata_addtag")
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
            GC Handle Pointer to .Net type EventData
        """
        tagId_ptr = InteropUtils.utf8_to_ptr(tagId)
        tagValue_ptr = InteropUtils.utf8_to_ptr(tagValue)
        
        result = InteropUtils.invoke("eventdata_addtag", self.__pointer, tagId_ptr, tagValue_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdata_addtags")
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
            GC Handle Pointer to .Net type EventData
        """
        result = InteropUtils.invoke("eventdata_addtags", self.__pointer, tags)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdata_removetag")
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
            GC Handle Pointer to .Net type EventData
        """
        tagId_ptr = InteropUtils.utf8_to_ptr(tagId)
        
        result = InteropUtils.invoke("eventdata_removetag", self.__pointer, tagId_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdata_get_timestampnanoseconds")
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
        result = InteropUtils.invoke("eventdata_get_timestampnanoseconds", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdata_get_timestampmilliseconds")
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
        result = InteropUtils.invoke("eventdata_get_timestampmilliseconds", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdata_get_timestamp")
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
        result = InteropUtils.invoke("eventdata_get_timestamp", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdata_get_timestampastimespan")
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
        result = InteropUtils.invoke("eventdata_get_timestampastimespan", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
