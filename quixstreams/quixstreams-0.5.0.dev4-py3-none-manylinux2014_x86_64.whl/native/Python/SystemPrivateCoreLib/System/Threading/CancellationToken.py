# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ....InteropHelpers.InteropUtils import InteropUtils


class CancellationToken(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        ----------
        
        CancellationToken:
            Instance wrapping the .net type CancellationToken
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = CancellationToken._CancellationToken__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(CancellationToken, cls).__new__(cls)
            CancellationToken._CancellationToken__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        ----------
        
        CancellationToken:
            Instance wrapping the .net type CancellationToken
        """
        if '_CancellationToken__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del CancellationToken._CancellationToken__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("cancellationtoken_constructor")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor(canceled: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        canceled: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationToken
        """
        canceled_bool = 1 if canceled else 0
        
        result = InteropUtils.invoke("cancellationtoken_constructor", canceled_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtoken_get_none")
    __interop_func.restype = c_void_p
    @staticmethod
    def get_None() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationToken
        """
        result = InteropUtils.invoke("cancellationtoken_get_none")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtoken_get_iscancellationrequested")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsCancellationRequested(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("cancellationtoken_get_iscancellationrequested", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtoken_get_canbecanceled")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_CanBeCanceled(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("cancellationtoken_get_canbecanceled", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtoken_equals")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Equals(self, other: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        other: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("cancellationtoken_equals", self.__pointer, other)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtoken_equals2")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Equals2(self, other: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        other: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("cancellationtoken_equals2", self.__pointer, other)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtoken_gethashcode")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def GetHashCode(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("cancellationtoken_gethashcode", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtoken_op_equality")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Equality(left: c_void_p, right: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        left: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        right: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("cancellationtoken_op_equality", left, right)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtoken_op_inequality")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Inequality(left: c_void_p, right: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        left: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        right: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("cancellationtoken_op_inequality", left, right)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtoken_throwifcancellationrequested")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p]
    def ThrowIfCancellationRequested(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("cancellationtoken_throwifcancellationrequested", self.__pointer)
