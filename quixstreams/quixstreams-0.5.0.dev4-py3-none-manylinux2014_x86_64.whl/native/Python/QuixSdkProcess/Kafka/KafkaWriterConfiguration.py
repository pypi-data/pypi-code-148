# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...InteropHelpers.InteropUtils import InteropUtils


class KafkaWriterConfiguration(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type KafkaWriterConfiguration
        
        Returns
        ----------
        
        KafkaWriterConfiguration:
            Instance wrapping the .net type KafkaWriterConfiguration
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = KafkaWriterConfiguration._KafkaWriterConfiguration__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(KafkaWriterConfiguration, cls).__new__(cls)
            KafkaWriterConfiguration._KafkaWriterConfiguration__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type KafkaWriterConfiguration
        
        Returns
        ----------
        
        KafkaWriterConfiguration:
            Instance wrapping the .net type KafkaWriterConfiguration
        """
        if '_KafkaWriterConfiguration__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del KafkaWriterConfiguration._KafkaWriterConfiguration__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("kafkawriterconfiguration_constructor")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Constructor(brokerList: str, properties: c_void_p = None) -> c_void_p:
        """
        Parameters
        ----------
        
        brokerList: str
            Underlying .Net type is string
        
        properties: c_void_p
            (Optional) GC Handle Pointer to .Net type IDictionary<string, string>. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type KafkaWriterConfiguration
        """
        brokerList_ptr = InteropUtils.utf8_to_ptr(brokerList)
        
        result = InteropUtils.invoke("kafkawriterconfiguration_constructor", brokerList_ptr, properties)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkawriterconfiguration_get_brokerlist")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_BrokerList(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("kafkawriterconfiguration_get_brokerlist", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkawriterconfiguration_get_maxmessagesize")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_MaxMessageSize(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("kafkawriterconfiguration_get_maxmessagesize", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkawriterconfiguration_get_maxkeysize")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_MaxKeySize(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("kafkawriterconfiguration_get_maxkeysize", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkawriterconfiguration_get_properties")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Properties(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IDictionary<string, string>
        """
        result = InteropUtils.invoke("kafkawriterconfiguration_get_properties", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
