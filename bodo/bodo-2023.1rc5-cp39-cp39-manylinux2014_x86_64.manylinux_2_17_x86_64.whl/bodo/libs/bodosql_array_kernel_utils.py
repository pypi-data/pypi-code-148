"""
Common utilities for all BodoSQL array kernels
"""
import math
import re
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from numba.core import types
import bodo
from bodo.hiframes.datetime_timedelta_ext import PDTimeDeltaType
from bodo.hiframes.pd_series_ext import is_datetime_date_series_typ, is_timedelta64_series_typ, pd_timedelta_type, pd_timestamp_tz_naive_type
from bodo.utils.typing import is_overload_bool, is_overload_constant_bool, is_overload_constant_bytes, is_overload_constant_number, is_overload_constant_str, is_overload_float, is_overload_int, is_overload_none, raise_bodo_error


def indent_block(text, indentation):
    if text is None:
        return ''
    tfhna__jsglx = text.splitlines()[0]
    i = len(tfhna__jsglx) - len(tfhna__jsglx.lstrip())
    return '\n'.join([(' ' * indentation + pkiw__bqjes[i:]) for pkiw__bqjes in
        text.splitlines()]) + '\n'


def gen_vectorized(arg_names, arg_types, propagate_null, scalar_text,
    out_dtype, arg_string=None, arg_sources=None, array_override=None,
    support_dict_encoding=True, may_cause_duplicate_dict_array_values=False,
    prefix_code=None, suffix_code=None, res_list=False, extra_globals=None,
    alloc_array_scalars=True, synthesize_dict_if_vector=None,
    synthesize_dict_setup_text=None, synthesize_dict_scalar_text=None,
    synthesize_dict_global=False, synthesize_dict_unique=False):
    assert not (res_list and support_dict_encoding
        ), 'Cannot use res_list with support_dict_encoding'
    fit__gljao = [bodo.utils.utils.is_array_typ(mwupw__qzd, True) for
        mwupw__qzd in arg_types]
    kozho__zqvk = not any(fit__gljao)
    xoiai__mmw = any([propagate_null[i] for i in range(len(arg_types)) if 
        arg_types[i] == bodo.none])
    owsf__tpgfj = False
    if synthesize_dict_if_vector is not None:
        assert synthesize_dict_setup_text is not None, 'synthesize_dict_setup_text must be provided if synthesize_dict_if_vector is provided'
        assert synthesize_dict_scalar_text is not None, 'synthesize_dict_scalar_text must be provided if synthesize_dict_if_vector is provided'
        owsf__tpgfj = True
        for i in range(len(arg_types)):
            if fit__gljao[i] and synthesize_dict_if_vector[i] == 'S':
                owsf__tpgfj = False
            if not fit__gljao[i] and synthesize_dict_if_vector[i] == 'V':
                owsf__tpgfj = False
    qxa__snywk = 0
    izkol__xgqj = -1
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            qxa__snywk += 1
            if arg_types[i] == bodo.dict_str_arr_type:
                izkol__xgqj = i
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            qxa__snywk += 1
            if arg_types[i].data == bodo.dict_str_arr_type:
                izkol__xgqj = i
    xhtcp__qmc = support_dict_encoding and qxa__snywk == 1 and izkol__xgqj >= 0
    bsw__uzcri = xhtcp__qmc and out_dtype == bodo.string_array_type and (any
        (arg_types[i] == bodo.none and propagate_null[i] for i in range(len
        (arg_types))) or 'bodo.libs.array_kernels.setna' in scalar_text)
    if arg_string is None:
        arg_string = ', '.join(arg_names)
    dnymf__ysfz = f'def impl({arg_string}):\n'
    if arg_sources is not None:
        for zcnyo__pvp, sulbe__qdyeq in arg_sources.items():
            dnymf__ysfz += f'   {zcnyo__pvp} = {sulbe__qdyeq}\n'
    if kozho__zqvk and array_override == None:
        if xoiai__mmw:
            dnymf__ysfz += '   return None'
        else:
            dnymf__ysfz += indent_block(prefix_code, 3)
            for i in range(len(arg_names)):
                dnymf__ysfz += f'   arg{i} = {arg_names[i]}\n'
            zwrzg__jnxyl = scalar_text.replace('res[i] =', 'answer =').replace(
                'bodo.libs.array_kernels.setna(res, i)', 'return None')
            dnymf__ysfz += indent_block(zwrzg__jnxyl, 3)
            dnymf__ysfz += '   return answer'
    else:
        for i in range(len(arg_names)):
            if bodo.hiframes.pd_series_ext.is_series_type(arg_types[i]):
                dnymf__ysfz += f"""   {arg_names[i]} = bodo.hiframes.pd_series_ext.get_series_data({arg_names[i]})
"""
        if array_override != None:
            plr__jgsu = f'len({array_override})'
        else:
            for i in range(len(arg_names)):
                if fit__gljao[i]:
                    plr__jgsu = f'len({arg_names[i]})'
                    break
        if xhtcp__qmc:
            if out_dtype == bodo.string_array_type:
                dnymf__ysfz += (
                    f'   indices = {arg_names[izkol__xgqj]}._indices.copy()\n')
                dnymf__ysfz += (
                    f'   has_global = {arg_names[izkol__xgqj]}._has_global_dictionary\n'
                    )
                if may_cause_duplicate_dict_array_values:
                    dnymf__ysfz += f'   is_dict_unique = False\n'
                else:
                    dnymf__ysfz += f"""   is_dict_unique = {arg_names[izkol__xgqj]}._has_deduped_local_dictionary
"""
                dnymf__ysfz += (
                    f'   {arg_names[i]} = {arg_names[izkol__xgqj]}._data\n')
            else:
                dnymf__ysfz += (
                    f'   indices = {arg_names[izkol__xgqj]}._indices\n')
                dnymf__ysfz += (
                    f'   {arg_names[i]} = {arg_names[izkol__xgqj]}._data\n')
        dnymf__ysfz += f'   n = {plr__jgsu}\n'
        if prefix_code is not None and not xoiai__mmw:
            dnymf__ysfz += indent_block(prefix_code, 3)
        if owsf__tpgfj:
            dnymf__ysfz += indent_block(synthesize_dict_setup_text, 3)
            out_dtype = bodo.libs.dict_arr_ext.dict_indices_arr_type
            dnymf__ysfz += (
                '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
            dnymf__ysfz += '   numba.parfors.parfor.init_prange()\n'
            dnymf__ysfz += (
                '   for i in numba.parfors.parfor.internal_prange(n):\n')
        elif xhtcp__qmc:
            cdzyk__vbfgc = 'n' if propagate_null[izkol__xgqj] else '(n + 1)'
            if not propagate_null[izkol__xgqj]:
                jbmw__xxib = arg_names[izkol__xgqj]
                dnymf__ysfz += f"""   {jbmw__xxib} = bodo.libs.array_kernels.concat([{jbmw__xxib}, bodo.libs.array_kernels.gen_na_array(1, {jbmw__xxib})])
"""
            if out_dtype == bodo.string_array_type:
                dnymf__ysfz += f"""   res = bodo.libs.str_arr_ext.pre_alloc_string_array({cdzyk__vbfgc}, -1)
"""
            else:
                dnymf__ysfz += f"""   res = bodo.utils.utils.alloc_type({cdzyk__vbfgc}, out_dtype, (-1,))
"""
            dnymf__ysfz += f'   for i in range({cdzyk__vbfgc}):\n'
        elif res_list:
            dnymf__ysfz += '   res = []\n'
            dnymf__ysfz += '   for i in range(n):\n'
        else:
            dnymf__ysfz += (
                '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
            dnymf__ysfz += '   numba.parfors.parfor.init_prange()\n'
            dnymf__ysfz += (
                '   for i in numba.parfors.parfor.internal_prange(n):\n')
        if xoiai__mmw:
            dnymf__ysfz += f'      bodo.libs.array_kernels.setna(res, i)\n'
        else:
            for i in range(len(arg_names)):
                if fit__gljao[i]:
                    if propagate_null[i]:
                        dnymf__ysfz += f"""      if bodo.libs.array_kernels.isna({arg_names[i]}, i):
"""
                        if res_list:
                            dnymf__ysfz += '         res.append(None)\n'
                        else:
                            dnymf__ysfz += (
                                '         bodo.libs.array_kernels.setna(res, i)\n'
                                )
                        dnymf__ysfz += '         continue\n'
            for i in range(len(arg_names)):
                if fit__gljao[i]:
                    if alloc_array_scalars:
                        dnymf__ysfz += f'      arg{i} = {arg_names[i]}[i]\n'
                else:
                    dnymf__ysfz += f'      arg{i} = {arg_names[i]}\n'
            if not owsf__tpgfj:
                dnymf__ysfz += indent_block(scalar_text, 6)
            else:
                dnymf__ysfz += indent_block(synthesize_dict_scalar_text, 6)
        if xhtcp__qmc:
            if bsw__uzcri:
                dnymf__ysfz += '   numba.parfors.parfor.init_prange()\n'
                dnymf__ysfz += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                dnymf__ysfz += (
                    '      if not bodo.libs.array_kernels.isna(indices, i):\n')
                dnymf__ysfz += '         loc = indices[i]\n'
                dnymf__ysfz += (
                    '         if bodo.libs.array_kernels.isna(res, loc):\n')
                dnymf__ysfz += (
                    '            bodo.libs.array_kernels.setna(indices, i)\n')
            if out_dtype == bodo.string_array_type:
                dnymf__ysfz += """   res = bodo.libs.dict_arr_ext.init_dict_arr(res, indices, has_global, is_dict_unique)
"""
            else:
                dnymf__ysfz += """   res2 = bodo.utils.utils.alloc_type(len(indices), out_dtype, (-1,))
"""
                dnymf__ysfz += '   numba.parfors.parfor.init_prange()\n'
                dnymf__ysfz += (
                    '   for i in numba.parfors.parfor.internal_prange(len(indices)):\n'
                    )
                if propagate_null[izkol__xgqj]:
                    dnymf__ysfz += (
                        '      if bodo.libs.array_kernels.isna(indices, i):\n')
                    dnymf__ysfz += (
                        '         bodo.libs.array_kernels.setna(res2, i)\n')
                    dnymf__ysfz += '         continue\n'
                    dnymf__ysfz += '      loc = indices[i]\n'
                else:
                    dnymf__ysfz += """      loc = n if bodo.libs.array_kernels.isna(indices, i) else indices[i]
"""
                dnymf__ysfz += (
                    '      if bodo.libs.array_kernels.isna(res, loc):\n')
                dnymf__ysfz += (
                    '         bodo.libs.array_kernels.setna(res2, i)\n')
                dnymf__ysfz += '      else:\n'
                dnymf__ysfz += '         res2[i] = res[loc]\n'
                dnymf__ysfz += '   res = res2\n'
        dnymf__ysfz += indent_block(suffix_code, 3)
        if owsf__tpgfj:
            dnymf__ysfz += f"""   return bodo.libs.dict_arr_ext.init_dict_arr(dict_res, res, {synthesize_dict_global}, {synthesize_dict_unique})
"""
        else:
            dnymf__ysfz += '   return res'
    dol__xmw = {}
    qwxln__ugscf = {'bodo': bodo, 'math': math, 'numba': numba, 're': re,
        'np': np, 'out_dtype': out_dtype, 'pd': pd}
    if not extra_globals is None:
        qwxln__ugscf.update(extra_globals)
    exec(dnymf__ysfz, qwxln__ugscf, dol__xmw)
    llgfn__ogbq = dol__xmw['impl']
    return llgfn__ogbq


def unopt_argument(func_name, arg_names, i, container_arg=0,
    container_length=None):
    if container_length != None:
        mvefb__hpoaa = [(f'{arg_names[i]}{[rdh__bozen]}' if rdh__bozen !=
            container_arg else 'None') for rdh__bozen in range(
            container_length)]
        rbarc__qvvt = ',' if container_length != 0 else ''
        afj__hdga = f"({', '.join(mvefb__hpoaa)}{rbarc__qvvt})"
        ryy__dmx = [(f'{arg_names[i]}{[rdh__bozen]}' if rdh__bozen !=
            container_arg else
            f'bodo.utils.indexing.unoptional({arg_names[i]}[{rdh__bozen}])'
            ) for rdh__bozen in range(container_length)]
        dloiw__fox = f"({', '.join(ryy__dmx)}{rbarc__qvvt})"
        bgc__nmzur = [(arg_names[rdh__bozen] if rdh__bozen != i else
            afj__hdga) for rdh__bozen in range(len(arg_names))]
        iboqx__ykd = [(arg_names[rdh__bozen] if rdh__bozen != i else
            dloiw__fox) for rdh__bozen in range(len(arg_names))]
        dnymf__ysfz = f"def impl({', '.join(arg_names)}):\n"
        dnymf__ysfz += f'   if {arg_names[i]}[{container_arg}] is None:\n'
        dnymf__ysfz += f"      return {func_name}({', '.join(bgc__nmzur)})\n"
        dnymf__ysfz += f'   else:\n'
        dnymf__ysfz += f"      return {func_name}({', '.join(iboqx__ykd)})\n"
    else:
        mvefb__hpoaa = [(arg_names[rdh__bozen] if rdh__bozen != i else
            'None') for rdh__bozen in range(len(arg_names))]
        ryy__dmx = [(arg_names[rdh__bozen] if rdh__bozen != i else
            f'bodo.utils.indexing.unoptional({arg_names[rdh__bozen]})') for
            rdh__bozen in range(len(arg_names))]
        dnymf__ysfz = f"def impl({', '.join(arg_names)}):\n"
        dnymf__ysfz += f'   if {arg_names[i]} is None:\n'
        dnymf__ysfz += f"      return {func_name}({', '.join(mvefb__hpoaa)})\n"
        dnymf__ysfz += f'   else:\n'
        dnymf__ysfz += f"      return {func_name}({', '.join(ryy__dmx)})\n"
    dol__xmw = {}
    exec(dnymf__ysfz, {'bodo': bodo, 'numba': numba}, dol__xmw)
    llgfn__ogbq = dol__xmw['impl']
    return llgfn__ogbq


def is_valid_int_arg(arg):
    return not (arg != types.none and not isinstance(arg, types.Integer) and
        not (bodo.utils.utils.is_array_typ(arg, True) and isinstance(arg.
        dtype, types.Integer)) and not is_overload_int(arg))


def is_valid_float_arg(arg):
    return not (arg != types.none and not isinstance(arg, types.Float) and 
        not (bodo.utils.utils.is_array_typ(arg, True) and isinstance(arg.
        dtype, types.Float)) and not is_overload_float(arg))


def is_valid_numeric_bool(arg):
    return not (arg != types.none and not isinstance(arg, (types.Integer,
        types.Float, types.Boolean)) and not (bodo.utils.utils.is_array_typ
        (arg, True) and isinstance(arg.dtype, (types.Integer, types.Float,
        types.Boolean))) and not is_overload_constant_number(arg) and not
        is_overload_constant_bool(arg))


def verify_int_arg(arg, f_name, a_name):
    if not is_valid_int_arg(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be an integer, integer column, or null'
            )


def verify_int_float_arg(arg, f_name, a_name):
    if arg != types.none and not isinstance(arg, (types.Integer, types.
        Float, types.Boolean)) and not (bodo.utils.utils.is_array_typ(arg, 
        True) and isinstance(arg.dtype, (types.Integer, types.Float, types.
        Boolean))) and not is_overload_constant_number(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a numeric, numeric column, or null'
            )


def is_valid_string_arg(arg):
    arg = types.unliteral(arg)
    return not (arg not in (types.none, types.unicode_type) and not (bodo.
        utils.utils.is_array_typ(arg, True) and arg.dtype == types.
        unicode_type) and not is_overload_constant_str(arg))


def is_valid_binary_arg(arg):
    return not (arg != bodo.bytes_type and not (bodo.utils.utils.
        is_array_typ(arg, True) and arg.dtype == bodo.bytes_type) and not
        is_overload_constant_bytes(arg) and not isinstance(arg, types.Bytes))


def is_valid_datetime_or_date_arg(arg):
    return arg == pd_timestamp_tz_naive_type or bodo.utils.utils.is_array_typ(
        arg, True) and (is_datetime_date_series_typ(arg) or isinstance(arg,
        bodo.DatetimeArrayType) or arg.dtype == bodo.datetime64ns)


def is_valid_timedelta_arg(arg):
    return arg == pd_timedelta_type or bodo.utils.utils.is_array_typ(arg, True
        ) and (is_timedelta64_series_typ(arg) or isinstance(arg,
        PDTimeDeltaType) or arg.dtype == bodo.timedelta64ns)


def is_valid_boolean_arg(arg):
    return not (arg != types.boolean and not (bodo.utils.utils.is_array_typ
        (arg, True) and arg.dtype == types.boolean) and not
        is_overload_constant_bool(arg))


def verify_string_arg(arg, f_name, a_name):
    if not is_valid_string_arg(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a string, string column, or null'
            )


def verify_scalar_string_arg(arg, f_name, a_name):
    if arg not in (types.unicode_type, bodo.none) and not isinstance(arg,
        types.StringLiteral):
        raise_bodo_error(f'{f_name} {a_name} argument must be a scalar string')


def verify_binary_arg(arg, f_name, a_name):
    if not is_valid_binary_arg(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be binary data or null')


def verify_string_binary_arg(arg, f_name, a_name):
    nvc__ydess = is_valid_string_arg(arg)
    avhx__lse = is_valid_binary_arg(arg)
    if nvc__ydess or avhx__lse:
        return nvc__ydess
    else:
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a binary data, string, string column, or null'
            )


def verify_string_numeric_arg(arg, f_name, a_name):
    if not is_valid_string_arg(arg) and not is_valid_numeric_bool(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a string, integer, float, boolean, string column, integer column, float column, or boolean column'
            )


def verify_boolean_arg(arg, f_name, a_name):
    if arg not in (types.none, types.boolean) and not (bodo.utils.utils.
        is_array_typ(arg, True) and arg.dtype == types.boolean
        ) and not is_overload_bool(arg):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a boolean, boolean column, or null'
            )


def is_valid_date_arg(arg):
    return arg == bodo.datetime_date_type or bodo.utils.utils.is_array_typ(arg,
        True) and arg.dtype == bodo.datetime_date_type


def is_valid_tz_naive_datetime_arg(arg):
    return arg in (bodo.datetime64ns, bodo.pd_timestamp_tz_naive_type
        ) or bodo.utils.utils.is_array_typ(arg, True
        ) and arg.dtype == bodo.datetime64ns


def is_valid_tz_aware_datetime_arg(arg):
    return isinstance(arg, bodo.PandasTimestampType
        ) and arg.tz is not None or bodo.utils.utils.is_array_typ(arg, True
        ) and isinstance(arg.dtype, bodo.libs.pd_datetime_arr_ext.
        PandasDatetimeTZDtype)


def verify_datetime_arg(arg, f_name, a_name):
    if not (is_overload_none(arg) or is_valid_date_arg(arg) or
        is_valid_tz_naive_datetime_arg(arg)):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a datetime, datetime column, or null without a tz'
            )


def verify_datetime_arg_allow_tz(arg, f_name, a_name):
    if not (is_overload_none(arg) or is_valid_date_arg(arg) or
        is_valid_tz_naive_datetime_arg(arg) or
        is_valid_tz_aware_datetime_arg(arg)):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a datetime, datetime column, or null'
            )


def verify_datetime_arg_require_tz(arg, f_name, a_name):
    if not (is_overload_none(arg) or is_valid_tz_aware_datetime_arg(arg)):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a tz-aware datetime, datetime column, or null'
            )


def verify_sql_interval(arg, f_name, a_name):
    if not (is_overload_none(arg) or is_valid_timedelta_arg(arg) or arg ==
        bodo.date_offset_type):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a Timedelta scalar/column, DateOffset, or null'
            )


def get_tz_if_exists(arg):
    if is_valid_tz_aware_datetime_arg(arg):
        if bodo.utils.utils.is_array_typ(arg, True):
            return arg.dtype.tz
        else:
            return arg.tz
    return None


def is_valid_time_arg(arg):
    return isinstance(arg, bodo.TimeType) or bodo.utils.utils.is_array_typ(arg,
        True) and isinstance(arg.dtype, bodo.bodo.TimeType)


def verify_time_or_datetime_arg_allow_tz(arg, f_name, a_name):
    if not (is_overload_none(arg) or is_valid_date_arg(arg) or
        is_valid_time_arg(arg) or is_valid_tz_naive_datetime_arg(arg) or
        is_valid_tz_aware_datetime_arg(arg)):
        raise_bodo_error(
            f'{f_name} {a_name} argument must be a time/datetime, time/datetime column, or null without a tz'
            )


def get_common_broadcasted_type(arg_types, func_name):
    kcm__hffz = []
    for i in range(len(arg_types)):
        if bodo.utils.utils.is_array_typ(arg_types[i], False):
            kcm__hffz.append(arg_types[i])
        elif bodo.utils.utils.is_array_typ(arg_types[i], True):
            kcm__hffz.append(arg_types[i].data)
        else:
            kcm__hffz.append(arg_types[i])
    if len(kcm__hffz) == 0:
        return bodo.none
    elif len(kcm__hffz) == 1:
        if bodo.utils.utils.is_array_typ(kcm__hffz[0]):
            return bodo.utils.typing.to_nullable_type(kcm__hffz[0])
        elif kcm__hffz[0] == bodo.none:
            return bodo.none
        else:
            return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
                dtype_to_array_type(kcm__hffz[0]))
    else:
        pgr__tdsic = []
        for i in range(len(arg_types)):
            if bodo.utils.utils.is_array_typ(arg_types[i]):
                pgr__tdsic.append(kcm__hffz[i].dtype)
            elif kcm__hffz[i] == bodo.none:
                pass
            else:
                pgr__tdsic.append(kcm__hffz[i])
        if len(pgr__tdsic) == 0:
            return bodo.none
        ahbdh__midf, quf__asjl = bodo.utils.typing.get_common_scalar_dtype(
            pgr__tdsic)
        if not quf__asjl:
            raise_bodo_error(
                f'Cannot call {func_name} on columns with different dtypes')
        return bodo.utils.typing.to_nullable_type(bodo.utils.typing.
            dtype_to_array_type(ahbdh__midf))


def vectorized_sol(args, scalar_fn, dtype, manual_coercion=False):
    skqo__enb = -1
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            skqo__enb = len(arg)
            break
    if skqo__enb == -1:
        return dtype(scalar_fn(*args)) if manual_coercion else scalar_fn(*args)
    zmvgy__dqk = []
    for arg in args:
        if isinstance(arg, (pd.core.arrays.base.ExtensionArray, pd.Series,
            np.ndarray, pa.Array)):
            zmvgy__dqk.append(arg)
        else:
            zmvgy__dqk.append([arg] * skqo__enb)
    if manual_coercion:
        return pd.Series([dtype(scalar_fn(*hiii__uwoba)) for hiii__uwoba in
            zip(*zmvgy__dqk)])
    else:
        return pd.Series([scalar_fn(*hiii__uwoba) for hiii__uwoba in zip(*
            zmvgy__dqk)], dtype=dtype)


def gen_windowed(calculate_block, constant_block, out_dtype, setup_block=
    None, enter_block=None, exit_block=None, empty_block=None):
    sxd__yrrj = calculate_block.splitlines()
    fnt__erls = len(sxd__yrrj[0]) - len(sxd__yrrj[0].lstrip())
    if constant_block != None:
        ejlwy__fiong = constant_block.splitlines()
        fmy__fyjcm = len(ejlwy__fiong[0]) - len(ejlwy__fiong[0].lstrip())
    if setup_block != None:
        chp__qumft = setup_block.splitlines()
        jzf__odd = len(chp__qumft[0]) - len(chp__qumft[0].lstrip())
    if enter_block != None:
        lfl__psgxi = enter_block.splitlines()
        fvrbc__emrl = len(lfl__psgxi[0]) - len(lfl__psgxi[0].lstrip())
    if exit_block != None:
        fun__kzvf = exit_block.splitlines()
        ermv__eelv = len(fun__kzvf[0]) - len(fun__kzvf[0].lstrip())
    if empty_block == None:
        empty_block = 'bodo.libs.array_kernels.setna(res, i)'
    bri__nll = empty_block.splitlines()
    nmnc__damt = len(bri__nll[0]) - len(bri__nll[0].lstrip())
    dnymf__ysfz = 'def impl(S, lower_bound, upper_bound):\n'
    dnymf__ysfz += '   n = len(S)\n'
    dnymf__ysfz += '   arr = bodo.utils.conversion.coerce_to_array(S)\n'
    dnymf__ysfz += (
        '   res = bodo.utils.utils.alloc_type(n, out_dtype, (-1,))\n')
    dnymf__ysfz += '   if upper_bound < lower_bound:\n'
    dnymf__ysfz += '      for i in range(n):\n'
    dnymf__ysfz += '         bodo.libs.array_kernels.setna(res, i)\n'
    if constant_block != None:
        dnymf__ysfz += '   elif lower_bound <= -n+1 and n-1 <= upper_bound:\n'
        dnymf__ysfz += '      if S.count() == 0:\n'
        dnymf__ysfz += '         for i in range(n):\n'
        dnymf__ysfz += '\n'.join([(' ' * 12 + pkiw__bqjes[nmnc__damt:]) for
            pkiw__bqjes in bri__nll]) + '\n'
        dnymf__ysfz += '      else:\n'
        dnymf__ysfz += '\n'.join([(' ' * 9 + pkiw__bqjes[fmy__fyjcm:]) for
            pkiw__bqjes in ejlwy__fiong]) + '\n'
        dnymf__ysfz += '         for i in range(n):\n'
        dnymf__ysfz += '            res[i] = constant_value\n'
    dnymf__ysfz += '   else:\n'
    dnymf__ysfz += '      exiting = lower_bound\n'
    dnymf__ysfz += '      entering = upper_bound\n'
    dnymf__ysfz += '      in_window = 0\n'
    if setup_block != None:
        dnymf__ysfz += '\n'.join([(' ' * 6 + pkiw__bqjes[jzf__odd:]) for
            pkiw__bqjes in chp__qumft]) + '\n'
    dnymf__ysfz += (
        '      for i in range(min(max(0, exiting), n), min(max(0, entering + 1), n)):\n'
        )
    dnymf__ysfz += '         if not bodo.libs.array_kernels.isna(arr, i):\n'
    dnymf__ysfz += '            in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            dnymf__ysfz += '            elem = arr[i]\n'
        dnymf__ysfz += '\n'.join([(' ' * 12 + pkiw__bqjes[fvrbc__emrl:]) for
            pkiw__bqjes in lfl__psgxi]) + '\n'
    dnymf__ysfz += '      for i in range(n):\n'
    dnymf__ysfz += '         if in_window == 0:\n'
    dnymf__ysfz += '\n'.join([(' ' * 12 + pkiw__bqjes[nmnc__damt:]) for
        pkiw__bqjes in bri__nll]) + '\n'
    dnymf__ysfz += '         else:\n'
    dnymf__ysfz += '\n'.join([(' ' * 12 + pkiw__bqjes[fnt__erls:]) for
        pkiw__bqjes in sxd__yrrj]) + '\n'
    dnymf__ysfz += '         if 0 <= exiting < n:\n'
    dnymf__ysfz += (
        '            if not bodo.libs.array_kernels.isna(arr, exiting):\n')
    dnymf__ysfz += '               in_window -= 1\n'
    if exit_block != None:
        if 'elem' in exit_block:
            dnymf__ysfz += '               elem = arr[exiting]\n'
        dnymf__ysfz += '\n'.join([(' ' * 15 + pkiw__bqjes[ermv__eelv:]) for
            pkiw__bqjes in fun__kzvf]) + '\n'
    dnymf__ysfz += '         exiting += 1\n'
    dnymf__ysfz += '         entering += 1\n'
    dnymf__ysfz += '         if 0 <= entering < n:\n'
    dnymf__ysfz += (
        '            if not bodo.libs.array_kernels.isna(arr, entering):\n')
    dnymf__ysfz += '               in_window += 1\n'
    if enter_block != None:
        if 'elem' in enter_block:
            dnymf__ysfz += '               elem = arr[entering]\n'
        dnymf__ysfz += '\n'.join([(' ' * 15 + pkiw__bqjes[fvrbc__emrl:]) for
            pkiw__bqjes in lfl__psgxi]) + '\n'
    dnymf__ysfz += '   return res'
    dol__xmw = {}
    exec(dnymf__ysfz, {'bodo': bodo, 'numba': numba, 'np': np, 'out_dtype':
        out_dtype, 'pd': pd}, dol__xmw)
    llgfn__ogbq = dol__xmw['impl']
    return llgfn__ogbq
