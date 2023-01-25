# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

from typing import Any, Dict, List
from ctypes import c_void_p, c_int, c_long, POINTER, c_bool
import ctypes
from ...InteropUtils import InteropUtils
from .Array import Array


class Dictionary:

    # ctypes function return type//parameter fix
    interop_func = InteropUtils.get_function("dictionary_constructor_string_string")
    interop_func.argtypes = []
    interop_func.restype = c_void_p
    @staticmethod
    def ConstructorForStringString() -> c_void_p:
        ptr = InteropUtils.invoke("dictionary_constructor_string_string")
        return c_void_p(ptr) if ptr is not None else None

    # ctypes function return type//parameter fix
    interop_func = InteropUtils.get_function("dictionary_get_value")
    interop_func.argtypes = [c_void_p, c_void_p]
    interop_func.restype = c_void_p
    @staticmethod
    def GetValue(dictionary_hptr: c_void_p, key_hptr: c_void_p) -> Any:
        ptr = InteropUtils.invoke("dictionary_get_value", dictionary_hptr, key_hptr)
        return c_void_p(ptr) if ptr is not None else None
        
    # ctypes function return type//parameter fix
    interop_func = InteropUtils.get_function("dictionary_set_value")
    interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def SetValue(dictionary_hptr: c_void_p, key_hptr: c_void_p, value_hptr: c_void_p) -> None:
        InteropUtils.invoke("dictionary_set_value", dictionary_hptr, key_hptr, value_hptr)
        
    # ctypes function return type//parameter fix
    interop_func = InteropUtils.get_function("dictionary_contains")
    interop_func.argtypes = [c_void_p, c_void_p]
    interop_func.restype = c_bool
    @staticmethod
    def Contains(dictionary_hptr: c_void_p, key_hptr: c_void_p) -> bool:
        return InteropUtils.invoke("dictionary_contains", dictionary_hptr, key_hptr)
        
    # ctypes function return type//parameter fix
    interop_func = InteropUtils.get_function("dictionary_clear")
    interop_func.argtypes = [c_void_p]
    @staticmethod
    def Clear(dictionary_hptr: c_void_p) -> None:
        InteropUtils.invoke("dictionary_clear", dictionary_hptr)
        
    # ctypes function return type//parameter fix
    interop_func = InteropUtils.get_function("dictionary_remove")
    interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Remove(dictionary_hptr: c_void_p, key_hptr: c_void_p) -> None:
        InteropUtils.invoke("dictionary_remove", dictionary_hptr, key_hptr)
        
    # ctypes function return type//parameter fix
    interop_func = InteropUtils.get_function("dictionary_get_count")
    interop_func.argtypes = [c_void_p]
    interop_func.restype = c_int
    @staticmethod
    def GetCount(dictionary_hptr: c_void_p) -> int:
        return InteropUtils.invoke("dictionary_get_count", dictionary_hptr)

    # ctypes function return type//parameter fix
    interop_func = InteropUtils.get_function("dictionary_get_keys")
    interop_func.argtypes = [c_void_p]
    interop_func.restype = c_void_p
    @staticmethod
    def GetKeys(dictionary_hptr: c_void_p) -> c_void_p:
        ptr = InteropUtils.invoke("dictionary_get_keys", dictionary_hptr)
        return c_void_p(ptr) if ptr is not None else None

    # ctypes function return type//parameter fix
    interop_func = InteropUtils.get_function("dictionary_get_values")
    interop_func.argtypes = [c_void_p]
    interop_func.restype = c_void_p
    @staticmethod
    def GetValues(dictionary_hptr: c_void_p) -> c_void_p:
        ptr = InteropUtils.invoke("dictionary_get_values", dictionary_hptr)
        return c_void_p(ptr) if ptr is not None else None

    @staticmethod
    def ReadStringStringDictionary(dictionary_hptr: c_void_p) -> Dict[str, str]:
        keys_uptr = Dictionary.GetKeys(dictionary_hptr)
        keys = Array.ReadStrings(keys_uptr)

        values_uptr = Dictionary.GetValues(dictionary_hptr)
        values = Array.ReadStrings(values_uptr)

        dic = {}
        for index, key in enumerate(keys):
            dic[key] = values[index]

        return dic


    @staticmethod
    def ReadStringReferenceDictionary(dictionary_hptr: c_void_p) -> Dict[str, c_void_p]:
        keys_uptr = Dictionary.GetKeys(dictionary_hptr)
        keys = Array.ReadStrings(keys_uptr)

        values_uptr = Dictionary.GetValues(dictionary_hptr)
        values = Array.ReadReferences(values_uptr)

        dic = {}
        for index, key in enumerate(keys):
            dic[key] = values[index]

        return dic


    # ctypes function return type//parameter fix
    interop_func = InteropUtils.get_function("dictionary_read_string_longarray_dictionary")
    interop_func.argtypes = [c_void_p]
    interop_func.restype = c_void_p
    @staticmethod
    def ReadStringLongArrayDictionary(dictionary_hptr: c_void_p) -> Dict[str, List[int]]:

        uptr = InteropUtils.invoke("dictionary_read_string_longarray_dictionary", dictionary_hptr)
        uptr = c_void_p(uptr) if uptr is not None else None

        result = Dictionary.ReadGenericDictionary(uptr,
                                                 c_void_p,  # key type (pointer to str)
                                                 lambda x: InteropUtils.uptr_to_utf8(x),  # key callback
                                                 c_void_p,  # value type (pointer to long[])
                                                 lambda x: Array.ReadBlittables(ctypes.c_int64)  # value callback
                                                 )
        return result

    interop_func = InteropUtils.get_function("dictionary_read_string_bytearray2_dictionary")
    interop_func.argtypes = [c_void_p]
    interop_func.restype = c_void_p
    @staticmethod
    def ReadStringByteArray2Dictionary(dictionary_hptr: c_void_p) -> Dict[str, List[bytes]]:

        uptr = InteropUtils.invoke("dictionary_read_string_bytearray2_dictionary", dictionary_hptr)
        uptr = c_void_p(uptr) if uptr is not None else None

        def UPtrToUPtr(interim_uptr):
            return Array.ReadBlittables(interim_uptr, c_void_p, UPtrToBytes)

        def UPtrToBytes(interim_uptr):
            # doesn't need to be modifyable, so bytes is enough
            return bytes(Array.ReadBlittables(interim_uptr, ctypes.c_ubyte))

        result = Dictionary.ReadGenericDictionary(uptr,
                                                 c_void_p,  # key type (pointer to str)
                                                 lambda x: InteropUtils.uptr_to_utf8(x),  # key callback
                                                 c_void_p,  # value type (pointer to long[])
                                                 lambda x: UPtrToUPtr(x)  # value callback
                                                 )
        return result

    # ctypes function return type//parameter fix
    interop_func = InteropUtils.get_function("dictionary_read_string_stringarray_dictionary")
    interop_func.argtypes = [c_void_p]
    interop_func.restype = c_void_p
    @staticmethod
    def ReadStringStringArrayDictionary(dictionary_hptr: c_void_p) -> Dict[str, List[str]]:

        uptr = InteropUtils.invoke("dictionary_read_string_stringarray_dictionary", dictionary_hptr)
        uptr = c_void_p(uptr) if uptr is not None else None

        result = Dictionary.ReadGenericDictionary(uptr,
                                                 c_void_p,  # key type (pointer to str)
                                                 lambda x: InteropUtils.uptr_to_utf8(x),  # key callback
                                                 c_void_p,  # value type (pointer to str[])
                                                 lambda x: Array.ReadBlittables(x, ctypes.c_void_p, InteropUtils.uptr_to_utf8)  # value callback
                                                 )
        return result

    # ctypes function return type//parameter fix
    interop_func = InteropUtils.get_function("dictionary_read_string_nullabledoublearray_dictionary")
    interop_func.argtypes = [c_void_p]
    interop_func.restype = c_void_p
    @staticmethod
    def ReadStringNullableDoubleArrayDictionary(dictionary_hptr: c_void_p) -> Dict[str, List[float]]:

        uptr = InteropUtils.invoke("dictionary_read_string_nullabledoublearray_dictionary", dictionary_hptr)
        uptr = c_void_p(uptr) if uptr is not None else None

        result = Dictionary.ReadGenericDictionary(uptr,
                                                 c_void_p,  # key type (pointer to str)
                                                 lambda x: InteropUtils.uptr_to_utf8(x),  # key callback
                                                 c_void_p,  # value type (pointer to double[])
                                                 lambda x: Array.ReadNullableDoubles(x)  # value callback
                                                 )
        return result


    # ctypes function return type//parameter fix
    interop_func = InteropUtils.get_function("dictionary_read_any")
    interop_func.argtypes = [c_void_p]
    interop_func.restype = c_void_p
    @staticmethod
    def ReadAny(dictionary_hptr: c_void_p) -> c_void_p:
        """
        Read any dictionary that implement IEnumerable<KeyValuePair<,>>. Useful for dictionaries
        that do not implement IDictionary, such as ReadOnlyDictionary
        :param dictionary_hptr: Handler pointer to a dictionary 
        :return: Pointer to array with elements [c_void_p, c_void_p] where first is the key array, 2nd is the value array
        """
        uptr = InteropUtils.invoke("dictionary_read_any", dictionary_hptr)
        return c_void_p(uptr) if uptr is not None else None

    @staticmethod
    def ReadAnyStringReferenceDictionary(dictionary_hptr: c_void_p, value_callback) -> Dict[str, Any]:
        """
        Read any dictionary that implements IEnumerable<KeyValuePair<string,object>>. Useful for dictionaries
        that do not implement IDictionary, such as ReadOnlyDictionary
        :param dictionary_hptr: Handler pointer to a dictionary 
        :return: Dictionary of [str, c_void_p]
        """

        uptr = Dictionary.ReadAny(dictionary_hptr)

        result = Dictionary.ReadGenericDictionary(uptr,
                                                 c_void_p,  # key type (pointer to str)
                                                 lambda x: InteropUtils.uptr_to_utf8(x),  # key callback
                                                 c_void_p,  # value type (pointer to reference type)
                                                 lambda x: value_callback(x) if x is not None else None  # value callback
                                                 )
        return result

    @staticmethod
    def ReadAnyStringStringDictionary(dictionary_hptr: c_void_p) -> Dict[str, str]:
        """
        Read any dictionary that implements IEnumerable<KeyValuePair<string,string>>. Useful for dictionaries
        that do not implement IDictionary, such as ReadOnlyDictionary
        :param dictionary_hptr: Handler pointer to a dictionary 
        :return: Dictionary of [str, str]
        """

        uptr = Dictionary.ReadAny(dictionary_hptr)

        result = Dictionary.ReadGenericDictionary(uptr,
                                                 c_void_p,  # key type (pointer to str)
                                                 lambda x: InteropUtils.uptr_to_utf8(x),  # key callback
                                                 c_void_p,  # value type (pointer to reference type)
                                                 lambda x: InteropUtils.uptr_to_utf8(x),  # value callback
                                                 )
        return result

    @staticmethod
    def ReadGenericDictionary(read_dictionary_uptr: c_void_p, key_type, key_callback, value_type, value_callback) -> Dict[Any, Any]:
        """
        Reads read_dictionary_hptr as a pointer to an array of pointers with length of 2. First pointer is to the keys, send is to the values
        read_dictionary_uptr will be freed as a side-effect
        
        :param read_dictionary_hptr: 
        :param key_type: The type of the key, such as c_void_p
        :param key_callback: Key conversion callback, if any
        :param value_type: The type of the value, such as c_void_p
        :param value_callback: Value conversion callback, if any
        :return: Parsed dictionary of the provided types
        """


        array_uptrs = Array.ReadBlittables(read_dictionary_uptr, c_void_p)  # known length of 2

        keys_uptr = array_uptrs[0]
        keys_array = Array.ReadBlittables(keys_uptr, key_type, key_callback)

        values_uptr = array_uptrs[1]
        values_array = Array.ReadBlittables(values_uptr, value_type, value_callback)

        dict_len = len(keys_array)  # same as values array length, so either works

        result = {}
        for i in range(dict_len):
            result[keys_array[i]] = values_array[i]

        return result
                
    # ctypes function return type//parameter fix
    interop_func = InteropUtils.get_function("dictionary_get_test")
    interop_func.argtypes = []
    interop_func.restype = c_void_p
    @staticmethod
    def GetTest() -> c_void_p:
        ptr = InteropUtils.invoke("dictionary_get_test")
        return c_void_p(ptr) if ptr is not None else None


    interop_func = InteropUtils.get_function("dictionary_get_test2")
    interop_func.argtypes = []
    interop_func.restype = c_void_p
    @staticmethod
    def GetTest2() -> c_void_p:
        ptr = InteropUtils.invoke("dictionary_get_test2")
        return c_void_p(ptr) if ptr is not None else None

    interop_func = InteropUtils.get_function("dictionary_get_test3")
    interop_func.argtypes = []
    interop_func.restype = c_void_p
    @staticmethod
    def GetTest3() -> c_void_p:
        ptr = InteropUtils.invoke("dictionary_get_test3")
        return c_void_p(ptr) if ptr is not None else None

    interop_func = InteropUtils.get_function("dictionary_get_test4")
    interop_func.argtypes = []
    interop_func.restype = c_void_p
    @staticmethod
    def GetTest4() -> c_void_p:
        ptr = InteropUtils.invoke("dictionary_get_test4")
        return c_void_p(ptr) if ptr is not None else None