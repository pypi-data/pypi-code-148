# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .CancellationToken import CancellationToken
from ....InteropHelpers.InteropUtils import InteropUtils


class CancellationTokenSource(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type CancellationTokenSource
        
        Returns
        ----------
        
        CancellationTokenSource:
            Instance wrapping the .net type CancellationTokenSource
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = CancellationTokenSource._CancellationTokenSource__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(CancellationTokenSource, cls).__new__(cls)
            CancellationTokenSource._CancellationTokenSource__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type CancellationTokenSource
        
        Returns
        ----------
        
        CancellationTokenSource:
            Instance wrapping the .net type CancellationTokenSource
        """
        if '_CancellationTokenSource__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del CancellationTokenSource._CancellationTokenSource__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("cancellationtokensource_constructor")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationTokenSource
        """
        result = InteropUtils.invoke("cancellationtokensource_constructor")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtokensource_constructor2")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    @staticmethod
    def Constructor2(delay: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        delay: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationTokenSource
        """
        result = InteropUtils.invoke("cancellationtokensource_constructor2", delay)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtokensource_constructor3")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor3(millisecondsDelay: int) -> c_void_p:
        """
        Parameters
        ----------
        
        millisecondsDelay: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationTokenSource
        """
        result = InteropUtils.invoke("cancellationtokensource_constructor3", millisecondsDelay)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtokensource_get_iscancellationrequested")
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
        result = InteropUtils.invoke("cancellationtokensource_get_iscancellationrequested", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtokensource_get_token")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Token(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationToken
        """
        result = InteropUtils.invoke("cancellationtokensource_get_token", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtokensource_cancel")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p]
    def Cancel(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("cancellationtokensource_cancel", self.__pointer)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtokensource_cancel2")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, ctypes.c_ubyte]
    def Cancel2(self, throwOnFirstException: bool) -> None:
        """
        Parameters
        ----------
        
        throwOnFirstException: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        throwOnFirstException_bool = 1 if throwOnFirstException else 0
        
        InteropUtils.invoke("cancellationtokensource_cancel2", self.__pointer, throwOnFirstException_bool)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtokensource_cancelafter")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def CancelAfter(self, delay: c_void_p) -> None:
        """
        Parameters
        ----------
        
        delay: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("cancellationtokensource_cancelafter", self.__pointer, delay)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtokensource_cancelafter2")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, ctypes.c_int]
    def CancelAfter2(self, millisecondsDelay: int) -> None:
        """
        Parameters
        ----------
        
        millisecondsDelay: int
            Underlying .Net type is int
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("cancellationtokensource_cancelafter2", self.__pointer, millisecondsDelay)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtokensource_tryreset")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def TryReset(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("cancellationtokensource_tryreset", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtokensource_dispose")
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
        InteropUtils.invoke("cancellationtokensource_dispose", self.__pointer)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtokensource_createlinkedtokensource")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def CreateLinkedTokenSource(token1: c_void_p, token2: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        token1: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        token2: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationTokenSource
        """
        result = InteropUtils.invoke("cancellationtokensource_createlinkedtokensource", token1, token2)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtokensource_createlinkedtokensource2")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    @staticmethod
    def CreateLinkedTokenSource2(token: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        token: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationTokenSource
        """
        result = InteropUtils.invoke("cancellationtokensource_createlinkedtokensource2", token)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("cancellationtokensource_createlinkedtokensource3")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    @staticmethod
    def CreateLinkedTokenSource3(tokens: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        tokens: c_void_p
            GC Handle Pointer to .Net type CancellationToken[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationTokenSource
        """
        result = InteropUtils.invoke("cancellationtokensource_createlinkedtokensource3", tokens)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
