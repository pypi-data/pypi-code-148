# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .SaslMechanism import SaslMechanism
from ...InteropHelpers.InteropUtils import InteropUtils


class SecurityOptions(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type SecurityOptions
        
        Returns
        ----------
        
        SecurityOptions:
            Instance wrapping the .net type SecurityOptions
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = SecurityOptions._SecurityOptions__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(SecurityOptions, cls).__new__(cls)
            SecurityOptions._SecurityOptions__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type SecurityOptions
        
        Returns
        ----------
        
        SecurityOptions:
            Instance wrapping the .net type SecurityOptions
        """
        if '_SecurityOptions__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del SecurityOptions._SecurityOptions__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("securityoptions_constructor")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type SecurityOptions
        """
        result = InteropUtils.invoke("securityoptions_constructor")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("securityoptions_constructor2")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor2(sslCertificates: str, username: str, password: str, saslMechanism: SaslMechanism = SaslMechanism.ScramSha256) -> c_void_p:
        """
        Parameters
        ----------
        
        sslCertificates: str
            Underlying .Net type is string
        
        username: str
            Underlying .Net type is string
        
        password: str
            Underlying .Net type is string
        
        saslMechanism: SaslMechanism
            (Optional) Underlying .Net type is SaslMechanism. Defaults to ScramSha256
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type SecurityOptions
        """
        sslCertificates_ptr = InteropUtils.utf8_to_ptr(sslCertificates)
        username_ptr = InteropUtils.utf8_to_ptr(username)
        password_ptr = InteropUtils.utf8_to_ptr(password)
        
        result = InteropUtils.invoke("securityoptions_constructor2", sslCertificates_ptr, username_ptr, password_ptr, saslMechanism.value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("securityoptions_get_saslmechanism")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_SaslMechanism(self) -> SaslMechanism:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        SaslMechanism:
            Underlying .Net type is SaslMechanism
        """
        result = InteropUtils.invoke("securityoptions_get_saslmechanism", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("securityoptions_set_saslmechanism")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, ctypes.c_int]
    def set_SaslMechanism(self, value: SaslMechanism) -> None:
        """
        Parameters
        ----------
        
        value: SaslMechanism
            Underlying .Net type is SaslMechanism
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("securityoptions_set_saslmechanism", self.__pointer, value.value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("securityoptions_get_username")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Username(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("securityoptions_get_username", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("securityoptions_set_username")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Username(self, value: str) -> None:
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
        
        InteropUtils.invoke("securityoptions_set_username", self.__pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("securityoptions_get_password")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Password(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("securityoptions_get_password", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("securityoptions_set_password")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Password(self, value: str) -> None:
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
        
        InteropUtils.invoke("securityoptions_set_password", self.__pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("securityoptions_get_sslcertificates")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_SslCertificates(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("securityoptions_get_sslcertificates", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("securityoptions_set_sslcertificates")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_SslCertificates(self, value: str) -> None:
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
        
        InteropUtils.invoke("securityoptions_set_sslcertificates", self.__pointer, value_ptr)
