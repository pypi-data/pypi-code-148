# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...InteropHelpers.InteropUtils import InteropUtils


class ParameterDefinition(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterDefinition
        
        Returns
        ----------
        
        ParameterDefinition:
            Instance wrapping the .net type ParameterDefinition
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = ParameterDefinition._ParameterDefinition__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(ParameterDefinition, cls).__new__(cls)
            ParameterDefinition._ParameterDefinition__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterDefinition
        
        Returns
        ----------
        
        ParameterDefinition:
            Instance wrapping the .net type ParameterDefinition
        """
        if '_ParameterDefinition__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del ParameterDefinition._ParameterDefinition__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("parameterdefinition2_constructor")
    __interop_func.restype = c_void_p
    @staticmethod
    def Constructor() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDefinition
        """
        result = InteropUtils.invoke("parameterdefinition2_constructor")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdefinition2_get_id")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Id(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("parameterdefinition2_get_id", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdefinition2_set_id")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Id(self, value: str) -> None:
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
        
        InteropUtils.invoke("parameterdefinition2_set_id", self.__pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdefinition2_get_name")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Name(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("parameterdefinition2_get_name", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdefinition2_set_name")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Name(self, value: str) -> None:
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
        
        InteropUtils.invoke("parameterdefinition2_set_name", self.__pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdefinition2_get_description")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Description(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("parameterdefinition2_get_description", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdefinition2_set_description")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Description(self, value: str) -> None:
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
        
        InteropUtils.invoke("parameterdefinition2_set_description", self.__pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdefinition2_get_minimumvalue")
    __interop_func.restype = InteropUtils.create_nullable(ctypes.c_double)
    __interop_func.argtypes = [c_void_p]
    def get_MinimumValue(self) -> Optional[float]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[float]:
            Underlying .Net type is double?
        """
        result = InteropUtils.invoke("parameterdefinition2_get_minimumvalue", self.__pointer)
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdefinition2_set_minimumvalue")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, InteropUtils.create_nullable(ctypes.c_double)]
    def set_MinimumValue(self, value: Optional[float]) -> None:
        """
        Parameters
        ----------
        
        value: Optional[float]
            Underlying .Net type is double?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_nullable = InteropUtils.create_nullable(ctypes.c_double)(value)
        
        InteropUtils.invoke("parameterdefinition2_set_minimumvalue", self.__pointer, value_nullable)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdefinition2_get_maximumvalue")
    __interop_func.restype = InteropUtils.create_nullable(ctypes.c_double)
    __interop_func.argtypes = [c_void_p]
    def get_MaximumValue(self) -> Optional[float]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[float]:
            Underlying .Net type is double?
        """
        result = InteropUtils.invoke("parameterdefinition2_get_maximumvalue", self.__pointer)
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdefinition2_set_maximumvalue")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, InteropUtils.create_nullable(ctypes.c_double)]
    def set_MaximumValue(self, value: Optional[float]) -> None:
        """
        Parameters
        ----------
        
        value: Optional[float]
            Underlying .Net type is double?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_nullable = InteropUtils.create_nullable(ctypes.c_double)(value)
        
        InteropUtils.invoke("parameterdefinition2_set_maximumvalue", self.__pointer, value_nullable)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdefinition2_get_unit")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Unit(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("parameterdefinition2_get_unit", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdefinition2_set_unit")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Unit(self, value: str) -> None:
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
        
        InteropUtils.invoke("parameterdefinition2_set_unit", self.__pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdefinition2_get_format")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Format(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("parameterdefinition2_get_format", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdefinition2_set_format")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_Format(self, value: str) -> None:
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
        
        InteropUtils.invoke("parameterdefinition2_set_format", self.__pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdefinition2_get_customproperties")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_CustomProperties(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("parameterdefinition2_get_customproperties", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("parameterdefinition2_set_customproperties")
    __interop_func.restype = None
    __interop_func.argtypes = [c_void_p, c_void_p]
    def set_CustomProperties(self, value: str) -> None:
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
        
        InteropUtils.invoke("parameterdefinition2_set_customproperties", self.__pointer, value_ptr)
