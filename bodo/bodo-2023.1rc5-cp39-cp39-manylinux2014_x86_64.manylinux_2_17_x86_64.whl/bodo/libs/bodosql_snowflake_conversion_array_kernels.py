"""
Implements a number of array kernels that handling casting functions for BodoSQL
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.extending import overload, register_jitable
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import get_literal_value, get_overload_const_bool, is_literal_type, is_overload_none, raise_bodo_error


@numba.generated_jit(nopython=True)
def try_to_boolean(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.to_boolean',
            ['arr'], 0)

    def impl(arr):
        return to_boolean_util(arr, numba.literally(True))
    return impl


@numba.generated_jit(nopython=True)
def to_boolean(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.to_boolean',
            ['arr'], 0)

    def impl(arr):
        return to_boolean_util(arr, numba.literally(False))
    return impl


@numba.generated_jit(nopython=True)
def to_boolean_util(arr, _try=False):
    verify_string_numeric_arg(arr, 'TO_BOOLEAN', 'arr')
    yyjt__xllwf = is_valid_string_arg(arr)
    yoysa__vaw = is_valid_float_arg(arr)
    _try = get_overload_const_bool(_try)
    if _try:
        cwpy__tayu = 'bodo.libs.array_kernels.setna(res, i)\n'
    else:
        if yyjt__xllwf:
            gyr__umxfb = (
                "string must be one of {'true', 't', 'yes', 'y', 'on', '1'} or {'false', 'f', 'no', 'n', 'off', '0'}"
                )
        else:
            gyr__umxfb = 'value must be a valid numeric expression'
        cwpy__tayu = (
            f'raise ValueError("invalid value for boolean conversion: {gyr__umxfb}")'
            )
    rbo__ufa = ['arr', '_try']
    cpop__plq = [arr, _try]
    eigqm__kzzy = [True, False]
    zqkvf__ffwae = None
    if yyjt__xllwf:
        zqkvf__ffwae = "true_vals = {'true', 't', 'yes', 'y', 'on', '1'}\n"
        zqkvf__ffwae += "false_vals = {'false', 'f', 'no', 'n', 'off', '0'}"
    if yyjt__xllwf:
        kxig__roaih = 's = arg0.lower()\n'
        kxig__roaih += f'is_true_val = s in true_vals\n'
        kxig__roaih += f'res[i] = is_true_val\n'
        kxig__roaih += f'if not (is_true_val or s in false_vals):\n'
        kxig__roaih += f'  {cwpy__tayu}\n'
    elif yoysa__vaw:
        kxig__roaih = 'if np.isinf(arg0) or np.isnan(arg0):\n'
        kxig__roaih += f'  {cwpy__tayu}\n'
        kxig__roaih += 'else:\n'
        kxig__roaih += f'  res[i] = bool(arg0)\n'
    else:
        kxig__roaih = f'res[i] = bool(arg0)'
    mcztd__qvg = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(rbo__ufa, cpop__plq, eigqm__kzzy, kxig__roaih,
        mcztd__qvg, prefix_code=zqkvf__ffwae)


@numba.generated_jit(nopython=True)
def try_to_date(conversionVal, optionalConversionFormatString):
    args = [conversionVal, optionalConversionFormatString]
    for fdjyv__tnr in range(2):
        if isinstance(args[fdjyv__tnr], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.try_to_date'
                , ['conversionVal', 'optionalConversionFormatString'],
                fdjyv__tnr)

    def impl(conversionVal, optionalConversionFormatString):
        return to_date_util(conversionVal, optionalConversionFormatString,
            numba.literally(False))
    return impl


@numba.generated_jit(nopython=True)
def to_date(conversionVal, optionalConversionFormatString):
    args = [conversionVal, optionalConversionFormatString]
    for fdjyv__tnr in range(2):
        if isinstance(args[fdjyv__tnr], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.to_date',
                ['conversionVal', 'optionalConversionFormatString'], fdjyv__tnr
                )

    def impl(conversionVal, optionalConversionFormatString):
        return to_date_util(conversionVal, optionalConversionFormatString,
            numba.literally(True))
    return impl


@numba.generated_jit(nopython=True)
def to_char(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.to_char', [
            'arr'], 0)

    def impl(arr):
        return to_char_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def to_char_util(arr):
    rbo__ufa = ['arr']
    cpop__plq = [arr]
    eigqm__kzzy = [True]
    if is_valid_binary_arg(arr):
        kxig__roaih = 'with bodo.objmode(r=bodo.string_type):\n'
        kxig__roaih += '  r = arg0.hex()\n'
        kxig__roaih += 'res[i] = r'
    elif isinstance(arr, bodo.TimeType) or bodo.utils.utils.is_array_typ(arr
        ) and isinstance(arr.dtype, bodo.TimeType):
        kxig__roaih = (
            "h_str = str(arg0.hour) if arg0.hour > 10 else '0' + str(arg0.hour)\n"
            )
        kxig__roaih += (
            "m_str = str(arg0.minute) if arg0.minute > 10 else '0' + str(arg0.minute)\n"
            )
        kxig__roaih += (
            "s_str = str(arg0.second) if arg0.second > 10 else '0' + str(arg0.second)\n"
            )
        kxig__roaih += """ms_str = str(arg0.millisecond) if arg0.millisecond > 100 else ('0' + str(arg0.millisecond) if arg0.millisecond > 10 else '00' + str(arg0.millisecond))
"""
        kxig__roaih += """us_str = str(arg0.microsecond) if arg0.microsecond > 100 else ('0' + str(arg0.microsecond) if arg0.microsecond > 10 else '00' + str(arg0.microsecond))
"""
        kxig__roaih += """ns_str = str(arg0.nanosecond) if arg0.nanosecond > 100 else ('0' + str(arg0.nanosecond) if arg0.nanosecond > 10 else '00' + str(arg0.nanosecond))
"""
        kxig__roaih += "part_str = h_str + ':' + m_str + ':' + s_str\n"
        kxig__roaih += 'if arg0.nanosecond > 0:\n'
        kxig__roaih += (
            "  part_str = part_str + '.' + ms_str + us_str + ns_str\n")
        kxig__roaih += 'elif arg0.microsecond > 0:\n'
        kxig__roaih += "  part_str = part_str + '.' + ms_str + us_str\n"
        kxig__roaih += 'elif arg0.millisecond > 0:\n'
        kxig__roaih += "  part_str = part_str + '.' + ms_str\n"
        kxig__roaih += 'res[i] = part_str'
    elif is_valid_timedelta_arg(arr):
        kxig__roaih = (
            'v = bodo.utils.conversion.unbox_if_tz_naive_timestamp(arg0)\n')
        kxig__roaih += 'with bodo.objmode(r=bodo.string_type):\n'
        kxig__roaih += '    r = str(v)\n'
        kxig__roaih += 'res[i] = r'
    elif is_valid_datetime_or_date_arg(arr):
        if is_valid_tz_aware_datetime_arg(arr):
            kxig__roaih = "tz_raw = arg0.strftime('%z')\n"
            kxig__roaih += 'tz = tz_raw[:3] + ":" + tz_raw[3:]\n'
            kxig__roaih += "res[i] = arg0.isoformat(' ') + tz\n"
        else:
            kxig__roaih = "res[i] = pd.Timestamp(arg0).isoformat(' ')\n"
    elif is_valid_float_arg(arr):
        kxig__roaih = 'if np.isinf(arg0):\n'
        kxig__roaih += "  res[i] = 'inf' if arg0 > 0 else '-inf'\n"
        kxig__roaih += 'elif np.isnan(arg0):\n'
        kxig__roaih += "  res[i] = 'NaN'\n"
        kxig__roaih += 'else:\n'
        kxig__roaih += '  res[i] = str(arg0)'
    elif is_valid_boolean_arg(arr):
        kxig__roaih = "res[i] = 'true' if arg0 else 'false'"
    else:
        adzvx__cayd = {(8): np.int8, (16): np.int16, (32): np.int32, (64):
            np.int64}
        if is_valid_int_arg(arr):
            if hasattr(arr, 'dtype'):
                whhu__kmz = arr.dtype.bitwidth
            else:
                whhu__kmz = arr.bitwidth
            kxig__roaih = (
                f'if arg0 == {np.iinfo(adzvx__cayd[whhu__kmz]).min}:\n')
            kxig__roaih += (
                f"  res[i] = '{np.iinfo(adzvx__cayd[whhu__kmz]).min}'\n")
            kxig__roaih += 'else:\n'
            kxig__roaih += '  res[i] = str(arg0)'
        else:
            kxig__roaih = 'res[i] = str(arg0)'
    mcztd__qvg = bodo.string_array_type
    return gen_vectorized(rbo__ufa, cpop__plq, eigqm__kzzy, kxig__roaih,
        mcztd__qvg)


@register_jitable
def convert_sql_date_format_str_to_py_format(val):
    raise RuntimeError(
        'Converting to date values with format strings not currently supported'
        )


@numba.generated_jit(nopython=True)
def int_to_datetime(val):

    def impl(val):
        if val < 31536000000:
            rugtf__dci = pd.to_datetime(val, unit='s')
        elif val < 31536000000000:
            rugtf__dci = pd.to_datetime(val, unit='ms')
        elif val < 31536000000000000:
            rugtf__dci = pd.to_datetime(val, unit='us')
        else:
            rugtf__dci = pd.to_datetime(val, unit='ns')
        return rugtf__dci
    return impl


@numba.generated_jit(nopython=True)
def float_to_datetime(val):

    def impl(val):
        if val < 31536000000:
            rugtf__dci = pd.Timestamp(val, unit='s')
        elif val < 31536000000000:
            rugtf__dci = pd.Timestamp(val, unit='ms')
        elif val < 31536000000000000:
            rugtf__dci = pd.Timestamp(val, unit='us')
        else:
            rugtf__dci = pd.Timestamp(val, unit='ns')
        return rugtf__dci
    return impl


@register_jitable
def pd_to_datetime_error_checked(val, dayfirst=False, yearfirst=False, utc=
    None, format=None, exact=True, unit=None, infer_datetime_format=False,
    origin='unix', cache=True):
    if val is not None:
        txo__tcv = val.split(' ')[0]
        if len(txo__tcv) < 10:
            return False, None
        else:
            kieed__dubz = txo__tcv.count('/') in [0, 2]
            ywy__eyi = txo__tcv.count('-') in [0, 2]
            if not (kieed__dubz and ywy__eyi):
                return False, None
    with numba.objmode(ret_val='pd_timestamp_tz_naive_type', success_flag=
        'bool_'):
        success_flag = True
        ret_val = pd.Timestamp(0)
        pco__zezl = pd.to_datetime(val, errors='coerce', dayfirst=dayfirst,
            yearfirst=yearfirst, utc=utc, format=format, exact=exact, unit=
            unit, infer_datetime_format=infer_datetime_format, origin=
            origin, cache=cache)
        if pd.isna(pco__zezl):
            success_flag = False
        else:
            ret_val = pco__zezl
    return success_flag, ret_val


@numba.generated_jit(nopython=True)
def to_date_util(conversionVal, optionalConversionFormatString, errorOnFail,
    _keep_time=False):
    errorOnFail = get_overload_const_bool(errorOnFail)
    _keep_time = get_overload_const_bool(_keep_time)
    if errorOnFail:
        ufr__xvd = (
            "raise ValueError('Invalid input while converting to date value')")
    else:
        ufr__xvd = 'bodo.libs.array_kernels.setna(res, i)'
    if _keep_time:
        lwsvn__fwe = ''
    else:
        lwsvn__fwe = '.normalize()'
    verify_string_arg(optionalConversionFormatString,
        'TO_DATE and TRY_TO_DATE', 'optionalConversionFormatString')
    cxy__fss = bodo.utils.utils.is_array_typ(conversionVal, True
        ) or bodo.utils.utils.is_array_typ(optionalConversionFormatString, True
        )
    fljvn__jzg = 'unbox_if_tz_naive_timestamp' if cxy__fss else ''
    if not is_overload_none(optionalConversionFormatString):
        verify_string_arg(conversionVal, 'TO_DATE and TRY_TO_DATE',
            'optionalConversionFormatString')
        kxig__roaih = (
            'py_format_str = convert_sql_date_format_str_to_py_format(arg1)\n')
        kxig__roaih += """was_successful, tmp_val = pd_to_datetime_error_checked(arg0, format=py_format_str)
"""
        kxig__roaih += 'if not was_successful:\n'
        kxig__roaih += f'  {ufr__xvd}\n'
        kxig__roaih += 'else:\n'
        kxig__roaih += f'  res[i] = {fljvn__jzg}(tmp_val{lwsvn__fwe})\n'
    elif is_valid_string_arg(conversionVal):
        """
        If no format string is specified, snowflake will use attempt to parse the string according to these date formats:
        https://docs.snowflake.com/en/user-guide/date-time-input-output.html#date-formats. All of the examples listed are
        handled by pd.to_datetime() in Bodo jit code.

        It will also check if the string is convertable to int, IE '12345' or '-4321'"""
        kxig__roaih = 'arg0 = str(arg0)\n'
        kxig__roaih += """if (arg0.isnumeric() or (len(arg0) > 1 and arg0[0] == '-' and arg0[1:].isnumeric())):
"""
        kxig__roaih += (
            f'   res[i] = {fljvn__jzg}(int_to_datetime(np.int64(arg0)){lwsvn__fwe})\n'
            )
        kxig__roaih += 'else:\n'
        kxig__roaih += (
            '   was_successful, tmp_val = pd_to_datetime_error_checked(arg0)\n'
            )
        kxig__roaih += '   if not was_successful:\n'
        kxig__roaih += f'      {ufr__xvd}\n'
        kxig__roaih += '   else:\n'
        kxig__roaih += f'      res[i] = {fljvn__jzg}(tmp_val{lwsvn__fwe})\n'
    elif is_valid_int_arg(conversionVal):
        kxig__roaih = (
            f'res[i] = {fljvn__jzg}(int_to_datetime(arg0){lwsvn__fwe})\n')
    elif is_valid_float_arg(conversionVal):
        kxig__roaih = (
            f'res[i] = {fljvn__jzg}(float_to_datetime(arg0){lwsvn__fwe})\n')
    elif is_valid_datetime_or_date_arg(conversionVal):
        kxig__roaih = (
            f'res[i] = {fljvn__jzg}(pd.Timestamp(arg0){lwsvn__fwe})\n')
    elif is_valid_tz_aware_datetime_arg(conversionVal):
        kxig__roaih = f'res[i] = arg0{lwsvn__fwe}\n'
    else:
        raise raise_bodo_error(
            f'Internal error: unsupported type passed to to_date_util for argument conversionVal: {conversionVal}'
            )
    rbo__ufa = ['conversionVal', 'optionalConversionFormatString',
        'errorOnFail', '_keep_time']
    cpop__plq = [conversionVal, optionalConversionFormatString, errorOnFail,
        _keep_time]
    eigqm__kzzy = [True, False, False, False]
    if isinstance(conversionVal, bodo.DatetimeArrayType) or isinstance(
        conversionVal, bodo.PandasTimestampType
        ) and conversionVal.tz is not None:
        mcztd__qvg = bodo.DatetimeArrayType(conversionVal.tz)
    else:
        mcztd__qvg = types.Array(bodo.datetime64ns, 1, 'C')
    nbwfq__kovsv = {'pd_to_datetime_error_checked':
        pd_to_datetime_error_checked, 'int_to_datetime': int_to_datetime,
        'float_to_datetime': float_to_datetime,
        'convert_sql_date_format_str_to_py_format':
        convert_sql_date_format_str_to_py_format,
        'unbox_if_tz_naive_timestamp': bodo.utils.conversion.
        unbox_if_tz_naive_timestamp}
    return gen_vectorized(rbo__ufa, cpop__plq, eigqm__kzzy, kxig__roaih,
        mcztd__qvg, extra_globals=nbwfq__kovsv)


def cast_tz_naive_to_tz_aware(arr, tz):
    pass


@overload(cast_tz_naive_to_tz_aware, no_unliteral=True)
def overload_cast_tz_naive_to_tz_aware(arr, tz):
    if not is_literal_type(tz):
        raise_bodo_error(
            "cast_tz_naive_to_tz_aware(): 'tz' must be a literal value")
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.cast_tz_naive_to_tz_aware', [
            'arr', 'tz'], 0)

    def impl(arr, tz):
        return cast_tz_naive_to_tz_aware_util(arr, tz)
    return impl


def cast_tz_naive_to_tz_aware_util(arr, tz):
    pass


@overload(cast_tz_naive_to_tz_aware_util, no_unliteral=True)
def overload_cast_tz_naive_to_tz_aware_util(arr, tz):
    if not is_literal_type(tz):
        raise_bodo_error(
            "cast_tz_naive_to_tz_aware(): 'tz' must be a literal value")
    verify_datetime_arg(arr, 'cast_tz_naive_to_tz_aware', 'arr')
    rbo__ufa = ['arr', 'tz']
    cpop__plq = [arr, tz]
    eigqm__kzzy = [True, False]
    snmqn__qjiwt = ('bodo.utils.conversion.box_if_dt64' if bodo.utils.utils
        .is_array_typ(arr) else '')
    kxig__roaih = f'res[i] = {snmqn__qjiwt}(arg0).tz_localize(arg1)'
    tz = get_literal_value(tz)
    mcztd__qvg = bodo.DatetimeArrayType(tz)
    return gen_vectorized(rbo__ufa, cpop__plq, eigqm__kzzy, kxig__roaih,
        mcztd__qvg)


def cast_tz_aware_to_tz_naive(arr, normalize):
    pass


@overload(cast_tz_aware_to_tz_naive, no_unliteral=True)
def overload_cast_tz_aware_to_tz_naive(arr, normalize):
    if not is_overload_constant_bool(normalize):
        raise_bodo_error(
            "cast_tz_aware_to_tz_naive(): 'normalize' must be a literal value")
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.cast_tz_aware_to_tz_naive', [
            'arr', 'normalize'], 0)

    def impl(arr, normalize):
        return cast_tz_aware_to_tz_naive_util(arr, normalize)
    return impl


def cast_tz_aware_to_tz_naive_util(arr, normalize):
    pass


@overload(cast_tz_aware_to_tz_naive_util, no_unliteral=True)
def overload_cast_tz_aware_to_tz_naive_util(arr, normalize):
    if not is_overload_constant_bool(normalize):
        raise_bodo_error(
            "cast_tz_aware_to_tz_naive(): 'normalize' must be a literal value")
    normalize = get_overload_const_bool(normalize)
    verify_datetime_arg_require_tz(arr, 'cast_tz_aware_to_tz_naive', 'arr')
    rbo__ufa = ['arr', 'normalize']
    cpop__plq = [arr, normalize]
    eigqm__kzzy = [True, False]
    fljvn__jzg = ('bodo.utils.conversion.unbox_if_tz_naive_timestamp' if
        bodo.utils.utils.is_array_typ(arr) else '')
    kxig__roaih = ''
    if normalize:
        kxig__roaih += (
            'ts = pd.Timestamp(year=arg0.year, month=arg0.month, day=arg0.day)\n'
            )
    else:
        kxig__roaih += 'ts = arg0.tz_localize(None)\n'
    kxig__roaih += f'res[i] = {fljvn__jzg}(ts)'
    mcztd__qvg = types.Array(bodo.datetime64ns, 1, 'C')
    return gen_vectorized(rbo__ufa, cpop__plq, eigqm__kzzy, kxig__roaih,
        mcztd__qvg)


def cast_str_to_tz_aware(arr, tz):
    pass


@overload(cast_str_to_tz_aware, no_unliteral=True)
def overload_cast_str_to_tz_aware(arr, tz):
    if not is_literal_type(tz):
        raise_bodo_error("cast_str_to_tz_aware(): 'tz' must be a literal value"
            )
    if isinstance(arr, types.optional):
        return unopt_argument(
            'bodo.libs.bodosql_array_kernels.cast_str_to_tz_aware', ['arr',
            'tz'], 0)

    def impl(arr, tz):
        return cast_str_to_tz_aware_util(arr, tz)
    return impl


def cast_str_to_tz_aware_util(arr, tz):
    pass


@overload(cast_str_to_tz_aware_util, no_unliteral=True)
def overload_cast_str_to_tz_aware_util(arr, tz):
    if not is_literal_type(tz):
        raise_bodo_error("cast_str_to_tz_aware(): 'tz' must be a literal value"
            )
    verify_string_arg(arr, 'cast_str_to_tz_aware', 'arr')
    rbo__ufa = ['arr', 'tz']
    cpop__plq = [arr, tz]
    eigqm__kzzy = [True, False]
    kxig__roaih = f'res[i] = pd.to_datetime(arg0).tz_localize(arg1)'
    tz = get_literal_value(tz)
    mcztd__qvg = bodo.DatetimeArrayType(tz)
    return gen_vectorized(rbo__ufa, cpop__plq, eigqm__kzzy, kxig__roaih,
        mcztd__qvg)
