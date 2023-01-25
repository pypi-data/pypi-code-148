# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from typing import Callable
from ....SystemPrivateCoreLib.System.DateTime import DateTime
from ....InteropHelpers.InteropUtils import InteropUtils


class StreamPropertiesReader(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamPropertiesReader
        
        Returns
        ----------
        
        StreamPropertiesReader:
            Instance wrapping the .net type StreamPropertiesReader
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = StreamPropertiesReader._StreamPropertiesReader__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(StreamPropertiesReader, cls).__new__(cls)
            StreamPropertiesReader._StreamPropertiesReader__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamPropertiesReader
        
        Returns
        ----------
        
        StreamPropertiesReader:
            Instance wrapping the .net type StreamPropertiesReader
        """
        if '_StreamPropertiesReader__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del StreamPropertiesReader._StreamPropertiesReader__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("streampropertiesreader_add_onchanged")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnChanged(self, value: Callable[[], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[], None]
            Underlying .Net type is Action
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda : value()

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in streampropertiesreader_add_onchanged, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO StreamPropertiesReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in streampropertiesreader_add_onchanged, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("streampropertiesreader_add_onchanged", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertiesreader_remove_onchanged")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnChanged(self, value: Callable[[], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[], None]
            Underlying .Net type is Action
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda : value()

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in streampropertiesreader_remove_onchanged, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO StreamPropertiesReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in streampropertiesreader_remove_onchanged, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("streampropertiesreader_remove_onchanged", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertiesreader_get_name")
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
        result = InteropUtils.invoke("streampropertiesreader_get_name", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertiesreader_get_location")
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
        result = InteropUtils.invoke("streampropertiesreader_get_location", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertiesreader_get_timeofrecording")
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
        result = InteropUtils.invoke("streampropertiesreader_get_timeofrecording", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertiesreader_get_metadata")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Metadata(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Dictionary<string, string>
        """
        result = InteropUtils.invoke("streampropertiesreader_get_metadata", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertiesreader_get_parents")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Parents(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type List<string>
        """
        result = InteropUtils.invoke("streampropertiesreader_get_parents", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampropertiesreader_dispose")
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
        InteropUtils.invoke("streampropertiesreader_dispose", self.__pointer)
