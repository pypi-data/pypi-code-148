from numba.core import cgutils, types
from numba.extending import NativeValue, box, make_attribute_wrapper, models, register_model, typeof_impl, unbox


def install_py_obj_class(types_name, module, python_type=None, class_name=
    None, model_name=None):
    class_name = ''.join(map(str.title, types_name.split('_'))
        ) if class_name is None else class_name
    model_name = f'{class_name}Model' if model_name is None else model_name
    djr__kipg = f'class {class_name}(types.Opaque):\n'
    djr__kipg += f'    def __init__(self):\n'
    djr__kipg += f"       types.Opaque.__init__(self, name='{class_name}')\n"
    djr__kipg += f'    def __reduce__(self):\n'
    djr__kipg += (
        f"        return (types.Opaque, ('{class_name}',), self.__dict__)\n")
    eysyq__vwbk = {}
    exec(djr__kipg, {'types': types, 'models': models}, eysyq__vwbk)
    fdiya__awv = eysyq__vwbk[class_name]
    setattr(module, class_name, fdiya__awv)
    class_instance = fdiya__awv()
    setattr(types, types_name, class_instance)
    djr__kipg = f'class {model_name}(models.StructModel):\n'
    djr__kipg += f'    def __init__(self, dmm, fe_type):\n'
    djr__kipg += f'        members = [\n'
    djr__kipg += (
        f"            ('meminfo', types.MemInfoPointer({types_name})),\n")
    djr__kipg += f"            ('pyobj', types.voidptr),\n"
    djr__kipg += f'        ]\n'
    djr__kipg += (
        f'        models.StructModel.__init__(self, dmm, fe_type, members)\n')
    exec(djr__kipg, {'types': types, 'models': models, types_name:
        class_instance}, eysyq__vwbk)
    hyqob__hguyk = eysyq__vwbk[model_name]
    setattr(module, model_name, hyqob__hguyk)
    register_model(fdiya__awv)(hyqob__hguyk)
    make_attribute_wrapper(fdiya__awv, 'pyobj', '_pyobj')
    if python_type is not None:
        typeof_impl.register(python_type)(lambda val, c: class_instance)
    unbox(fdiya__awv)(unbox_py_obj)
    box(fdiya__awv)(box_py_obj)
    return fdiya__awv


def box_py_obj(typ, val, c):
    uokoo__odgx = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    obj = uokoo__odgx.pyobj
    c.pyapi.incref(obj)
    c.context.nrt.decref(c.builder, typ, val)
    return obj


def unbox_py_obj(typ, obj, c):
    uokoo__odgx = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    uokoo__odgx.meminfo = c.pyapi.nrt_meminfo_new_from_pyobject(c.context.
        get_constant_null(types.voidptr), obj)
    uokoo__odgx.pyobj = obj
    return NativeValue(uokoo__odgx._getvalue())
