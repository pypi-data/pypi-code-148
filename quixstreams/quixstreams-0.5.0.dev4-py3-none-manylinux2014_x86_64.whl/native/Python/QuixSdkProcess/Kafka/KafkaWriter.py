# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from typing import Callable
from ...InteropHelpers.InteropUtils import InteropUtils


class KafkaWriter(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type KafkaWriter
        
        Returns
        ----------
        
        KafkaWriter:
            Instance wrapping the .net type KafkaWriter
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = KafkaWriter._KafkaWriter__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(KafkaWriter, cls).__new__(cls)
            KafkaWriter._KafkaWriter__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type KafkaWriter
        
        Returns
        ----------
        
        KafkaWriter:
            Instance wrapping the .net type KafkaWriter
        """
        if '_KafkaWriter__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del KafkaWriter._KafkaWriter__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("kafkawriter_constructor")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Constructor(input: c_void_p, streamId: str = None) -> c_void_p:
        """
        Parameters
        ----------
        
        input: c_void_p
            GC Handle Pointer to .Net type IInput
        
        streamId: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type KafkaWriter
        """
        streamId_ptr = InteropUtils.utf8_to_ptr(streamId)
        
        result = InteropUtils.invoke("kafkawriter_constructor", input, streamId_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkawriter_constructor2")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Constructor2(input: c_void_p, byteSplitter: c_void_p, streamId: str = None) -> c_void_p:
        """
        Parameters
        ----------
        
        input: c_void_p
            GC Handle Pointer to .Net type IInput
        
        byteSplitter: c_void_p
            GC Handle Pointer to .Net type IByteSplitter
        
        streamId: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type KafkaWriter
        """
        streamId_ptr = InteropUtils.utf8_to_ptr(streamId)
        
        result = InteropUtils.invoke("kafkawriter_constructor2", input, byteSplitter, streamId_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkawriter_get_streamid")
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
        result = InteropUtils.invoke("kafkawriter_get_streamid", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkawriter_add_onwriteexception")
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
                print("Registering value_converter_func_wrapper in kafkawriter_add_onwriteexception, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO KafkaWriter.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in kafkawriter_add_onwriteexception, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("kafkawriter_add_onwriteexception", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkawriter_remove_onwriteexception")
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
                print("Registering value_converter_func_wrapper in kafkawriter_remove_onwriteexception, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO KafkaWriter.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in kafkawriter_remove_onwriteexception, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("kafkawriter_remove_onwriteexception", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkawriter_dispose")
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
        InteropUtils.invoke("kafkawriter_dispose", self.__pointer)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkawriter_get_onstreamprocessassigned")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_OnStreamProcessAssigned(self) -> Callable[[], None]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Callable[[], None]:
            Underlying .Net type is Action
        """
        result = InteropUtils.invoke("kafkawriter_get_onstreamprocessassigned", self.__pointer)
        return Exception("NOT IMPLEMENTED YET")
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkawriter_set_onstreamprocessassigned")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_OnStreamProcessAssigned(self, value: Callable[[], None]) -> None:
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
                print("Registering value_converter_func_wrapper in kafkawriter_set_onstreamprocessassigned, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO KafkaWriter.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in kafkawriter_set_onstreamprocessassigned, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("kafkawriter_set_onstreamprocessassigned", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
