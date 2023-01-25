# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...SystemPrivateCoreLib.System.Type import Type
from ...QuixSdkTransport.IO.TransportContext import TransportContext
from ...InteropHelpers.InteropUtils import InteropUtils


class StreamPackage(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamPackage
        
        Returns
        ----------
        
        StreamPackage:
            Instance wrapping the .net type StreamPackage
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = StreamPackage._StreamPackage__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(StreamPackage, cls).__new__(cls)
            StreamPackage._StreamPackage__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamPackage
        
        Returns
        ----------
        
        StreamPackage:
            Instance wrapping the .net type StreamPackage
        """
        if '_StreamPackage__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del StreamPackage._StreamPackage__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("streampackage_constructor")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Constructor(type: c_void_p, value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        type: c_void_p
            GC Handle Pointer to .Net type Type
        
        value: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StreamPackage
        """
        result = InteropUtils.invoke("streampackage_constructor", type, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampackage_get_type")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Type(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("streampackage_get_type", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampackage_set_type")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Type(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streampackage_set_type", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampackage_get_transportcontext")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_TransportContext(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TransportContext
        """
        result = InteropUtils.invoke("streampackage_get_transportcontext", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampackage_set_transportcontext")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_TransportContext(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type TransportContext
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streampackage_set_transportcontext", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampackage_get_value")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Value(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Object
        """
        result = InteropUtils.invoke("streampackage_get_value", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampackage_set_value")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Value(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streampackage_set_value", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streampackage_tojson")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def ToJson(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("streampackage_tojson", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
