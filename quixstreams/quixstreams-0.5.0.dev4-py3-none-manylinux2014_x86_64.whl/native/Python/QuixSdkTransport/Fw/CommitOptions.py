# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...InteropHelpers.InteropUtils import InteropUtils


class CommitOptions(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type CommitOptions
        
        Returns
        ----------
        
        CommitOptions:
            Instance wrapping the .net type CommitOptions
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = CommitOptions._CommitOptions__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(CommitOptions, cls).__new__(cls)
            CommitOptions._CommitOptions__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type CommitOptions
        
        Returns
        ----------
        
        CommitOptions:
            Instance wrapping the .net type CommitOptions
        """
        if '_CommitOptions__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del CommitOptions._CommitOptions__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("commitoptions_constructor")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CommitOptions
        """
        result = InteropUtils.invoke("commitoptions_constructor")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("commitoptions_get_autocommitenabled")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_AutoCommitEnabled(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("commitoptions_get_autocommitenabled", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("commitoptions_set_autocommitenabled")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, ctypes.c_ubyte]
    def set_AutoCommitEnabled(self, value: bool) -> None:
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
        
        InteropUtils.invoke("commitoptions_set_autocommitenabled", self.__pointer, value_bool)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("commitoptions_get_commitinterval")
    __interop_func.restype = InteropUtils.create_nullable(ctypes.c_int)
    __interop_func.argtypes = [c_void_p]
    def get_CommitInterval(self) -> Optional[int]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[int]:
            Underlying .Net type is int?
        """
        result = InteropUtils.invoke("commitoptions_get_commitinterval", self.__pointer)
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("commitoptions_set_commitinterval")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, InteropUtils.create_nullable(ctypes.c_int)]
    def set_CommitInterval(self, value: Optional[int]) -> None:
        """
        Parameters
        ----------
        
        value: Optional[int]
            Underlying .Net type is int?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_nullable = InteropUtils.create_nullable(ctypes.c_int)(value)
        
        InteropUtils.invoke("commitoptions_set_commitinterval", self.__pointer, value_nullable)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("commitoptions_get_commitevery")
    __interop_func.restype = InteropUtils.create_nullable(ctypes.c_int)
    __interop_func.argtypes = [c_void_p]
    def get_CommitEvery(self) -> Optional[int]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[int]:
            Underlying .Net type is int?
        """
        result = InteropUtils.invoke("commitoptions_get_commitevery", self.__pointer)
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("commitoptions_set_commitevery")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, InteropUtils.create_nullable(ctypes.c_int)]
    def set_CommitEvery(self, value: Optional[int]) -> None:
        """
        Parameters
        ----------
        
        value: Optional[int]
            Underlying .Net type is int?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_nullable = InteropUtils.create_nullable(ctypes.c_int)(value)
        
        InteropUtils.invoke("commitoptions_set_commitevery", self.__pointer, value_nullable)
