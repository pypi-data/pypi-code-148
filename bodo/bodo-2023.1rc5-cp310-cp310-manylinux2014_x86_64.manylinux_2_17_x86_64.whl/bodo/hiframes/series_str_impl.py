"""
Support for Series.str methods
"""
import operator
import re
import numba
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import StringIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.split_impl import get_split_view_data_ptr, get_split_view_index, string_array_split_view_type
from bodo.libs.array import get_search_regex
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.str_arr_ext import get_utf8_size, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import str_findall_count
from bodo.utils.typing import BodoError, create_unsupported_overload, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_str_len, is_bin_arr_type, is_list_like_index_type, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, is_str_arr_type, raise_bodo_error
from bodo.utils.utils import synchronize_error_njit


class SeriesStrMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        qrrr__gkgsl = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(qrrr__gkgsl)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        xnrkr__fbxgu = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, xnrkr__fbxgu)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        rxo__oyaqv, = args
        juj__keue = signature.return_type
        hqziq__yzdu = cgutils.create_struct_proxy(juj__keue)(context, builder)
        hqziq__yzdu.obj = rxo__oyaqv
        context.nrt.incref(builder, signature.args[0], rxo__oyaqv)
        return hqziq__yzdu._getvalue()
    return SeriesStrMethodType(obj)(obj), codegen


def str_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.UnicodeType) and not is_overload_constant_str(
        arg):
        raise_bodo_error(
            "Series.str.{}(): parameter '{}' expected a string object, not {}"
            .format(func_name, arg_name, arg))


def int_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.Integer) and not is_overload_constant_int(arg
        ):
        raise BodoError(
            "Series.str.{}(): parameter '{}' expected an int object, not {}"
            .format(func_name, arg_name, arg))


def not_supported_arg_check(func_name, arg_name, arg, defval):
    if arg_name == 'na':
        if not isinstance(arg, types.Omitted) and (not isinstance(arg,
            float) or not np.isnan(arg)):
            raise BodoError(
                "Series.str.{}(): parameter '{}' is not supported, default: np.nan"
                .format(func_name, arg_name))
    elif not isinstance(arg, types.Omitted) and arg != defval:
        raise BodoError(
            "Series.str.{}(): parameter '{}' is not supported, default: {}"
            .format(func_name, arg_name, defval))


def common_validate_padding(func_name, width, fillchar):
    if is_overload_constant_str(fillchar):
        if get_overload_const_str_len(fillchar) != 1:
            raise BodoError(
                'Series.str.{}(): fillchar must be a character, not str'.
                format(func_name))
    elif not isinstance(fillchar, types.UnicodeType):
        raise BodoError('Series.str.{}(): fillchar must be a character, not {}'
            .format(func_name, fillchar))
    int_arg_check(func_name, 'width', width)


@overload_attribute(SeriesType, 'str')
def overload_series_str(S):
    if not (is_str_arr_type(S.data) or S.data ==
        string_array_split_view_type or isinstance(S.data,
        ArrayItemArrayType) or is_bin_arr_type(S.data)):
        raise_bodo_error(
            'Series.str: input should be a series of string/binary or arrays')
    return lambda S: bodo.hiframes.series_str_impl.init_series_str_method(S)


@overload_method(SeriesStrMethodType, 'len', inline='always', no_unliteral=True
    )
def overload_str_method_len(S_str):
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_len_dict_impl(S_str):
            S = S_str._obj
            bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_len(bqxr__pbbg)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return _str_len_dict_impl

    def impl(S_str):
        S = S_str._obj
        bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
        tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
        qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(bqxr__pbbg, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, tnt__gkqh,
            qrrr__gkgsl)
    return impl


@overload_method(SeriesStrMethodType, 'split', inline='always',
    no_unliteral=True)
def overload_str_method_split(S_str, pat=None, n=-1, expand=False):
    if not is_overload_none(pat):
        str_arg_check('split', 'pat', pat)
    int_arg_check('split', 'n', n)
    not_supported_arg_check('split', 'expand', expand, False)
    if is_overload_constant_str(pat) and len(get_overload_const_str(pat)
        ) == 1 and get_overload_const_str(pat).isascii(
        ) and is_overload_constant_int(n) and get_overload_const_int(n
        ) == -1 and S_str.stype.data == string_array_type:

        def _str_split_view_impl(S_str, pat=None, n=-1, expand=False):
            S = S_str._obj
            bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(bqxr__pbbg,
                pat)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
        tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
        qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(bqxr__pbbg, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, tnt__gkqh,
            qrrr__gkgsl)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    maahh__awru = S_str.stype.data
    if (maahh__awru != string_array_split_view_type and not is_str_arr_type
        (maahh__awru)) and not isinstance(maahh__awru, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(maahh__awru, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(bqxr__pbbg, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return _str_get_array_impl
    if maahh__awru == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(bqxr__pbbg)
            amwz__dfek = 0
            for rfiqv__jyhak in numba.parfors.parfor.internal_prange(n):
                zelfx__bylr, zelfx__bylr, vcdki__droxs = get_split_view_index(
                    bqxr__pbbg, rfiqv__jyhak, i)
                amwz__dfek += vcdki__droxs
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, amwz__dfek)
            for kkzex__lzx in numba.parfors.parfor.internal_prange(n):
                skpv__tiwgr, jdvc__yxsf, vcdki__droxs = get_split_view_index(
                    bqxr__pbbg, kkzex__lzx, i)
                if skpv__tiwgr == 0:
                    bodo.libs.array_kernels.setna(out_arr, kkzex__lzx)
                    jpl__our = get_split_view_data_ptr(bqxr__pbbg, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr,
                        kkzex__lzx)
                    jpl__our = get_split_view_data_ptr(bqxr__pbbg, jdvc__yxsf)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    kkzex__lzx, jpl__our, vcdki__droxs)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return _str_get_split_impl
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_get_dict_impl(S_str, i):
            S = S_str._obj
            bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_get(bqxr__pbbg, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return _str_get_dict_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
        tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
        qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(bqxr__pbbg)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for kkzex__lzx in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(bqxr__pbbg, kkzex__lzx) or not len(
                bqxr__pbbg[kkzex__lzx]) > i >= -len(bqxr__pbbg[kkzex__lzx]):
                out_arr[kkzex__lzx] = ''
                bodo.libs.array_kernels.setna(out_arr, kkzex__lzx)
            else:
                out_arr[kkzex__lzx] = bqxr__pbbg[kkzex__lzx][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, tnt__gkqh,
            qrrr__gkgsl)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    maahh__awru = S_str.stype.data
    if (maahh__awru != string_array_split_view_type and maahh__awru !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(
        maahh__awru)):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        vbfp__xyc = bodo.hiframes.pd_series_ext.get_series_data(S)
        qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
        tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(vbfp__xyc)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for kkzex__lzx in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(vbfp__xyc, kkzex__lzx):
                out_arr[kkzex__lzx] = ''
                bodo.libs.array_kernels.setna(out_arr, kkzex__lzx)
            else:
                jhhr__jcg = vbfp__xyc[kkzex__lzx]
                out_arr[kkzex__lzx] = sep.join(jhhr__jcg)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, tnt__gkqh,
            qrrr__gkgsl)
    return impl


@overload_method(SeriesStrMethodType, 'replace', inline='always',
    no_unliteral=True)
def overload_str_method_replace(S_str, pat, repl, n=-1, case=None, flags=0,
    regex=True):
    not_supported_arg_check('replace', 'n', n, -1)
    not_supported_arg_check('replace', 'case', case, None)
    str_arg_check('replace', 'pat', pat)
    str_arg_check('replace', 'repl', repl)
    int_arg_check('replace', 'flags', flags)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_replace_dict_impl(S_str, pat, repl, n=-1, case=None, flags
            =0, regex=True):
            S = S_str._obj
            bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(bqxr__pbbg, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            eljqq__plrze = re.compile(pat, flags)
            yze__svnqv = len(bqxr__pbbg)
            out_arr = pre_alloc_string_array(yze__svnqv, -1)
            for kkzex__lzx in numba.parfors.parfor.internal_prange(yze__svnqv):
                if bodo.libs.array_kernels.isna(bqxr__pbbg, kkzex__lzx):
                    out_arr[kkzex__lzx] = ''
                    bodo.libs.array_kernels.setna(out_arr, kkzex__lzx)
                    continue
                out_arr[kkzex__lzx] = eljqq__plrze.sub(repl, bqxr__pbbg[
                    kkzex__lzx])
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
        tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
        qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        yze__svnqv = len(bqxr__pbbg)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(yze__svnqv, -1)
        for kkzex__lzx in numba.parfors.parfor.internal_prange(yze__svnqv):
            if bodo.libs.array_kernels.isna(bqxr__pbbg, kkzex__lzx):
                out_arr[kkzex__lzx] = ''
                bodo.libs.array_kernels.setna(out_arr, kkzex__lzx)
                continue
            out_arr[kkzex__lzx] = bqxr__pbbg[kkzex__lzx].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, tnt__gkqh,
            qrrr__gkgsl)
    return _str_replace_noregex_impl


@numba.njit
def series_contains_regex(S, pat, case, flags, na, regex):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = pd.array(S.array, 'string')._str_contains(pat, case,
            flags, na, regex)
    return out_arr


@numba.njit
def series_match_regex(S, pat, case, flags, na):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = S.array._str_match(pat, case, flags, na)
    return out_arr


def is_regex_unsupported(pat):
    xot__jjcwz = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(nzc__wai in pat) for nzc__wai in xot__jjcwz])
    else:
        return True


@overload_method(SeriesStrMethodType, 'contains', no_unliteral=True)
def overload_str_method_contains(S_str, pat, case=True, flags=0, na=np.nan,
    regex=True):
    not_supported_arg_check('contains', 'na', na, np.nan)
    str_arg_check('contains', 'pat', pat)
    int_arg_check('contains', 'flags', flags)
    if not is_overload_constant_bool(regex):
        raise BodoError(
            "Series.str.contains(): 'regex' argument should be a constant boolean"
            )
    if not is_overload_constant_bool(case):
        raise BodoError(
            "Series.str.contains(): 'case' argument should be a constant boolean"
            )
    qonk__slurn = re.IGNORECASE.value
    wqjx__pjpg = 'def impl(\n'
    wqjx__pjpg += '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n'
    wqjx__pjpg += '):\n'
    wqjx__pjpg += '  S = S_str._obj\n'
    wqjx__pjpg += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    wqjx__pjpg += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    wqjx__pjpg += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    wqjx__pjpg += '  l = len(arr)\n'
    wqjx__pjpg += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                wqjx__pjpg += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                wqjx__pjpg += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            wqjx__pjpg += """  get_search_regex(arr, case, False, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        wqjx__pjpg += (
            '  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)\n'
            )
    else:
        wqjx__pjpg += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            wqjx__pjpg += '  upper_pat = pat.upper()\n'
        wqjx__pjpg += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        wqjx__pjpg += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        wqjx__pjpg += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        wqjx__pjpg += '      else: \n'
        if is_overload_true(case):
            wqjx__pjpg += '          out_arr[i] = pat in arr[i]\n'
        else:
            wqjx__pjpg += (
                '          out_arr[i] = upper_pat in arr[i].upper()\n')
    wqjx__pjpg += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    zvxu__jcngi = {}
    exec(wqjx__pjpg, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': qonk__slurn, 'get_search_regex':
        get_search_regex}, zvxu__jcngi)
    impl = zvxu__jcngi['impl']
    return impl


@overload_method(SeriesStrMethodType, 'match', inline='always',
    no_unliteral=True)
def overload_str_method_match(S_str, pat, case=True, flags=0, na=np.nan):
    not_supported_arg_check('match', 'na', na, np.nan)
    str_arg_check('match', 'pat', pat)
    int_arg_check('match', 'flags', flags)
    if not is_overload_constant_bool(case):
        raise BodoError(
            "Series.str.match(): 'case' argument should be a constant boolean")
    qonk__slurn = re.IGNORECASE.value
    wqjx__pjpg = 'def impl(S_str, pat, case=True, flags=0, na=np.nan):\n'
    wqjx__pjpg += '        S = S_str._obj\n'
    wqjx__pjpg += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    wqjx__pjpg += '        l = len(arr)\n'
    wqjx__pjpg += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    wqjx__pjpg += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    if not is_regex_unsupported(pat) and flags == 0:
        wqjx__pjpg += (
            '        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        wqjx__pjpg += """        get_search_regex(arr, case, True, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        wqjx__pjpg += """        out_arr = bodo.libs.dict_arr_ext.str_match(arr, pat, case, flags, na)
"""
    else:
        wqjx__pjpg += (
            '        out_arr = series_match_regex(S, pat, case, flags, na)\n')
    wqjx__pjpg += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    zvxu__jcngi = {}
    exec(wqjx__pjpg, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': qonk__slurn, 'get_search_regex':
        get_search_regex}, zvxu__jcngi)
    impl = zvxu__jcngi['impl']
    return impl


@overload_method(SeriesStrMethodType, 'cat', no_unliteral=True)
def overload_str_method_cat(S_str, others=None, sep=None, na_rep=None, join
    ='left'):
    if not isinstance(others, DataFrameType):
        raise_bodo_error(
            "Series.str.cat(): 'others' must be a DataFrame currently")
    if not is_overload_none(sep):
        str_arg_check('cat', 'sep', sep)
    if not is_overload_constant_str(join) or get_overload_const_str(join
        ) != 'left':
        raise_bodo_error("Series.str.cat(): 'join' not supported yet")
    wqjx__pjpg = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    wqjx__pjpg += '  S = S_str._obj\n'
    wqjx__pjpg += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    wqjx__pjpg += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    wqjx__pjpg += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    wqjx__pjpg += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        wqjx__pjpg += f"""  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})
"""
    if S_str.stype.data == bodo.dict_str_arr_type and all(kpzh__ovp == bodo
        .dict_str_arr_type for kpzh__ovp in others.data):
        tebw__haci = ', '.join(f'data{i}' for i in range(len(others.columns)))
        wqjx__pjpg += (
            f'  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {tebw__haci}), sep)\n'
            )
    else:
        ttq__brn = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] + [
            f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len(
            others.columns))])
        wqjx__pjpg += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        wqjx__pjpg += '  numba.parfors.parfor.init_prange()\n'
        wqjx__pjpg += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        wqjx__pjpg += f'      if {ttq__brn}:\n'
        wqjx__pjpg += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        wqjx__pjpg += '          continue\n'
        hqz__hnwlk = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range(
            len(others.columns))])
        fds__uhwej = "''" if is_overload_none(sep) else 'sep'
        wqjx__pjpg += f'      out_arr[i] = {fds__uhwej}.join([{hqz__hnwlk}])\n'
    wqjx__pjpg += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    zvxu__jcngi = {}
    exec(wqjx__pjpg, {'bodo': bodo, 'numba': numba}, zvxu__jcngi)
    impl = zvxu__jcngi['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_count_dict_impl(S_str, pat, flags=0):
            S = S_str._obj
            bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_count(bqxr__pbbg, pat, flags)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return _str_count_dict_impl

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        vbfp__xyc = bodo.hiframes.pd_series_ext.get_series_data(S)
        qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
        tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
        eljqq__plrze = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        yze__svnqv = len(vbfp__xyc)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(yze__svnqv, np.int64)
        for i in numba.parfors.parfor.internal_prange(yze__svnqv):
            if bodo.libs.array_kernels.isna(vbfp__xyc, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(eljqq__plrze, vbfp__xyc[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, tnt__gkqh,
            qrrr__gkgsl)
    return impl


@overload_method(SeriesStrMethodType, 'find', inline='always', no_unliteral
    =True)
def overload_str_method_find(S_str, sub, start=0, end=None):
    str_arg_check('find', 'sub', sub)
    int_arg_check('find', 'start', start)
    if not is_overload_none(end):
        int_arg_check('find', 'end', end)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_find_dict_impl(S_str, sub, start=0, end=None):
            S = S_str._obj
            bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_find(bqxr__pbbg, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return _str_find_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        vbfp__xyc = bodo.hiframes.pd_series_ext.get_series_data(S)
        qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
        tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        yze__svnqv = len(vbfp__xyc)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(yze__svnqv, np.int64)
        for i in numba.parfors.parfor.internal_prange(yze__svnqv):
            if bodo.libs.array_kernels.isna(vbfp__xyc, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = vbfp__xyc[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, tnt__gkqh,
            qrrr__gkgsl)
    return impl


@overload_method(SeriesStrMethodType, 'rfind', inline='always',
    no_unliteral=True)
def overload_str_method_rfind(S_str, sub, start=0, end=None):
    str_arg_check('rfind', 'sub', sub)
    if start != 0:
        int_arg_check('rfind', 'start', start)
    if not is_overload_none(end):
        int_arg_check('rfind', 'end', end)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_rfind_dict_impl(S_str, sub, start=0, end=None):
            S = S_str._obj
            bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rfind(bqxr__pbbg, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return _str_rfind_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        vbfp__xyc = bodo.hiframes.pd_series_ext.get_series_data(S)
        qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
        tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        yze__svnqv = len(vbfp__xyc)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(yze__svnqv, np.int64)
        for i in numba.parfors.parfor.internal_prange(yze__svnqv):
            if bodo.libs.array_kernels.isna(vbfp__xyc, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = vbfp__xyc[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, tnt__gkqh,
            qrrr__gkgsl)
    return impl


@overload_method(SeriesStrMethodType, 'index', inline='always',
    no_unliteral=True)
def overload_str_method_index(S_str, sub, start=0, end=None):
    str_arg_check('index', 'sub', sub)
    int_arg_check('index', 'start', start)
    if not is_overload_none(end):
        int_arg_check('index', 'end', end)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_index_dict_impl(S_str, sub, start=0, end=None):
            S = S_str._obj
            bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_index(bqxr__pbbg, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return _str_index_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        vbfp__xyc = bodo.hiframes.pd_series_ext.get_series_data(S)
        qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
        tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
        yze__svnqv = len(vbfp__xyc)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(yze__svnqv, np.int64)
        numba.parfors.parfor.init_prange()
        ulauk__zmq = False
        for i in numba.parfors.parfor.internal_prange(yze__svnqv):
            if bodo.libs.array_kernels.isna(vbfp__xyc, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = vbfp__xyc[i].find(sub, start, end)
                if out_arr[i] == -1:
                    ulauk__zmq = True
        oaxl__rjo = 'substring not found' if ulauk__zmq else ''
        synchronize_error_njit('ValueError', oaxl__rjo)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, tnt__gkqh,
            qrrr__gkgsl)
    return impl


@overload_method(SeriesStrMethodType, 'rindex', inline='always',
    no_unliteral=True)
def overload_str_method_rindex(S_str, sub, start=0, end=None):
    str_arg_check('rindex', 'sub', sub)
    int_arg_check('rindex', 'start', start)
    if not is_overload_none(end):
        int_arg_check('rindex', 'end', end)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_rindex_dict_impl(S_str, sub, start=0, end=None):
            S = S_str._obj
            bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_rindex(bqxr__pbbg, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return _str_rindex_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        vbfp__xyc = bodo.hiframes.pd_series_ext.get_series_data(S)
        qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
        tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
        yze__svnqv = len(vbfp__xyc)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(yze__svnqv, np.int64)
        numba.parfors.parfor.init_prange()
        ulauk__zmq = False
        for i in numba.parfors.parfor.internal_prange(yze__svnqv):
            if bodo.libs.array_kernels.isna(vbfp__xyc, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = vbfp__xyc[i].rindex(sub, start, end)
                if out_arr[i] == -1:
                    ulauk__zmq = True
        oaxl__rjo = 'substring not found' if ulauk__zmq else ''
        synchronize_error_njit('ValueError', oaxl__rjo)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, tnt__gkqh,
            qrrr__gkgsl)
    return impl


@overload_method(SeriesStrMethodType, 'slice_replace', inline='always',
    no_unliteral=True)
def overload_str_method_slice_replace(S_str, start=0, stop=None, repl=''):
    int_arg_check('slice_replace', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice_replace', 'stop', stop)
    str_arg_check('slice_replace', 'repl', repl)

    def impl(S_str, start=0, stop=None, repl=''):
        S = S_str._obj
        vbfp__xyc = bodo.hiframes.pd_series_ext.get_series_data(S)
        qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
        tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        yze__svnqv = len(vbfp__xyc)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(yze__svnqv, -1)
        for kkzex__lzx in numba.parfors.parfor.internal_prange(yze__svnqv):
            if bodo.libs.array_kernels.isna(vbfp__xyc, kkzex__lzx):
                bodo.libs.array_kernels.setna(out_arr, kkzex__lzx)
            else:
                if stop is not None:
                    deadx__hggc = vbfp__xyc[kkzex__lzx][stop:]
                else:
                    deadx__hggc = ''
                out_arr[kkzex__lzx] = vbfp__xyc[kkzex__lzx][:start
                    ] + repl + deadx__hggc
        return bodo.hiframes.pd_series_ext.init_series(out_arr, tnt__gkqh,
            qrrr__gkgsl)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):
        if S_str.stype.data == bodo.dict_str_arr_type:

            def _str_repeat_int_dict_impl(S_str, repeats):
                S = S_str._obj
                bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
                tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
                qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
                out_arr = bodo.libs.dict_arr_ext.str_repeat_int(bqxr__pbbg,
                    repeats)
                return bodo.hiframes.pd_series_ext.init_series(out_arr,
                    tnt__gkqh, qrrr__gkgsl)
            return _str_repeat_int_dict_impl

        def impl(S_str, repeats):
            S = S_str._obj
            vbfp__xyc = bodo.hiframes.pd_series_ext.get_series_data(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            yze__svnqv = len(vbfp__xyc)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(yze__svnqv,
                -1)
            for kkzex__lzx in numba.parfors.parfor.internal_prange(yze__svnqv):
                if bodo.libs.array_kernels.isna(vbfp__xyc, kkzex__lzx):
                    bodo.libs.array_kernels.setna(out_arr, kkzex__lzx)
                else:
                    out_arr[kkzex__lzx] = vbfp__xyc[kkzex__lzx] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return impl
    elif is_overload_constant_list(repeats):
        zipza__bvlw = get_overload_const_list(repeats)
        xvkul__hzx = all([isinstance(uzv__ngbh, int) for uzv__ngbh in
            zipza__bvlw])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        xvkul__hzx = True
    else:
        xvkul__hzx = False
    if xvkul__hzx:

        def impl(S_str, repeats):
            S = S_str._obj
            vbfp__xyc = bodo.hiframes.pd_series_ext.get_series_data(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            bbagr__wbzf = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            yze__svnqv = len(vbfp__xyc)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(yze__svnqv,
                -1)
            for kkzex__lzx in numba.parfors.parfor.internal_prange(yze__svnqv):
                if bodo.libs.array_kernels.isna(vbfp__xyc, kkzex__lzx):
                    bodo.libs.array_kernels.setna(out_arr, kkzex__lzx)
                else:
                    out_arr[kkzex__lzx] = vbfp__xyc[kkzex__lzx] * bbagr__wbzf[
                        kkzex__lzx]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return impl
    else:
        raise BodoError(
            'Series.str.repeat(): repeats argument must either be an integer or a sequence of integers'
            )


def create_ljust_rjust_center_overload(func_name):
    wqjx__pjpg = f"""def dict_impl(S_str, width, fillchar=' '):
    S = S_str._obj
    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    out_arr = bodo.libs.dict_arr_ext.str_{func_name}(arr, width, fillchar)
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
def impl(S_str, width, fillchar=' '):
    S = S_str._obj
    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    numba.parfors.parfor.init_prange()
    l = len(str_arr)
    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
    for j in numba.parfors.parfor.internal_prange(l):
        if bodo.libs.array_kernels.isna(str_arr, j):
            bodo.libs.array_kernels.setna(out_arr, j)
        else:
            out_arr[j] = str_arr[j].{func_name}(width, fillchar)
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    zvxu__jcngi = {}
    wbn__ogvps = {'bodo': bodo, 'numba': numba}
    exec(wqjx__pjpg, wbn__ogvps, zvxu__jcngi)
    impl = zvxu__jcngi['impl']
    akvl__snd = zvxu__jcngi['dict_impl']

    def overload_ljust_rjust_center_method(S_str, width, fillchar=' '):
        common_validate_padding(func_name, width, fillchar)
        if S_str.stype.data == bodo.dict_str_arr_type:
            return akvl__snd
        return impl
    return overload_ljust_rjust_center_method


def _install_ljust_rjust_center():
    for nrn__hbww in ['ljust', 'rjust', 'center']:
        impl = create_ljust_rjust_center_overload(nrn__hbww)
        overload_method(SeriesStrMethodType, nrn__hbww, inline='always',
            no_unliteral=True)(impl)


_install_ljust_rjust_center()


@overload_method(SeriesStrMethodType, 'pad', no_unliteral=True)
def overload_str_method_pad(S_str, width, side='left', fillchar=' '):
    common_validate_padding('pad', width, fillchar)
    if is_overload_constant_str(side):
        if get_overload_const_str(side) not in ['left', 'right', 'both']:
            raise BodoError('Series.str.pad(): Invalid Side')
    else:
        raise BodoError('Series.str.pad(): Invalid Side')
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_pad_dict_impl(S_str, width, side='left', fillchar=' '):
            S = S_str._obj
            bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            if side == 'left':
                out_arr = bodo.libs.dict_arr_ext.str_rjust(bqxr__pbbg,
                    width, fillchar)
            elif side == 'right':
                out_arr = bodo.libs.dict_arr_ext.str_ljust(bqxr__pbbg,
                    width, fillchar)
            elif side == 'both':
                out_arr = bodo.libs.dict_arr_ext.str_center(bqxr__pbbg,
                    width, fillchar)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return _str_pad_dict_impl

    def impl(S_str, width, side='left', fillchar=' '):
        S = S_str._obj
        vbfp__xyc = bodo.hiframes.pd_series_ext.get_series_data(S)
        qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
        tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        yze__svnqv = len(vbfp__xyc)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(yze__svnqv, -1)
        for kkzex__lzx in numba.parfors.parfor.internal_prange(yze__svnqv):
            if bodo.libs.array_kernels.isna(vbfp__xyc, kkzex__lzx):
                out_arr[kkzex__lzx] = ''
                bodo.libs.array_kernels.setna(out_arr, kkzex__lzx)
            elif side == 'left':
                out_arr[kkzex__lzx] = vbfp__xyc[kkzex__lzx].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[kkzex__lzx] = vbfp__xyc[kkzex__lzx].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[kkzex__lzx] = vbfp__xyc[kkzex__lzx].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, tnt__gkqh,
            qrrr__gkgsl)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_zfill_dict_impl(S_str, width):
            S = S_str._obj
            bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_zfill(bqxr__pbbg, width)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return _str_zfill_dict_impl

    def impl(S_str, width):
        S = S_str._obj
        vbfp__xyc = bodo.hiframes.pd_series_ext.get_series_data(S)
        qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
        tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        yze__svnqv = len(vbfp__xyc)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(yze__svnqv, -1)
        for kkzex__lzx in numba.parfors.parfor.internal_prange(yze__svnqv):
            if bodo.libs.array_kernels.isna(vbfp__xyc, kkzex__lzx):
                out_arr[kkzex__lzx] = ''
                bodo.libs.array_kernels.setna(out_arr, kkzex__lzx)
            else:
                out_arr[kkzex__lzx] = vbfp__xyc[kkzex__lzx].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, tnt__gkqh,
            qrrr__gkgsl)
    return impl


@overload_method(SeriesStrMethodType, 'slice', no_unliteral=True)
def overload_str_method_slice(S_str, start=None, stop=None, step=None):
    if not is_overload_none(start):
        int_arg_check('slice', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice', 'stop', stop)
    if not is_overload_none(step):
        int_arg_check('slice', 'step', step)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_slice_dict_impl(S_str, start=None, stop=None, step=None):
            S = S_str._obj
            bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_slice(bqxr__pbbg, start,
                stop, step)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return _str_slice_dict_impl

    def impl(S_str, start=None, stop=None, step=None):
        S = S_str._obj
        vbfp__xyc = bodo.hiframes.pd_series_ext.get_series_data(S)
        qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
        tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        yze__svnqv = len(vbfp__xyc)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(yze__svnqv, -1)
        for kkzex__lzx in numba.parfors.parfor.internal_prange(yze__svnqv):
            if bodo.libs.array_kernels.isna(vbfp__xyc, kkzex__lzx):
                out_arr[kkzex__lzx] = ''
                bodo.libs.array_kernels.setna(out_arr, kkzex__lzx)
            else:
                out_arr[kkzex__lzx] = vbfp__xyc[kkzex__lzx][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, tnt__gkqh,
            qrrr__gkgsl)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(bqxr__pbbg, pat, na
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        vbfp__xyc = bodo.hiframes.pd_series_ext.get_series_data(S)
        qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
        tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        yze__svnqv = len(vbfp__xyc)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(yze__svnqv)
        for i in numba.parfors.parfor.internal_prange(yze__svnqv):
            if bodo.libs.array_kernels.isna(vbfp__xyc, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = vbfp__xyc[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, tnt__gkqh,
            qrrr__gkgsl)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
            tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
            qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(bqxr__pbbg, pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                tnt__gkqh, qrrr__gkgsl)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        vbfp__xyc = bodo.hiframes.pd_series_ext.get_series_data(S)
        qrrr__gkgsl = bodo.hiframes.pd_series_ext.get_series_name(S)
        tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        yze__svnqv = len(vbfp__xyc)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(yze__svnqv)
        for i in numba.parfors.parfor.internal_prange(yze__svnqv):
            if bodo.libs.array_kernels.isna(vbfp__xyc, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = vbfp__xyc[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, tnt__gkqh,
            qrrr__gkgsl)
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_str_method_getitem(S_str, ind):
    if not isinstance(S_str, SeriesStrMethodType):
        return
    if not isinstance(types.unliteral(ind), (types.SliceType, types.Integer)):
        raise BodoError(
            'index input to Series.str[] should be a slice or an integer')
    if isinstance(ind, types.SliceType):
        return lambda S_str, ind: S_str.slice(ind.start, ind.stop, ind.step)
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda S_str, ind: S_str.get(ind)


@overload_method(SeriesStrMethodType, 'extract', inline='always',
    no_unliteral=True)
def overload_str_method_extract(S_str, pat, flags=0, expand=True):
    if not is_overload_constant_bool(expand):
        raise BodoError(
            "Series.str.extract(): 'expand' argument should be a constant bool"
            )
    wpcvz__kzwy, regex = _get_column_names_from_regex(pat, flags, 'extract')
    bvu__lgs = len(wpcvz__kzwy)
    if S_str.stype.data == bodo.dict_str_arr_type:
        wqjx__pjpg = 'def impl(S_str, pat, flags=0, expand=True):\n'
        wqjx__pjpg += '  S = S_str._obj\n'
        wqjx__pjpg += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        wqjx__pjpg += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        wqjx__pjpg += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        wqjx__pjpg += f"""  out_arr_list = bodo.libs.dict_arr_ext.str_extract(arr, pat, flags, {bvu__lgs})
"""
        for i in range(bvu__lgs):
            wqjx__pjpg += f'  out_arr_{i} = out_arr_list[{i}]\n'
    else:
        wqjx__pjpg = 'def impl(S_str, pat, flags=0, expand=True):\n'
        wqjx__pjpg += '  regex = re.compile(pat, flags=flags)\n'
        wqjx__pjpg += '  S = S_str._obj\n'
        wqjx__pjpg += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        wqjx__pjpg += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        wqjx__pjpg += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        wqjx__pjpg += '  numba.parfors.parfor.init_prange()\n'
        wqjx__pjpg += '  n = len(str_arr)\n'
        for i in range(bvu__lgs):
            wqjx__pjpg += (
                '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
                .format(i))
        wqjx__pjpg += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        wqjx__pjpg += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        for i in range(bvu__lgs):
            wqjx__pjpg += "          out_arr_{}[j] = ''\n".format(i)
            wqjx__pjpg += (
                '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
                format(i))
        wqjx__pjpg += '      else:\n'
        wqjx__pjpg += '          m = regex.search(str_arr[j])\n'
        wqjx__pjpg += '          if m:\n'
        wqjx__pjpg += '            g = m.groups()\n'
        for i in range(bvu__lgs):
            wqjx__pjpg += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
        wqjx__pjpg += '          else:\n'
        for i in range(bvu__lgs):
            wqjx__pjpg += "            out_arr_{}[j] = ''\n".format(i)
            wqjx__pjpg += (
                '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'
                .format(i))
    if is_overload_false(expand) and regex.groups == 1:
        qrrr__gkgsl = "'{}'".format(list(regex.groupindex.keys()).pop()
            ) if len(regex.groupindex.keys()) > 0 else 'name'
        wqjx__pjpg += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(qrrr__gkgsl))
        zvxu__jcngi = {}
        exec(wqjx__pjpg, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, zvxu__jcngi)
        impl = zvxu__jcngi['impl']
        return impl
    zkys__qplb = ', '.join('out_arr_{}'.format(i) for i in range(bvu__lgs))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(wqjx__pjpg,
        wpcvz__kzwy, zkys__qplb, 'index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    wpcvz__kzwy, zelfx__bylr = _get_column_names_from_regex(pat, flags,
        'extractall')
    bvu__lgs = len(wpcvz__kzwy)
    qqrs__sxn = isinstance(S_str.stype.index, StringIndexType)
    czm__yuhdr = bvu__lgs > 1
    xmxe__ocy = '_multi' if czm__yuhdr else ''
    if S_str.stype.data == bodo.dict_str_arr_type:
        wqjx__pjpg = 'def impl(S_str, pat, flags=0):\n'
        wqjx__pjpg += '  S = S_str._obj\n'
        wqjx__pjpg += (
            '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        wqjx__pjpg += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        wqjx__pjpg += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        wqjx__pjpg += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        wqjx__pjpg += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        wqjx__pjpg += '  regex = re.compile(pat, flags=flags)\n'
        wqjx__pjpg += '  out_ind_arr, out_match_arr, out_arr_list = '
        wqjx__pjpg += f'bodo.libs.dict_arr_ext.str_extractall{xmxe__ocy}(\n'
        wqjx__pjpg += f'arr, regex, {bvu__lgs}, index_arr)\n'
        for i in range(bvu__lgs):
            wqjx__pjpg += f'  out_arr_{i} = out_arr_list[{i}]\n'
        wqjx__pjpg += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        wqjx__pjpg += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    else:
        wqjx__pjpg = 'def impl(S_str, pat, flags=0):\n'
        wqjx__pjpg += '  regex = re.compile(pat, flags=flags)\n'
        wqjx__pjpg += '  S = S_str._obj\n'
        wqjx__pjpg += (
            '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        wqjx__pjpg += (
            '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        wqjx__pjpg += (
            '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        wqjx__pjpg += (
            '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
        wqjx__pjpg += (
            '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n'
            )
        wqjx__pjpg += '  numba.parfors.parfor.init_prange()\n'
        wqjx__pjpg += '  n = len(str_arr)\n'
        wqjx__pjpg += '  out_n_l = [0]\n'
        for i in range(bvu__lgs):
            wqjx__pjpg += '  num_chars_{} = 0\n'.format(i)
        if qqrs__sxn:
            wqjx__pjpg += '  index_num_chars = 0\n'
        wqjx__pjpg += '  for i in numba.parfors.parfor.internal_prange(n):\n'
        if qqrs__sxn:
            wqjx__pjpg += (
                '      index_num_chars += get_utf8_size(index_arr[i])\n')
        wqjx__pjpg += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
        wqjx__pjpg += '          continue\n'
        wqjx__pjpg += '      m = regex.findall(str_arr[i])\n'
        wqjx__pjpg += '      out_n_l[0] += len(m)\n'
        for i in range(bvu__lgs):
            wqjx__pjpg += '      l_{} = 0\n'.format(i)
        wqjx__pjpg += '      for s in m:\n'
        for i in range(bvu__lgs):
            wqjx__pjpg += '        l_{} += get_utf8_size(s{})\n'.format(i, 
                '[{}]'.format(i) if bvu__lgs > 1 else '')
        for i in range(bvu__lgs):
            wqjx__pjpg += '      num_chars_{0} += l_{0}\n'.format(i)
        wqjx__pjpg += (
            '  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)\n'
            )
        for i in range(bvu__lgs):
            wqjx__pjpg += (
                """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
                .format(i))
        if qqrs__sxn:
            wqjx__pjpg += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
        else:
            wqjx__pjpg += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
        wqjx__pjpg += '  out_match_arr = np.empty(out_n, np.int64)\n'
        wqjx__pjpg += '  out_ind = 0\n'
        wqjx__pjpg += '  for j in numba.parfors.parfor.internal_prange(n):\n'
        wqjx__pjpg += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
        wqjx__pjpg += '          continue\n'
        wqjx__pjpg += '      m = regex.findall(str_arr[j])\n'
        wqjx__pjpg += '      for k, s in enumerate(m):\n'
        for i in range(bvu__lgs):
            wqjx__pjpg += (
                """        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})
"""
                .format(i, '[{}]'.format(i) if bvu__lgs > 1 else ''))
        wqjx__pjpg += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
        wqjx__pjpg += """        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)
"""
        wqjx__pjpg += '        out_ind += 1\n'
        wqjx__pjpg += (
            '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n'
            )
        wqjx__pjpg += (
            "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    zkys__qplb = ', '.join('out_arr_{}'.format(i) for i in range(bvu__lgs))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(wqjx__pjpg,
        wpcvz__kzwy, zkys__qplb, 'out_index', extra_globals={
        'get_utf8_size': get_utf8_size, 're': re})
    return impl


def _get_column_names_from_regex(pat, flags, func_name):
    if not is_overload_constant_str(pat):
        raise BodoError(
            "Series.str.{}(): 'pat' argument should be a constant string".
            format(func_name))
    if not is_overload_constant_int(flags):
        raise BodoError(
            "Series.str.{}(): 'flags' argument should be a constant int".
            format(func_name))
    pat = get_overload_const_str(pat)
    flags = get_overload_const_int(flags)
    regex = re.compile(pat, flags=flags)
    if regex.groups == 0:
        raise BodoError(
            'Series.str.{}(): pattern {} contains no capture groups'.format
            (func_name, pat))
    uyc__ttiw = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
    wpcvz__kzwy = [uyc__ttiw.get(1 + i, i) for i in range(regex.groups)]
    return wpcvz__kzwy, regex


def create_str2str_methods_overload(func_name):
    tdta__hat = func_name in ['lstrip', 'rstrip', 'strip']
    wqjx__pjpg = f"""def f({'S_str, to_strip=None' if tdta__hat else 'S_str'}):
    S = S_str._obj
    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    str_arr = decode_if_dict_array(str_arr)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    numba.parfors.parfor.init_prange()
    n = len(str_arr)
    num_chars = {'-1' if tdta__hat else 'num_total_chars(str_arr)'}
    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)
    for j in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(str_arr, j):
            out_arr[j] = ""
            bodo.libs.array_kernels.setna(out_arr, j)
        else:
            out_arr[j] = str_arr[j].{func_name}({'to_strip' if tdta__hat else ''})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    wqjx__pjpg += f"""def _dict_impl({'S_str, to_strip=None' if tdta__hat else 'S_str'}):
    S = S_str._obj
    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    out_arr = bodo.libs.dict_arr_ext.str_{func_name}({'arr, to_strip' if tdta__hat else 'arr'})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    zvxu__jcngi = {}
    exec(wqjx__pjpg, {'bodo': bodo, 'numba': numba, 'num_total_chars': bodo
        .libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, zvxu__jcngi)
    ytnam__hpdxo = zvxu__jcngi['f']
    aefb__yuv = zvxu__jcngi['_dict_impl']
    if tdta__hat:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            if S_str.stype.data == bodo.dict_str_arr_type:
                return aefb__yuv
            return ytnam__hpdxo
        return overload_strip_method
    else:

        def overload_str_method_dict_supported(S_str):
            if S_str.stype.data == bodo.dict_str_arr_type:
                return aefb__yuv
            return ytnam__hpdxo
        return overload_str_method_dict_supported


def create_str2bool_methods_overload(func_name):
    wqjx__pjpg = 'def dict_impl(S_str):\n'
    wqjx__pjpg += '    S = S_str._obj\n'
    wqjx__pjpg += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    wqjx__pjpg += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    wqjx__pjpg += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    wqjx__pjpg += (
        f'    out_arr = bodo.libs.dict_arr_ext.str_{func_name}(arr)\n')
    wqjx__pjpg += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    wqjx__pjpg += 'def impl(S_str):\n'
    wqjx__pjpg += '    S = S_str._obj\n'
    wqjx__pjpg += (
        '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    wqjx__pjpg += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    wqjx__pjpg += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    wqjx__pjpg += '    numba.parfors.parfor.init_prange()\n'
    wqjx__pjpg += '    l = len(str_arr)\n'
    wqjx__pjpg += '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    wqjx__pjpg += '    for i in numba.parfors.parfor.internal_prange(l):\n'
    wqjx__pjpg += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
    wqjx__pjpg += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
    wqjx__pjpg += '        else:\n'
    wqjx__pjpg += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'.
        format(func_name))
    wqjx__pjpg += '    return bodo.hiframes.pd_series_ext.init_series(\n'
    wqjx__pjpg += '      out_arr,index, name)\n'
    zvxu__jcngi = {}
    exec(wqjx__pjpg, {'bodo': bodo, 'numba': numba, 'np': np}, zvxu__jcngi)
    impl = zvxu__jcngi['impl']
    akvl__snd = zvxu__jcngi['dict_impl']

    def overload_str2bool_methods(S_str):
        if S_str.stype.data == bodo.dict_str_arr_type:
            return akvl__snd
        return impl
    return overload_str2bool_methods


def _install_str2str_methods():
    for jnvz__uwd in bodo.hiframes.pd_series_ext.str2str_methods:
        htbcb__ynlcg = create_str2str_methods_overload(jnvz__uwd)
        overload_method(SeriesStrMethodType, jnvz__uwd, inline='always',
            no_unliteral=True)(htbcb__ynlcg)


def _install_str2bool_methods():
    for jnvz__uwd in bodo.hiframes.pd_series_ext.str2bool_methods:
        htbcb__ynlcg = create_str2bool_methods_overload(jnvz__uwd)
        overload_method(SeriesStrMethodType, jnvz__uwd, inline='always',
            no_unliteral=True)(htbcb__ynlcg)


_install_str2str_methods()
_install_str2bool_methods()


@overload_attribute(SeriesType, 'cat')
def overload_series_cat(s):
    if not isinstance(s.dtype, bodo.hiframes.pd_categorical_ext.
        PDCategoricalDtype):
        raise BodoError('Can only use .cat accessor with categorical values.')
    return lambda s: bodo.hiframes.series_str_impl.init_series_cat_method(s)


class SeriesCatMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        qrrr__gkgsl = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(qrrr__gkgsl)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        xnrkr__fbxgu = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, xnrkr__fbxgu)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        rxo__oyaqv, = args
        vlj__ugirc = signature.return_type
        fsh__stfcx = cgutils.create_struct_proxy(vlj__ugirc)(context, builder)
        fsh__stfcx.obj = rxo__oyaqv
        context.nrt.incref(builder, signature.args[0], rxo__oyaqv)
        return fsh__stfcx._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        bqxr__pbbg = bodo.hiframes.pd_series_ext.get_series_data(S)
        tnt__gkqh = bodo.hiframes.pd_series_ext.get_series_index(S)
        qrrr__gkgsl = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(bqxr__pbbg),
            tnt__gkqh, qrrr__gkgsl)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for cwaph__chg in unsupported_cat_attrs:
        iiqj__whv = 'Series.cat.' + cwaph__chg
        overload_attribute(SeriesCatMethodType, cwaph__chg)(
            create_unsupported_overload(iiqj__whv))
    for vwmgl__rywkd in unsupported_cat_methods:
        iiqj__whv = 'Series.cat.' + vwmgl__rywkd
        overload_method(SeriesCatMethodType, vwmgl__rywkd)(
            create_unsupported_overload(iiqj__whv))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for vwmgl__rywkd in unsupported_str_methods:
        iiqj__whv = 'Series.str.' + vwmgl__rywkd
        overload_method(SeriesStrMethodType, vwmgl__rywkd)(
            create_unsupported_overload(iiqj__whv))


_install_strseries_unsupported()
