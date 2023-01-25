# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ....SystemPrivateCoreLib.System.DateTime import DateTime
from .EventDataBuilder import EventDataBuilder
from .EventDefinitionBuilder import EventDefinitionBuilder
from ....InteropHelpers.InteropUtils import InteropUtils


class StreamEventsWriter(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamEventsWriter
        
        Returns
        ----------
        
        StreamEventsWriter:
            Instance wrapping the .net type StreamEventsWriter
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = StreamEventsWriter._StreamEventsWriter__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(StreamEventsWriter, cls).__new__(cls)
            StreamEventsWriter._StreamEventsWriter__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamEventsWriter
        
        Returns
        ----------
        
        StreamEventsWriter:
            Instance wrapping the .net type StreamEventsWriter
        """
        if '_StreamEventsWriter__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del StreamEventsWriter._StreamEventsWriter__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("streameventswriter_get_defaulttags")
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
        result = InteropUtils.invoke("streameventswriter_get_defaulttags", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventswriter_set_defaulttags")
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
        InteropUtils.invoke("streameventswriter_set_defaulttags", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventswriter_get_defaultlocation")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_DefaultLocation(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("streameventswriter_get_defaultlocation", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventswriter_set_defaultlocation")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_DefaultLocation(self, value: str) -> None:
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
        
        InteropUtils.invoke("streameventswriter_set_defaultlocation", self.__pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventswriter_get_epoch")
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
        result = InteropUtils.invoke("streameventswriter_get_epoch", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventswriter_set_epoch")
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
        InteropUtils.invoke("streameventswriter_set_epoch", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventswriter_addtimestamp")
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
            GC Handle Pointer to .Net type EventDataBuilder
        """
        result = InteropUtils.invoke("streameventswriter_addtimestamp", self.__pointer, dateTime)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventswriter_addtimestamp2")
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
            GC Handle Pointer to .Net type EventDataBuilder
        """
        result = InteropUtils.invoke("streameventswriter_addtimestamp2", self.__pointer, timeSpan)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventswriter_addtimestampmilliseconds")
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
            GC Handle Pointer to .Net type EventDataBuilder
        """
        timeMilliseconds_long = ctypes.c_longlong(timeMilliseconds)
        
        result = InteropUtils.invoke("streameventswriter_addtimestampmilliseconds", self.__pointer, timeMilliseconds_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventswriter_addtimestampnanoseconds")
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
            GC Handle Pointer to .Net type EventDataBuilder
        """
        timeNanoseconds_long = ctypes.c_longlong(timeNanoseconds)
        
        result = InteropUtils.invoke("streameventswriter_addtimestampnanoseconds", self.__pointer, timeNanoseconds_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventswriter_adddefinitions")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def AddDefinitions(self, definitions: c_void_p) -> None:
        """
        Parameters
        ----------
        
        definitions: c_void_p
            GC Handle Pointer to .Net type List<EventDefinition>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streameventswriter_adddefinitions", self.__pointer, definitions)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventswriter_adddefinition")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
    def AddDefinition(self, eventId: str, name: str = None, description: str = None) -> c_void_p:
        """
        Parameters
        ----------
        
        eventId: str
            Underlying .Net type is string
        
        name: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        description: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventDefinitionBuilder
        """
        eventId_ptr = InteropUtils.utf8_to_ptr(eventId)
        name_ptr = InteropUtils.utf8_to_ptr(name)
        description_ptr = InteropUtils.utf8_to_ptr(description)
        
        result = InteropUtils.invoke("streameventswriter_adddefinition", self.__pointer, eventId_ptr, name_ptr, description_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventswriter_addlocation")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def AddLocation(self, location: str) -> c_void_p:
        """
        Parameters
        ----------
        
        location: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventDefinitionBuilder
        """
        location_ptr = InteropUtils.utf8_to_ptr(location)
        
        result = InteropUtils.invoke("streameventswriter_addlocation", self.__pointer, location_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventswriter_flush")
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
        InteropUtils.invoke("streameventswriter_flush", self.__pointer)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventswriter_write")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Write(self, data: c_void_p) -> None:
        """
        Parameters
        ----------
        
        data: c_void_p
            GC Handle Pointer to .Net type EventData
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streameventswriter_write", self.__pointer, data)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventswriter_write2")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Write2(self, events: c_void_p) -> None:
        """
        Parameters
        ----------
        
        events: c_void_p
            GC Handle Pointer to .Net type ICollection<EventData>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streameventswriter_write2", self.__pointer, events)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventswriter_dispose")
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
        InteropUtils.invoke("streameventswriter_dispose", self.__pointer)
