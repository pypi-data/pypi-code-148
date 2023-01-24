"""
Wrapper class for Tuples that supports tracking null entries.
This is primarily used for maintaining null information for
Series values used in df.apply
"""
import operator
import numba
from numba.core import cgutils, types
from numba.extending import box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_method, register_model


class NullableTupleType(types.IterableType):

    def __init__(self, tuple_typ, null_typ):
        self._tuple_typ = tuple_typ
        self._null_typ = null_typ
        super(NullableTupleType, self).__init__(name=
            f'NullableTupleType({tuple_typ}, {null_typ})')

    @property
    def tuple_typ(self):
        return self._tuple_typ

    @property
    def null_typ(self):
        return self._null_typ

    def __getitem__(self, i):
        return self._tuple_typ[i]

    @property
    def key(self):
        return self._tuple_typ

    @property
    def dtype(self):
        return self.tuple_typ.dtype

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    @property
    def iterator_type(self):
        return self.tuple_typ.iterator_type

    def __len__(self):
        return len(self.tuple_typ)


@register_model(NullableTupleType)
class NullableTupleModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yqtq__kyap = [('data', fe_type.tuple_typ), ('null_values', fe_type.
            null_typ)]
        super(NullableTupleModel, self).__init__(dmm, fe_type, yqtq__kyap)


make_attribute_wrapper(NullableTupleType, 'data', '_data')
make_attribute_wrapper(NullableTupleType, 'null_values', '_null_values')


@intrinsic
def build_nullable_tuple(typingctx, data_tuple, null_values):
    assert isinstance(data_tuple, types.BaseTuple
        ), "build_nullable_tuple 'data_tuple' argument must be a tuple"
    assert isinstance(null_values, types.BaseTuple
        ), "build_nullable_tuple 'null_values' argument must be a tuple"
    data_tuple = types.unliteral(data_tuple)
    null_values = types.unliteral(null_values)

    def codegen(context, builder, signature, args):
        data_tuple, null_values = args
        pvozv__dspkr = cgutils.create_struct_proxy(signature.return_type)(
            context, builder)
        pvozv__dspkr.data = data_tuple
        pvozv__dspkr.null_values = null_values
        context.nrt.incref(builder, signature.args[0], data_tuple)
        context.nrt.incref(builder, signature.args[1], null_values)
        return pvozv__dspkr._getvalue()
    sig = NullableTupleType(data_tuple, null_values)(data_tuple, null_values)
    return sig, codegen


@box(NullableTupleType)
def box_nullable_tuple(typ, val, c):
    gvxn__grvof = cgutils.create_struct_proxy(typ)(c.context, c.builder,
        value=val)
    c.context.nrt.incref(c.builder, typ.tuple_typ, gvxn__grvof.data)
    c.context.nrt.incref(c.builder, typ.null_typ, gvxn__grvof.null_values)
    ulrlv__hkxvk = c.pyapi.from_native_value(typ.tuple_typ, gvxn__grvof.
        data, c.env_manager)
    wjh__xbc = c.pyapi.from_native_value(typ.null_typ, gvxn__grvof.
        null_values, c.env_manager)
    vthuw__ftvp = c.context.get_constant(types.int64, len(typ.tuple_typ))
    frr__xhcev = c.pyapi.list_new(vthuw__ftvp)
    with cgutils.for_range(c.builder, vthuw__ftvp) as ibq__omvt:
        i = ibq__omvt.index
        bcscd__ctrs = c.pyapi.long_from_longlong(i)
        itpc__fpl = c.pyapi.object_getitem(wjh__xbc, bcscd__ctrs)
        tlxj__rud = c.pyapi.to_native_value(types.bool_, itpc__fpl).value
        with c.builder.if_else(tlxj__rud) as (uinr__wes, feru__jovku):
            with uinr__wes:
                c.pyapi.list_setitem(frr__xhcev, i, c.pyapi.make_none())
            with feru__jovku:
                ddh__udpz = c.pyapi.object_getitem(ulrlv__hkxvk, bcscd__ctrs)
                c.pyapi.list_setitem(frr__xhcev, i, ddh__udpz)
        c.pyapi.decref(bcscd__ctrs)
        c.pyapi.decref(itpc__fpl)
    adp__issl = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    rce__mds = c.pyapi.call_function_objargs(adp__issl, (frr__xhcev,))
    c.pyapi.decref(ulrlv__hkxvk)
    c.pyapi.decref(wjh__xbc)
    c.pyapi.decref(adp__issl)
    c.pyapi.decref(frr__xhcev)
    c.context.nrt.decref(c.builder, typ, val)
    return rce__mds


@overload(operator.getitem)
def overload_getitem(A, idx):
    if not isinstance(A, NullableTupleType):
        return
    return lambda A, idx: A._data[idx]


@overload(len)
def overload_len(A):
    if not isinstance(A, NullableTupleType):
        return
    return lambda A: len(A._data)


@lower_builtin('getiter', NullableTupleType)
def nullable_tuple_getiter(context, builder, sig, args):
    pvozv__dspkr = cgutils.create_struct_proxy(sig.args[0])(context,
        builder, value=args[0])
    impl = context.get_function('getiter', sig.return_type(sig.args[0].
        tuple_typ))
    return impl(builder, (pvozv__dspkr.data,))


@overload(operator.eq)
def nullable_tuple_eq(val1, val2):
    if not isinstance(val1, NullableTupleType) or not isinstance(val2,
        NullableTupleType):
        return
    if val1 != val2:
        return lambda val1, val2: False
    yxx__cfrsw = 'def impl(val1, val2):\n'
    yxx__cfrsw += '    data_tup1 = val1._data\n'
    yxx__cfrsw += '    null_tup1 = val1._null_values\n'
    yxx__cfrsw += '    data_tup2 = val2._data\n'
    yxx__cfrsw += '    null_tup2 = val2._null_values\n'
    xasyg__utbk = val1._tuple_typ
    for i in range(len(xasyg__utbk)):
        yxx__cfrsw += f'    null1_{i} = null_tup1[{i}]\n'
        yxx__cfrsw += f'    null2_{i} = null_tup2[{i}]\n'
        yxx__cfrsw += f'    data1_{i} = data_tup1[{i}]\n'
        yxx__cfrsw += f'    data2_{i} = data_tup2[{i}]\n'
        yxx__cfrsw += f'    if null1_{i} != null2_{i}:\n'
        yxx__cfrsw += '        return False\n'
        yxx__cfrsw += f'    if null1_{i} and (data1_{i} != data2_{i}):\n'
        yxx__cfrsw += f'        return False\n'
    yxx__cfrsw += f'    return True\n'
    zrt__ocre = {}
    exec(yxx__cfrsw, {}, zrt__ocre)
    impl = zrt__ocre['impl']
    return impl


@overload_method(NullableTupleType, '__hash__')
def nullable_tuple_hash(val):

    def impl(val):
        return _nullable_tuple_hash(val)
    return impl


_PyHASH_XXPRIME_1 = numba.cpython.hashing._PyHASH_XXPRIME_1
_PyHASH_XXPRIME_2 = numba.cpython.hashing._PyHASH_XXPRIME_1
_PyHASH_XXPRIME_5 = numba.cpython.hashing._PyHASH_XXPRIME_1


@numba.generated_jit(nopython=True)
def _nullable_tuple_hash(nullable_tup):
    yxx__cfrsw = 'def impl(nullable_tup):\n'
    yxx__cfrsw += '    data_tup = nullable_tup._data\n'
    yxx__cfrsw += '    null_tup = nullable_tup._null_values\n'
    yxx__cfrsw += '    tl = numba.cpython.hashing._Py_uhash_t(len(data_tup))\n'
    yxx__cfrsw += '    acc = _PyHASH_XXPRIME_5\n'
    xasyg__utbk = nullable_tup._tuple_typ
    for i in range(len(xasyg__utbk)):
        yxx__cfrsw += f'    null_val_{i} = null_tup[{i}]\n'
        yxx__cfrsw += f'    null_lane_{i} = hash(null_val_{i})\n'
        yxx__cfrsw += (
            f'    if null_lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n'
            )
        yxx__cfrsw += '        return -1\n'
        yxx__cfrsw += f'    acc += null_lane_{i} * _PyHASH_XXPRIME_2\n'
        yxx__cfrsw += '    acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n'
        yxx__cfrsw += '    acc *= _PyHASH_XXPRIME_1\n'
        yxx__cfrsw += f'    if not null_val_{i}:\n'
        yxx__cfrsw += f'        lane_{i} = hash(data_tup[{i}])\n'
        yxx__cfrsw += (
            f'        if lane_{i} == numba.cpython.hashing._Py_uhash_t(-1):\n')
        yxx__cfrsw += f'            return -1\n'
        yxx__cfrsw += f'        acc += lane_{i} * _PyHASH_XXPRIME_2\n'
        yxx__cfrsw += (
            '        acc = numba.cpython.hashing._PyHASH_XXROTATE(acc)\n')
        yxx__cfrsw += '        acc *= _PyHASH_XXPRIME_1\n'
    yxx__cfrsw += """    acc += tl ^ (_PyHASH_XXPRIME_5 ^ numba.cpython.hashing._Py_uhash_t(3527539))
"""
    yxx__cfrsw += '    if acc == numba.cpython.hashing._Py_uhash_t(-1):\n'
    yxx__cfrsw += (
        '        return numba.cpython.hashing.process_return(1546275796)\n')
    yxx__cfrsw += '    return numba.cpython.hashing.process_return(acc)\n'
    zrt__ocre = {}
    exec(yxx__cfrsw, {'numba': numba, '_PyHASH_XXPRIME_1':
        _PyHASH_XXPRIME_1, '_PyHASH_XXPRIME_2': _PyHASH_XXPRIME_2,
        '_PyHASH_XXPRIME_5': _PyHASH_XXPRIME_5}, zrt__ocre)
    impl = zrt__ocre['impl']
    return impl
