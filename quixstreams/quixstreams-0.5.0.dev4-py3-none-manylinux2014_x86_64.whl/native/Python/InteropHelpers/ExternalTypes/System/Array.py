# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

from typing import Any, Union, List
from ctypes import c_void_p
import ctypes
from ...InteropUtils import InteropUtils


class Array:
    __nullable_double = InteropUtils.create_nullable(ctypes.c_double)

    @staticmethod
    def ReadBlittables(array_uptr: ctypes.c_void_p, valuetype, valuemapper=None) -> []:
        """
        Reads blittable values starting from the array pointer using the specified type and mapper then frees the pointer
        
        :param array_uptr: Unmanaged memory pointer to the first element of the array.
        :param valuetype: Type of the value
        :param valuemapper: Conversion function for the value
        :return: The converted array to the given type using the mapper
        """
        if array_uptr is None:
            return None

        # c_void_p type is not getting correctly set for the object but others are
        if valuetype is c_void_p:
            if valuemapper is None:
                valuemapper = lambda x: c_void_p(x)
            else:
                original_valuemapper = valuemapper
                valuemapper = lambda x: original_valuemapper(c_void_p(x) if x is not None else None)

        try:
            # first 4 bytes contains the length as int
            length = int(ctypes.cast(array_uptr, ctypes.POINTER(ctypes.c_int32)).contents.value)
            if length == 0:
                return []

            ctypes_pointer = ctypes.cast(array_uptr.value + 4, ctypes.POINTER(valuetype))

            if valuemapper == None:
                return [ctypes_pointer[i] for i in range(length)]

            vals = [valuemapper(ctypes_pointer[i]) for i in range(length)]
            return vals
        finally:
            InteropUtils.free_uptr(array_uptr)

    @staticmethod
    def WriteBlittables(blittables: [any], valuetype, valuemapper=None) -> c_void_p:
        """
        Writes a list of blittables (like int) into unmanaged memory, returning a pointer to the array, where first 4 bytes is the length
        """

        if blittables is None:
            return None

        blit_len = len(blittables)
        if blit_len == 0:
            buffer_uptr = InteropUtils.allocate_uptr(4)
        else:

            if valuemapper is not None:
                blittables = [valuemapper(i) for i in blittables]


            arr = (valuetype * blit_len)(*blittables)
            #bytes = bytearray(4 + ctypes.sizeof(valuetype) * len(blittables))

            arrsize = ctypes.sizeof(valuetype) * blit_len
            buffer_uptr = InteropUtils.allocate_uptr(4 + arrsize)

            ctypes.memmove(buffer_uptr.value + 4, arr, arrsize)
        size_bytes = ctypes.c_int32.from_address(buffer_uptr.value)
        size_bytes.value = blit_len
        return buffer_uptr

    @staticmethod
    def ReadLongs(array_uptr: ctypes.c_void_p) -> [int]:
        """
        Reads from unmanaged memory, returning list of long (int64[])
        """
        return Array.ReadBlittables(array_uptr, ctypes.c_int64)

    @staticmethod
    def WriteLongs(longs: [any]) -> c_void_p:
        """
        Writes a list of long (int64[]) into unmanaged memory, returning a pointer to the array, where first 4 bytes is the length
        """

        return Array.WriteBlittables(longs, ctypes.c_int64)

    @staticmethod
    def ReadLongsArray(array_hptr: ctypes.c_void_p) -> [[int]]:
        """
        Reads from unmanaged memory, returning list of long sets (int64[][])
        """
        inter_arrays = Array.ReadReferences(array_hptr)

        return [Array.ReadLongs(inter_array) for inter_array in inter_arrays]

    @staticmethod
    def WriteLongsArray(longs: [any]) -> c_void_p:
        """
        Writes an array of long sets (int64[][]) into unmanaged memory, returning a pointer to the array, where first 4 bytes is the length
        """

        return Array.WriteBlittables(longs, ctypes.c_void_p, Array.WriteLongs)

    @staticmethod
    def ReadStrings(array_uptr: ctypes.c_void_p) -> [str]:
        """
        Reads from unmanaged memory, returning list of strings (str[])
        """
        return Array.ReadBlittables(array_uptr, ctypes.c_void_p, lambda x: InteropUtils.uptr_to_utf8(x))

    @staticmethod
    def WriteStrings(strings: [any]) -> c_void_p:
        """
        Writes a list of strings into unmanaged memory, returning a pointer to the array, where first 4 bytes is the length
        """

        return Array.WriteBlittables(strings, ctypes.c_void_p, lambda x: InteropUtils.utf8_to_uptr(x))

    @staticmethod
    def ReadDoubles(array_uptr: ctypes.c_void_p) -> [float]:
        """
        Reads from unmanaged memory, returning list of doubles (float[])
        """
        return Array.ReadBlittables(array_uptr, ctypes.c_double)

    @staticmethod
    def WriteDoubles(doubles: [any]) -> c_void_p:
        """
        Writes a list of doubles into unmanaged memory, returning a pointer to the array, where first 4 bytes is the length
        """

        return Array.WriteBlittables(doubles, ctypes.c_double)

    @staticmethod
    def WriteDoublesArray(doubles: [any]) -> c_void_p:
        """
        Writes an array of long sets (float[][]) into unmanaged memory, returning a pointer to the array, where first 4 bytes is the length
        """

        return Array.WriteBlittables(doubles, ctypes.c_void_p, Array.WriteDoubles)


    @staticmethod
    def ReadNullables(array_uptr: ctypes.c_void_p, nullable_type) -> [Any]:
        """
        Parameters
        ----------

        array_ptr: c_void_p
            Pointer to .Net nullable array.

        nullable_type:
            nullable type created by InteropUtils.create_nullable

        Returns
        -------
        []:
           array of underlying type with possible None values
        """

        nullables = Array.ReadBlittables(array_uptr, nullable_type)

        result = []
        for nullable in nullables:
            if nullable.HasValue:
                result.append(nullable.Value)
            else:
                result.append(None)
        return result

    @staticmethod
    def ReadNullableDoubles(array_uptr: ctypes.c_void_p) -> [float]:
        """
        Reads from unmanaged memory, returning list of double (double[]) with None where had no value
        """
        return Array.ReadNullables(array_uptr, Array.__nullable_double)

    @staticmethod
    def WriteNullableDoubles(doubles: [float]) -> c_void_p:
        """
        Writes a list of nullable doubles into unmanaged memory, returning a pointer to the array, where first 4 bytes is the length
        """

        return Array.WriteBlittables(doubles, Array.__nullable_double, lambda x: Array.__nullable_double(x))

    @staticmethod
    def ReadReferences(pointers: [c_void_p]) -> c_void_p:
        """
        Reads from unmanaged memory, returning list of pointers (c_void[])
        """

        return Array.ReadBlittables(pointers, ctypes.c_void_p)

    @staticmethod
    def WriteReferences(pointers: [c_void_p]) -> c_void_p:
        """
        Writes a list of pointers into unmanaged memory, returning a pointer to the array, where first 4 bytes is the length
        """

        return Array.WriteBlittables(pointers, ctypes.c_void_p)

    @staticmethod
    def ReadBytes(array_uptr: ctypes.c_void_p) -> bytes:
        """
        Reads from unmanaged memory, returning bytes (byte[])
        """
        return bytes(Array.ReadBlittables(array_uptr, ctypes.c_ubyte))

    @staticmethod
    def WriteBytes(bytesval: Union[bytes, bytearray]) -> c_void_p:
        """
        Writes a set of bytes (byte[]) into unmanaged memory, returning a pointer to the array, where first 4 bytes is the length
        """

        return Array.WriteBlittables(bytesval, ctypes.c_ubyte)

    @staticmethod
    def ReadByteArrays(array_uptr: ctypes.c_void_p) -> [bytes]:
        """
        Reads from unmanaged memory, returning array of byte sets (byte[][])
        """
        return Array.ReadBlittables(array_uptr, ctypes.c_void_p, Array.ReadBytes)

    @staticmethod
    def WriteByteArrays(bytes_array: Union[List[bytes], List[bytearray]]) -> c_void_p:
        """
        Writes an array of byte sets (byte[][]) into unmanaged memory, returning a pointer to the array, where first 4 bytes is the length
        """

        return Array.WriteBlittables(bytes_array, ctypes.c_void_p, Array.WriteBytes)
