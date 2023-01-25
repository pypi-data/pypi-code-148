# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ..SystemPrivateUri.System.Uri import Uri
from ..SystemPrivateCoreLib.System.TimeSpan import TimeSpan
from ..InteropHelpers.InteropUtils import InteropUtils


class HttpClient(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type HttpClient
        
        Returns
        ----------
        
        HttpClient:
            Instance wrapping the .net type HttpClient
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = HttpClient._HttpClient__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(HttpClient, cls).__new__(cls)
            HttpClient._HttpClient__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type HttpClient
        
        Returns
        ----------
        
        HttpClient:
            Instance wrapping the .net type HttpClient
        """
        if '_HttpClient__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del HttpClient._HttpClient__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("httpclient_constructor")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type HttpClient
        """
        result = InteropUtils.invoke("httpclient_constructor")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("httpclient_get_baseaddress")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_BaseAddress(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Uri
        """
        result = InteropUtils.invoke("httpclient_get_baseaddress", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("httpclient_set_baseaddress")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_BaseAddress(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Uri
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("httpclient_set_baseaddress", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("httpclient_get_timeout")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Timeout(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("httpclient_get_timeout", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("httpclient_set_timeout")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Timeout(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("httpclient_set_timeout", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("httpclient_get_maxresponsecontentbuffersize")
    __interop_func.restype = ctypes.c_longlong
    __interop_func.argtypes = [c_void_p]
    def get_MaxResponseContentBufferSize(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("httpclient_get_maxresponsecontentbuffersize", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("httpclient_set_maxresponsecontentbuffersize")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, ctypes.c_longlong]
    def set_MaxResponseContentBufferSize(self, value: int) -> None:
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
        
        InteropUtils.invoke("httpclient_set_maxresponsecontentbuffersize", self.__pointer, value_long)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("httpclient_cancelpendingrequests")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p]
    def CancelPendingRequests(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("httpclient_cancelpendingrequests", self.__pointer)
