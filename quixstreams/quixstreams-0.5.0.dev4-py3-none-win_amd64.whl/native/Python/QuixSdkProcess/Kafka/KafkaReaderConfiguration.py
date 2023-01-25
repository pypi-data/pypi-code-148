# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...QuixSdkTransport.Fw.CommitOptions import CommitOptions
from ...InteropHelpers.InteropUtils import InteropUtils


class KafkaReaderConfiguration(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type KafkaReaderConfiguration
        
        Returns
        ----------
        
        KafkaReaderConfiguration:
            Instance wrapping the .net type KafkaReaderConfiguration
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = KafkaReaderConfiguration._KafkaReaderConfiguration__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(KafkaReaderConfiguration, cls).__new__(cls)
            KafkaReaderConfiguration._KafkaReaderConfiguration__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type KafkaReaderConfiguration
        
        Returns
        ----------
        
        KafkaReaderConfiguration:
            Instance wrapping the .net type KafkaReaderConfiguration
        """
        if '_KafkaReaderConfiguration__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del KafkaReaderConfiguration._KafkaReaderConfiguration__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("kafkareaderconfiguration_constructor")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Constructor(brokerList: str, consumerGroupId: str = None, properties: c_void_p = None) -> c_void_p:
        """
        Parameters
        ----------
        
        brokerList: str
            Underlying .Net type is string
        
        consumerGroupId: str
            (Optional) Underlying .Net type is string. Defaults to Default
        
        properties: c_void_p
            (Optional) GC Handle Pointer to .Net type IDictionary<string, string>. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type KafkaReaderConfiguration
        """
        brokerList_ptr = InteropUtils.utf8_to_ptr(brokerList)
        consumerGroupId_ptr = InteropUtils.utf8_to_ptr(consumerGroupId)
        
        result = InteropUtils.invoke("kafkareaderconfiguration_constructor", brokerList_ptr, consumerGroupId_ptr, properties)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareaderconfiguration_get_brokerlist")
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
        result = InteropUtils.invoke("kafkareaderconfiguration_get_brokerlist", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareaderconfiguration_get_consumergroupid")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_ConsumerGroupId(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("kafkareaderconfiguration_get_consumergroupid", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareaderconfiguration_get_commitoptions")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_CommitOptions(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CommitOptions
        """
        result = InteropUtils.invoke("kafkareaderconfiguration_get_commitoptions", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareaderconfiguration_set_commitoptions")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_CommitOptions(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type CommitOptions
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("kafkareaderconfiguration_set_commitoptions", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareaderconfiguration_get_properties")
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
        result = InteropUtils.invoke("kafkareaderconfiguration_get_properties", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
