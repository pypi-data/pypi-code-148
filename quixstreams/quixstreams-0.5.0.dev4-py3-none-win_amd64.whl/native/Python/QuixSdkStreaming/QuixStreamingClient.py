# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .QuixStreamingClientTokenValidationConfiguration import QuixStreamingClientTokenValidationConfiguration
from ..QuixSdkProcess.Kafka.AutoOffsetReset import AutoOffsetReset
from .IInputTopic import IInputTopic
from .Raw.IRawInputTopic import IRawInputTopic
from .Raw.IRawOutputTopic import IRawOutputTopic
from .IOutputTopic import IOutputTopic
from ..SystemPrivateUri.System.Uri import Uri
from ..SystemPrivateCoreLib.System.TimeSpan import TimeSpan
from ..InteropHelpers.InteropUtils import InteropUtils


class QuixStreamingClient(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type QuixStreamingClient
        
        Returns
        ----------
        
        QuixStreamingClient:
            Instance wrapping the .net type QuixStreamingClient
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = QuixStreamingClient._QuixStreamingClient__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(QuixStreamingClient, cls).__new__(cls)
            QuixStreamingClient._QuixStreamingClient__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type QuixStreamingClient
        
        Returns
        ----------
        
        QuixStreamingClient:
            Instance wrapping the .net type QuixStreamingClient
        """
        if '_QuixStreamingClient__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del QuixStreamingClient._QuixStreamingClient__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("quixstreamingclient_constructor")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_ubyte, c_void_p, ctypes.c_ubyte, c_void_p]
    @staticmethod
    def Constructor(token: str = None, autoCreateTopics: bool = True, properties: c_void_p = None, debug: bool = False, httpClient: c_void_p = None) -> c_void_p:
        """
        Parameters
        ----------
        
        token: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        autoCreateTopics: bool
            (Optional) Underlying .Net type is Boolean. Defaults to True
        
        properties: c_void_p
            (Optional) GC Handle Pointer to .Net type IDictionary<string, string>. Defaults to None
        
        debug: bool
            (Optional) Underlying .Net type is Boolean. Defaults to False
        
        httpClient: c_void_p
            (Optional) GC Handle Pointer to .Net type HttpClient. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type QuixStreamingClient
        """
        token_ptr = InteropUtils.utf8_to_ptr(token)
        autoCreateTopics_bool = 1 if autoCreateTopics else 0
        debug_bool = 1 if debug else 0
        
        result = InteropUtils.invoke("quixstreamingclient_constructor", token_ptr, autoCreateTopics_bool, properties, debug_bool, httpClient)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("quixstreamingclient_get_tokenvalidationconfig")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_TokenValidationConfig(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type QuixStreamingClient.TokenValidationConfiguration
        """
        result = InteropUtils.invoke("quixstreamingclient_get_tokenvalidationconfig", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("quixstreamingclient_set_tokenvalidationconfig")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_TokenValidationConfig(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type QuixStreamingClient.TokenValidationConfiguration
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("quixstreamingclient_set_tokenvalidationconfig", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("quixstreamingclient_openinputtopic")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p, ctypes.c_int]
    def OpenInputTopic(self, topicIdOrName: str, consumerGroup: str = None, options: c_void_p = None, autoOffset: AutoOffsetReset = AutoOffsetReset.Earliest) -> c_void_p:
        """
        Parameters
        ----------
        
        topicIdOrName: str
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
        topicIdOrName_ptr = InteropUtils.utf8_to_ptr(topicIdOrName)
        consumerGroup_ptr = InteropUtils.utf8_to_ptr(consumerGroup)
        
        result = InteropUtils.invoke("quixstreamingclient_openinputtopic", self.__pointer, topicIdOrName_ptr, consumerGroup_ptr, options, autoOffset.value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("quixstreamingclient_openrawinputtopic")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p, InteropUtils.create_nullable(ctypes.c_int)]
    def OpenRawInputTopic(self, topicIdOrName: str, consumerGroup: str = None, autoOffset: Optional[AutoOffsetReset] = None) -> c_void_p:
        """
        Parameters
        ----------
        
        topicIdOrName: str
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
        topicIdOrName_ptr = InteropUtils.utf8_to_ptr(topicIdOrName)
        consumerGroup_ptr = InteropUtils.utf8_to_ptr(consumerGroup)
        autoOffset_conv = autoOffset.value
        autoOffset_nullable = InteropUtils.create_nullable(ctypes.c_int)(autoOffset_conv)
        
        result = InteropUtils.invoke("quixstreamingclient_openrawinputtopic", self.__pointer, topicIdOrName_ptr, consumerGroup_ptr, autoOffset_nullable)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("quixstreamingclient_openrawoutputtopic")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def OpenRawOutputTopic(self, topicIdOrName: str) -> c_void_p:
        """
        Parameters
        ----------
        
        topicIdOrName: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IRawOutputTopic
        """
        topicIdOrName_ptr = InteropUtils.utf8_to_ptr(topicIdOrName)
        
        result = InteropUtils.invoke("quixstreamingclient_openrawoutputtopic", self.__pointer, topicIdOrName_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("quixstreamingclient_openoutputtopic")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def OpenOutputTopic(self, topicIdOrName: str) -> c_void_p:
        """
        Parameters
        ----------
        
        topicIdOrName: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IOutputTopic
        """
        topicIdOrName_ptr = InteropUtils.utf8_to_ptr(topicIdOrName)
        
        result = InteropUtils.invoke("quixstreamingclient_openoutputtopic", self.__pointer, topicIdOrName_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("quixstreamingclient_get_apiurl")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_ApiUrl(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Uri
        """
        result = InteropUtils.invoke("quixstreamingclient_get_apiurl", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("quixstreamingclient_set_apiurl")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_ApiUrl(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Uri
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("quixstreamingclient_set_apiurl", self.__pointer, value)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("quixstreamingclient_get_cacheperiod")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_CachePeriod(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("quixstreamingclient_get_cacheperiod", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("quixstreamingclient_set_cacheperiod")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_CachePeriod(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("quixstreamingclient_set_cacheperiod", self.__pointer, value)
