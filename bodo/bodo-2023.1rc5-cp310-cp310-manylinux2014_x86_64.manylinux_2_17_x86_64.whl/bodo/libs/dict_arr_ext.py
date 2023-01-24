"""Dictionary encoded array data type, similar to DictionaryArray of Arrow.
The purpose is to improve memory consumption and performance over string_array_type for
string arrays that have a lot of repetitive values (typical in practice).
Can be extended to be used with types other than strings as well.
See:
https://bodo.atlassian.net/browse/BE-2295
https://bodo.atlassian.net/wiki/spaces/B/pages/993722369/Dictionary-encoded+String+Array+Support+in+Parquet+read+compute+...
https://arrow.apache.org/docs/cpp/api/array.html#dictionary-encoded
"""
import operator
import re
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_new_ref, lower_builtin, lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
import bodo
from bodo.libs import hstr_ext
from bodo.libs.bool_arr_ext import init_bool_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, get_str_arr_item_length, overload_str_arr_astype, pre_alloc_string_array, string_array_type
from bodo.utils.typing import BodoArrayIterator, is_overload_none, raise_bodo_error
from bodo.utils.utils import synchronize_error_njit
ll.add_symbol('box_dict_str_array', hstr_ext.box_dict_str_array)
dict_indices_arr_type = IntegerArrayType(types.int32)


class DictionaryArrayType(types.IterableType, types.ArrayCompatible):

    def __init__(self, arr_data_type):
        self.data = arr_data_type
        super(DictionaryArrayType, self).__init__(name=
            f'DictionaryArrayType({arr_data_type})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    @property
    def iterator_type(self):
        return BodoArrayIterator(self)

    @property
    def dtype(self):
        return self.data.dtype

    def copy(self):
        return DictionaryArrayType(self.data)

    @property
    def indices_type(self):
        return dict_indices_arr_type

    @property
    def indices_dtype(self):
        return dict_indices_arr_type.dtype

    def unify(self, typingctx, other):
        if other == string_array_type:
            return string_array_type


dict_str_arr_type = DictionaryArrayType(string_array_type)


@register_model(DictionaryArrayType)
class DictionaryArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        kjs__hvzo = [('data', fe_type.data), ('indices',
            dict_indices_arr_type), ('has_global_dictionary', types.bool_),
            ('has_deduped_local_dictionary', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, kjs__hvzo)


make_attribute_wrapper(DictionaryArrayType, 'data', '_data')
make_attribute_wrapper(DictionaryArrayType, 'indices', '_indices')
make_attribute_wrapper(DictionaryArrayType, 'has_global_dictionary',
    '_has_global_dictionary')
make_attribute_wrapper(DictionaryArrayType, 'has_deduped_local_dictionary',
    '_has_deduped_local_dictionary')
lower_builtin('getiter', dict_str_arr_type)(numba.np.arrayobj.getiter_array)


@intrinsic
def init_dict_arr(typingctx, data_t, indices_t, glob_dict_t, unique_dict_t):
    assert indices_t == dict_indices_arr_type, 'invalid indices type for dict array'

    def codegen(context, builder, signature, args):
        bpuuh__wggq, yemh__evuc, zzew__vjr, vwz__fskf = args
        gzx__vcs = cgutils.create_struct_proxy(signature.return_type)(context,
            builder)
        gzx__vcs.data = bpuuh__wggq
        gzx__vcs.indices = yemh__evuc
        gzx__vcs.has_global_dictionary = zzew__vjr
        gzx__vcs.has_deduped_local_dictionary = vwz__fskf
        context.nrt.incref(builder, signature.args[0], bpuuh__wggq)
        context.nrt.incref(builder, signature.args[1], yemh__evuc)
        return gzx__vcs._getvalue()
    nuw__ntyc = DictionaryArrayType(data_t)
    rhlh__lsw = nuw__ntyc(data_t, indices_t, types.bool_, types.bool_)
    return rhlh__lsw, codegen


@typeof_impl.register(pa.DictionaryArray)
def typeof_dict_value(val, c):
    if val.type.value_type == pa.string():
        return dict_str_arr_type


def to_pa_dict_arr(A):
    if isinstance(A, pa.DictionaryArray):
        return A
    if isinstance(A, pd.arrays.ArrowStringArray) and pa.types.is_dictionary(A
        ._data.type) and (pa.types.is_string(A._data.type.value_type) or pa
        .types.is_large_string(A._data.type.value_type)) and pa.types.is_int32(
        A._data.type.index_type):
        return A._data.combine_chunks()
    return pd.array(A, 'string[pyarrow]')._data.combine_chunks(
        ).dictionary_encode()


@unbox(DictionaryArrayType)
def unbox_dict_arr(typ, val, c):
    xlei__bpk = c.pyapi.unserialize(c.pyapi.serialize_object(to_pa_dict_arr))
    val = c.pyapi.call_function_objargs(xlei__bpk, [val])
    c.pyapi.decref(xlei__bpk)
    gzx__vcs = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    pjapl__yjslu = c.pyapi.object_getattr_string(val, 'dictionary')
    moxk__hzcxo = c.pyapi.bool_from_bool(c.context.get_constant(types.bool_,
        False))
    gemqd__ukw = c.pyapi.call_method(pjapl__yjslu, 'to_numpy', (moxk__hzcxo,))
    gzx__vcs.data = c.unbox(typ.data, gemqd__ukw).value
    ssfy__tiv = c.pyapi.object_getattr_string(val, 'indices')
    dfk__cjefq = c.context.insert_const_string(c.builder.module, 'pandas')
    qpec__tciyp = c.pyapi.import_module_noblock(dfk__cjefq)
    wav__skzn = c.pyapi.string_from_constant_string('Int32')
    ncfmw__yvvj = c.pyapi.call_method(qpec__tciyp, 'array', (ssfy__tiv,
        wav__skzn))
    gzx__vcs.indices = c.unbox(dict_indices_arr_type, ncfmw__yvvj).value
    gzx__vcs.has_global_dictionary = c.context.get_constant(types.bool_, False)
    gzx__vcs.has_deduped_local_dictionary = c.context.get_constant(types.
        bool_, False)
    c.pyapi.decref(pjapl__yjslu)
    c.pyapi.decref(moxk__hzcxo)
    c.pyapi.decref(gemqd__ukw)
    c.pyapi.decref(ssfy__tiv)
    c.pyapi.decref(qpec__tciyp)
    c.pyapi.decref(wav__skzn)
    c.pyapi.decref(ncfmw__yvvj)
    c.pyapi.decref(val)
    oqfc__gedvt = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(gzx__vcs._getvalue(), is_error=oqfc__gedvt)


@box(DictionaryArrayType)
def box_dict_arr(typ, val, c):
    gzx__vcs = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ == dict_str_arr_type:
        if bodo.libs.str_arr_ext.use_pd_pyarrow_string_array:
            from bodo.libs.array import array_info_type, array_to_info_codegen
            wlo__wnmg = array_to_info_codegen(c.context, c.builder,
                array_info_type(typ), (val,), incref=False)
            tyq__zgzyp = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(8).
                as_pointer()])
            rdq__neum = 'pd_pyarrow_array_from_string_array'
            krk__roi = cgutils.get_or_insert_function(c.builder.module,
                tyq__zgzyp, name=rdq__neum)
            arr = c.builder.call(krk__roi, [wlo__wnmg])
            c.context.nrt.decref(c.builder, typ, val)
            return arr
        c.context.nrt.incref(c.builder, typ.data, gzx__vcs.data)
        uocu__lmhp = c.box(typ.data, gzx__vcs.data)
        aecpq__xfde = cgutils.create_struct_proxy(dict_indices_arr_type)(c.
            context, c.builder, gzx__vcs.indices)
        tyq__zgzyp = lir.FunctionType(c.pyapi.pyobj, [lir.IntType(64), c.
            pyapi.pyobj, lir.IntType(32).as_pointer(), lir.IntType(8).
            as_pointer()])
        krk__roi = cgutils.get_or_insert_function(c.builder.module,
            tyq__zgzyp, name='box_dict_str_array')
        kfnk__ltifl = cgutils.create_struct_proxy(types.Array(types.int32, 
            1, 'C'))(c.context, c.builder, aecpq__xfde.data)
        korb__krq = c.builder.extract_value(kfnk__ltifl.shape, 0)
        rdl__xzl = kfnk__ltifl.data
        cxw__amlxe = cgutils.create_struct_proxy(types.Array(types.int8, 1,
            'C'))(c.context, c.builder, aecpq__xfde.null_bitmap).data
        gemqd__ukw = c.builder.call(krk__roi, [korb__krq, uocu__lmhp,
            rdl__xzl, cxw__amlxe])
        c.pyapi.decref(uocu__lmhp)
    else:
        dfk__cjefq = c.context.insert_const_string(c.builder.module, 'pyarrow')
        turmz__wrjcy = c.pyapi.import_module_noblock(dfk__cjefq)
        tqsu__uskmo = c.pyapi.object_getattr_string(turmz__wrjcy,
            'DictionaryArray')
        c.context.nrt.incref(c.builder, typ.data, gzx__vcs.data)
        uocu__lmhp = c.box(typ.data, gzx__vcs.data)
        c.context.nrt.incref(c.builder, dict_indices_arr_type, gzx__vcs.indices
            )
        ssfy__tiv = c.box(dict_indices_arr_type, gzx__vcs.indices)
        zmqwh__zyfy = c.pyapi.call_method(tqsu__uskmo, 'from_arrays', (
            ssfy__tiv, uocu__lmhp))
        moxk__hzcxo = c.pyapi.bool_from_bool(c.context.get_constant(types.
            bool_, False))
        gemqd__ukw = c.pyapi.call_method(zmqwh__zyfy, 'to_numpy', (
            moxk__hzcxo,))
        c.pyapi.decref(turmz__wrjcy)
        c.pyapi.decref(uocu__lmhp)
        c.pyapi.decref(ssfy__tiv)
        c.pyapi.decref(tqsu__uskmo)
        c.pyapi.decref(zmqwh__zyfy)
        c.pyapi.decref(moxk__hzcxo)
    c.context.nrt.decref(c.builder, typ, val)
    return gemqd__ukw


@overload(len, no_unliteral=True)
def overload_dict_arr_len(A):
    if isinstance(A, DictionaryArrayType):
        return lambda A: len(A._indices)


@overload_attribute(DictionaryArrayType, 'shape')
def overload_dict_arr_shape(A):
    return lambda A: (len(A._indices),)


@overload_attribute(DictionaryArrayType, 'ndim')
def overload_dict_arr_ndim(A):
    return lambda A: 1


@overload_attribute(DictionaryArrayType, 'size')
def overload_dict_arr_size(A):
    return lambda A: len(A._indices)


@overload_method(DictionaryArrayType, 'tolist', no_unliteral=True)
def overload_dict_arr_tolist(A):
    return lambda A: list(A)


overload_method(DictionaryArrayType, 'astype', no_unliteral=True)(
    overload_str_arr_astype)


@overload_method(DictionaryArrayType, 'copy', no_unliteral=True)
def overload_dict_arr_copy(A):

    def copy_impl(A):
        return init_dict_arr(A._data.copy(), A._indices.copy(), A.
            _has_global_dictionary, A._has_deduped_local_dictionary)
    return copy_impl


@overload_attribute(DictionaryArrayType, 'dtype')
def overload_dict_arr_dtype(A):
    return lambda A: A._data.dtype


@overload_attribute(DictionaryArrayType, 'nbytes')
def dict_arr_nbytes_overload(A):
    return lambda A: A._data.nbytes + A._indices.nbytes


@lower_constant(DictionaryArrayType)
def lower_constant_dict_arr(context, builder, typ, pyval):
    if bodo.hiframes.boxing._use_dict_str_type and isinstance(pyval, np.ndarray
        ):
        pyval = pa.array(pyval).dictionary_encode()
    ybb__ddm = pyval.dictionary.to_numpy(False)
    dks__wku = pd.array(pyval.indices, 'Int32')
    ybb__ddm = context.get_constant_generic(builder, typ.data, ybb__ddm)
    dks__wku = context.get_constant_generic(builder, dict_indices_arr_type,
        dks__wku)
    njug__mnott = context.get_constant(types.bool_, False)
    ovdpd__qcrsv = context.get_constant(types.bool_, False)
    vkiz__kuemu = lir.Constant.literal_struct([ybb__ddm, dks__wku,
        njug__mnott, ovdpd__qcrsv])
    return vkiz__kuemu


@overload(operator.getitem, no_unliteral=True)
def dict_arr_getitem(A, ind):
    if not isinstance(A, DictionaryArrayType):
        return
    if isinstance(ind, types.Integer):

        def dict_arr_getitem_impl(A, ind):
            if bodo.libs.array_kernels.isna(A._indices, ind):
                return ''
            rtwt__skpt = A._indices[ind]
            return A._data[rtwt__skpt]
        return dict_arr_getitem_impl
    return lambda A, ind: init_dict_arr(A._data, A._indices[ind], A.
        _has_global_dictionary, A._has_deduped_local_dictionary)


@overload_method(DictionaryArrayType, '_decode', no_unliteral=True)
def overload_dict_arr_decode(A):

    def impl(A):
        bpuuh__wggq = A._data
        yemh__evuc = A._indices
        korb__krq = len(yemh__evuc)
        ydkxi__rowpo = [get_str_arr_item_length(bpuuh__wggq, i) for i in
            range(len(bpuuh__wggq))]
        qmiy__mep = 0
        for i in range(korb__krq):
            if not bodo.libs.array_kernels.isna(yemh__evuc, i):
                qmiy__mep += ydkxi__rowpo[yemh__evuc[i]]
        pib__farak = pre_alloc_string_array(korb__krq, qmiy__mep)
        for i in range(korb__krq):
            if bodo.libs.array_kernels.isna(yemh__evuc, i):
                bodo.libs.array_kernels.setna(pib__farak, i)
                continue
            ind = yemh__evuc[i]
            if bodo.libs.array_kernels.isna(bpuuh__wggq, ind):
                bodo.libs.array_kernels.setna(pib__farak, i)
                continue
            pib__farak[i] = bpuuh__wggq[ind]
        return pib__farak
    return impl


@overload(operator.setitem)
def dict_arr_setitem(A, idx, val):
    if not isinstance(A, DictionaryArrayType):
        return
    raise_bodo_error(
        "DictionaryArrayType is read-only and doesn't support setitem yet")


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind_unique(arr, val):
    rtwt__skpt = -1
    bpuuh__wggq = arr._data
    for i in range(len(bpuuh__wggq)):
        if bodo.libs.array_kernels.isna(bpuuh__wggq, i):
            continue
        if bpuuh__wggq[i] == val:
            rtwt__skpt = i
            break
    return rtwt__skpt


@numba.njit(no_cpython_wrapper=True)
def find_dict_ind_non_unique(arr, val):
    vyh__czxb = set()
    bpuuh__wggq = arr._data
    for i in range(len(bpuuh__wggq)):
        if bodo.libs.array_kernels.isna(bpuuh__wggq, i):
            continue
        if bpuuh__wggq[i] == val:
            vyh__czxb.add(i)
    return vyh__czxb


@numba.njit(no_cpython_wrapper=True)
def dict_arr_eq(arr, val):
    korb__krq = len(arr)
    if arr._has_deduped_local_dictionary:
        rtwt__skpt = find_dict_ind_unique(arr, val)
        if rtwt__skpt == -1:
            return init_bool_array(np.full(korb__krq, False, np.bool_), arr
                ._indices._null_bitmap.copy())
        return arr._indices == rtwt__skpt
    else:
        exha__xxg = find_dict_ind_non_unique(arr, val)
        if len(exha__xxg) == 0:
            return init_bool_array(np.full(korb__krq, False, np.bool_), arr
                ._indices._null_bitmap.copy())
        oanzi__wfrtf = np.empty(korb__krq, dtype=np.bool_)
        for i in range(len(arr._indices)):
            oanzi__wfrtf[i] = arr._indices[i] in exha__xxg
        return init_bool_array(oanzi__wfrtf, arr._indices._null_bitmap.copy())


@numba.njit(no_cpython_wrapper=True)
def dict_arr_ne(arr, val):
    korb__krq = len(arr)
    if arr._has_deduped_local_dictionary:
        rtwt__skpt = find_dict_ind_unique(arr, val)
        if rtwt__skpt == -1:
            return init_bool_array(np.full(korb__krq, True, np.bool_), arr.
                _indices._null_bitmap.copy())
        return arr._indices != rtwt__skpt
    else:
        exha__xxg = find_dict_ind_non_unique(arr, val)
        if len(exha__xxg) == 0:
            return init_bool_array(np.full(korb__krq, True, np.bool_), arr.
                _indices._null_bitmap.copy())
        oanzi__wfrtf = np.empty(korb__krq, dtype=np.bool_)
        for i in range(len(arr._indices)):
            oanzi__wfrtf[i] = arr._indices[i] not in exha__xxg
        return init_bool_array(oanzi__wfrtf, arr._indices._null_bitmap.copy())


def get_binary_op_overload(op, lhs, rhs):
    if op == operator.eq:
        if lhs == dict_str_arr_type and types.unliteral(rhs
            ) == bodo.string_type:
            return lambda lhs, rhs: bodo.libs.dict_arr_ext.dict_arr_eq(lhs, rhs
                )
        if rhs == dict_str_arr_type and types.unliteral(lhs
            ) == bodo.string_type:
            return lambda lhs, rhs: bodo.libs.dict_arr_ext.dict_arr_eq(rhs, lhs
                )
    if op == operator.ne:
        if lhs == dict_str_arr_type and types.unliteral(rhs
            ) == bodo.string_type:
            return lambda lhs, rhs: bodo.libs.dict_arr_ext.dict_arr_ne(lhs, rhs
                )
        if rhs == dict_str_arr_type and types.unliteral(lhs
            ) == bodo.string_type:
            return lambda lhs, rhs: bodo.libs.dict_arr_ext.dict_arr_ne(rhs, lhs
                )


def convert_dict_arr_to_int(arr, dtype):
    return arr


@overload(convert_dict_arr_to_int)
def convert_dict_arr_to_int_overload(arr, dtype):

    def impl(arr, dtype):
        qowh__efi = arr._data
        ftkus__jizy = bodo.libs.int_arr_ext.alloc_int_array(len(qowh__efi),
            dtype)
        for iocvq__ecc in range(len(qowh__efi)):
            if bodo.libs.array_kernels.isna(qowh__efi, iocvq__ecc):
                bodo.libs.array_kernels.setna(ftkus__jizy, iocvq__ecc)
                continue
            ftkus__jizy[iocvq__ecc] = np.int64(qowh__efi[iocvq__ecc])
        korb__krq = len(arr)
        yemh__evuc = arr._indices
        pib__farak = bodo.libs.int_arr_ext.alloc_int_array(korb__krq, dtype)
        for i in range(korb__krq):
            if bodo.libs.array_kernels.isna(yemh__evuc, i):
                bodo.libs.array_kernels.setna(pib__farak, i)
                continue
            pib__farak[i] = ftkus__jizy[yemh__evuc[i]]
        return pib__farak
    return impl


def cat_dict_str(arrs, sep):
    pass


@overload(cat_dict_str)
def cat_dict_str_overload(arrs, sep):
    tox__lxapt = len(arrs)
    dhu__ihazl = 'def impl(arrs, sep):\n'
    dhu__ihazl += '  ind_map = {}\n'
    dhu__ihazl += '  out_strs = []\n'
    dhu__ihazl += '  n = len(arrs[0])\n'
    for i in range(tox__lxapt):
        dhu__ihazl += f'  indices{i} = arrs[{i}]._indices\n'
    for i in range(tox__lxapt):
        dhu__ihazl += f'  data{i} = arrs[{i}]._data\n'
    dhu__ihazl += (
        '  out_indices = bodo.libs.int_arr_ext.alloc_int_array(n, np.int32)\n')
    dhu__ihazl += '  for i in range(n):\n'
    pwxiy__uooy = ' or '.join([
        f'bodo.libs.array_kernels.isna(arrs[{i}], i)' for i in range(
        tox__lxapt)])
    dhu__ihazl += f'    if {pwxiy__uooy}:\n'
    dhu__ihazl += '      bodo.libs.array_kernels.setna(out_indices, i)\n'
    dhu__ihazl += '      continue\n'
    for i in range(tox__lxapt):
        dhu__ihazl += f'    ind{i} = indices{i}[i]\n'
    dqe__hpo = '(' + ', '.join(f'ind{i}' for i in range(tox__lxapt)) + ')'
    dhu__ihazl += f'    if {dqe__hpo} not in ind_map:\n'
    dhu__ihazl += '      out_ind = len(out_strs)\n'
    dhu__ihazl += f'      ind_map[{dqe__hpo}] = out_ind\n'
    dbi__ltugz = "''" if is_overload_none(sep) else 'sep'
    wqv__ayrxi = ', '.join([f'data{i}[ind{i}]' for i in range(tox__lxapt)])
    dhu__ihazl += f'      v = {dbi__ltugz}.join([{wqv__ayrxi}])\n'
    dhu__ihazl += '      out_strs.append(v)\n'
    dhu__ihazl += '    else:\n'
    dhu__ihazl += f'      out_ind = ind_map[{dqe__hpo}]\n'
    dhu__ihazl += '    out_indices[i] = out_ind\n'
    dhu__ihazl += (
        '  out_str_arr = bodo.libs.str_arr_ext.str_arr_from_sequence(out_strs)\n'
        )
    dhu__ihazl += """  return bodo.libs.dict_arr_ext.init_dict_arr(out_str_arr, out_indices, False, False)
"""
    crzr__vrn = {}
    exec(dhu__ihazl, {'bodo': bodo, 'numba': numba, 'np': np}, crzr__vrn)
    impl = crzr__vrn['impl']
    return impl


@lower_cast(DictionaryArrayType, StringArrayType)
def cast_dict_str_arr_to_str_arr(context, builder, fromty, toty, val):
    if fromty != dict_str_arr_type:
        return
    vcl__hzkni = bodo.utils.typing.decode_if_dict_array_overload(fromty)
    rhlh__lsw = toty(fromty)
    fak__xue = context.compile_internal(builder, vcl__hzkni, rhlh__lsw, (val,))
    return impl_ret_new_ref(context, builder, toty, fak__xue)


@register_jitable
def dict_arr_to_numeric(arr, errors, downcast):
    gzx__vcs = arr._data
    dict_arr_out = pd.to_numeric(gzx__vcs, errors, downcast)
    dks__wku = arr._indices
    jvzj__wop = len(dks__wku)
    pib__farak = bodo.utils.utils.alloc_type(jvzj__wop, dict_arr_out, (-1,))
    for i in range(jvzj__wop):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(pib__farak, i)
            continue
        rtwt__skpt = dks__wku[i]
        if bodo.libs.array_kernels.isna(dict_arr_out, rtwt__skpt):
            bodo.libs.array_kernels.setna(pib__farak, i)
            continue
        pib__farak[i] = dict_arr_out[rtwt__skpt]
    return pib__farak


@register_jitable
def str_replace(arr, pat, repl, flags, regex):
    ybb__ddm = arr._data
    fkdk__ekzu = len(ybb__ddm)
    oes__fnn = pre_alloc_string_array(fkdk__ekzu, -1)
    if regex:
        aedq__qpz = re.compile(pat, flags)
        for i in range(fkdk__ekzu):
            if bodo.libs.array_kernels.isna(ybb__ddm, i):
                bodo.libs.array_kernels.setna(oes__fnn, i)
                continue
            oes__fnn[i] = aedq__qpz.sub(repl=repl, string=ybb__ddm[i])
    else:
        for i in range(fkdk__ekzu):
            if bodo.libs.array_kernels.isna(ybb__ddm, i):
                bodo.libs.array_kernels.setna(oes__fnn, i)
                continue
            oes__fnn[i] = ybb__ddm[i].replace(pat, repl)
    return init_dict_arr(oes__fnn, arr._indices.copy(), arr.
        _has_global_dictionary, False)


@register_jitable
def str_startswith(arr, pat, na):
    gzx__vcs = arr._data
    lzjga__klhi = len(gzx__vcs)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(lzjga__klhi)
    for i in range(lzjga__klhi):
        dict_arr_out[i] = gzx__vcs[i].startswith(pat)
    dks__wku = arr._indices
    jvzj__wop = len(dks__wku)
    pib__farak = bodo.libs.bool_arr_ext.alloc_bool_array(jvzj__wop)
    for i in range(jvzj__wop):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(pib__farak, i)
        else:
            pib__farak[i] = dict_arr_out[dks__wku[i]]
    return pib__farak


@register_jitable
def str_endswith(arr, pat, na):
    gzx__vcs = arr._data
    lzjga__klhi = len(gzx__vcs)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(lzjga__klhi)
    for i in range(lzjga__klhi):
        dict_arr_out[i] = gzx__vcs[i].endswith(pat)
    dks__wku = arr._indices
    jvzj__wop = len(dks__wku)
    pib__farak = bodo.libs.bool_arr_ext.alloc_bool_array(jvzj__wop)
    for i in range(jvzj__wop):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(pib__farak, i)
        else:
            pib__farak[i] = dict_arr_out[dks__wku[i]]
    return pib__farak


@numba.njit
def str_series_contains_regex(arr, pat, case, flags, na, regex):
    gzx__vcs = arr._data
    ncr__zdaq = pd.Series(gzx__vcs)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = pd.array(ncr__zdaq.array, 'string')._str_contains(pat,
            case, flags, na, regex)
    dks__wku = arr._indices
    jvzj__wop = len(dks__wku)
    pib__farak = bodo.libs.bool_arr_ext.alloc_bool_array(jvzj__wop)
    for i in range(jvzj__wop):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(pib__farak, i)
        else:
            pib__farak[i] = dict_arr_out[dks__wku[i]]
    return pib__farak


@register_jitable
def str_contains_non_regex(arr, pat, case):
    gzx__vcs = arr._data
    lzjga__klhi = len(gzx__vcs)
    dict_arr_out = bodo.libs.bool_arr_ext.alloc_bool_array(lzjga__klhi)
    if not case:
        vfp__yzpt = pat.upper()
    for i in range(lzjga__klhi):
        if case:
            dict_arr_out[i] = pat in gzx__vcs[i]
        else:
            dict_arr_out[i] = vfp__yzpt in gzx__vcs[i].upper()
    dks__wku = arr._indices
    jvzj__wop = len(dks__wku)
    pib__farak = bodo.libs.bool_arr_ext.alloc_bool_array(jvzj__wop)
    for i in range(jvzj__wop):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(pib__farak, i)
        else:
            pib__farak[i] = dict_arr_out[dks__wku[i]]
    return pib__farak


@numba.njit
def str_match(arr, pat, case, flags, na):
    gzx__vcs = arr._data
    dks__wku = arr._indices
    jvzj__wop = len(dks__wku)
    pib__farak = bodo.libs.bool_arr_ext.alloc_bool_array(jvzj__wop)
    ncr__zdaq = pd.Series(gzx__vcs)
    with numba.objmode(dict_arr_out=bodo.boolean_array):
        dict_arr_out = ncr__zdaq.array._str_match(pat, case, flags, na)
    for i in range(jvzj__wop):
        if bodo.libs.array_kernels.isna(arr, i):
            bodo.libs.array_kernels.setna(pib__farak, i)
        else:
            pib__farak[i] = dict_arr_out[dks__wku[i]]
    return pib__farak


def create_simple_str2str_methods(func_name, func_args, can_create_non_unique):
    dhu__ihazl = f"""def str_{func_name}({', '.join(func_args)}):
    data_arr = arr._data
    n_data = len(data_arr)
    out_str_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n_data, -1)
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            bodo.libs.array_kernels.setna(out_str_arr, i)
            continue
        out_str_arr[i] = data_arr[i].{func_name}({', '.join(func_args[1:])})
"""
    if can_create_non_unique:
        dhu__ihazl += """    return init_dict_arr(out_str_arr, arr._indices.copy(), arr._has_global_dictionary, False)
"""
    else:
        dhu__ihazl += """    return init_dict_arr(out_str_arr, arr._indices.copy(), arr._has_global_dictionary, arr._has_deduped_local_dictionary)
"""
    crzr__vrn = {}
    exec(dhu__ihazl, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr}, crzr__vrn)
    return crzr__vrn[f'str_{func_name}']


def _register_simple_str2str_methods():
    earhf__ignnt = {**dict.fromkeys(['capitalize', 'lower', 'swapcase',
        'title', 'upper'], ('arr',)), **dict.fromkeys(['lstrip', 'rstrip',
        'strip'], ('arr', 'to_strip')), **dict.fromkeys(['center', 'ljust',
        'rjust'], ('arr', 'width', 'fillchar')), **dict.fromkeys(['zfill'],
        ('arr', 'width'))}
    sxt__jat = {**dict.fromkeys(['capitalize', 'lower', 'title', 'upper',
        'lstrip', 'rstrip', 'strip', 'center', 'zfill', 'ljust', 'rjust'], 
        True), **dict.fromkeys(['swapcase'], False)}
    for func_name in earhf__ignnt.keys():
        iwzt__tbh = create_simple_str2str_methods(func_name, earhf__ignnt[
            func_name], sxt__jat[func_name])
        iwzt__tbh = register_jitable(iwzt__tbh)
        globals()[f'str_{func_name}'] = iwzt__tbh


_register_simple_str2str_methods()


@register_jitable
def str_index(arr, sub, start, end):
    ybb__ddm = arr._data
    dks__wku = arr._indices
    fkdk__ekzu = len(ybb__ddm)
    jvzj__wop = len(dks__wku)
    iqmcc__jmxxl = bodo.libs.int_arr_ext.alloc_int_array(fkdk__ekzu, np.int64)
    pib__farak = bodo.libs.int_arr_ext.alloc_int_array(jvzj__wop, np.int64)
    bva__rvy = False
    for i in range(fkdk__ekzu):
        if bodo.libs.array_kernels.isna(ybb__ddm, i):
            bodo.libs.array_kernels.setna(iqmcc__jmxxl, i)
        else:
            iqmcc__jmxxl[i] = ybb__ddm[i].find(sub, start, end)
    for i in range(jvzj__wop):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(iqmcc__jmxxl, dks__wku[i]):
            bodo.libs.array_kernels.setna(pib__farak, i)
        else:
            pib__farak[i] = iqmcc__jmxxl[dks__wku[i]]
            if pib__farak[i] == -1:
                bva__rvy = True
    cazu__sgamb = 'substring not found' if bva__rvy else ''
    synchronize_error_njit('ValueError', cazu__sgamb)
    return pib__farak


@register_jitable
def str_rindex(arr, sub, start, end):
    ybb__ddm = arr._data
    dks__wku = arr._indices
    fkdk__ekzu = len(ybb__ddm)
    jvzj__wop = len(dks__wku)
    iqmcc__jmxxl = bodo.libs.int_arr_ext.alloc_int_array(fkdk__ekzu, np.int64)
    pib__farak = bodo.libs.int_arr_ext.alloc_int_array(jvzj__wop, np.int64)
    bva__rvy = False
    for i in range(fkdk__ekzu):
        if bodo.libs.array_kernels.isna(ybb__ddm, i):
            bodo.libs.array_kernels.setna(iqmcc__jmxxl, i)
        else:
            iqmcc__jmxxl[i] = ybb__ddm[i].rindex(sub, start, end)
    for i in range(jvzj__wop):
        if bodo.libs.array_kernels.isna(arr, i
            ) or bodo.libs.array_kernels.isna(iqmcc__jmxxl, dks__wku[i]):
            bodo.libs.array_kernels.setna(pib__farak, i)
        else:
            pib__farak[i] = iqmcc__jmxxl[dks__wku[i]]
            if pib__farak[i] == -1:
                bva__rvy = True
    cazu__sgamb = 'substring not found' if bva__rvy else ''
    synchronize_error_njit('ValueError', cazu__sgamb)
    return pib__farak


def create_find_methods(func_name):
    dhu__ihazl = f"""def str_{func_name}(arr, sub, start, end):
  data_arr = arr._data
  indices_arr = arr._indices
  n_data = len(data_arr)
  n_indices = len(indices_arr)
  tmp_dict_arr = bodo.libs.int_arr_ext.alloc_int_array(n_data, np.int64)
  out_int_arr = bodo.libs.int_arr_ext.alloc_int_array(n_indices, np.int64)
  for i in range(n_data):
    if bodo.libs.array_kernels.isna(data_arr, i):
      bodo.libs.array_kernels.setna(tmp_dict_arr, i)
      continue
    tmp_dict_arr[i] = data_arr[i].{func_name}(sub, start, end)
  for i in range(n_indices):
    if bodo.libs.array_kernels.isna(indices_arr, i) or bodo.libs.array_kernels.isna(
      tmp_dict_arr, indices_arr[i]
    ):
      bodo.libs.array_kernels.setna(out_int_arr, i)
    else:
      out_int_arr[i] = tmp_dict_arr[indices_arr[i]]
  return out_int_arr"""
    crzr__vrn = {}
    exec(dhu__ihazl, {'bodo': bodo, 'numba': numba, 'init_dict_arr':
        init_dict_arr, 'np': np}, crzr__vrn)
    return crzr__vrn[f'str_{func_name}']


def _register_find_methods():
    wpq__vsewj = ['find', 'rfind']
    for func_name in wpq__vsewj:
        iwzt__tbh = create_find_methods(func_name)
        iwzt__tbh = register_jitable(iwzt__tbh)
        globals()[f'str_{func_name}'] = iwzt__tbh


_register_find_methods()


@register_jitable
def str_count(arr, pat, flags):
    ybb__ddm = arr._data
    dks__wku = arr._indices
    fkdk__ekzu = len(ybb__ddm)
    jvzj__wop = len(dks__wku)
    iqmcc__jmxxl = bodo.libs.int_arr_ext.alloc_int_array(fkdk__ekzu, np.int64)
    kpg__guvvx = bodo.libs.int_arr_ext.alloc_int_array(jvzj__wop, np.int64)
    regex = re.compile(pat, flags)
    for i in range(fkdk__ekzu):
        if bodo.libs.array_kernels.isna(ybb__ddm, i):
            bodo.libs.array_kernels.setna(iqmcc__jmxxl, i)
            continue
        iqmcc__jmxxl[i] = bodo.libs.str_ext.str_findall_count(regex,
            ybb__ddm[i])
    for i in range(jvzj__wop):
        if bodo.libs.array_kernels.isna(dks__wku, i
            ) or bodo.libs.array_kernels.isna(iqmcc__jmxxl, dks__wku[i]):
            bodo.libs.array_kernels.setna(kpg__guvvx, i)
        else:
            kpg__guvvx[i] = iqmcc__jmxxl[dks__wku[i]]
    return kpg__guvvx


@register_jitable
def str_len(arr):
    ybb__ddm = arr._data
    dks__wku = arr._indices
    jvzj__wop = len(dks__wku)
    iqmcc__jmxxl = bodo.libs.array_kernels.get_arr_lens(ybb__ddm, False)
    kpg__guvvx = bodo.libs.int_arr_ext.alloc_int_array(jvzj__wop, np.int64)
    for i in range(jvzj__wop):
        if bodo.libs.array_kernels.isna(dks__wku, i
            ) or bodo.libs.array_kernels.isna(iqmcc__jmxxl, dks__wku[i]):
            bodo.libs.array_kernels.setna(kpg__guvvx, i)
        else:
            kpg__guvvx[i] = iqmcc__jmxxl[dks__wku[i]]
    return kpg__guvvx


@register_jitable
def str_slice(arr, start, stop, step):
    ybb__ddm = arr._data
    fkdk__ekzu = len(ybb__ddm)
    oes__fnn = bodo.libs.str_arr_ext.pre_alloc_string_array(fkdk__ekzu, -1)
    for i in range(fkdk__ekzu):
        if bodo.libs.array_kernels.isna(ybb__ddm, i):
            bodo.libs.array_kernels.setna(oes__fnn, i)
            continue
        oes__fnn[i] = ybb__ddm[i][start:stop:step]
    return init_dict_arr(oes__fnn, arr._indices.copy(), arr.
        _has_global_dictionary, False)


@register_jitable
def str_get(arr, i):
    ybb__ddm = arr._data
    dks__wku = arr._indices
    fkdk__ekzu = len(ybb__ddm)
    jvzj__wop = len(dks__wku)
    oes__fnn = pre_alloc_string_array(fkdk__ekzu, -1)
    pib__farak = pre_alloc_string_array(jvzj__wop, -1)
    for iocvq__ecc in range(fkdk__ekzu):
        if bodo.libs.array_kernels.isna(ybb__ddm, iocvq__ecc) or not -len(
            ybb__ddm[iocvq__ecc]) <= i < len(ybb__ddm[iocvq__ecc]):
            bodo.libs.array_kernels.setna(oes__fnn, iocvq__ecc)
            continue
        oes__fnn[iocvq__ecc] = ybb__ddm[iocvq__ecc][i]
    for iocvq__ecc in range(jvzj__wop):
        if bodo.libs.array_kernels.isna(dks__wku, iocvq__ecc
            ) or bodo.libs.array_kernels.isna(oes__fnn, dks__wku[iocvq__ecc]):
            bodo.libs.array_kernels.setna(pib__farak, iocvq__ecc)
            continue
        pib__farak[iocvq__ecc] = oes__fnn[dks__wku[iocvq__ecc]]
    return pib__farak


@register_jitable
def str_repeat_int(arr, repeats):
    ybb__ddm = arr._data
    fkdk__ekzu = len(ybb__ddm)
    oes__fnn = pre_alloc_string_array(fkdk__ekzu, -1)
    for i in range(fkdk__ekzu):
        if bodo.libs.array_kernels.isna(ybb__ddm, i):
            bodo.libs.array_kernels.setna(oes__fnn, i)
            continue
        oes__fnn[i] = ybb__ddm[i] * repeats
    return init_dict_arr(oes__fnn, arr._indices.copy(), arr.
        _has_global_dictionary, arr._has_deduped_local_dictionary and 
        repeats != 0)


def create_str2bool_methods(func_name):
    dhu__ihazl = f"""def str_{func_name}(arr):
    data_arr = arr._data
    indices_arr = arr._indices
    n_data = len(data_arr)
    n_indices = len(indices_arr)
    out_dict_arr = bodo.libs.bool_arr_ext.alloc_bool_array(n_data)
    out_bool_arr = bodo.libs.bool_arr_ext.alloc_bool_array(n_indices)
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            bodo.libs.array_kernels.setna(out_dict_arr, i)
            continue
        out_dict_arr[i] = np.bool_(data_arr[i].{func_name}())
    for i in range(n_indices):
        if bodo.libs.array_kernels.isna(indices_arr, i) or bodo.libs.array_kernels.isna(
            data_arr, indices_arr[i]        ):
            bodo.libs.array_kernels.setna(out_bool_arr, i)
        else:
            out_bool_arr[i] = out_dict_arr[indices_arr[i]]
    return out_bool_arr"""
    crzr__vrn = {}
    exec(dhu__ihazl, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr}, crzr__vrn)
    return crzr__vrn[f'str_{func_name}']


def _register_str2bool_methods():
    for func_name in bodo.hiframes.pd_series_ext.str2bool_methods:
        iwzt__tbh = create_str2bool_methods(func_name)
        iwzt__tbh = register_jitable(iwzt__tbh)
        globals()[f'str_{func_name}'] = iwzt__tbh


_register_str2bool_methods()


@register_jitable
def str_extract(arr, pat, flags, n_cols):
    ybb__ddm = arr._data
    dks__wku = arr._indices
    fkdk__ekzu = len(ybb__ddm)
    jvzj__wop = len(dks__wku)
    regex = re.compile(pat, flags=flags)
    upzdm__znz = []
    for fobk__bdfi in range(n_cols):
        upzdm__znz.append(pre_alloc_string_array(fkdk__ekzu, -1))
    rrkx__mtg = bodo.libs.bool_arr_ext.alloc_bool_array(fkdk__ekzu)
    ltlzt__tbfa = dks__wku.copy()
    for i in range(fkdk__ekzu):
        if bodo.libs.array_kernels.isna(ybb__ddm, i):
            rrkx__mtg[i] = True
            for iocvq__ecc in range(n_cols):
                bodo.libs.array_kernels.setna(upzdm__znz[iocvq__ecc], i)
            continue
        zofvm__kcjvk = regex.search(ybb__ddm[i])
        if zofvm__kcjvk:
            rrkx__mtg[i] = False
            ohtkx__svsqu = zofvm__kcjvk.groups()
            for iocvq__ecc in range(n_cols):
                upzdm__znz[iocvq__ecc][i] = ohtkx__svsqu[iocvq__ecc]
        else:
            rrkx__mtg[i] = True
            for iocvq__ecc in range(n_cols):
                bodo.libs.array_kernels.setna(upzdm__znz[iocvq__ecc], i)
    for i in range(jvzj__wop):
        if rrkx__mtg[ltlzt__tbfa[i]]:
            bodo.libs.array_kernels.setna(ltlzt__tbfa, i)
    nklg__nqdnf = [init_dict_arr(upzdm__znz[i], ltlzt__tbfa.copy(), arr.
        _has_global_dictionary, False) for i in range(n_cols)]
    return nklg__nqdnf


def create_extractall_methods(is_multi_group):
    ilz__nzjv = '_multi' if is_multi_group else ''
    dhu__ihazl = f"""def str_extractall{ilz__nzjv}(arr, regex, n_cols, index_arr):
    data_arr = arr._data
    indices_arr = arr._indices
    n_data = len(data_arr)
    n_indices = len(indices_arr)
    indices_count = [0 for _ in range(n_data)]
    for i in range(n_indices):
        if not bodo.libs.array_kernels.isna(indices_arr, i):
            indices_count[indices_arr[i]] += 1
    dict_group_count = []
    out_dict_len = out_ind_len = 0
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            continue
        m = regex.findall(data_arr[i])
        dict_group_count.append((out_dict_len, len(m)))
        out_dict_len += len(m)
        out_ind_len += indices_count[i] * len(m)
    out_dict_arr_list = []
    for _ in range(n_cols):
        out_dict_arr_list.append(pre_alloc_string_array(out_dict_len, -1))
    out_indices_arr = bodo.libs.int_arr_ext.alloc_int_array(out_ind_len, np.int32)
    out_ind_arr = bodo.utils.utils.alloc_type(out_ind_len, index_arr, (-1,))
    out_match_arr = np.empty(out_ind_len, np.int64)
    curr_ind = 0
    for i in range(n_data):
        if bodo.libs.array_kernels.isna(data_arr, i):
            continue
        m = regex.findall(data_arr[i])
        for s in m:
            for j in range(n_cols):
                out_dict_arr_list[j][curr_ind] = s{'[j]' if is_multi_group else ''}
            curr_ind += 1
    curr_ind = 0
    for i in range(n_indices):
        if bodo.libs.array_kernels.isna(indices_arr, i):
            continue
        n_rows = dict_group_count[indices_arr[i]][1]
        for k in range(n_rows):
            out_indices_arr[curr_ind] = dict_group_count[indices_arr[i]][0] + k
            out_ind_arr[curr_ind] = index_arr[i]
            out_match_arr[curr_ind] = k
            curr_ind += 1
    out_arr_list = [
        init_dict_arr(
            out_dict_arr_list[i], out_indices_arr.copy(), arr._has_global_dictionary, False
        )
        for i in range(n_cols)
    ]
    return (out_ind_arr, out_match_arr, out_arr_list) 
"""
    crzr__vrn = {}
    exec(dhu__ihazl, {'bodo': bodo, 'numba': numba, 'np': np,
        'init_dict_arr': init_dict_arr, 'pre_alloc_string_array':
        pre_alloc_string_array}, crzr__vrn)
    return crzr__vrn[f'str_extractall{ilz__nzjv}']


def _register_extractall_methods():
    for is_multi_group in [True, False]:
        ilz__nzjv = '_multi' if is_multi_group else ''
        iwzt__tbh = create_extractall_methods(is_multi_group)
        iwzt__tbh = register_jitable(iwzt__tbh)
        globals()[f'str_extractall{ilz__nzjv}'] = iwzt__tbh


_register_extractall_methods()
