# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .IStreamWriter import IStreamWriter
from typing import Callable
from ..InteropHelpers.InteropUtils import InteropUtils


class IOutputTopic(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type IOutputTopic
        
        Returns
        ----------
        
        IOutputTopic:
            Instance wrapping the .net type IOutputTopic
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = IOutputTopic._IOutputTopic__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(IOutputTopic, cls).__new__(cls)
            IOutputTopic._IOutputTopic__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type IOutputTopic
        
        Returns
        ----------
        
        IOutputTopic:
            Instance wrapping the .net type IOutputTopic
        """
        if '_IOutputTopic__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del IOutputTopic._IOutputTopic__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("ioutputtopic_createstream")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def CreateStream(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IStreamWriter
        """
        result = InteropUtils.invoke("ioutputtopic_createstream", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("ioutputtopic_createstream2")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def CreateStream2(self, streamId: str) -> c_void_p:
        """
        Parameters
        ----------
        
        streamId: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IStreamWriter
        """
        streamId_ptr = InteropUtils.utf8_to_ptr(streamId)
        
        result = InteropUtils.invoke("ioutputtopic_createstream2", self.__pointer, streamId_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("ioutputtopic_getstream")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def GetStream(self, streamId: str) -> c_void_p:
        """
        Parameters
        ----------
        
        streamId: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IStreamWriter
        """
        streamId_ptr = InteropUtils.utf8_to_ptr(streamId)
        
        result = InteropUtils.invoke("ioutputtopic_getstream", self.__pointer, streamId_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("ioutputtopic_getorcreatestream")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def GetOrCreateStream(self, streamId: str, onStreamCreated: Callable[[c_void_p], None] = None) -> c_void_p:
        """
        Parameters
        ----------
        
        streamId: str
            Underlying .Net type is string
        
        onStreamCreated: Callable[[c_void_p], None]
            (Optional) Underlying .Net type is Action<IStreamWriter>. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IStreamWriter
        """
        streamId_ptr = InteropUtils.utf8_to_ptr(streamId)
        onStreamCreated_func_wrapper_addr = None
        if onStreamCreated is not None:
            onStreamCreated_converter = lambda p0: onStreamCreated(c_void_p(p0))

            onStreamCreated_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p)(onStreamCreated_converter)
            onStreamCreated_func_wrapper_addr = ctypes.cast(onStreamCreated_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering onStreamCreated_converter_func_wrapper in ioutputtopic_getorcreatestream, addr {}".format(onStreamCreated_func_wrapper_addr))
                onStreamCreated_func_wrapper_addr_val = onStreamCreated_func_wrapper_addr.value
                # TODO IOutputTopic.__weakrefs.append(weakref.ref(onStreamCreated_converter_func_wrapper, lambda x: print("De-referenced onStreamCreated_converter_func_wrapper in ioutputtopic_getorcreatestream, addr {}".format(onStreamCreated_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("ioutputtopic_getorcreatestream", self.__pointer, streamId_ptr, onStreamCreated_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, onStreamCreated_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("ioutputtopic_add_ondisposed")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnDisposed(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0, p1: value(c_void_p(p0), c_void_p(p1))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in ioutputtopic_add_ondisposed, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO IOutputTopic.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in ioutputtopic_add_ondisposed, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("ioutputtopic_add_ondisposed", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("ioutputtopic_remove_ondisposed")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnDisposed(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0, p1: value(c_void_p(p0), c_void_p(p1))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in ioutputtopic_remove_ondisposed, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO IOutputTopic.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in ioutputtopic_remove_ondisposed, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("ioutputtopic_remove_ondisposed", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
