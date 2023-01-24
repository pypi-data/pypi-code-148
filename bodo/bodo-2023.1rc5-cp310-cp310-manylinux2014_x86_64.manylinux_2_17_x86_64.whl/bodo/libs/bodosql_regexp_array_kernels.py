"""
Implements regexp array kernels that are specific to BodoSQL
"""
import re
import numba
from numba.core import types
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


def posix_to_re(pattern):
    fkjxu__soprm = {'[:alnum:]': 'A-Za-z0-9', '[:alpha:]': 'A-Za-z',
        '[:ascii:]': '\x01-\x7f', '[:blank:]': ' \t', '[:cntrl:]':
        '\x01-\x1f\x7f', '[:digit:]': '0-9', '[:graph:]': '!-~',
        '[:lower:]': 'a-z', '[:print:]': ' -~', '[:punct:]':
        '\\]\\[!"#$%&\'()*+,./:;<=>?@\\^_`{|}~-', '[:space:]':
        ' \t\r\n\x0b\x0c', '[:upper:]': 'A-Z', '[:word:]': 'A-Za-z0-9_',
        '[:xdigit:]': 'A-Fa-f0-9'}
    for yxnzy__qedx in fkjxu__soprm:
        pattern = pattern.replace(yxnzy__qedx, fkjxu__soprm[yxnzy__qedx])
    return pattern


def make_flag_bitvector(flags):
    qtukx__gdrm = 0
    if 'i' in flags:
        if 'c' not in flags or flags.rindex('i') > flags.rindex('c'):
            qtukx__gdrm = qtukx__gdrm | re.I
    if 'm' in flags:
        qtukx__gdrm = qtukx__gdrm | re.M
    if 's' in flags:
        qtukx__gdrm = qtukx__gdrm | re.S
    return qtukx__gdrm


@numba.generated_jit(nopython=True)
def regexp_count(arr, pattern, position, flags):
    args = [arr, pattern, position, flags]
    for lpdw__kbm in range(4):
        if isinstance(args[lpdw__kbm], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_count', ['arr',
                'pattern', 'position', 'flags'], lpdw__kbm)

    def impl(arr, pattern, position, flags):
        return regexp_count_util(arr, numba.literally(pattern), position,
            numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_instr(arr, pattern, position, occurrence, option, flags, group):
    args = [arr, pattern, position, occurrence, option, flags, group]
    for lpdw__kbm in range(7):
        if isinstance(args[lpdw__kbm], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_instr', ['arr',
                'pattern', 'position', 'occurrence', 'option', 'flags',
                'group'], lpdw__kbm)

    def impl(arr, pattern, position, occurrence, option, flags, group):
        return regexp_instr_util(arr, numba.literally(pattern), position,
            occurrence, option, numba.literally(flags), group)
    return impl


@numba.generated_jit(nopython=True)
def regexp_like(arr, pattern, flags):
    args = [arr, pattern, flags]
    for lpdw__kbm in range(3):
        if isinstance(args[lpdw__kbm], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.regexp_like'
                , ['arr', 'pattern', 'flags'], lpdw__kbm)

    def impl(arr, pattern, flags):
        return regexp_like_util(arr, numba.literally(pattern), numba.
            literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_replace(arr, pattern, replacement, position, occurrence, flags):
    args = [arr, pattern, replacement, position, occurrence, flags]
    for lpdw__kbm in range(6):
        if isinstance(args[lpdw__kbm], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_replace', ['arr',
                'pattern', 'replacement', 'position', 'occurrence', 'flags'
                ], lpdw__kbm)

    def impl(arr, pattern, replacement, position, occurrence, flags):
        return regexp_replace_util(arr, numba.literally(pattern),
            replacement, position, occurrence, numba.literally(flags))
    return impl


@numba.generated_jit(nopython=True)
def regexp_substr(arr, pattern, position, occurrence, flags, group):
    args = [arr, pattern, position, occurrence, flags, group]
    for lpdw__kbm in range(6):
        if isinstance(args[lpdw__kbm], types.optional):
            return unopt_argument(
                'bodo.libs.bodosql_array_kernels.regexp_substr', ['arr',
                'pattern', 'position', 'occurrence', 'flags', 'group'],
                lpdw__kbm)

    def impl(arr, pattern, position, occurrence, flags, group):
        return regexp_substr_util(arr, numba.literally(pattern), position,
            occurrence, numba.literally(flags), group)
    return impl


@numba.generated_jit(nopython=True)
def regexp_count_util(arr, pattern, position, flags):
    verify_string_arg(arr, 'REGEXP_COUNT', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_COUNT', 'pattern')
    verify_int_arg(position, 'REGEXP_COUNT', 'position')
    verify_scalar_string_arg(flags, 'REGEXP_COUNT', 'flags')
    bswzx__giroe = ['arr', 'pattern', 'position', 'flags']
    yxmih__joluy = [arr, pattern, position, flags]
    gry__fjg = [True] * 4
    vhw__nou = bodo.utils.typing.get_overload_const_str(pattern)
    bsve__efcs = posix_to_re(vhw__nou)
    buap__rkxsu = bodo.utils.typing.get_overload_const_str(flags)
    aab__fzesc = make_flag_bitvector(buap__rkxsu)
    nvz__zkzl = '\n'
    dnl__ddjwv = ''
    if bodo.utils.utils.is_array_typ(position, True):
        dnl__ddjwv += """if arg2 <= 0: raise ValueError('REGEXP_COUNT requires a positive position')
"""
    else:
        nvz__zkzl += """if position <= 0: raise ValueError('REGEXP_COUNT requires a positive position')
"""
    if bsve__efcs == '':
        dnl__ddjwv += 'res[i] = 0'
    else:
        nvz__zkzl += f'r = re.compile({repr(bsve__efcs)}, {aab__fzesc})'
        dnl__ddjwv += 'res[i] = len(r.findall(arg0[arg2-1:]))'
    rax__yae = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(bswzx__giroe, yxmih__joluy, gry__fjg, dnl__ddjwv,
        rax__yae, prefix_code=nvz__zkzl)


@numba.generated_jit(nopython=True)
def regexp_instr_util(arr, pattern, position, occurrence, option, flags, group
    ):
    verify_string_arg(arr, 'REGEXP_INSTR', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_INSTR', 'pattern')
    verify_int_arg(position, 'REGEXP_INSTR', 'position')
    verify_int_arg(occurrence, 'REGEXP_INSTR', 'occurrence')
    verify_int_arg(option, 'REGEXP_INSTR', 'option')
    verify_scalar_string_arg(flags, 'REGEXP_INSTR', 'flags')
    verify_int_arg(group, 'REGEXP_INSTR', 'group')
    bswzx__giroe = ['arr', 'pattern', 'position', 'occurrence', 'option',
        'flags', 'group']
    yxmih__joluy = [arr, pattern, position, occurrence, option, flags, group]
    gry__fjg = [True] * 7
    vhw__nou = bodo.utils.typing.get_overload_const_str(pattern)
    bsve__efcs = posix_to_re(vhw__nou)
    yebv__uxvec = re.compile(vhw__nou).groups
    buap__rkxsu = bodo.utils.typing.get_overload_const_str(flags)
    aab__fzesc = make_flag_bitvector(buap__rkxsu)
    nvz__zkzl = '\n'
    dnl__ddjwv = ''
    if bodo.utils.utils.is_array_typ(position, True):
        dnl__ddjwv += """if arg2 <= 0: raise ValueError('REGEXP_INSTR requires a positive position')
"""
    else:
        nvz__zkzl += """if position <= 0: raise ValueError('REGEXP_INSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        dnl__ddjwv += """if arg3 <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    else:
        nvz__zkzl += """if occurrence <= 0: raise ValueError('REGEXP_INSTR requires a positive occurrence')
"""
    if bodo.utils.utils.is_array_typ(option, True):
        dnl__ddjwv += """if arg4 != 0 and arg4 != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    else:
        nvz__zkzl += """if option != 0 and option != 1: raise ValueError('REGEXP_INSTR requires option to be 0 or 1')
"""
    if 'e' in buap__rkxsu:
        if bodo.utils.utils.is_array_typ(group, True):
            dnl__ddjwv += f"""if not (1 <= arg6 <= {yebv__uxvec}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
        else:
            nvz__zkzl += f"""if not (1 <= group <= {yebv__uxvec}): raise ValueError('REGEXP_INSTR requires a valid group number')
"""
    if bsve__efcs == '':
        dnl__ddjwv += 'res[i] = 0'
    else:
        nvz__zkzl += f'r = re.compile({repr(bsve__efcs)}, {aab__fzesc})'
        dnl__ddjwv += 'arg0 = arg0[arg2-1:]\n'
        dnl__ddjwv += 'res[i] = 0\n'
        dnl__ddjwv += 'offset = arg2\n'
        dnl__ddjwv += 'for j in range(arg3):\n'
        dnl__ddjwv += '   match = r.search(arg0)\n'
        dnl__ddjwv += '   if match is None:\n'
        dnl__ddjwv += '      res[i] = 0\n'
        dnl__ddjwv += '      break\n'
        dnl__ddjwv += '   start, end = match.span()\n'
        dnl__ddjwv += '   if j == arg3 - 1:\n'
        if 'e' in buap__rkxsu:
            dnl__ddjwv += '      res[i] = offset + match.span(arg6)[arg4]\n'
        else:
            dnl__ddjwv += '      res[i] = offset + match.span()[arg4]\n'
        dnl__ddjwv += '   else:\n'
        dnl__ddjwv += '      offset += end\n'
        dnl__ddjwv += '      arg0 = arg0[end:]\n'
    rax__yae = bodo.libs.int_arr_ext.IntegerArrayType(types.int32)
    return gen_vectorized(bswzx__giroe, yxmih__joluy, gry__fjg, dnl__ddjwv,
        rax__yae, prefix_code=nvz__zkzl)


@numba.generated_jit(nopython=True)
def regexp_like_util(arr, pattern, flags):
    verify_string_arg(arr, 'REGEXP_LIKE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_LIKE', 'pattern')
    verify_scalar_string_arg(flags, 'REGEXP_LIKE', 'flags')
    bswzx__giroe = ['arr', 'pattern', 'flags']
    yxmih__joluy = [arr, pattern, flags]
    gry__fjg = [True] * 3
    vhw__nou = bodo.utils.typing.get_overload_const_str(pattern)
    bsve__efcs = posix_to_re(vhw__nou)
    buap__rkxsu = bodo.utils.typing.get_overload_const_str(flags)
    aab__fzesc = make_flag_bitvector(buap__rkxsu)
    if bsve__efcs == '':
        nvz__zkzl = None
        dnl__ddjwv = 'res[i] = len(arg0) == 0'
    else:
        nvz__zkzl = f'r = re.compile({repr(bsve__efcs)}, {aab__fzesc})'
        dnl__ddjwv = 'if r.fullmatch(arg0) is None:\n'
        dnl__ddjwv += '   res[i] = False\n'
        dnl__ddjwv += 'else:\n'
        dnl__ddjwv += '   res[i] = True\n'
    rax__yae = bodo.libs.bool_arr_ext.boolean_array
    return gen_vectorized(bswzx__giroe, yxmih__joluy, gry__fjg, dnl__ddjwv,
        rax__yae, prefix_code=nvz__zkzl)


@numba.generated_jit(nopython=True)
def regexp_replace_util(arr, pattern, replacement, position, occurrence, flags
    ):
    verify_string_arg(arr, 'REGEXP_REPLACE', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_REPLACE', 'pattern')
    verify_string_arg(replacement, 'REGEXP_REPLACE', 'replacement')
    verify_int_arg(position, 'REGEXP_REPLACE', 'position')
    verify_int_arg(occurrence, 'REGEXP_REPLACE', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_REPLACE', 'flags')
    bswzx__giroe = ['arr', 'pattern', 'replacement', 'position',
        'occurrence', 'flags']
    yxmih__joluy = [arr, pattern, replacement, position, occurrence, flags]
    gry__fjg = [True] * 6
    vhw__nou = bodo.utils.typing.get_overload_const_str(pattern)
    bsve__efcs = posix_to_re(vhw__nou)
    buap__rkxsu = bodo.utils.typing.get_overload_const_str(flags)
    aab__fzesc = make_flag_bitvector(buap__rkxsu)
    nvz__zkzl = '\n'
    dnl__ddjwv = ''
    if bodo.utils.utils.is_array_typ(position, True):
        dnl__ddjwv += """if arg3 <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    else:
        nvz__zkzl += """if position <= 0: raise ValueError('REGEXP_REPLACE requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        dnl__ddjwv += """if arg4 < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    else:
        nvz__zkzl += """if occurrence < 0: raise ValueError('REGEXP_REPLACE requires a non-negative occurrence')
"""
    if bsve__efcs == '':
        dnl__ddjwv += 'res[i] = arg0'
    else:
        nvz__zkzl += f'r = re.compile({repr(bsve__efcs)}, {aab__fzesc})'
        dnl__ddjwv += 'result = arg0[:arg3-1]\n'
        dnl__ddjwv += 'arg0 = arg0[arg3-1:]\n'
        dnl__ddjwv += 'if arg4 == 0:\n'
        dnl__ddjwv += '   res[i] = result + r.sub(arg2, arg0)\n'
        dnl__ddjwv += 'else:\n'
        dnl__ddjwv += '   nomatch = False\n'
        dnl__ddjwv += '   for j in range(arg4 - 1):\n'
        dnl__ddjwv += '      match = r.search(arg0)\n'
        dnl__ddjwv += '      if match is None:\n'
        dnl__ddjwv += '         res[i] = result + arg0\n'
        dnl__ddjwv += '         nomatch = True\n'
        dnl__ddjwv += '         break\n'
        dnl__ddjwv += '      _, end = match.span()\n'
        dnl__ddjwv += '      result += arg0[:end]\n'
        dnl__ddjwv += '      arg0 = arg0[end:]\n'
        dnl__ddjwv += '   if nomatch == False:\n'
        dnl__ddjwv += '      result += r.sub(arg2, arg0, count=1)\n'
        dnl__ddjwv += '      res[i] = result'
    rax__yae = bodo.string_array_type
    return gen_vectorized(bswzx__giroe, yxmih__joluy, gry__fjg, dnl__ddjwv,
        rax__yae, prefix_code=nvz__zkzl)


@numba.generated_jit(nopython=True)
def regexp_substr_util(arr, pattern, position, occurrence, flags, group):
    verify_string_arg(arr, 'REGEXP_SUBSTR', 'arr')
    verify_scalar_string_arg(pattern, 'REGEXP_SUBSTR', 'pattern')
    verify_int_arg(position, 'REGEXP_SUBSTR', 'position')
    verify_int_arg(occurrence, 'REGEXP_SUBSTR', 'occurrence')
    verify_scalar_string_arg(flags, 'REGEXP_SUBSTR', 'flags')
    verify_int_arg(group, 'REGEXP_SUBSTR', 'group')
    bswzx__giroe = ['arr', 'pattern', 'position', 'occurrence', 'flags',
        'group']
    yxmih__joluy = [arr, pattern, position, occurrence, flags, group]
    gry__fjg = [True] * 6
    vhw__nou = bodo.utils.typing.get_overload_const_str(pattern)
    bsve__efcs = posix_to_re(vhw__nou)
    yebv__uxvec = re.compile(vhw__nou).groups
    buap__rkxsu = bodo.utils.typing.get_overload_const_str(flags)
    aab__fzesc = make_flag_bitvector(buap__rkxsu)
    nvz__zkzl = '\n'
    dnl__ddjwv = ''
    if bodo.utils.utils.is_array_typ(position, True):
        dnl__ddjwv += """if arg2 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    else:
        nvz__zkzl += """if position <= 0: raise ValueError('REGEXP_SUBSTR requires a positive position')
"""
    if bodo.utils.utils.is_array_typ(occurrence, True):
        dnl__ddjwv += """if arg3 <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    else:
        nvz__zkzl += """if occurrence <= 0: raise ValueError('REGEXP_SUBSTR requires a positive occurrence')
"""
    if 'e' in buap__rkxsu:
        if bodo.utils.utils.is_array_typ(group, True):
            dnl__ddjwv += f"""if not (1 <= arg5 <= {yebv__uxvec}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
        else:
            nvz__zkzl += f"""if not (1 <= group <= {yebv__uxvec}): raise ValueError('REGEXP_SUBSTR requires a valid group number')
"""
    if bsve__efcs == '':
        dnl__ddjwv += 'bodo.libs.array_kernels.setna(res, i)'
    else:
        nvz__zkzl += f'r = re.compile({repr(bsve__efcs)}, {aab__fzesc})'
        if 'e' in buap__rkxsu:
            dnl__ddjwv += 'matches = r.findall(arg0[arg2-1:])\n'
            dnl__ddjwv += f'if len(matches) < arg3:\n'
            dnl__ddjwv += '   bodo.libs.array_kernels.setna(res, i)\n'
            dnl__ddjwv += 'else:\n'
            if yebv__uxvec == 1:
                dnl__ddjwv += '   res[i] = matches[arg3-1]\n'
            else:
                dnl__ddjwv += '   res[i] = matches[arg3-1][arg5-1]\n'
        else:
            dnl__ddjwv += 'arg0 = str(arg0)[arg2-1:]\n'
            dnl__ddjwv += 'for j in range(arg3):\n'
            dnl__ddjwv += '   match = r.search(arg0)\n'
            dnl__ddjwv += '   if match is None:\n'
            dnl__ddjwv += '      bodo.libs.array_kernels.setna(res, i)\n'
            dnl__ddjwv += '      break\n'
            dnl__ddjwv += '   start, end = match.span()\n'
            dnl__ddjwv += '   if j == arg3 - 1:\n'
            dnl__ddjwv += '      res[i] = arg0[start:end]\n'
            dnl__ddjwv += '   else:\n'
            dnl__ddjwv += '      arg0 = arg0[end:]\n'
    rax__yae = bodo.string_array_type
    return gen_vectorized(bswzx__giroe, yxmih__joluy, gry__fjg, dnl__ddjwv,
        rax__yae, prefix_code=nvz__zkzl)
