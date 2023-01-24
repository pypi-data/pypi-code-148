import operator
import re
import llvmlite.binding as ll
import numba
import numpy as np
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, bound_function, infer_getattr, infer_global, signature
from numba.extending import intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, register_jitable, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.libs import hstr_ext
from bodo.utils.typing import BodoError, get_overload_const_int, get_overload_const_str, is_overload_constant_int, is_overload_constant_str


def unliteral_all(args):
    return tuple(types.unliteral(a) for a in args)


ll.add_symbol('del_str', hstr_ext.del_str)
ll.add_symbol('unicode_to_utf8', hstr_ext.unicode_to_utf8)
ll.add_symbol('memcmp', hstr_ext.memcmp)
ll.add_symbol('int_to_hex', hstr_ext.int_to_hex)
string_type = types.unicode_type


@numba.njit
def contains_regex(e, in_str):
    with numba.objmode(res='bool_'):
        res = bool(e.search(in_str))
    return res


@numba.generated_jit
def str_findall_count(regex, in_str):

    def _str_findall_count_impl(regex, in_str):
        with numba.objmode(res='int64'):
            res = len(regex.findall(in_str))
        return res
    return _str_findall_count_impl


utf8_str_type = types.ArrayCTypes(types.Array(types.uint8, 1, 'C'))


@intrinsic
def unicode_to_utf8_and_len(typingctx, str_typ):
    assert str_typ in (string_type, types.Optional(string_type)) or isinstance(
        str_typ, types.StringLiteral)
    zztf__gdy = types.Tuple([utf8_str_type, types.int64])

    def codegen(context, builder, sig, args):
        zin__wegyu, = args
        tjf__ejmtf = cgutils.create_struct_proxy(string_type)(context,
            builder, value=zin__wegyu)
        afzg__elwrp = cgutils.create_struct_proxy(utf8_str_type)(context,
            builder)
        wcs__xhve = cgutils.create_struct_proxy(zztf__gdy)(context, builder)
        is_ascii = builder.icmp_unsigned('==', tjf__ejmtf.is_ascii, lir.
            Constant(tjf__ejmtf.is_ascii.type, 1))
        with builder.if_else(is_ascii) as (ymvf__cdc, tpy__woghu):
            with ymvf__cdc:
                context.nrt.incref(builder, string_type, zin__wegyu)
                afzg__elwrp.data = tjf__ejmtf.data
                afzg__elwrp.meminfo = tjf__ejmtf.meminfo
                wcs__xhve.f1 = tjf__ejmtf.length
            with tpy__woghu:
                ezwig__qjv = lir.FunctionType(lir.IntType(64), [lir.IntType
                    (8).as_pointer(), lir.IntType(8).as_pointer(), lir.
                    IntType(64), lir.IntType(32)])
                rymol__zjmx = cgutils.get_or_insert_function(builder.module,
                    ezwig__qjv, name='unicode_to_utf8')
                hsoeh__vohlt = context.get_constant_null(types.voidptr)
                qxu__vlry = builder.call(rymol__zjmx, [hsoeh__vohlt,
                    tjf__ejmtf.data, tjf__ejmtf.length, tjf__ejmtf.kind])
                wcs__xhve.f1 = qxu__vlry
                lsshv__hkl = builder.add(qxu__vlry, lir.Constant(lir.
                    IntType(64), 1))
                afzg__elwrp.meminfo = context.nrt.meminfo_alloc_aligned(builder
                    , size=lsshv__hkl, align=32)
                afzg__elwrp.data = context.nrt.meminfo_data(builder,
                    afzg__elwrp.meminfo)
                builder.call(rymol__zjmx, [afzg__elwrp.data, tjf__ejmtf.
                    data, tjf__ejmtf.length, tjf__ejmtf.kind])
                builder.store(lir.Constant(lir.IntType(8), 0), builder.gep(
                    afzg__elwrp.data, [qxu__vlry]))
        wcs__xhve.f0 = afzg__elwrp._getvalue()
        return wcs__xhve._getvalue()
    return zztf__gdy(string_type), codegen


def unicode_to_utf8(s):
    return s


@overload(unicode_to_utf8)
def overload_unicode_to_utf8(s):
    return lambda s: unicode_to_utf8_and_len(s)[0]


def unicode_to_utf8_len(s):
    return s


@overload(unicode_to_utf8_len)
def overload_unicode_to_utf8_len(s):
    return lambda s: unicode_to_utf8_and_len(s)[1]


@overload(max)
def overload_builtin_max(lhs, rhs):
    if lhs == types.unicode_type and rhs == types.unicode_type:

        def impl(lhs, rhs):
            return lhs if lhs > rhs else rhs
        return impl


@overload(min)
def overload_builtin_min(lhs, rhs):
    if lhs == types.unicode_type and rhs == types.unicode_type:

        def impl(lhs, rhs):
            return lhs if lhs < rhs else rhs
        return impl


@intrinsic
def memcmp(typingctx, dest_t, src_t, count_t=None):

    def codegen(context, builder, sig, args):
        ezwig__qjv = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(64)])
        szak__erk = cgutils.get_or_insert_function(builder.module,
            ezwig__qjv, name='memcmp')
        return builder.call(szak__erk, args)
    return types.int32(types.voidptr, types.voidptr, types.intp), codegen


def int_to_str_len(n):
    return len(str(n))


@overload(int_to_str_len)
def overload_int_to_str_len(n):
    ohdil__ljxn = n(10)

    def impl(n):
        if n == 0:
            return 1
        yzkda__xkzn = 0
        if n < 0:
            n = -n
            yzkda__xkzn += 1
        while n > 0:
            n = n // ohdil__ljxn
            yzkda__xkzn += 1
        return yzkda__xkzn
    return impl


class StdStringType(types.Opaque):

    def __init__(self):
        super(StdStringType, self).__init__(name='StdStringType')


std_str_type = StdStringType()
register_model(StdStringType)(models.OpaqueModel)
del_str = types.ExternalFunction('del_str', types.void(std_str_type))
get_c_str = types.ExternalFunction('get_c_str', types.voidptr(std_str_type))
dummy_use = numba.njit(lambda a: None)


@overload(int)
def int_str_overload(in_str, base=10):
    if in_str == string_type:
        if is_overload_constant_int(base) and get_overload_const_int(base
            ) == 10:

            def _str_to_int_impl(in_str, base=10):
                val = _str_to_int64(in_str._data, in_str._length)
                dummy_use(in_str)
                return val
            return _str_to_int_impl

        def _str_to_int_base_impl(in_str, base=10):
            val = _str_to_int64_base(in_str._data, in_str._length, base)
            dummy_use(in_str)
            return val
        return _str_to_int_base_impl


@infer_global(float)
class StrToFloat(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        [ufas__pyzwc] = args
        if isinstance(ufas__pyzwc, StdStringType):
            return signature(types.float64, ufas__pyzwc)
        if ufas__pyzwc == string_type:
            return signature(types.float64, ufas__pyzwc)


ll.add_symbol('init_string_const', hstr_ext.init_string_const)
ll.add_symbol('get_c_str', hstr_ext.get_c_str)
ll.add_symbol('str_to_int64', hstr_ext.str_to_int64)
ll.add_symbol('str_to_uint64', hstr_ext.str_to_uint64)
ll.add_symbol('str_to_int64_base', hstr_ext.str_to_int64_base)
ll.add_symbol('str_to_float64', hstr_ext.str_to_float64)
ll.add_symbol('str_to_float32', hstr_ext.str_to_float32)
ll.add_symbol('get_str_len', hstr_ext.get_str_len)
ll.add_symbol('str_from_float32', hstr_ext.str_from_float32)
ll.add_symbol('str_from_float64', hstr_ext.str_from_float64)
get_std_str_len = types.ExternalFunction('get_str_len', signature(types.
    intp, std_str_type))
init_string_from_chars = types.ExternalFunction('init_string_const',
    std_str_type(types.voidptr, types.intp))
_str_to_int64 = types.ExternalFunction('str_to_int64', signature(types.
    int64, types.voidptr, types.int64))
_str_to_uint64 = types.ExternalFunction('str_to_uint64', signature(types.
    uint64, types.voidptr, types.int64))
_str_to_int64_base = types.ExternalFunction('str_to_int64_base', signature(
    types.int64, types.voidptr, types.int64, types.int64))


def gen_unicode_to_std_str(context, builder, unicode_val):
    tjf__ejmtf = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    ezwig__qjv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.IntType
        (8).as_pointer(), lir.IntType(64)])
    krx__egjbh = cgutils.get_or_insert_function(builder.module, ezwig__qjv,
        name='init_string_const')
    return builder.call(krx__egjbh, [tjf__ejmtf.data, tjf__ejmtf.length])


def gen_std_str_to_unicode(context, builder, std_str_val, del_str=False):
    kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

    def _std_str_to_unicode(std_str):
        length = bodo.libs.str_ext.get_std_str_len(std_str)
        xpxb__grxoh = numba.cpython.unicode._empty_string(kind, length, 1)
        bodo.libs.str_arr_ext._memcpy(xpxb__grxoh._data, bodo.libs.str_ext.
            get_c_str(std_str), length, 1)
        if del_str:
            bodo.libs.str_ext.del_str(std_str)
        return xpxb__grxoh
    val = context.compile_internal(builder, _std_str_to_unicode,
        string_type(bodo.libs.str_ext.std_str_type), [std_str_val])
    return val


def gen_get_unicode_chars(context, builder, unicode_val):
    tjf__ejmtf = cgutils.create_struct_proxy(string_type)(context, builder,
        value=unicode_val)
    return tjf__ejmtf.data


@intrinsic
def unicode_to_std_str(typingctx, unicode_t=None):

    def codegen(context, builder, sig, args):
        return gen_unicode_to_std_str(context, builder, args[0])
    return std_str_type(string_type), codegen


@intrinsic
def std_str_to_unicode(typingctx, unicode_t=None):

    def codegen(context, builder, sig, args):
        return gen_std_str_to_unicode(context, builder, args[0], True)
    return string_type(std_str_type), codegen


class RandomAccessStringArrayType(types.ArrayCompatible):

    def __init__(self):
        super(RandomAccessStringArrayType, self).__init__(name=
            'RandomAccessStringArrayType()')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def dtype(self):
        return string_type

    def copy(self):
        RandomAccessStringArrayType()


random_access_string_array = RandomAccessStringArrayType()


@register_model(RandomAccessStringArrayType)
class RandomAccessStringArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        xcn__wkwr = [('data', types.List(string_type))]
        models.StructModel.__init__(self, dmm, fe_type, xcn__wkwr)


make_attribute_wrapper(RandomAccessStringArrayType, 'data', '_data')


@intrinsic
def alloc_random_access_string_array(typingctx, n_t=None):

    def codegen(context, builder, sig, args):
        foezs__qhe, = args
        mdw__ackyo = types.List(string_type)
        mbyh__owyny = numba.cpython.listobj.ListInstance.allocate(context,
            builder, mdw__ackyo, foezs__qhe)
        mbyh__owyny.size = foezs__qhe
        lbq__efbpy = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        lbq__efbpy.data = mbyh__owyny.value
        return lbq__efbpy._getvalue()
    return random_access_string_array(types.intp), codegen


@overload(operator.getitem, no_unliteral=True)
def random_access_str_arr_getitem(A, ind):
    if A != random_access_string_array:
        return
    if isinstance(ind, types.Integer):
        return lambda A, ind: A._data[ind]


@overload(operator.setitem)
def random_access_str_arr_setitem(A, idx, val):
    if A != random_access_string_array:
        return
    if isinstance(idx, types.Integer):
        assert val == string_type

        def impl_scalar(A, idx, val):
            A._data[idx] = val
        return impl_scalar


@overload(len, no_unliteral=True)
def overload_str_arr_len(A):
    if A == random_access_string_array:
        return lambda A: len(A._data)


@overload_attribute(RandomAccessStringArrayType, 'shape')
def overload_str_arr_shape(A):
    return lambda A: (len(A._data),)


def alloc_random_access_str_arr_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_libs_str_ext_alloc_random_access_string_array
    ) = alloc_random_access_str_arr_equiv
str_from_float32 = types.ExternalFunction('str_from_float32', types.void(
    types.voidptr, types.float32))
str_from_float64 = types.ExternalFunction('str_from_float64', types.void(
    types.voidptr, types.float64))


def float_to_str(s, v):
    pass


@overload(float_to_str)
def float_to_str_overload(s, v):
    assert isinstance(v, types.Float)
    if v == types.float32:
        return lambda s, v: str_from_float32(s._data, v)
    return lambda s, v: str_from_float64(s._data, v)


@overload(str)
def float_str_overload(v):
    if isinstance(v, types.Float):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(v):
            if v == 0:
                return '0.0'
            pbw__zlret = 0
            aagg__ifa = v
            if aagg__ifa < 0:
                pbw__zlret = 1
                aagg__ifa = -aagg__ifa
            if aagg__ifa < 1:
                swoqu__mlhsa = 1
            else:
                swoqu__mlhsa = 1 + int(np.floor(np.log10(aagg__ifa)))
            length = pbw__zlret + swoqu__mlhsa + 1 + 6
            s = numba.cpython.unicode._malloc_string(kind, 1, length, True)
            float_to_str(s, v)
            return s
        return impl


@overload(format, no_unliteral=True)
def overload_format(value, format_spec=''):
    if is_overload_constant_str(format_spec) and get_overload_const_str(
        format_spec) == '':

        def impl_fast(value, format_spec=''):
            return str(value)
        return impl_fast

    def impl(value, format_spec=''):
        with numba.objmode(res='string'):
            res = format(value, format_spec)
        return res
    return impl


@lower_cast(StdStringType, types.float64)
def cast_str_to_float64(context, builder, fromty, toty, val):
    ezwig__qjv = lir.FunctionType(lir.DoubleType(), [lir.IntType(8).
        as_pointer()])
    krx__egjbh = cgutils.get_or_insert_function(builder.module, ezwig__qjv,
        name='str_to_float64')
    res = builder.call(krx__egjbh, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(StdStringType, types.float32)
def cast_str_to_float32(context, builder, fromty, toty, val):
    ezwig__qjv = lir.FunctionType(lir.FloatType(), [lir.IntType(8).
        as_pointer()])
    krx__egjbh = cgutils.get_or_insert_function(builder.module, ezwig__qjv,
        name='str_to_float32')
    res = builder.call(krx__egjbh, (val,))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.float64)
def cast_unicode_str_to_float64(context, builder, fromty, toty, val):
    std_str = gen_unicode_to_std_str(context, builder, val)
    return cast_str_to_float64(context, builder, std_str_type, toty, std_str)


@lower_cast(string_type, types.float32)
def cast_unicode_str_to_float32(context, builder, fromty, toty, val):
    std_str = gen_unicode_to_std_str(context, builder, val)
    return cast_str_to_float32(context, builder, std_str_type, toty, std_str)


@lower_cast(string_type, types.int64)
@lower_cast(string_type, types.int32)
@lower_cast(string_type, types.int16)
@lower_cast(string_type, types.int8)
def cast_unicode_str_to_int64(context, builder, fromty, toty, val):
    tjf__ejmtf = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    ezwig__qjv = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(
        8).as_pointer(), lir.IntType(64)])
    krx__egjbh = cgutils.get_or_insert_function(builder.module, ezwig__qjv,
        name='str_to_int64')
    res = builder.call(krx__egjbh, (tjf__ejmtf.data, tjf__ejmtf.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@lower_cast(string_type, types.uint64)
@lower_cast(string_type, types.uint32)
@lower_cast(string_type, types.uint16)
@lower_cast(string_type, types.uint8)
def cast_unicode_str_to_uint64(context, builder, fromty, toty, val):
    tjf__ejmtf = cgutils.create_struct_proxy(string_type)(context, builder,
        value=val)
    ezwig__qjv = lir.FunctionType(lir.IntType(toty.bitwidth), [lir.IntType(
        8).as_pointer(), lir.IntType(64)])
    krx__egjbh = cgutils.get_or_insert_function(builder.module, ezwig__qjv,
        name='str_to_uint64')
    res = builder.call(krx__egjbh, (tjf__ejmtf.data, tjf__ejmtf.length))
    bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context, builder
        )
    return res


@infer_getattr
class StringAttribute(AttributeTemplate):
    key = types.UnicodeType

    @bound_function('str.format', no_unliteral=True)
    def resolve_format(self, string_typ, args, kws):
        kws = dict(kws)
        emih__hxicq = ', '.join('e{}'.format(zni__bul) for zni__bul in
            range(len(args)))
        if emih__hxicq:
            emih__hxicq += ', '
        ooyth__khd = ', '.join("{} = ''".format(a) for a in kws.keys())
        jqtd__ejgu = f'def format_stub(string, {emih__hxicq} {ooyth__khd}):\n'
        jqtd__ejgu += '    pass\n'
        jgjsj__tgpo = {}
        exec(jqtd__ejgu, {}, jgjsj__tgpo)
        jfre__lvd = jgjsj__tgpo['format_stub']
        rtruu__heuf = numba.core.utils.pysignature(jfre__lvd)
        ikl__woef = (string_typ,) + args + tuple(kws.values())
        return signature(string_typ, ikl__woef).replace(pysig=rtruu__heuf)


@numba.njit(cache=True)
def str_split(arr, pat, n):
    nba__zwrp = pat is not None and len(pat) > 1
    if nba__zwrp:
        riqs__okbuy = re.compile(pat)
        if n == -1:
            n = 0
    elif n == 0:
        n = -1
    mbyh__owyny = len(arr)
    ejgkv__jrq = 0
    lkut__qwr = 0
    for zni__bul in numba.parfors.parfor.internal_prange(mbyh__owyny):
        if bodo.libs.array_kernels.isna(arr, zni__bul):
            continue
        if nba__zwrp:
            nuam__ikaha = riqs__okbuy.split(arr[zni__bul], maxsplit=n)
        elif pat == '':
            nuam__ikaha = [''] + list(arr[zni__bul]) + ['']
        else:
            nuam__ikaha = arr[zni__bul].split(pat, n)
        ejgkv__jrq += len(nuam__ikaha)
        for s in nuam__ikaha:
            lkut__qwr += bodo.libs.str_arr_ext.get_utf8_size(s)
    bqtt__uuam = bodo.libs.array_item_arr_ext.pre_alloc_array_item_array(
        mbyh__owyny, (ejgkv__jrq, lkut__qwr), bodo.libs.str_arr_ext.
        string_array_type)
    ysg__yvjax = bodo.libs.array_item_arr_ext.get_offsets(bqtt__uuam)
    zselv__nny = bodo.libs.array_item_arr_ext.get_null_bitmap(bqtt__uuam)
    bids__cgtir = bodo.libs.array_item_arr_ext.get_data(bqtt__uuam)
    shsm__ajf = 0
    for cpih__kznw in numba.parfors.parfor.internal_prange(mbyh__owyny):
        ysg__yvjax[cpih__kznw] = shsm__ajf
        if bodo.libs.array_kernels.isna(arr, cpih__kznw):
            bodo.libs.int_arr_ext.set_bit_to_arr(zselv__nny, cpih__kznw, 0)
            continue
        bodo.libs.int_arr_ext.set_bit_to_arr(zselv__nny, cpih__kznw, 1)
        if nba__zwrp:
            nuam__ikaha = riqs__okbuy.split(arr[cpih__kznw], maxsplit=n)
        elif pat == '':
            nuam__ikaha = [''] + list(arr[cpih__kznw]) + ['']
        else:
            nuam__ikaha = arr[cpih__kznw].split(pat, n)
        xqd__eew = len(nuam__ikaha)
        for gis__zsa in range(xqd__eew):
            s = nuam__ikaha[gis__zsa]
            bids__cgtir[shsm__ajf] = s
            shsm__ajf += 1
    ysg__yvjax[mbyh__owyny] = shsm__ajf
    return bqtt__uuam


@overload(hex)
def overload_hex(x):
    if isinstance(x, types.Integer):
        kind = numba.cpython.unicode.PY_UNICODE_1BYTE_KIND

        def impl(x):
            x = np.int64(x)
            if x < 0:
                wbprf__zwpx = '-0x'
                x = x * -1
            else:
                wbprf__zwpx = '0x'
            x = np.uint64(x)
            if x == 0:
                zrepz__bviyg = 1
            else:
                zrepz__bviyg = fast_ceil_log2(x + 1)
                zrepz__bviyg = (zrepz__bviyg + 3) // 4
            length = len(wbprf__zwpx) + zrepz__bviyg
            output = numba.cpython.unicode._empty_string(kind, length, 1)
            bodo.libs.str_arr_ext._memcpy(output._data, wbprf__zwpx._data,
                len(wbprf__zwpx), 1)
            int_to_hex(output, zrepz__bviyg, len(wbprf__zwpx), x)
            return output
        return impl


@register_jitable
def fast_ceil_log2(x):
    rgbg__mtgtf = 0 if x & x - 1 == 0 else 1
    tzjwf__wkcc = [np.uint64(18446744069414584320), np.uint64(4294901760),
        np.uint64(65280), np.uint64(240), np.uint64(12), np.uint64(2)]
    rdx__etly = 32
    for zni__bul in range(len(tzjwf__wkcc)):
        bhvtv__jmu = 0 if x & tzjwf__wkcc[zni__bul] == 0 else rdx__etly
        rgbg__mtgtf = rgbg__mtgtf + bhvtv__jmu
        x = x >> bhvtv__jmu
        rdx__etly = rdx__etly >> 1
    return rgbg__mtgtf


@intrinsic
def int_to_hex(typingctx, output, out_len, header_len, int_val):

    def codegen(context, builder, sig, args):
        output, out_len, header_len, int_val = args
        wme__doqd = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=output)
        ezwig__qjv = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(64)])
        jvpeb__vjp = cgutils.get_or_insert_function(builder.module,
            ezwig__qjv, name='int_to_hex')
        lpkei__crljw = builder.inttoptr(builder.add(builder.ptrtoint(
            wme__doqd.data, lir.IntType(64)), header_len), lir.IntType(8).
            as_pointer())
        builder.call(jvpeb__vjp, (lpkei__crljw, out_len, int_val))
    return types.void(output, out_len, header_len, int_val), codegen


def alloc_empty_bytes_or_string_data(typ, kind, length, is_ascii=0):
    pass


@overload(alloc_empty_bytes_or_string_data)
def overload_alloc_empty_bytes_or_string_data(typ, kind, length, is_ascii=0):
    typ = typ.instance_type if isinstance(typ, types.TypeRef) else typ
    if typ == bodo.bytes_type:
        return lambda typ, kind, length, is_ascii=0: np.empty(length, np.uint8)
    if typ == string_type:
        return (lambda typ, kind, length, is_ascii=0: numba.cpython.unicode
            ._empty_string(kind, length, is_ascii))
    raise BodoError(
        f'Internal Error: Expected Bytes or String type, found {typ}')


def get_unicode_or_numpy_data(val):
    pass


@overload(get_unicode_or_numpy_data)
def overload_get_unicode_or_numpy_data(val):
    if val == string_type:
        return lambda val: val._data
    if isinstance(val, types.Array):
        return lambda val: val.ctypes
    raise BodoError(
        f'Internal Error: Expected String or Numpy Array, found {val}')
