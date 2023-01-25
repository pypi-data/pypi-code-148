# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ..QuixSdkProcess.Kafka.AutoOffsetReset import AutoOffsetReset
from .IInputTopic import IInputTopic
from .Raw.IRawInputTopic import IRawInputTopic
from .Raw.IRawOutputTopic import IRawOutputTopic
from .IOutputTopic import IOutputTopic
from ..InteropHelpers.InteropUtils import InteropUtils


class KafkaStreamingClient(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type KafkaStreamingClient
        
        Returns
        ----------
        
        KafkaStreamingClient:
            Instance wrapping the .net type KafkaStreamingClient
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = KafkaStreamingClient._KafkaStreamingClient__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(KafkaStreamingClient, cls).__new__(cls)
            KafkaStreamingClient._KafkaStreamingClient__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type KafkaStreamingClient
        
        Returns
        ----------
        
        KafkaStreamingClient:
            Instance wrapping the .net type KafkaStreamingClient
        """
        if '_KafkaStreamingClient__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del KafkaStreamingClient._KafkaStreamingClient__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("kafkastreamingclient_constructor")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p, ctypes.c_ubyte]
    @staticmethod
    def Constructor(brokerAddress: str, securityOptions: c_void_p = None, properties: c_void_p = None, debug: bool = False) -> c_void_p:
        """
        Parameters
        ----------
        
        brokerAddress: str
            Underlying .Net type is string
        
        securityOptions: c_void_p
            (Optional) GC Handle Pointer to .Net type SecurityOptions. Defaults to None
        
        properties: c_void_p
            (Optional) GC Handle Pointer to .Net type IDictionary<string, string>. Defaults to None
        
        debug: bool
            (Optional) Underlying .Net type is Boolean. Defaults to False
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type KafkaStreamingClient
        """
        brokerAddress_ptr = InteropUtils.utf8_to_ptr(brokerAddress)
        debug_bool = 1 if debug else 0
        
        result = InteropUtils.invoke("kafkastreamingclient_constructor", brokerAddress_ptr, securityOptions, properties, debug_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkastreamingclient_openinputtopic")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p, ctypes.c_int]
    def OpenInputTopic(self, topic: str, consumerGroup: str = None, options: c_void_p = None, autoOffset: AutoOffsetReset = AutoOffsetReset.Earliest) -> c_void_p:
        """
        Parameters
        ----------
        
        topic: str
            Underlying .Net type is string
        
        consumerGroup: str
            (Optional) Underlying .Net type is string. Defaults to Default
        
        options: c_void_p
            (Optional) GC Handle Pointer to .Net type CommitOptions. Defaults to None
        
        autoOffset: AutoOffsetReset
            (Optional) Underlying .Net type is AutoOffsetReset. Defaults to Earliest
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IInputTopic
        """
        topic_ptr = InteropUtils.utf8_to_ptr(topic)
        consumerGroup_ptr = InteropUtils.utf8_to_ptr(consumerGroup)
        
        result = InteropUtils.invoke("kafkastreamingclient_openinputtopic", self.__pointer, topic_ptr, consumerGroup_ptr, options, autoOffset.value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkastreamingclient_openrawinputtopic")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p, InteropUtils.create_nullable(ctypes.c_int)]
    def OpenRawInputTopic(self, topic: str, consumerGroup: str = None, autoOffset: Optional[AutoOffsetReset] = None) -> c_void_p:
        """
        Parameters
        ----------
        
        topic: str
            Underlying .Net type is string
        
        consumerGroup: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        autoOffset: Optional[AutoOffsetReset]
            (Optional) Underlying .Net type is AutoOffsetReset?. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IRawInputTopic
        """
        topic_ptr = InteropUtils.utf8_to_ptr(topic)
        consumerGroup_ptr = InteropUtils.utf8_to_ptr(consumerGroup)
        autoOffset_conv = autoOffset.value
        autoOffset_nullable = InteropUtils.create_nullable(ctypes.c_int)(autoOffset_conv)
        
        result = InteropUtils.invoke("kafkastreamingclient_openrawinputtopic", self.__pointer, topic_ptr, consumerGroup_ptr, autoOffset_nullable)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkastreamingclient_openrawoutputtopic")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def OpenRawOutputTopic(self, topic: str) -> c_void_p:
        """
        Parameters
        ----------
        
        topic: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IRawOutputTopic
        """
        topic_ptr = InteropUtils.utf8_to_ptr(topic)
        
        result = InteropUtils.invoke("kafkastreamingclient_openrawoutputtopic", self.__pointer, topic_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkastreamingclient_openoutputtopic")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def OpenOutputTopic(self, topic: str) -> c_void_p:
        """
        Parameters
        ----------
        
        topic: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IOutputTopic
        """
        topic_ptr = InteropUtils.utf8_to_ptr(topic)
        
        result = InteropUtils.invoke("kafkastreamingclient_openoutputtopic", self.__pointer, topic_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
