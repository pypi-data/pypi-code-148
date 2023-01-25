# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...InteropHelpers.InteropUtils import InteropUtils


class Type(object):
    
    __weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        ----------
        
        Type:
            Instance wrapping the .net type Type
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer._get_interop_ptr()
        
        instance = Type._Type__weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(Type, cls).__new__(cls)
            Type._Type__weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        ----------
        
        Type:
            Instance wrapping the .net type Type
        """
        if '_Type__pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self.__pointer_owner = net_pointer
            self.__pointer = net_pointer._get_interop_ptr()
        else:
            self.__pointer = net_pointer
        
        self.__finalizer = weakref.finalize(self, self.__finalizerfunc)
        self.__finalizer.atexit = False
    
    def __finalizerfunc(self):
        del Type._Type__weakrefs[self.__pointer.value]
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
    __interop_func = InteropUtils.get_function("type_get_isinterface")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsInterface(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isinterface", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_gettype")
    __interop_func.restype = c_void_p
    @staticmethod
    def GetType(typeName: str, throwOnError: bool, ignoreCase: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        typeName: str
            Underlying .Net type is string
        
        throwOnError: bool
            Underlying .Net type is Boolean
        
        ignoreCase: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        typeName_ptr = InteropUtils.utf8_to_ptr(typeName)
        throwOnError_bool = 1 if throwOnError else 0
        ignoreCase_bool = 1 if ignoreCase else 0
        
        result = InteropUtils.invoke("type_gettype", typeName_ptr, throwOnError_bool, ignoreCase_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_gettype2")
    __interop_func.restype = c_void_p
    @staticmethod
    def GetType2(typeName: str, throwOnError: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        typeName: str
            Underlying .Net type is string
        
        throwOnError: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        typeName_ptr = InteropUtils.utf8_to_ptr(typeName)
        throwOnError_bool = 1 if throwOnError else 0
        
        result = InteropUtils.invoke("type_gettype2", typeName_ptr, throwOnError_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_gettype3")
    __interop_func.restype = c_void_p
    @staticmethod
    def GetType3(typeName: str) -> c_void_p:
        """
        Parameters
        ----------
        
        typeName: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        typeName_ptr = InteropUtils.utf8_to_ptr(typeName)
        
        result = InteropUtils.invoke("type_gettype3", typeName_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_gettype7")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def GetType7(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_gettype7", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_namespace")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_Namespace(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("type_get_namespace", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_assemblyqualifiedname")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_AssemblyQualifiedName(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("type_get_assemblyqualifiedname", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_fullname")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_FullName(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("type_get_fullname", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isnested")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsNested(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isnested", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_declaringtype")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_DeclaringType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_get_declaringtype", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_reflectedtype")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_ReflectedType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_get_reflectedtype", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_underlyingsystemtype")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_UnderlyingSystemType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_get_underlyingsystemtype", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_istypedefinition")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsTypeDefinition(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_istypedefinition", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isarray")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsArray(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isarray", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isbyref")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsByRef(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isbyref", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_ispointer")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsPointer(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_ispointer", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isconstructedgenerictype")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsConstructedGenericType(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isconstructedgenerictype", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isgenericparameter")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsGenericParameter(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isgenericparameter", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isgenerictypeparameter")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsGenericTypeParameter(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isgenerictypeparameter", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isgenericmethodparameter")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsGenericMethodParameter(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isgenericmethodparameter", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isgenerictype")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsGenericType(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isgenerictype", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isgenerictypedefinition")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsGenericTypeDefinition(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isgenerictypedefinition", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isszarray")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsSZArray(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isszarray", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isvariableboundarray")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsVariableBoundArray(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isvariableboundarray", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isbyreflike")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsByRefLike(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isbyreflike", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_haselementtype")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_HasElementType(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_haselementtype", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_getelementtype")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def GetElementType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_getelementtype", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_getarrayrank")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def GetArrayRank(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("type_getarrayrank", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_getgenerictypedefinition")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def GetGenericTypeDefinition(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_getgenerictypedefinition", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_generictypearguments")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_GenericTypeArguments(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_get_generictypearguments", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_getgenericarguments")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def GetGenericArguments(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_getgenericarguments", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_genericparameterposition")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def get_GenericParameterPosition(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("type_get_genericparameterposition", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_getgenericparameterconstraints")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def GetGenericParameterConstraints(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_getgenericparameterconstraints", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isabstract")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsAbstract(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isabstract", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isimport")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsImport(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isimport", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_issealed")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsSealed(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_issealed", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isspecialname")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsSpecialName(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isspecialname", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isclass")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsClass(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isclass", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isnestedassembly")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsNestedAssembly(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isnestedassembly", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isnestedfamandassem")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsNestedFamANDAssem(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isnestedfamandassem", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isnestedfamily")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsNestedFamily(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isnestedfamily", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isnestedfamorassem")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsNestedFamORAssem(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isnestedfamorassem", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isnestedprivate")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsNestedPrivate(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isnestedprivate", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isnestedpublic")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsNestedPublic(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isnestedpublic", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isnotpublic")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsNotPublic(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isnotpublic", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_ispublic")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsPublic(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_ispublic", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isautolayout")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsAutoLayout(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isautolayout", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isexplicitlayout")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsExplicitLayout(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isexplicitlayout", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_islayoutsequential")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsLayoutSequential(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_islayoutsequential", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isansiclass")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsAnsiClass(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isansiclass", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isautoclass")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsAutoClass(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isautoclass", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isunicodeclass")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsUnicodeClass(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isunicodeclass", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_iscomobject")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsCOMObject(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_iscomobject", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_iscontextful")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsContextful(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_iscontextful", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isenum")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsEnum(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isenum", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_ismarshalbyref")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsMarshalByRef(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_ismarshalbyref", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isprimitive")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsPrimitive(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isprimitive", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isvaluetype")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsValueType(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isvaluetype", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_isassignableto")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    def IsAssignableTo(self, targetType: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        targetType: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_isassignableto", self.__pointer, targetType)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_issignaturetype")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsSignatureType(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_issignaturetype", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_issecuritycritical")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsSecurityCritical(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_issecuritycritical", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_issecuritysafecritical")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsSecuritySafeCritical(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_issecuritysafecritical", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_issecuritytransparent")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsSecurityTransparent(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_issecuritytransparent", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_getnestedtype")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def GetNestedType(self, name: str) -> c_void_p:
        """
        Parameters
        ----------
        
        name: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        name_ptr = InteropUtils.utf8_to_ptr(name)
        
        result = InteropUtils.invoke("type_getnestedtype", self.__pointer, name_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_getnestedtypes")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def GetNestedTypes(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_getnestedtypes", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_gettypearray")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    @staticmethod
    def GetTypeArray(args: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        args: c_void_p
            GC Handle Pointer to .Net type Object[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_gettypearray", args)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_gettypefromprogid")
    __interop_func.restype = c_void_p
    @staticmethod
    def GetTypeFromProgID(progID: str) -> c_void_p:
        """
        Parameters
        ----------
        
        progID: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        progID_ptr = InteropUtils.utf8_to_ptr(progID)
        
        result = InteropUtils.invoke("type_gettypefromprogid", progID_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_gettypefromprogid2")
    __interop_func.restype = c_void_p
    @staticmethod
    def GetTypeFromProgID2(progID: str, throwOnError: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        progID: str
            Underlying .Net type is string
        
        throwOnError: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        progID_ptr = InteropUtils.utf8_to_ptr(progID)
        throwOnError_bool = 1 if throwOnError else 0
        
        result = InteropUtils.invoke("type_gettypefromprogid2", progID_ptr, throwOnError_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_gettypefromprogid3")
    __interop_func.restype = c_void_p
    @staticmethod
    def GetTypeFromProgID3(progID: str, server: str) -> c_void_p:
        """
        Parameters
        ----------
        
        progID: str
            Underlying .Net type is string
        
        server: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        progID_ptr = InteropUtils.utf8_to_ptr(progID)
        server_ptr = InteropUtils.utf8_to_ptr(server)
        
        result = InteropUtils.invoke("type_gettypefromprogid3", progID_ptr, server_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_gettypefromprogid4")
    __interop_func.restype = c_void_p
    @staticmethod
    def GetTypeFromProgID4(progID: str, server: str, throwOnError: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        progID: str
            Underlying .Net type is string
        
        server: str
            Underlying .Net type is string
        
        throwOnError: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        progID_ptr = InteropUtils.utf8_to_ptr(progID)
        server_ptr = InteropUtils.utf8_to_ptr(server)
        throwOnError_bool = 1 if throwOnError else 0
        
        result = InteropUtils.invoke("type_gettypefromprogid4", progID_ptr, server_ptr, throwOnError_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_basetype")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def get_BaseType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_get_basetype", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_getinterface")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def GetInterface(self, name: str) -> c_void_p:
        """
        Parameters
        ----------
        
        name: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        name_ptr = InteropUtils.utf8_to_ptr(name)
        
        result = InteropUtils.invoke("type_getinterface", self.__pointer, name_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_getinterface2")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_ubyte]
    def GetInterface2(self, name: str, ignoreCase: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        name: str
            Underlying .Net type is string
        
        ignoreCase: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        name_ptr = InteropUtils.utf8_to_ptr(name)
        ignoreCase_bool = 1 if ignoreCase else 0
        
        result = InteropUtils.invoke("type_getinterface2", self.__pointer, name_ptr, ignoreCase_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_getinterfaces")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def GetInterfaces(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_getinterfaces", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_isinstanceoftype")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    def IsInstanceOfType(self, o: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        o: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_isinstanceoftype", self.__pointer, o)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_isequivalentto")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    def IsEquivalentTo(self, other: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        other: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_isequivalentto", self.__pointer, other)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_getenumunderlyingtype")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def GetEnumUnderlyingType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_getenumunderlyingtype", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_getenumvalues")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def GetEnumValues(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Array
        """
        result = InteropUtils.invoke("type_getenumvalues", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_getenumvaluesasunderlyingtype")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def GetEnumValuesAsUnderlyingType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Array
        """
        result = InteropUtils.invoke("type_getenumvaluesasunderlyingtype", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_makearraytype")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def MakeArrayType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_makearraytype", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_makearraytype2")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, ctypes.c_int]
    def MakeArrayType2(self, rank: int) -> c_void_p:
        """
        Parameters
        ----------
        
        rank: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_makearraytype2", self.__pointer, rank)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_makebyreftype")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def MakeByRefType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_makebyreftype", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_makegenerictype")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def MakeGenericType(self, typeArguments: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        typeArguments: c_void_p
            GC Handle Pointer to .Net type Type[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_makegenerictype", self.__pointer, typeArguments)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_makepointertype")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def MakePointerType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_makepointertype", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_makegenericsignaturetype")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def MakeGenericSignatureType(genericTypeDefinition: c_void_p, typeArguments: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        genericTypeDefinition: c_void_p
            GC Handle Pointer to .Net type Type
        
        typeArguments: c_void_p
            GC Handle Pointer to .Net type Type[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_makegenericsignaturetype", genericTypeDefinition, typeArguments)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_makegenericmethodparameter")
    __interop_func.restype = c_void_p
    @staticmethod
    def MakeGenericMethodParameter(position: int) -> c_void_p:
        """
        Parameters
        ----------
        
        position: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_makegenericmethodparameter", position)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_tostring")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def ToString(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("type_tostring", self.__pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_equals")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Equals(self, o: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        o: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_equals", self.__pointer, o)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_gethashcode")
    __interop_func.restype = ctypes.c_int
    __interop_func.argtypes = [c_void_p]
    def GetHashCode(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("type_gethashcode", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_equals2")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    def Equals2(self, o: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        o: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_equals2", self.__pointer, o)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_op_equality")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Equality(left: c_void_p, right: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        left: c_void_p
            GC Handle Pointer to .Net type Type
        
        right: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_op_equality", left, right)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_op_inequality")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Inequality(left: c_void_p, right: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        left: c_void_p
            GC Handle Pointer to .Net type Type
        
        right: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_op_inequality", left, right)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_reflectiononlygettype")
    __interop_func.restype = c_void_p
    @staticmethod
    def ReflectionOnlyGetType(typeName: str, throwIfNotFound: bool, ignoreCase: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        typeName: str
            Underlying .Net type is string
        
        throwIfNotFound: bool
            Underlying .Net type is Boolean
        
        ignoreCase: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        typeName_ptr = InteropUtils.utf8_to_ptr(typeName)
        throwIfNotFound_bool = 1 if throwIfNotFound else 0
        ignoreCase_bool = 1 if ignoreCase else 0
        
        result = InteropUtils.invoke("type_reflectiononlygettype", typeName_ptr, throwIfNotFound_bool, ignoreCase_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_isenumdefined")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    def IsEnumDefined(self, value: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_isenumdefined", self.__pointer, value)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_getenumname")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p, c_void_p]
    def GetEnumName(self, value: c_void_p) -> str:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("type_getenumname", self.__pointer, value)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_getenumnames")
    __interop_func.restype = c_void_p
    __interop_func.argtypes = [c_void_p]
    def GetEnumNames(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type string[]
        """
        result = InteropUtils.invoke("type_getenumnames", self.__pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isserializable")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsSerializable(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isserializable", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_containsgenericparameters")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_ContainsGenericParameters(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_containsgenericparameters", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_isvisible")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p]
    def get_IsVisible(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isvisible", self.__pointer)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_issubclassof")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    def IsSubclassOf(self, c: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        c: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_issubclassof", self.__pointer, c)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_isassignablefrom")
    __interop_func.restype = ctypes.c_ubyte
    __interop_func.argtypes = [c_void_p, c_void_p]
    def IsAssignableFrom(self, c: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        c: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_isassignablefrom", self.__pointer, c)
        return result
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_emptytypes")
    __interop_func.restype = c_void_p
    @staticmethod
    def get_EmptyTypes() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_get_emptytypes")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    __interop_func = InteropUtils.get_function("type_get_missing")
    __interop_func.restype = c_void_p
    @staticmethod
    def get_Missing() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Object
        """
        result = InteropUtils.invoke("type_get_missing")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
