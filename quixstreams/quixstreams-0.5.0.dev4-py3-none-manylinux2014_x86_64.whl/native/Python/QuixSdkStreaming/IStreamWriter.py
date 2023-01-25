# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ..SystemPrivateCoreLib.System.DateTime import DateTime
from .Models.StreamWriter.StreamPropertiesWriter import StreamPropertiesWriter
from .Models.StreamWriter.StreamParametersWriter import StreamParametersWriter
from .Models.StreamWriter.StreamEventsWriter import StreamEventsWriter
from ..QuixSdkProcess.Models.StreamEndType import StreamEndType
from typing import Callable
from ..InteropHelpers.InteropUtils import InteropUtils


class IStreamWriter(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type IStreamWriter
        
        Returns
        ----------
        
        IStreamWriter:
            Instance wrapping the .net type IStreamWriter
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = IStreamWriter._IStreamWriter__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(IStreamWriter, cls).__new__(cls)
            IStreamWriter._IStreamWriter__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type IStreamWriter
        
        Returns
        ----------
        
        IStreamWriter:
            Instance wrapping the .net type IStreamWriter
        """
        if '_IStreamWriter__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del IStreamWriter._IStreamWriter__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("istreamwriter_get_streamid")
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
        result = InteropUtils.invoke("istreamwriter_get_streamid", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamwriter_get_epoch")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Epoch(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("istreamwriter_get_epoch", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamwriter_set_epoch")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Epoch(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("istreamwriter_set_epoch", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamwriter_get_properties")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Properties(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StreamPropertiesWriter
        """
        result = InteropUtils.invoke("istreamwriter_get_properties", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamwriter_get_parameters")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Parameters(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StreamParametersWriter
        """
        result = InteropUtils.invoke("istreamwriter_get_parameters", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamwriter_get_events")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Events(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StreamEventsWriter
        """
        result = InteropUtils.invoke("istreamwriter_get_events", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamwriter_close")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, ctypes.c_int]
    def Close(self, streamState: StreamEndType = StreamEndType.Closed) -> None:
        """
        Parameters
        ----------
        
        streamState: StreamEndType
            (Optional) Underlying .Net type is StreamEndType. Defaults to Closed
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("istreamwriter_close", self.__pointer, streamState.value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamwriter_add_onwriteexception")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnWriteException(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler<Exception>
        
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
                print("Registering value_converter_func_wrapper in istreamwriter_add_onwriteexception, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO IStreamWriter.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in istreamwriter_add_onwriteexception, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("istreamwriter_add_onwriteexception", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("istreamwriter_remove_onwriteexception")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnWriteException(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler<Exception>
        
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
                print("Registering value_converter_func_wrapper in istreamwriter_remove_onwriteexception, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO IStreamWriter.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in istreamwriter_remove_onwriteexception, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("istreamwriter_remove_onwriteexception", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
