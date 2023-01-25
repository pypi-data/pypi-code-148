# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...QuixSdkProcess.Kafka.AutoOffsetReset import AutoOffsetReset
from typing import Callable
from ...InteropHelpers.InteropUtils import InteropUtils


class RawInputTopic(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type RawInputTopic
        
        Returns
        ----------
        
        RawInputTopic:
            Instance wrapping the .net type RawInputTopic
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = RawInputTopic._RawInputTopic__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(RawInputTopic, cls).__new__(cls)
            RawInputTopic._RawInputTopic__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type RawInputTopic
        
        Returns
        ----------
        
        RawInputTopic:
            Instance wrapping the .net type RawInputTopic
        """
        if '_RawInputTopic__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del RawInputTopic._RawInputTopic__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("rawinputtopic_constructor")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p, InteropUtils.create_nullable(ctypes.c_int)]
    @staticmethod
    def Constructor(brokerAddress: str, topicName: str, consumerGroup: str, brokerProperties: c_void_p = None, autoOffset: Optional[AutoOffsetReset] = None) -> c_void_p:
        """
        Parameters
        ----------
        
        brokerAddress: str
            Underlying .Net type is string
        
        topicName: str
            Underlying .Net type is string
        
        consumerGroup: str
            Underlying .Net type is string
        
        brokerProperties: c_void_p
            (Optional) GC Handle Pointer to .Net type Dictionary<string, string>. Defaults to None
        
        autoOffset: Optional[AutoOffsetReset]
            (Optional) Underlying .Net type is AutoOffsetReset?. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type RawInputTopic
        """
        brokerAddress_ptr = InteropUtils.utf8_to_ptr(brokerAddress)
        topicName_ptr = InteropUtils.utf8_to_ptr(topicName)
        consumerGroup_ptr = InteropUtils.utf8_to_ptr(consumerGroup)
        autoOffset_conv = autoOffset.value
        autoOffset_nullable = InteropUtils.create_nullable(ctypes.c_int)(autoOffset_conv)
        
        result = InteropUtils.invoke("rawinputtopic_constructor", brokerAddress_ptr, topicName_ptr, consumerGroup_ptr, brokerProperties, autoOffset_nullable)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("rawinputtopic_add_onmessageread")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnMessageRead(self, value: Callable[[c_void_p], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p], None]
            Underlying .Net type is Action<RawMessage>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0: value(c_void_p(p0))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in rawinputtopic_add_onmessageread, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO RawInputTopic.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in rawinputtopic_add_onmessageread, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("rawinputtopic_add_onmessageread", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("rawinputtopic_remove_onmessageread")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnMessageRead(self, value: Callable[[c_void_p], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p], None]
            Underlying .Net type is Action<RawMessage>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0: value(c_void_p(p0))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in rawinputtopic_remove_onmessageread, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO RawInputTopic.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in rawinputtopic_remove_onmessageread, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("rawinputtopic_remove_onmessageread", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("rawinputtopic_add_ondisposed")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnDisposed(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler
        
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
                print("Registering value_converter_func_wrapper in rawinputtopic_add_ondisposed, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO RawInputTopic.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in rawinputtopic_add_ondisposed, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("rawinputtopic_add_ondisposed", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("rawinputtopic_remove_ondisposed")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnDisposed(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler
        
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
                print("Registering value_converter_func_wrapper in rawinputtopic_remove_ondisposed, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO RawInputTopic.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in rawinputtopic_remove_ondisposed, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("rawinputtopic_remove_ondisposed", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("rawinputtopic_add_onerroroccurred")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnErrorOccurred(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
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
                print("Registering value_converter_func_wrapper in rawinputtopic_add_onerroroccurred, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO RawInputTopic.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in rawinputtopic_add_onerroroccurred, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("rawinputtopic_add_onerroroccurred", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("rawinputtopic_remove_onerroroccurred")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnErrorOccurred(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
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
                print("Registering value_converter_func_wrapper in rawinputtopic_remove_onerroroccurred, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO RawInputTopic.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in rawinputtopic_remove_onerroroccurred, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("rawinputtopic_remove_onerroroccurred", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("rawinputtopic_startreading")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p]
    def StartReading(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("rawinputtopic_startreading", self.__pointer)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("rawinputtopic_dispose")
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
        InteropUtils.invoke("rawinputtopic_dispose", self.__pointer)
