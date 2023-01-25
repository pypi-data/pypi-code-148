# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ....InteropHelpers.InteropUtils import InteropUtils


class EventDataBuilder(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type EventDataBuilder
        
        Returns
        ----------
        
        EventDataBuilder:
            Instance wrapping the .net type EventDataBuilder
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = EventDataBuilder._EventDataBuilder__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(EventDataBuilder, cls).__new__(cls)
            EventDataBuilder._EventDataBuilder__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type EventDataBuilder
        
        Returns
        ----------
        
        EventDataBuilder:
            Instance wrapping the .net type EventDataBuilder
        """
        if '_EventDataBuilder__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del EventDataBuilder._EventDataBuilder__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("eventdatabuilder_constructor")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_longlong]
    @staticmethod
    def Constructor(streamEventsWriter: c_void_p, timestampNanoseconds: int) -> c_void_p:
        """
        Parameters
        ----------
        
        streamEventsWriter: c_void_p
            GC Handle Pointer to .Net type StreamEventsWriter
        
        timestampNanoseconds: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventDataBuilder
        """
        timestampNanoseconds_long = ctypes.c_longlong(timestampNanoseconds)
        
        result = InteropUtils.invoke("eventdatabuilder_constructor", streamEventsWriter, timestampNanoseconds_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdatabuilder_addvalue")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def AddValue(self, eventId: str, value: str) -> c_void_p:
        """
        Parameters
        ----------
        
        eventId: str
            Underlying .Net type is string
        
        value: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventDataBuilder
        """
        eventId_ptr = InteropUtils.utf8_to_ptr(eventId)
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        result = InteropUtils.invoke("eventdatabuilder_addvalue", self.__pointer, eventId_ptr, value_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdatabuilder_addtag")
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
            GC Handle Pointer to .Net type EventDataBuilder
        """
        tagId_ptr = InteropUtils.utf8_to_ptr(tagId)
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        result = InteropUtils.invoke("eventdatabuilder_addtag", self.__pointer, tagId_ptr, value_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdatabuilder_addtags")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def AddTags(self, tagsValues: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        tagsValues: c_void_p
            GC Handle Pointer to .Net type IEnumerable<KeyValuePair<string, string>>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventDataBuilder
        """
        result = InteropUtils.invoke("eventdatabuilder_addtags", self.__pointer, tagsValues)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("eventdatabuilder_write")
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
        InteropUtils.invoke("eventdatabuilder_write", self.__pointer)
