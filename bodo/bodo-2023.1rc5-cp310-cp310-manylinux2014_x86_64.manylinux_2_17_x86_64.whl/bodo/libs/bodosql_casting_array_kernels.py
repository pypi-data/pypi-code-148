"""
Implements a number of array kernels that handling casting functions for BodoSQL
"""
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import BodoError


def cast_float64(arr):
    return


def cast_float64_util(arr):
    return


def cast_float32(arr):
    return


def cast_float32_util(arr):
    return


def cast_int64(arr):
    return


def cast_int64_util(arr):
    return


def cast_int32(arr):
    return


def cast_int32_util(arr):
    return


def cast_int16(arr):
    return


def cast_int16_util(arr):
    return


def cast_int8(arr):
    return


def cast_int8_util(arr):
    return


def cast_boolean(arr):
    return


def cast_char(arr):
    return


def cast_date(arr):
    return arr


def cast_timestamp(arr):
    return


def cast_interval(arr):
    return


def cast_interval_util(arr):
    return


cast_funcs_utils_names = (cast_float64, cast_float64_util, 'float64'), (
    cast_float32, cast_float32_util, 'float32'), (cast_int64,
    cast_int64_util, 'int64'), (cast_int32, cast_int32_util, 'int32'), (
    cast_int16, cast_int16_util, 'int16'), (cast_int8, cast_int8_util, 'int8'
    ), (cast_boolean, None, 'boolean'), (cast_char, None, 'char'), (cast_date,
    None, 'date'), (cast_timestamp, None, 'timestamp'), (cast_interval,
    cast_interval, 'interval')
fname_to_equiv = {'float64': 'np.float64', 'float32': 'np.float32', 'int64':
    'np.int64', 'int32': 'np.int32', 'int16': 'np.int16', 'int8': 'np.int8',
    'interval': 'pd.to_timedelta'}
fname_to_dtype = {'float64': types.Array(bodo.float64, 1, 'C'), 'float32':
    types.Array(bodo.float32, 1, 'C'), 'int64': bodo.libs.int_arr_ext.
    IntegerArrayType(types.int64), 'int32': bodo.libs.int_arr_ext.
    IntegerArrayType(types.int32), 'int16': bodo.libs.int_arr_ext.
    IntegerArrayType(types.int16), 'int8': bodo.libs.int_arr_ext.
    IntegerArrayType(types.int8), 'interval': np.dtype('timedelta64[ns]')}


def create_cast_func_overload(func_name):

    def overload_cast_func(arr):
        if isinstance(arr, types.optional):
            return unopt_argument(
                f'bodo.libs.bodosql_array_kernels.cast_{func_name}', ['arr'], 0
                )
        jgzbp__vqq = 'def impl(arr):\n'
        if func_name == 'boolean':
            jgzbp__vqq += f"""  return bodo.libs.bodosql_snowflake_conversion_array_kernels.to_boolean_util(arr, numba.literally(True))
"""
        elif func_name == 'char':
            jgzbp__vqq += f"""  return bodo.libs.bodosql_snowflake_conversion_array_kernels.to_char_util(arr)
"""
        elif func_name == 'date':
            jgzbp__vqq += f"""  return bodo.libs.bodosql_snowflake_conversion_array_kernels.to_date_util(arr, None, numba.literally(True), numba.literally(False))
"""
        elif func_name == 'timestamp':
            jgzbp__vqq += f"""  return bodo.libs.bodosql_snowflake_conversion_array_kernels.to_date_util(arr, None, numba.literally(False), numba.literally(True))
"""
        else:
            jgzbp__vqq += (
                f'  return bodo.libs.bodosql_array_kernels.cast_{func_name}_util(arr)'
                )
        ztgay__oqij = {}
        exec(jgzbp__vqq, {'bodo': bodo, 'numba': numba}, ztgay__oqij)
        return ztgay__oqij['impl']
    return overload_cast_func


def create_cast_util_overload(func_name):

    def overload_cast_util(arr):
        xki__hvpl = ['arr']
        mmek__dfzr = [arr]
        munzn__app = [True]
        ujgnp__byg = ''
        if func_name[:3
            ] == 'int' and func_name != 'interval' and not is_valid_boolean_arg(
            arr):
            if is_valid_int_arg(arr):
                ujgnp__byg += """if arg0 < np.iinfo(np.int64).min or arg0 > np.iinfo(np.int64).max:
"""
                ujgnp__byg += '  bodo.libs.array_kernels.setna(res, i)\n'
                ujgnp__byg += 'else:\n'
                ujgnp__byg += f'  res[i] = {fname_to_equiv[func_name]}(arg0)\n'
            else:
                if is_valid_string_arg(arr):
                    ujgnp__byg = 'i_val = 0\n'
                    ujgnp__byg += 'f_val = np.float64(arg0)\n'
                    ujgnp__byg += """is_valid = not (pd.isna(f_val) or np.isinf(f_val) or f_val < np.iinfo(np.int64).min or f_val > np.iinfo(np.int64).max)
"""
                    ujgnp__byg += 'is_int = (f_val % 1 == 0)\n'
                    ujgnp__byg += 'if not (is_valid and is_int):\n'
                    ujgnp__byg += '  val = f_val\n'
                    ujgnp__byg += 'else:\n'
                    ujgnp__byg += '  val = np.int64(arg0)\n'
                    ujgnp__byg += '  i_val = np.int64(arg0)\n'
                else:
                    if not is_valid_float_arg(arr):
                        raise BodoError(
                            'only strings, floats, booleans, and ints can be cast to ints'
                            )
                    ujgnp__byg += 'val = arg0\n'
                    ujgnp__byg += """is_valid = not(pd.isna(val) or np.isinf(val) or val < np.iinfo(np.int64).min or val > np.iinfo(np.int64).max)
"""
                    ujgnp__byg += 'is_int = (val % 1 == 0)\n'
                ujgnp__byg += 'if not is_valid:\n'
                ujgnp__byg += '  bodo.libs.array_kernels.setna(res, i)\n'
                ujgnp__byg += 'else:\n'
                if is_valid_float_arg(arr):
                    ujgnp__byg += '  i_val = np.int64(val)\n'
                ujgnp__byg += '  if not is_int:\n'
                ujgnp__byg += (
                    '    ans = np.int64(np.sign(val) * np.floor(np.abs(val) + 0.5))\n'
                    )
                ujgnp__byg += '  else:\n'
                ujgnp__byg += '    ans = i_val\n'
                if func_name == 'int64':
                    ujgnp__byg += f'  res[i] = ans\n'
                else:
                    ujgnp__byg += (
                        f'  res[i] = {fname_to_equiv[func_name]}(ans)')
        elif func_name == 'interval':
            apcwg__fvn = (
                'bodo.utils.conversion.unbox_if_tz_naive_timestamp' if bodo
                .utils.utils.is_array_typ(arr, True) else '')
            ujgnp__byg += f'res[i] = {apcwg__fvn}(pd.to_timedelta(arg0))'
        else:
            ujgnp__byg += f'res[i] = {fname_to_equiv[func_name]}(arg0)'
        legk__xdik = fname_to_dtype[func_name]
        return gen_vectorized(xki__hvpl, mmek__dfzr, munzn__app, ujgnp__byg,
            legk__xdik)
    return overload_cast_util


def _install_cast_func_overloads(funcs_utils_names):
    for rzg__ywxnd, kxze__iujz, xiw__eaih in funcs_utils_names:
        overload(rzg__ywxnd)(create_cast_func_overload(xiw__eaih))
        if xiw__eaih not in ('boolean', 'char', 'date', 'timestamp'):
            overload(kxze__iujz)(create_cast_util_overload(xiw__eaih))


_install_cast_func_overloads(cast_funcs_utils_names)
