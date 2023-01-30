import ctypes
from pyfie import _util


def is_x64():
    return ctypes.sizeof(ctypes.c_void_p) == 8


def ptr_inc(cty_ptr, n):
    return ctypes.cast(
        ctypes.byref(cty_ptr.contents, ctypes.sizeof(cty_ptr.contents) * n), cty_ptr.__class__)


def is_ptr(cty_obj):
    return isinstance(cty_obj, (ctypes.c_void_p, ctypes._Pointer))


def is_ptr_cls(cty_cls):
    return issubclass(cty_cls, (ctypes.c_void_p, ctypes._Pointer))


def is_same_ptr(cls1, cls2):
    """
    compare the referenced data type.
    """
    if issubclass(cls1, ctypes.c_void_p) and issubclass(cls2, ctypes.c_void_p):
        return True
    if not issubclass(cls1, ctypes._Pointer):
        return False
    if not issubclass(cls2, ctypes._Pointer):
        return False
    return cls1._type_ == cls2._type_


def is_same_size_ptr(cls1, cls2):
    """
    compare the size of referenced data type.
    """
    if not issubclass(cls1, ctypes._Pointer):
        return False
    if not issubclass(cls2, ctypes._Pointer):
        return False
    return ctypes.sizeof(cls1._type_) == ctypes.sizeof(cls2._type_)


def null_ptr(cty_obj):
    if isinstance(cty_obj, ctypes.c_void_p):
        cty_obj.value = None
        return

    if isinstance(cty_obj, ctypes._Pointer):
        ptr_storage = ctypes.c_longlong if is_x64() else ctypes.c_int
        cty_obj_ptr = ctypes.cast(ctypes.byref(
            cty_obj), ctypes.POINTER(ptr_storage))
        cty_obj_ptr.contents.value = 0
        return

    raise RuntimeError("{0} is not pointer.".format(cty_obj))


def get_str_encoding_for_fie():
    """Python 文字列をバイト列に変換するための FIE 用のエンコーディングを返す."""
    if _util.get_platform() == "Windows":
        # バージョン 3.5 の Windows 版 FIE ではマルチバイト文字セットが使用されている.
        return "mbcs"
    else:
        return "utf-8"


def convert_string(src_string, ctypes_cls):
    """
    Returns : instance of ctypes_cls (or None)
    """

    if isinstance(src_string, str):
        src_bytes = bytes(src_string, get_str_encoding_for_fie())
        ctypes_obj = ctypes.cast(src_bytes, ctypes_cls)
        ctypes_obj.ref_bytes = src_bytes  # avoid GC !!!
        return ctypes_obj

    if isinstance(src_string, bytes):
        ctypes_obj = ctypes.cast(src_string, ctypes_cls)
        return ctypes_obj

    return None


def serialize_compound_type(root_cls):
    elem_list = []

    if issubclass(root_cls, ctypes.Structure):
        for _, field_cls in root_cls._fields_:
            elem_list.extend(
                serialize_compound_type(field_cls)
            )
    elif issubclass(root_cls, ctypes.Array):
        elem_list.extend(
            serialize_compound_type(
                root_cls._type_) * root_cls._length_
        )
    else:
        elem_list.append(root_cls)

    return elem_list

def get_address_from_pycapsule(capsule):
    ctypes.pythonapi.PyCapsule_GetName.restype = ctypes.c_char_p
    ctypes.pythonapi.PyCapsule_GetName.argtypes = [ctypes.py_object]
    name = ctypes.pythonapi.PyCapsule_GetName(capsule)

    ctypes.pythonapi.PyCapsule_IsValid.restype = ctypes.c_int
    ctypes.pythonapi.PyCapsule_IsValid.argtypes = [ctypes.py_object, ctypes.c_char_p]
    is_valid = ctypes.pythonapi.PyCapsule_IsValid(capsule, name)
    if not is_valid:
        raise TypeError("Capsule is invalid")

    ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
    ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object, ctypes.c_char_p]
    return ctypes.pythonapi.PyCapsule_GetPointer(capsule, name)
