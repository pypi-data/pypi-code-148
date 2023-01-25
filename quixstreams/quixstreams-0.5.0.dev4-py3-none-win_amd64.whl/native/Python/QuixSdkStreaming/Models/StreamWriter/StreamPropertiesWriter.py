# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ....SystemPrivateCoreLib.System.DateTime import DateTime
from ....InteropHelpers.InteropUtils import InteropUtils


class StreamPropertiesWriter(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamPropertiesWriter
        
        Returns
        ----------
        
        StreamPropertiesWriter:
            Instance wrapping the .net type StreamPropertiesWriter
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = StreamPropertiesWriter._StreamPropertiesWriter__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(StreamPropertiesWriter, cls).__new__(cls)
            StreamPropertiesWriter._StreamPropertiesWriter__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamPropertiesWriter
        
        Returns
        ----------
        
        StreamPropertiesWriter:
            Instance wrapping the .net type StreamPropertiesWriter
        """
        if '_StreamPropertiesWriter__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del StreamPropertiesWriter._StreamPropertiesWriter__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("streampropertieswriter_get_flushinterval")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_FlushInterval(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("streampropertieswriter_get_flushinterval", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertieswriter_set_flushinterval")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, ctypes.c_int]
    def set_FlushInterval(self, value: int) -> None:
        """
        Parameters
        ----------
        
        value: int
            Underlying .Net type is int
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streampropertieswriter_set_flushinterval", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertieswriter_get_name")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Name(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("streampropertieswriter_get_name", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertieswriter_set_name")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Name(self, value: str) -> None:
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
        
        InteropUtils.invoke("streampropertieswriter_set_name", self.__pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertieswriter_get_location")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Location(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("streampropertieswriter_get_location", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertieswriter_set_location")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Location(self, value: str) -> None:
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
        
        InteropUtils.invoke("streampropertieswriter_set_location", self.__pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertieswriter_get_timeofrecording")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_TimeOfRecording(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime?
        """
        result = InteropUtils.invoke("streampropertieswriter_get_timeofrecording", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertieswriter_set_timeofrecording")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_TimeOfRecording(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type DateTime?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streampropertieswriter_set_timeofrecording", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertieswriter_get_metadata")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Metadata(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ObservableDictionary<string, string>
        """
        result = InteropUtils.invoke("streampropertieswriter_get_metadata", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertieswriter_get_parents")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Parents(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ObservableCollection<string>
        """
        result = InteropUtils.invoke("streampropertieswriter_get_parents", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertieswriter_addparent")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def AddParent(self, parentStreamId: str) -> None:
        """
        Parameters
        ----------
        
        parentStreamId: str
            Underlying .Net type is string
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        parentStreamId_ptr = InteropUtils.utf8_to_ptr(parentStreamId)
        
        InteropUtils.invoke("streampropertieswriter_addparent", self.__pointer, parentStreamId_ptr)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertieswriter_removeparent")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def RemoveParent(self, parentStreamId: str) -> None:
        """
        Parameters
        ----------
        
        parentStreamId: str
            Underlying .Net type is string
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        parentStreamId_ptr = InteropUtils.utf8_to_ptr(parentStreamId)
        
        InteropUtils.invoke("streampropertieswriter_removeparent", self.__pointer, parentStreamId_ptr)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertieswriter_flush")
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
        InteropUtils.invoke("streampropertieswriter_flush", self.__pointer)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertieswriter_dispose")
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
        InteropUtils.invoke("streampropertieswriter_dispose", self.__pointer)
