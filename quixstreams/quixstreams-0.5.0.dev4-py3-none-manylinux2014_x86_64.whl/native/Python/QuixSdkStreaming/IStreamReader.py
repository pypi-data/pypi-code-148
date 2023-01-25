# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .Models.StreamReader.StreamPropertiesReader import StreamPropertiesReader
from .Models.StreamReader.StreamParametersReader import StreamParametersReader
from .Models.StreamReader.StreamEventsReader import StreamEventsReader
from typing import Callable
from ..QuixSdkProcess.Models.StreamEndType import StreamEndType
from ..InteropHelpers.InteropUtils import InteropUtils


class IStreamReader(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type IStreamReader
        
        Returns
        ----------
        
        IStreamReader:
            Instance wrapping the .net type IStreamReader
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = IStreamReader._IStreamReader__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(IStreamReader, cls).__new__(cls)
            IStreamReader._IStreamReader__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type IStreamReader
        
        Returns
        ----------
        
        IStreamReader:
            Instance wrapping the .net type IStreamReader
        """
        if '_IStreamReader__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del IStreamReader._IStreamReader__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("istreamreader_get_streamid")
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
        result = InteropUtils.invoke("istreamreader_get_streamid", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamreader_get_properties")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Properties(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StreamPropertiesReader
        """
        result = InteropUtils.invoke("istreamreader_get_properties", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamreader_get_parameters")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Parameters(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StreamParametersReader
        """
        result = InteropUtils.invoke("istreamreader_get_parameters", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamreader_get_events")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Events(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StreamEventsReader
        """
        result = InteropUtils.invoke("istreamreader_get_events", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamreader_add_onpackagereceived")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnPackageReceived(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is Action<IStreamReader, StreamPackage>
        
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
                print("Registering value_converter_func_wrapper in istreamreader_add_onpackagereceived, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO IStreamReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in istreamreader_add_onpackagereceived, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("istreamreader_add_onpackagereceived", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamreader_remove_onpackagereceived")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnPackageReceived(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is Action<IStreamReader, StreamPackage>
        
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
                print("Registering value_converter_func_wrapper in istreamreader_remove_onpackagereceived, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO IStreamReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in istreamreader_remove_onpackagereceived, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("istreamreader_remove_onpackagereceived", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamreader_add_onstreamclosed")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnStreamClosed(self, value: Callable[[c_void_p, StreamEndType], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, StreamEndType], None]
            Underlying .Net type is Action<IStreamReader, StreamEndType>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0, p1: value(c_void_p(p0), StreamEndType(p1))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p, ctypes.c_int)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in istreamreader_add_onstreamclosed, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO IStreamReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in istreamreader_add_onstreamclosed, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("istreamreader_add_onstreamclosed", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamreader_remove_onstreamclosed")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnStreamClosed(self, value: Callable[[c_void_p, StreamEndType], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, StreamEndType], None]
            Underlying .Net type is Action<IStreamReader, StreamEndType>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0, p1: value(c_void_p(p0), StreamEndType(p1))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p, ctypes.c_int)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in istreamreader_remove_onstreamclosed, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO IStreamReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in istreamreader_remove_onstreamclosed, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("istreamreader_remove_onstreamclosed", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
