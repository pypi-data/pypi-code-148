# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ..SystemPrivateCoreLib.System.TimeSpan import TimeSpan
from ..InteropHelpers.InteropUtils import InteropUtils


class QuixStreamingClientTokenValidationConfiguration(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TokenValidationConfiguration
        
        Returns
        ----------
        
        QuixStreamingClientTokenValidationConfiguration:
            Instance wrapping the .net type TokenValidationConfiguration
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = QuixStreamingClientTokenValidationConfiguration._QuixStreamingClientTokenValidationConfiguration__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(QuixStreamingClientTokenValidationConfiguration, cls).__new__(cls)
            QuixStreamingClientTokenValidationConfiguration._QuixStreamingClientTokenValidationConfiguration__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TokenValidationConfiguration
        
        Returns
        ----------
        
        QuixStreamingClientTokenValidationConfiguration:
            Instance wrapping the .net type TokenValidationConfiguration
        """
        if '_QuixStreamingClientTokenValidationConfiguration__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del QuixStreamingClientTokenValidationConfiguration._QuixStreamingClientTokenValidationConfiguration__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("tokenvalidationconfiguration_constructor")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type QuixStreamingClient.TokenValidationConfiguration
        """
        result = InteropUtils.invoke("tokenvalidationconfiguration_constructor")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("tokenvalidationconfiguration_get_enabled")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_Enabled(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("tokenvalidationconfiguration_get_enabled", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("tokenvalidationconfiguration_set_enabled")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, ctypes.c_ubyte]
    def set_Enabled(self, value: bool) -> None:
        """
        Parameters
        ----------
        
        value: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_bool = 1 if value else 0
        
        InteropUtils.invoke("tokenvalidationconfiguration_set_enabled", self.__pointer, value_bool)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("tokenvalidationconfiguration_get_warningbeforeexpiry")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_WarningBeforeExpiry(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan?
        """
        result = InteropUtils.invoke("tokenvalidationconfiguration_get_warningbeforeexpiry", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("tokenvalidationconfiguration_set_warningbeforeexpiry")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_WarningBeforeExpiry(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type TimeSpan?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("tokenvalidationconfiguration_set_warningbeforeexpiry", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("tokenvalidationconfiguration_get_warnaboutnonpattoken")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_WarnAboutNonPatToken(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("tokenvalidationconfiguration_get_warnaboutnonpattoken", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("tokenvalidationconfiguration_set_warnaboutnonpattoken")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, ctypes.c_ubyte]
    def set_WarnAboutNonPatToken(self, value: bool) -> None:
        """
        Parameters
        ----------
        
        value: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_bool = 1 if value else 0
        
        InteropUtils.invoke("tokenvalidationconfiguration_set_warnaboutnonpattoken", self.__pointer, value_bool)
