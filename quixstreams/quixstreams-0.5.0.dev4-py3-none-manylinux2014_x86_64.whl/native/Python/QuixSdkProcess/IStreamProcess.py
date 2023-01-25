# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from typing import Callable
from ..InteropHelpers.InteropUtils import InteropUtils


class IStreamProcess(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type IStreamProcess
        
        Returns
        ----------
        
        IStreamProcess:
            Instance wrapping the .net type IStreamProcess
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = IStreamProcess._IStreamProcess__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(IStreamProcess, cls).__new__(cls)
            IStreamProcess._IStreamProcess__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type IStreamProcess
        
        Returns
        ----------
        
        IStreamProcess:
            Instance wrapping the .net type IStreamProcess
        """
        if '_IStreamProcess__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del IStreamProcess._IStreamProcess__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("istreamprocess_get_streamid")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_StreamId(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("istreamprocess_get_streamid", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamprocess_get_sourcemetadata")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_SourceMetadata(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Dictionary<string, string>
        """
        result = InteropUtils.invoke("istreamprocess_get_sourcemetadata", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamprocess_set_sourcemetadata")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_SourceMetadata(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, string>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("istreamprocess_set_sourcemetadata", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamprocess_subscribe3")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Subscribe3(self, onStreamPackage: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        onStreamPackage: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is Action<IStreamProcess, StreamPackage>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IStreamProcess
        """
        onStreamPackage_func_wrapper_addr = None
        if onStreamPackage is not None:
            onStreamPackage_converter = lambda p0, p1: onStreamPackage(c_void_p(p0), c_void_p(p1))

            onStreamPackage_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p, c_void_p)(onStreamPackage_converter)
            onStreamPackage_func_wrapper_addr = ctypes.cast(onStreamPackage_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering onStreamPackage_converter_func_wrapper in istreamprocess_subscribe3, addr {}".format(onStreamPackage_func_wrapper_addr))
                onStreamPackage_func_wrapper_addr_val = onStreamPackage_func_wrapper_addr.value
                # TODO IStreamProcess.__weakrefs.append(weakref.ref(onStreamPackage_converter_func_wrapper, lambda x: print("De-referenced onStreamPackage_converter_func_wrapper in istreamprocess_subscribe3, addr {}".format(onStreamPackage_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("istreamprocess_subscribe3", self.__pointer, onStreamPackage_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, onStreamPackage_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamprocess_close")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p]
    def Close(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("istreamprocess_close", self.__pointer)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamprocess_add_onclosing")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnClosing(self, value: Callable[[], None]) -> None:
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
                print("Registering value_converter_func_wrapper in istreamprocess_add_onclosing, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO IStreamProcess.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in istreamprocess_add_onclosing, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("istreamprocess_add_onclosing", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamprocess_remove_onclosing")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnClosing(self, value: Callable[[], None]) -> None:
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
                print("Registering value_converter_func_wrapper in istreamprocess_remove_onclosing, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO IStreamProcess.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in istreamprocess_remove_onclosing, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("istreamprocess_remove_onclosing", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamprocess_add_onclosed")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnClosed(self, value: Callable[[], None]) -> None:
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
                print("Registering value_converter_func_wrapper in istreamprocess_add_onclosed, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO IStreamProcess.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in istreamprocess_add_onclosed, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("istreamprocess_add_onclosed", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamprocess_remove_onclosed")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnClosed(self, value: Callable[[], None]) -> None:
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
                print("Registering value_converter_func_wrapper in istreamprocess_remove_onclosed, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO IStreamProcess.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in istreamprocess_remove_onclosed, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("istreamprocess_remove_onclosed", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
