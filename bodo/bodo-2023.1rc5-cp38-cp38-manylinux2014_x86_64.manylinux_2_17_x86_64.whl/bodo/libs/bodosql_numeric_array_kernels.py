"""
Implements numerical array kernels that are specific to BodoSQL
"""
import numba
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.utils import is_array_typ


def cbrt(arr):
    return


def ceil(arr):
    return


def factorial(arr):
    return


def floor(arr):
    return


def mod(arr0, arr1):
    return


def sign(arr):
    return


def sqrt(arr):
    return


def round(arr0, arr1):
    return


def trunc(arr0, arr1):
    return


def abs(arr):
    return


def ln(arr):
    return


def log2(arr):
    return


def log10(arr):
    return


def exp(arr):
    return


def power(arr0, arr1):
    return


def sqrt_util(arr):
    return


def square(arr):
    return


def cbrt_util(arr):
    return


def ceil_util(arr):
    return


def factorial_util(arr):
    return


def floor_util(arr):
    return


def mod_util(arr0, arr1):
    return


def sign_util(arr):
    return


def round_util(arr0, arr1):
    return


def trunc_util(arr0, arr1):
    return


def abs_util(arr):
    return


def ln_util(arr):
    return


def log2_util(arr):
    return


def log10_util(arr):
    return


def exp_util(arr):
    return


def power_util(arr0, arr1):
    return


def square_util(arr):
    return


funcs_utils_names = (abs, abs_util, 'ABS'), (cbrt, cbrt_util, 'CBRT'), (ceil,
    ceil_util, 'CEIL'), (factorial, factorial_util, 'FACTORIAL'), (floor,
    floor_util, 'FLOOR'), (ln, ln_util, 'LN'), (log2, log2_util, 'LOG2'), (
    log10, log10_util, 'LOG10'), (mod, mod_util, 'MOD'), (sign, sign_util,
    'SIGN'), (round, round_util, 'ROUND'), (trunc, trunc_util, 'TRUNC'), (exp,
    exp_util, 'EXP'), (power, power_util, 'POWER'), (sqrt, sqrt_util, 'SQRT'
    ), (square, square_util, 'SQUARE')
double_arg_funcs = 'MOD', 'TRUNC', 'POWER', 'ROUND'
single_arg_funcs = set(a[2] for a in funcs_utils_names if a[2] not in
    double_arg_funcs)
_float = {(16): types.float16, (32): types.float32, (64): types.float64}
_int = {(8): types.int8, (16): types.int16, (32): types.int32, (64): types.
    int64}
_uint = {(8): types.uint8, (16): types.uint16, (32): types.uint32, (64):
    types.uint64}


def _get_numeric_output_dtype(func_name, arr0, arr1=None):
    xzv__zau = arr0.dtype if is_array_typ(arr0) else arr0
    vyz__ggc = arr1.dtype if is_array_typ(arr1) else arr1
    gddlf__lpy = bodo.float64
    if (arr0 is None or xzv__zau == bodo.none
        ) or func_name in double_arg_funcs and (arr1 is None or vyz__ggc ==
        bodo.none):
        return types.Array(gddlf__lpy, 1, 'C')
    if isinstance(xzv__zau, types.Float):
        if isinstance(vyz__ggc, types.Float):
            gddlf__lpy = _float[max(xzv__zau.bitwidth, vyz__ggc.bitwidth)]
        else:
            gddlf__lpy = xzv__zau
    if func_name == 'SIGN':
        if isinstance(xzv__zau, types.Integer):
            gddlf__lpy = xzv__zau
    elif func_name == 'MOD':
        if isinstance(xzv__zau, types.Integer) and isinstance(vyz__ggc,
            types.Integer):
            if xzv__zau.signed:
                if vyz__ggc.signed:
                    gddlf__lpy = vyz__ggc
                else:
                    gddlf__lpy = _int[min(64, vyz__ggc.bitwidth * 2)]
            else:
                gddlf__lpy = vyz__ggc
    elif func_name == 'ABS':
        if isinstance(xzv__zau, types.Integer):
            if xzv__zau.signed:
                gddlf__lpy = _uint[min(64, xzv__zau.bitwidth * 2)]
            else:
                gddlf__lpy = xzv__zau
    elif func_name == 'ROUND':
        if isinstance(xzv__zau, (types.Float, types.Integer)):
            gddlf__lpy = xzv__zau
    elif func_name == 'FACTORIAL':
        gddlf__lpy = bodo.int64
    if isinstance(gddlf__lpy, types.Integer):
        return bodo.libs.int_arr_ext.IntegerArrayType(gddlf__lpy)
    else:
        return types.Array(gddlf__lpy, 1, 'C')


def create_numeric_func_overload(func_name):
    if func_name not in double_arg_funcs:
        func_name = func_name.lower()

        def overload_func(arr):
            if isinstance(arr, types.optional):
                return unopt_argument(
                    f'bodo.libs.bodosql_array_kernels.{func_name}', ['arr'], 0)
            uxss__teuu = 'def impl(arr):\n'
            uxss__teuu += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr)'
                )
            zsm__hvqr = {}
            exec(uxss__teuu, {'bodo': bodo}, zsm__hvqr)
            return zsm__hvqr['impl']
    else:
        func_name = func_name.lower()

        def overload_func(arr0, arr1):
            args = [arr0, arr1]
            for xecnb__zujb in range(2):
                if isinstance(args[xecnb__zujb], types.optional):
                    return unopt_argument(
                        f'bodo.libs.bodosql_array_kernels.{func_name}', [
                        'arr0', 'arr1'], xecnb__zujb)
            uxss__teuu = 'def impl(arr0, arr1):\n'
            uxss__teuu += (
                f'  return bodo.libs.bodosql_array_kernels.{func_name}_util(arr0, arr1)'
                )
            zsm__hvqr = {}
            exec(uxss__teuu, {'bodo': bodo}, zsm__hvqr)
            return zsm__hvqr['impl']
    return overload_func


def create_numeric_util_overload(func_name):
    if func_name not in double_arg_funcs:

        def overload_numeric_util(arr):
            verify_int_float_arg(arr, func_name, 'arr')
            qsciu__pekk = ['arr']
            eauah__uah = [arr]
            sjf__zituk = [True]
            jga__crgwn = ''
            if func_name in single_arg_funcs:
                if func_name == 'FACTORIAL':
                    jga__crgwn += (
                        'if arg0 > 20 or np.abs(np.int64(arg0)) != arg0:\n')
                    jga__crgwn += '  bodo.libs.array_kernels.setna(res, i)\n'
                    jga__crgwn += 'else:\n'
                    jga__crgwn += (
                        f'  res[i] = np.math.factorial(np.int64(arg0))')
                elif func_name == 'LN':
                    jga__crgwn += f'res[i] = np.log(arg0)'
                else:
                    jga__crgwn += f'res[i] = np.{func_name.lower()}(arg0)'
            else:
                ValueError(f'Unknown function name: {func_name}')
            gddlf__lpy = _get_numeric_output_dtype(func_name, arr)
            return gen_vectorized(qsciu__pekk, eauah__uah, sjf__zituk,
                jga__crgwn, gddlf__lpy)
    else:

        def overload_numeric_util(arr0, arr1):
            verify_int_float_arg(arr0, func_name, 'arr0')
            verify_int_float_arg(arr0, func_name, 'arr1')
            qsciu__pekk = ['arr0', 'arr1']
            eauah__uah = [arr0, arr1]
            sjf__zituk = [True, True]
            gddlf__lpy = _get_numeric_output_dtype(func_name, arr0, arr1)
            jga__crgwn = ''
            if func_name == 'MOD':
                jga__crgwn += 'if arg1 == 0:\n'
                jga__crgwn += '  bodo.libs.array_kernels.setna(res, i)\n'
                jga__crgwn += 'else:\n'
                jga__crgwn += (
                    '  res[i] = np.sign(arg0) * np.mod(np.abs(arg0), np.abs(arg1))'
                    )
            elif func_name == 'POWER':
                jga__crgwn += 'res[i] = np.power(np.float64(arg0), arg1)'
            elif func_name == 'ROUND':
                jga__crgwn += 'res[i] = np.round(arg0, arg1)'
            elif func_name == 'TRUNC':
                jga__crgwn += 'if int(arg1) == arg1:\n'
                jga__crgwn += (
                    '  res[i] = np.trunc(arg0 * (10.0 ** arg1)) * (10.0 ** -arg1)\n'
                    )
                jga__crgwn += 'else:\n'
                jga__crgwn += '  bodo.libs.array_kernels.setna(res, i)'
            else:
                raise ValueError(f'Unknown function name: {func_name}')
            return gen_vectorized(qsciu__pekk, eauah__uah, sjf__zituk,
                jga__crgwn, gddlf__lpy)
    return overload_numeric_util


def _install_numeric_overload(funcs_utils_names):
    for zmio__omv, dxpg__delv, func_name in funcs_utils_names:
        bqva__ntwz = create_numeric_func_overload(func_name)
        overload(zmio__omv)(bqva__ntwz)
        nhhk__dbbrr = create_numeric_util_overload(func_name)
        overload(dxpg__delv)(nhhk__dbbrr)


_install_numeric_overload(funcs_utils_names)


@numba.generated_jit(nopython=True)
def bitand(A, B):
    args = [A, B]
    for xecnb__zujb in range(2):
        if isinstance(args[xecnb__zujb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitand',
                ['A', 'B'], xecnb__zujb)

    def impl(A, B):
        return bitand_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftleft(A, B):
    args = [A, B]
    for xecnb__zujb in range(2):
        if isinstance(args[xecnb__zujb], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftleft', ['A', 'B'],
                xecnb__zujb)

    def impl(A, B):
        return bitshiftleft_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitnot(A):
    if isinstance(A, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.bitnot_util',
            ['A'], 0)

    def impl(A):
        return bitnot_util(A)
    return impl


@numba.generated_jit(nopython=True)
def bitor(A, B):
    args = [A, B]
    for xecnb__zujb in range(2):
        if isinstance(args[xecnb__zujb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitor',
                ['A', 'B'], xecnb__zujb)

    def impl(A, B):
        return bitor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitshiftright(A, B):
    args = [A, B]
    for xecnb__zujb in range(2):
        if isinstance(args[xecnb__zujb], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.bitshiftright', ['A', 'B'],
                xecnb__zujb)

    def impl(A, B):
        return bitshiftright_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def bitxor(A, B):
    args = [A, B]
    for xecnb__zujb in range(2):
        if isinstance(args[xecnb__zujb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.bitxor',
                ['A', 'B'], xecnb__zujb)

    def impl(A, B):
        return bitxor_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def conv(arr, old_base, new_base):
    args = [arr, old_base, new_base]
    for xecnb__zujb in range(3):
        if isinstance(args[xecnb__zujb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.conv', [
                'arr', 'old_base', 'new_base'], xecnb__zujb)

    def impl(arr, old_base, new_base):
        return conv_util(arr, old_base, new_base)
    return impl


@numba.generated_jit(nopython=True)
def getbit(A, B):
    args = [A, B]
    for xecnb__zujb in range(2):
        if isinstance(args[xecnb__zujb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.getbit',
                ['A', 'B'], xecnb__zujb)

    def impl(A, B):
        return getbit_util(A, B)
    return impl


@numba.generated_jit(nopython=True)
def haversine(lat1, lon1, lat2, lon2):
    args = [lat1, lon1, lat2, lon2]
    for xecnb__zujb in range(4):
        if isinstance(args[xecnb__zujb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.haversine',
                ['lat1', 'lon1', 'lat2', 'lon2'], xecnb__zujb)

    def impl(lat1, lon1, lat2, lon2):
        return haversine_util(lat1, lon1, lat2, lon2)
    return impl


@numba.generated_jit(nopython=True)
def div0(arr, divisor):
    args = [arr, divisor]
    for xecnb__zujb in range(2):
        if isinstance(args[xecnb__zujb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.div0', [
                'arr', 'divisor'], xecnb__zujb)

    def impl(arr, divisor):
        return div0_util(arr, divisor)
    return impl


@numba.generated_jit(nopython=True)
def log(arr, base):
    args = [arr, base]
    for xecnb__zujb in range(2):
        if isinstance(args[xecnb__zujb], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.log', [
                'arr', 'base'], xecnb__zujb)

    def impl(arr, base):
        return log_util(arr, base)
    return impl


@numba.generated_jit(nopython=True)
def negate(arr):
    if isinstance(arr, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.negate_util',
            ['arr'], 0)

    def impl(arr):
        return negate_util(arr)
    return impl


@numba.generated_jit(nopython=True)
def width_bucket(arr, min_val, max_val, num_buckets):
    args = [arr, min_val, max_val, num_buckets]
    for xecnb__zujb in range(4):
        if isinstance(args[xecnb__zujb], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.width_bucket', ['arr',
                'min_val', 'max_val', 'num_buckets'], xecnb__zujb)

    def impl(arr, min_val, max_val, num_buckets):
        return width_bucket_util(arr, min_val, max_val, num_buckets)
    return impl


@numba.generated_jit(nopython=True)
def bitand_util(A, B):
    verify_int_arg(A, 'bitand', 'A')
    verify_int_arg(B, 'bitand', 'B')
    qsciu__pekk = ['A', 'B']
    eauah__uah = [A, B]
    sjf__zituk = [True] * 2
    jga__crgwn = 'res[i] = arg0 & arg1'
    gddlf__lpy = get_common_broadcasted_type([A, B], 'bitand')
    return gen_vectorized(qsciu__pekk, eauah__uah, sjf__zituk, jga__crgwn,
        gddlf__lpy)


@numba.generated_jit(nopython=True)
def bitshiftleft_util(A, B):
    verify_int_arg(A, 'bitshiftleft', 'A')
    verify_int_arg(B, 'bitshiftleft', 'B')
    qsciu__pekk = ['A', 'B']
    eauah__uah = [A, B]
    sjf__zituk = [True] * 2
    jga__crgwn = 'res[i] = arg0 << arg1'
    gddlf__lpy = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(qsciu__pekk, eauah__uah, sjf__zituk, jga__crgwn,
        gddlf__lpy)


@numba.generated_jit(nopython=True)
def bitnot_util(A):
    verify_int_arg(A, 'bitnot', 'A')
    qsciu__pekk = ['A']
    eauah__uah = [A]
    sjf__zituk = [True]
    jga__crgwn = 'res[i] = ~arg0'
    if A == bodo.none:
        gddlf__lpy = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            ydef__aeb = A.dtype
        else:
            ydef__aeb = A
        gddlf__lpy = bodo.libs.int_arr_ext.IntegerArrayType(ydef__aeb)
    return gen_vectorized(qsciu__pekk, eauah__uah, sjf__zituk, jga__crgwn,
        gddlf__lpy)


@numba.generated_jit(nopython=True)
def bitor_util(A, B):
    verify_int_arg(A, 'bitor', 'A')
    verify_int_arg(B, 'bitor', 'B')
    qsciu__pekk = ['A', 'B']
    eauah__uah = [A, B]
    sjf__zituk = [True] * 2
    jga__crgwn = 'res[i] = arg0 | arg1'
    gddlf__lpy = get_common_broadcasted_type([A, B], 'bitor')
    return gen_vectorized(qsciu__pekk, eauah__uah, sjf__zituk, jga__crgwn,
        gddlf__lpy)


@numba.generated_jit(nopython=True)
def bitshiftright_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    qsciu__pekk = ['A', 'B']
    eauah__uah = [A, B]
    sjf__zituk = [True] * 2
    if A == bodo.none:
        ydef__aeb = gddlf__lpy = bodo.none
    else:
        if bodo.utils.utils.is_array_typ(A, True):
            ydef__aeb = A.dtype
        else:
            ydef__aeb = A
        gddlf__lpy = bodo.libs.int_arr_ext.IntegerArrayType(ydef__aeb)
    jga__crgwn = f'res[i] = arg0 >> arg1\n'
    return gen_vectorized(qsciu__pekk, eauah__uah, sjf__zituk, jga__crgwn,
        gddlf__lpy)


@numba.generated_jit(nopython=True)
def bitxor_util(A, B):
    verify_int_arg(A, 'bitxor', 'A')
    verify_int_arg(B, 'bitxor', 'B')
    qsciu__pekk = ['A', 'B']
    eauah__uah = [A, B]
    sjf__zituk = [True] * 2
    jga__crgwn = 'res[i] = arg0 ^ arg1'
    gddlf__lpy = get_common_broadcasted_type([A, B], 'bitxor')
    return gen_vectorized(qsciu__pekk, eauah__uah, sjf__zituk, jga__crgwn,
        gddlf__lpy)


@numba.generated_jit(nopython=True)
def conv_util(arr, old_base, new_base):
    verify_string_arg(arr, 'CONV', 'arr')
    verify_int_arg(old_base, 'CONV', 'old_base')
    verify_int_arg(new_base, 'CONV', 'new_base')
    qsciu__pekk = ['arr', 'old_base', 'new_base']
    eauah__uah = [arr, old_base, new_base]
    sjf__zituk = [True] * 3
    jga__crgwn = 'old_val = int(arg0, arg1)\n'
    jga__crgwn += 'if arg2 == 2:\n'
    jga__crgwn += "   res[i] = format(old_val, 'b')\n"
    jga__crgwn += 'elif arg2 == 8:\n'
    jga__crgwn += "   res[i] = format(old_val, 'o')\n"
    jga__crgwn += 'elif arg2 == 10:\n'
    jga__crgwn += "   res[i] = format(old_val, 'd')\n"
    jga__crgwn += 'elif arg2 == 16:\n'
    jga__crgwn += "   res[i] = format(old_val, 'x')\n"
    jga__crgwn += 'else:\n'
    jga__crgwn += '   bodo.libs.array_kernels.setna(res, i)\n'
    gddlf__lpy = bodo.string_array_type
    return gen_vectorized(qsciu__pekk, eauah__uah, sjf__zituk, jga__crgwn,
        gddlf__lpy)


@numba.generated_jit(nopython=True)
def getbit_util(A, B):
    verify_int_arg(A, 'bitshiftright', 'A')
    verify_int_arg(B, 'bitshiftright', 'B')
    qsciu__pekk = ['A', 'B']
    eauah__uah = [A, B]
    sjf__zituk = [True] * 2
    jga__crgwn = 'res[i] = (arg0 >> arg1) & 1'
    gddlf__lpy = bodo.libs.int_arr_ext.IntegerArrayType(types.uint8)
    return gen_vectorized(qsciu__pekk, eauah__uah, sjf__zituk, jga__crgwn,
        gddlf__lpy)


@numba.generated_jit(nopython=True)
def haversine_util(lat1, lon1, lat2, lon2):
    verify_int_float_arg(lat1, 'HAVERSINE', 'lat1')
    verify_int_float_arg(lon1, 'HAVERSINE', 'lon1')
    verify_int_float_arg(lat2, 'HAVERSINE', 'lat2')
    verify_int_float_arg(lon2, 'HAVERSINE', 'lon2')
    qsciu__pekk = ['lat1', 'lon1', 'lat2', 'lon2']
    eauah__uah = [lat1, lon1, lat2, lon2]
    kfhp__rchy = [True] * 4
    jga__crgwn = (
        'arg0, arg1, arg2, arg3 = map(np.radians, (arg0, arg1, arg2, arg3))\n')
    sdwa__npl = '(arg2 - arg0) * 0.5'
    zgslx__sxul = '(arg3 - arg1) * 0.5'
    zdy__udlkf = (
        f'np.square(np.sin({sdwa__npl})) + (np.cos(arg0) * np.cos(arg2) * np.square(np.sin({zgslx__sxul})))'
        )
    jga__crgwn += f'res[i] = 12742.0 * np.arcsin(np.sqrt({zdy__udlkf}))\n'
    gddlf__lpy = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(qsciu__pekk, eauah__uah, kfhp__rchy, jga__crgwn,
        gddlf__lpy)


@numba.generated_jit(nopython=True)
def div0_util(arr, divisor):
    verify_int_float_arg(arr, 'DIV0', 'arr')
    verify_int_float_arg(divisor, 'DIV0', 'divisor')
    qsciu__pekk = ['arr', 'divisor']
    eauah__uah = [arr, divisor]
    kfhp__rchy = [True] * 2
    jga__crgwn = 'res[i] = arg0 / arg1 if arg1 else 0\n'
    gddlf__lpy = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(qsciu__pekk, eauah__uah, kfhp__rchy, jga__crgwn,
        gddlf__lpy)


@numba.generated_jit(nopython=True)
def log_util(arr, base):
    verify_int_float_arg(arr, 'log', 'arr')
    verify_int_float_arg(base, 'log', 'base')
    qsciu__pekk = ['arr', 'base']
    eauah__uah = [arr, base]
    sjf__zituk = [True] * 2
    jga__crgwn = 'res[i] = np.log(arg0) / np.log(arg1)'
    gddlf__lpy = types.Array(bodo.float64, 1, 'C')
    return gen_vectorized(qsciu__pekk, eauah__uah, sjf__zituk, jga__crgwn,
        gddlf__lpy)


@numba.generated_jit(nopython=True)
def negate_util(arr):
    qsciu__pekk = ['arr']
    eauah__uah = [arr]
    sjf__zituk = [True]
    if bodo.utils.utils.is_array_typ(arr, False):
        ydef__aeb = arr.dtype
    elif bodo.utils.utils.is_array_typ(arr, True):
        ydef__aeb = arr.data.dtype
    else:
        ydef__aeb = arr
    jga__crgwn = {types.uint8: 'res[i] = -np.int16(arg0)', types.uint16:
        'res[i] = -np.int32(arg0)', types.uint32: 'res[i] = -np.int64(arg0)'
        }.get(ydef__aeb, 'res[i] = -arg0')
    ydef__aeb = {types.uint8: types.int16, types.uint16: types.int32, types
        .uint32: types.int64, types.uint64: types.int64}.get(ydef__aeb,
        ydef__aeb)
    if isinstance(ydef__aeb, types.Integer):
        gddlf__lpy = bodo.utils.typing.dtype_to_array_type(ydef__aeb)
    else:
        gddlf__lpy = arr
    gddlf__lpy = bodo.utils.typing.to_nullable_type(gddlf__lpy)
    return gen_vectorized(qsciu__pekk, eauah__uah, sjf__zituk, jga__crgwn,
        gddlf__lpy)


@numba.generated_jit(nopython=True)
def width_bucket_util(arr, min_val, max_val, num_buckets):
    verify_int_float_arg(arr, 'WIDTH_BUCKET', 'arr')
    verify_int_float_arg(min_val, 'WIDTH_BUCKET', 'min_val')
    verify_int_float_arg(max_val, 'WIDTH_BUCKET', 'max_val')
    verify_int_arg(num_buckets, 'WIDTH_BUCKET', 'num_buckets')
    qsciu__pekk = ['arr', 'min_val', 'max_val', 'num_buckets']
    eauah__uah = [arr, min_val, max_val, num_buckets]
    sjf__zituk = [True] * 4
    jga__crgwn = (
        "if arg1 >= arg2: raise ValueError('min_val must be less than max_val')\n"
        )
    jga__crgwn += (
        "if arg3 <= 0: raise ValueError('num_buckets must be a positive integer')\n"
        )
    jga__crgwn += (
        'res[i] = min(max(-1.0, math.floor((arg0 - arg1) / ((arg2 - arg1) / arg3))), arg3) + 1.0'
        )
    gddlf__lpy = bodo.libs.int_arr_ext.IntegerArrayType(types.int64)
    return gen_vectorized(qsciu__pekk, eauah__uah, sjf__zituk, jga__crgwn,
        gddlf__lpy)
