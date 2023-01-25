# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .ParametersBufferWriter import ParametersBufferWriter
from .ParameterDefinitionBuilder import ParameterDefinitionBuilder
from ....InteropHelpers.InteropUtils import InteropUtils


class StreamParametersWriter(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamParametersWriter
        
        Returns
        ----------
        
        StreamParametersWriter:
            Instance wrapping the .net type StreamParametersWriter
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = StreamParametersWriter._StreamParametersWriter__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(StreamParametersWriter, cls).__new__(cls)
            StreamParametersWriter._StreamParametersWriter__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamParametersWriter
        
        Returns
        ----------
        
        StreamParametersWriter:
            Instance wrapping the .net type StreamParametersWriter
        """
        if '_StreamParametersWriter__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del StreamParametersWriter._StreamParametersWriter__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("streamparameterswriter_get_buffer")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Buffer(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParametersBufferWriter
        """
        result = InteropUtils.invoke("streamparameterswriter_get_buffer", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streamparameterswriter_write")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Write(self, data: c_void_p) -> None:
        """
        Parameters
        ----------
        
        data: c_void_p
            GC Handle Pointer to .Net type ParameterData
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streamparameterswriter_write", self.__pointer, data)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streamparameterswriter_write2")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Write2(self, data: c_void_p) -> None:
        """
        Parameters
        ----------
        
        data: c_void_p
            GC Handle Pointer to .Net type ParameterDataRaw
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streamparameterswriter_write2", self.__pointer, data)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streamparameterswriter_get_defaultlocation")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_DefaultLocation(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("streamparameterswriter_get_defaultlocation", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streamparameterswriter_set_defaultlocation")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_DefaultLocation(self, value: str) -> None:
        """
        Parameters
        ----------
        
        value: str
            Underlying .Net type is string
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        InteropUtils.invoke("streamparameterswriter_set_defaultlocation", self.__pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streamparameterswriter_adddefinitions")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def AddDefinitions(self, definitions: c_void_p) -> None:
        """
        Parameters
        ----------
        
        definitions: c_void_p
            GC Handle Pointer to .Net type List<ParameterDefinition>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streamparameterswriter_adddefinitions", self.__pointer, definitions)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streamparameterswriter_adddefinition")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
    def AddDefinition(self, parameterId: str, name: str = None, description: str = None) -> c_void_p:
        """
        Parameters
        ----------
        
        parameterId: str
            Underlying .Net type is string
        
        name: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        description: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDefinitionBuilder
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        name_ptr = InteropUtils.utf8_to_ptr(name)
        description_ptr = InteropUtils.utf8_to_ptr(description)
        
        result = InteropUtils.invoke("streamparameterswriter_adddefinition", self.__pointer, parameterId_ptr, name_ptr, description_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streamparameterswriter_addlocation")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def AddLocation(self, location: str) -> c_void_p:
        """
        Parameters
        ----------
        
        location: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDefinitionBuilder
        """
        location_ptr = InteropUtils.utf8_to_ptr(location)
        
        result = InteropUtils.invoke("streamparameterswriter_addlocation", self.__pointer, location_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streamparameterswriter_flush")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p]
    def Flush(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streamparameterswriter_flush", self.__pointer)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("streamparameterswriter_dispose")
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
        InteropUtils.invoke("streamparameterswriter_dispose", self.__pointer)
