# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from typing import Callable
from .ParameterDataTimestamp import ParameterDataTimestamp
from .ParameterData import ParameterData
from ...InteropHelpers.InteropUtils import InteropUtils


class ParametersBufferConfiguration(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParametersBufferConfiguration
        
        Returns
        ----------
        
        ParametersBufferConfiguration:
            Instance wrapping the .net type ParametersBufferConfiguration
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = ParametersBufferConfiguration._ParametersBufferConfiguration__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(ParametersBufferConfiguration, cls).__new__(cls)
            ParametersBufferConfiguration._ParametersBufferConfiguration__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParametersBufferConfiguration
        
        Returns
        ----------
        
        ParametersBufferConfiguration:
            Instance wrapping the .net type ParametersBufferConfiguration
        """
        if '_ParametersBufferConfiguration__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del ParametersBufferConfiguration._ParametersBufferConfiguration__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("parametersbufferconfiguration_constructor")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParametersBufferConfiguration
        """
        result = InteropUtils.invoke("parametersbufferconfiguration_constructor")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferconfiguration_get_packetsize")
    __interop_func.restype = InteropUtils.create_nullable(ctypes.c_int)
    __interop_func.argtypes = [c_void_p]
    def get_PacketSize(self) -> Optional[int]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[int]:
            Underlying .Net type is int?
        """
        result = InteropUtils.invoke("parametersbufferconfiguration_get_packetsize", self.__pointer)
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferconfiguration_set_packetsize")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, InteropUtils.create_nullable(ctypes.c_int)]
    def set_PacketSize(self, value: Optional[int]) -> None:
        """
        Parameters
        ----------
        
        value: Optional[int]
            Underlying .Net type is int?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_nullable = InteropUtils.create_nullable(ctypes.c_int)(value)
        
        InteropUtils.invoke("parametersbufferconfiguration_set_packetsize", self.__pointer, value_nullable)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferconfiguration_get_timespaninnanoseconds")
    __interop_func.restype = InteropUtils.create_nullable(ctypes.c_longlong)
    __interop_func.argtypes = [c_void_p]
    def get_TimeSpanInNanoseconds(self) -> Optional[int]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[int]:
            Underlying .Net type is long?
        """
        result = InteropUtils.invoke("parametersbufferconfiguration_get_timespaninnanoseconds", self.__pointer)
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferconfiguration_set_timespaninnanoseconds")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, InteropUtils.create_nullable(ctypes.c_longlong)]
    def set_TimeSpanInNanoseconds(self, value: Optional[int]) -> None:
        """
        Parameters
        ----------
        
        value: Optional[int]
            Underlying .Net type is long?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_nullable = InteropUtils.create_nullable(ctypes.c_longlong)(value)
        
        InteropUtils.invoke("parametersbufferconfiguration_set_timespaninnanoseconds", self.__pointer, value_nullable)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferconfiguration_get_timespaninmilliseconds")
    __interop_func.restype = InteropUtils.create_nullable(ctypes.c_longlong)
    __interop_func.argtypes = [c_void_p]
    def get_TimeSpanInMilliseconds(self) -> Optional[int]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[int]:
            Underlying .Net type is long?
        """
        result = InteropUtils.invoke("parametersbufferconfiguration_get_timespaninmilliseconds", self.__pointer)
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferconfiguration_set_timespaninmilliseconds")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, InteropUtils.create_nullable(ctypes.c_longlong)]
    def set_TimeSpanInMilliseconds(self, value: Optional[int]) -> None:
        """
        Parameters
        ----------
        
        value: Optional[int]
            Underlying .Net type is long?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_nullable = InteropUtils.create_nullable(ctypes.c_longlong)(value)
        
        InteropUtils.invoke("parametersbufferconfiguration_set_timespaninmilliseconds", self.__pointer, value_nullable)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferconfiguration_get_customtriggerbeforeenqueue")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_CustomTriggerBeforeEnqueue(self) -> Callable[[c_void_p], bool]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Callable[[c_void_p], bool]:
            Underlying .Net type is Func<ParameterDataTimestamp, Boolean>
        """
        result = InteropUtils.invoke("parametersbufferconfiguration_get_customtriggerbeforeenqueue", self.__pointer)
        return Exception("NOT IMPLEMENTED YET")
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferconfiguration_set_customtriggerbeforeenqueue")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_CustomTriggerBeforeEnqueue(self, value: Callable[[c_void_p], bool]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p], bool]
            Underlying .Net type is Func<ParameterDataTimestamp, Boolean>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0: value(c_void_p(p0))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(ctypes.c_bool, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in parametersbufferconfiguration_set_customtriggerbeforeenqueue, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO ParametersBufferConfiguration.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in parametersbufferconfiguration_set_customtriggerbeforeenqueue, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("parametersbufferconfiguration_set_customtriggerbeforeenqueue", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferconfiguration_get_customtrigger")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_CustomTrigger(self) -> Callable[[c_void_p], bool]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Callable[[c_void_p], bool]:
            Underlying .Net type is Func<ParameterData, Boolean>
        """
        result = InteropUtils.invoke("parametersbufferconfiguration_get_customtrigger", self.__pointer)
        return Exception("NOT IMPLEMENTED YET")
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferconfiguration_set_customtrigger")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_CustomTrigger(self, value: Callable[[c_void_p], bool]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p], bool]
            Underlying .Net type is Func<ParameterData, Boolean>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0: value(c_void_p(p0))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(ctypes.c_bool, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in parametersbufferconfiguration_set_customtrigger, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO ParametersBufferConfiguration.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in parametersbufferconfiguration_set_customtrigger, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("parametersbufferconfiguration_set_customtrigger", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferconfiguration_get_filter")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Filter(self) -> Callable[[c_void_p], bool]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Callable[[c_void_p], bool]:
            Underlying .Net type is Func<ParameterDataTimestamp, Boolean>
        """
        result = InteropUtils.invoke("parametersbufferconfiguration_get_filter", self.__pointer)
        return Exception("NOT IMPLEMENTED YET")
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferconfiguration_set_filter")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Filter(self, value: Callable[[c_void_p], bool]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p], bool]
            Underlying .Net type is Func<ParameterDataTimestamp, Boolean>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0: value(c_void_p(p0))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(ctypes.c_bool, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in parametersbufferconfiguration_set_filter, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO ParametersBufferConfiguration.__weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in parametersbufferconfiguration_set_filter, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("parametersbufferconfiguration_set_filter", self.__pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferconfiguration_get_buffertimeout")
    __interop_func.restype = InteropUtils.create_nullable(ctypes.c_int)
    __interop_func.argtypes = [c_void_p]
    def get_BufferTimeout(self) -> Optional[int]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[int]:
            Underlying .Net type is int?
        """
        result = InteropUtils.invoke("parametersbufferconfiguration_get_buffertimeout", self.__pointer)
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parametersbufferconfiguration_set_buffertimeout")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, InteropUtils.create_nullable(ctypes.c_int)]
    def set_BufferTimeout(self, value: Optional[int]) -> None:
        """
        Parameters
        ----------
        
        value: Optional[int]
            Underlying .Net type is int?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_nullable = InteropUtils.create_nullable(ctypes.c_int)(value)
        
        InteropUtils.invoke("parametersbufferconfiguration_set_buffertimeout", self.__pointer, value_nullable)
