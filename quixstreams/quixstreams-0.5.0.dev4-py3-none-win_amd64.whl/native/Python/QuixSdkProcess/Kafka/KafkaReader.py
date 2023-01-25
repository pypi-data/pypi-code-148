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


class KafkaReader(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type KafkaReader
        
        Returns
        ----------
        
        KafkaReader:
            Instance wrapping the .net type KafkaReader
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = KafkaReader._KafkaReader__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(KafkaReader, cls).__new__(cls)
            KafkaReader._KafkaReader__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type KafkaReader
        
        Returns
        ----------
        
        KafkaReader:
            Instance wrapping the .net type KafkaReader
        """
        if '_KafkaReader__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del KafkaReader._KafkaReader__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("kafkareader_constructor")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Constructor(kafkaReaderConfiguration: c_void_p, topic: str) -> c_void_p:
        """
        Parameters
        ----------
        
        kafkaReaderConfiguration: c_void_p
            GC Handle Pointer to .Net type KafkaReaderConfiguration
        
        topic: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type KafkaReader
        """
        topic_ptr = InteropUtils.utf8_to_ptr(topic)
        
        result = InteropUtils.invoke("kafkareader_constructor", kafkaReaderConfiguration, topic_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareader_add_onreadexception")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnReadException(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
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
                print("Registering value_converter_func_wrapper in kafkareader_add_onreadexception, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO KafkaReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in kafkareader_add_onreadexception, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("kafkareader_add_onreadexception", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareader_remove_onreadexception")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnReadException(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
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
                print("Registering value_converter_func_wrapper in kafkareader_remove_onreadexception, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO KafkaReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in kafkareader_remove_onreadexception, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("kafkareader_remove_onreadexception", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareader_add_onstreamsrevoked")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnStreamsRevoked(self, value: Callable[[c_void_p], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p], None]
            Underlying .Net type is Action<IStreamProcess[]>
        
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
                print("Registering value_converter_func_wrapper in kafkareader_add_onstreamsrevoked, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO KafkaReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in kafkareader_add_onstreamsrevoked, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("kafkareader_add_onstreamsrevoked", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareader_remove_onstreamsrevoked")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnStreamsRevoked(self, value: Callable[[c_void_p], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p], None]
            Underlying .Net type is Action<IStreamProcess[]>
        
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
                print("Registering value_converter_func_wrapper in kafkareader_remove_onstreamsrevoked, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO KafkaReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in kafkareader_remove_onstreamsrevoked, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("kafkareader_remove_onstreamsrevoked", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareader_add_onrevoking")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnRevoking(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
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
                print("Registering value_converter_func_wrapper in kafkareader_add_onrevoking, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO KafkaReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in kafkareader_add_onrevoking, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("kafkareader_add_onrevoking", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareader_remove_onrevoking")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnRevoking(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
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
                print("Registering value_converter_func_wrapper in kafkareader_remove_onrevoking, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO KafkaReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in kafkareader_remove_onrevoking, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("kafkareader_remove_onrevoking", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareader_add_oncommitted")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnCommitted(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
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
                print("Registering value_converter_func_wrapper in kafkareader_add_oncommitted, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO KafkaReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in kafkareader_add_oncommitted, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("kafkareader_add_oncommitted", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareader_remove_oncommitted")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnCommitted(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
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
                print("Registering value_converter_func_wrapper in kafkareader_remove_oncommitted, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO KafkaReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in kafkareader_remove_oncommitted, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("kafkareader_remove_oncommitted", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareader_add_oncommitting")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnCommitting(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
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
                print("Registering value_converter_func_wrapper in kafkareader_add_oncommitting, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO KafkaReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in kafkareader_add_oncommitting, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("kafkareader_add_oncommitting", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareader_remove_oncommitting")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnCommitting(self, value: Callable[[c_void_p, c_void_p], None]) -> None:
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
                print("Registering value_converter_func_wrapper in kafkareader_remove_oncommitting, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO KafkaReader.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in kafkareader_remove_oncommitting, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("kafkareader_remove_oncommitting", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareader_start")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p]
    def Start(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("kafkareader_start", self.__pointer)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareader_foreach")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def ForEach(self, streamProcessFactoryHandler: Callable[[str], c_void_p]) -> None:
        """
        Parameters
        ----------
        
        streamProcessFactoryHandler: Callable[[str], c_void_p]
            Underlying .Net type is Func<string, IStreamProcess>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        streamProcessFactoryHandler_func_wrapper_addr = None
        if streamProcessFactoryHandler is not None:
            streamProcessFactoryHandler_converter = lambda p0: streamProcessFactoryHandler(str(p0))

            streamProcessFactoryHandler_converter_func_wrapper = ctypes.CFUNCTYPE(c_void_p, ctypes.c_char_p)(streamProcessFactoryHandler_converter)
            streamProcessFactoryHandler_func_wrapper_addr = ctypes.cast(streamProcessFactoryHandler_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering streamProcessFactoryHandler_converter_func_wrapper in kafkareader_foreach, addr {}".format(streamProcessFactoryHandler_func_wrapper_addr))
                streamProcessFactoryHandler_func_wrapper_addr_val = streamProcessFactoryHandler_func_wrapper_addr.value
                # TODO KafkaReader.__weakrefs.append(weakref.ref(streamProcessFactoryHandler_converter_func_wrapper, lambda x: print("De-referenced streamProcessFactoryHandler_converter_func_wrapper in kafkareader_foreach, addr {}".format(streamProcessFactoryHandler_func_wrapper_addr_val))))
        
        InteropUtils.invoke("kafkareader_foreach", self.__pointer, streamProcessFactoryHandler_func_wrapper_addr)
        return streamProcessFactoryHandler_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareader_stop")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p]
    def Stop(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("kafkareader_stop", self.__pointer)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareader_dispose")
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
        InteropUtils.invoke("kafkareader_dispose", self.__pointer)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("kafkareader_commit")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p]
    def Commit(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("kafkareader_commit", self.__pointer)
