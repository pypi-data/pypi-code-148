# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from typing import Callable
from ..EventDefinition import EventDefinition
from ....InteropHelpers.InteropUtils import InteropUtils


class StreamEventsReader(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamEventsReader
        
        Returns
        ----------
        
        StreamEventsReader:
            Instance wrapping the .net type StreamEventsReader
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = StreamEventsReader._StreamEventsReader__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(StreamEventsReader, cls).__new__(cls)
            StreamEventsReader._StreamEventsReader__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamEventsReader
        
        Returns
        ----------
        
        StreamEventsReader:
            Instance wrapping the .net type StreamEventsReader
        """
        if '_StreamEventsReader__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del StreamEventsReader._StreamEventsReader__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("streameventsreader_add_onread")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnRead(self, value: Callable[[c_void_p], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p], None]
            Underlying .Net type is Action<EventData>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0: value(c_void_p(p0))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in streameventsreader_add_onread, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO StreamEventsReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in streameventsreader_add_onread, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("streameventsreader_add_onread", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventsreader_remove_onread")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnRead(self, value: Callable[[c_void_p], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p], None]
            Underlying .Net type is Action<EventData>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0: value(c_void_p(p0))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in streameventsreader_remove_onread, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO StreamEventsReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in streameventsreader_remove_onread, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("streameventsreader_remove_onread", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventsreader_add_ondefinitionschanged")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnDefinitionsChanged(self, value: Callable[[], None]) -> None:
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
                print("Registering value_converter_func_wrapper in streameventsreader_add_ondefinitionschanged, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO StreamEventsReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in streameventsreader_add_ondefinitionschanged, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("streameventsreader_add_ondefinitionschanged", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventsreader_remove_ondefinitionschanged")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnDefinitionsChanged(self, value: Callable[[], None]) -> None:
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
                print("Registering value_converter_func_wrapper in streameventsreader_remove_ondefinitionschanged, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO StreamEventsReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in streameventsreader_remove_ondefinitionschanged, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("streameventsreader_remove_ondefinitionschanged", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventsreader_get_definitions")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Definitions(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IList<EventDefinition>
        """
        result = InteropUtils.invoke("streameventsreader_get_definitions", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streameventsreader_dispose")
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
        InteropUtils.invoke("streameventsreader_dispose", self.__pointer)
