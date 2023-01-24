"""
Implements array kernels that are specific to BodoSQL which have a variable
number of arguments
"""
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.bodosql_array_kernel_utils import *
from bodo.utils.typing import is_str_arr_type, raise_bodo_error


def coalesce(A):
    return


@overload(coalesce)
def overload_coalesce(A):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('Coalesce argument must be a tuple')
    for gxawq__yjpo in range(len(A)):
        if isinstance(A[gxawq__yjpo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.coalesce',
                ['A'], 0, container_arg=gxawq__yjpo, container_length=len(A))

    def impl(A):
        return coalesce_util(A)
    return impl


def coalesce_util(A):
    return


@overload(coalesce_util, no_unliteral=True)
def overload_coalesce_util(A):
    if len(A) == 0:
        raise_bodo_error('Cannot coalesce 0 columns')
    mxlbh__kvxvd = None
    sbdn__jwb = []
    yglo__egz = False
    for gxawq__yjpo in range(len(A)):
        if A[gxawq__yjpo] == bodo.none:
            sbdn__jwb.append(gxawq__yjpo)
        elif not bodo.utils.utils.is_array_typ(A[gxawq__yjpo]):
            for flg__mjthh in range(gxawq__yjpo + 1, len(A)):
                sbdn__jwb.append(flg__mjthh)
                if bodo.utils.utils.is_array_typ(A[flg__mjthh]):
                    mxlbh__kvxvd = f'A[{flg__mjthh}]'
                    yglo__egz = True
            break
        else:
            yglo__egz = True
    fcaxp__bfz = [f'A{gxawq__yjpo}' for gxawq__yjpo in range(len(A)) if 
        gxawq__yjpo not in sbdn__jwb]
    eis__lhnd = [A[gxawq__yjpo] for gxawq__yjpo in range(len(A)) if 
        gxawq__yjpo not in sbdn__jwb]
    gamm__iwei = get_common_broadcasted_type(eis__lhnd, 'COALESCE')
    bdvut__tfiaw = yglo__egz and is_str_arr_type(gamm__iwei)
    aqmcd__ptme = [False] * (len(A) - len(sbdn__jwb))
    ogrow__fzorp = False
    if bdvut__tfiaw:
        ogrow__fzorp = True
        for flg__mjthh, pwvjm__rdpu in enumerate(eis__lhnd):
            ogrow__fzorp = ogrow__fzorp and (pwvjm__rdpu == bodo.
                string_type or pwvjm__rdpu == bodo.dict_str_arr_type or 
                isinstance(pwvjm__rdpu, bodo.SeriesType) and pwvjm__rdpu.
                data == bodo.dict_str_arr_type)
    ixe__dovi = ''
    jiqr__ngp = True
    eptbj__vjb = False
    wvmn__aszk = 0
    orqya__jegtr = None
    if ogrow__fzorp:
        orqya__jegtr = 'num_strings = 0\n'
        orqya__jegtr += 'num_chars = 0\n'
        orqya__jegtr += 'is_dict_global = True\n'
        for gxawq__yjpo in range(len(A)):
            if gxawq__yjpo in sbdn__jwb:
                wvmn__aszk += 1
                continue
            elif eis__lhnd[gxawq__yjpo - wvmn__aszk] != bodo.string_type:
                orqya__jegtr += (
                    f'old_indices{gxawq__yjpo - wvmn__aszk} = A{gxawq__yjpo}._indices\n'
                    )
                orqya__jegtr += (
                    f'old_data{gxawq__yjpo - wvmn__aszk} = A{gxawq__yjpo}._data\n'
                    )
                orqya__jegtr += f"""is_dict_global = is_dict_global and A{gxawq__yjpo}._has_global_dictionary
"""
                orqya__jegtr += (
                    f'index_offset{gxawq__yjpo - wvmn__aszk} = num_strings\n')
                orqya__jegtr += (
                    f'num_strings += len(old_data{gxawq__yjpo - wvmn__aszk})\n'
                    )
                orqya__jegtr += f"""num_chars += bodo.libs.str_arr_ext.num_total_chars(old_data{gxawq__yjpo - wvmn__aszk})
"""
            else:
                orqya__jegtr += f'num_strings += 1\n'
                orqya__jegtr += f"""num_chars += bodo.libs.str_ext.unicode_to_utf8_len(A{gxawq__yjpo})
"""
    wvmn__aszk = 0
    for gxawq__yjpo in range(len(A)):
        if gxawq__yjpo in sbdn__jwb:
            wvmn__aszk += 1
            continue
        elif bodo.utils.utils.is_array_typ(A[gxawq__yjpo]):
            zwr__xnz = 'if' if jiqr__ngp else 'elif'
            ixe__dovi += (
                f'{zwr__xnz} not bodo.libs.array_kernels.isna(A{gxawq__yjpo}, i):\n'
                )
            if ogrow__fzorp:
                ixe__dovi += f"""   res[i] = old_indices{gxawq__yjpo - wvmn__aszk}[i] + index_offset{gxawq__yjpo - wvmn__aszk}
"""
            elif bdvut__tfiaw:
                ixe__dovi += f"""   bodo.libs.str_arr_ext.get_str_arr_item_copy(res, i, A{gxawq__yjpo}, i)
"""
            else:
                ixe__dovi += f'   res[i] = arg{gxawq__yjpo - wvmn__aszk}\n'
            jiqr__ngp = False
        else:
            assert not eptbj__vjb, 'should not encounter more than one scalar due to dead column pruning'
            kmtk__nbxcu = ''
            if not jiqr__ngp:
                ixe__dovi += 'else:\n'
                kmtk__nbxcu = '   '
            if ogrow__fzorp:
                ixe__dovi += f'{kmtk__nbxcu}res[i] = num_strings - 1\n'
            else:
                ixe__dovi += (
                    f'{kmtk__nbxcu}res[i] = arg{gxawq__yjpo - wvmn__aszk}\n')
            eptbj__vjb = True
            break
    if not eptbj__vjb:
        if not jiqr__ngp:
            ixe__dovi += 'else:\n'
            ixe__dovi += '   bodo.libs.array_kernels.setna(res, i)'
        else:
            ixe__dovi += 'bodo.libs.array_kernels.setna(res, i)'
    ugouc__tybj = None
    if ogrow__fzorp:
        wvmn__aszk = 0
        ugouc__tybj = """dict_data = bodo.libs.str_arr_ext.pre_alloc_string_array(num_strings, num_chars)
"""
        ugouc__tybj += 'curr_index = 0\n'
        for gxawq__yjpo in range(len(A)):
            if gxawq__yjpo in sbdn__jwb:
                wvmn__aszk += 1
            elif eis__lhnd[gxawq__yjpo - wvmn__aszk] != bodo.string_type:
                ugouc__tybj += (
                    f'section_len = len(old_data{gxawq__yjpo - wvmn__aszk})\n')
                ugouc__tybj += f'for l in range(section_len):\n'
                ugouc__tybj += f"""    bodo.libs.str_arr_ext.get_str_arr_item_copy(dict_data, curr_index + l, old_data{gxawq__yjpo - wvmn__aszk}, l)
"""
                ugouc__tybj += f'curr_index += section_len\n'
            else:
                ugouc__tybj += f'dict_data[curr_index] = A{gxawq__yjpo}\n'
                ugouc__tybj += f'curr_index += 1\n'
        ugouc__tybj += """duplicated_res = bodo.libs.dict_arr_ext.init_dict_arr(dict_data, res, is_dict_global, False)
"""
        ugouc__tybj += """res = bodo.libs.array.drop_duplicates_local_dictionary(duplicated_res, False)
"""
    uawb__upw = 'A'
    mnib__jdo = {f'A{gxawq__yjpo}': f'A[{gxawq__yjpo}]' for gxawq__yjpo in
        range(len(A)) if gxawq__yjpo not in sbdn__jwb}
    if ogrow__fzorp:
        gamm__iwei = bodo.libs.dict_arr_ext.dict_indices_arr_type
    return gen_vectorized(fcaxp__bfz, eis__lhnd, aqmcd__ptme, ixe__dovi,
        gamm__iwei, uawb__upw, mnib__jdo, mxlbh__kvxvd,
        support_dict_encoding=False, prefix_code=orqya__jegtr, suffix_code=
        ugouc__tybj, alloc_array_scalars=not bdvut__tfiaw)


@numba.generated_jit(nopython=True)
def decode(A):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('Decode argument must be a tuple')
    for gxawq__yjpo in range(len(A)):
        if isinstance(A[gxawq__yjpo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.decode',
                ['A'], 0, container_arg=gxawq__yjpo, container_length=len(A))

    def impl(A):
        return decode_util(A)
    return impl


@numba.generated_jit(nopython=True)
def decode_util(A):
    if len(A) < 3:
        raise_bodo_error('Need at least 3 arguments to DECODE')
    fcaxp__bfz = [f'A{gxawq__yjpo}' for gxawq__yjpo in range(len(A))]
    eis__lhnd = [A[gxawq__yjpo] for gxawq__yjpo in range(len(A))]
    aqmcd__ptme = [False] * len(A)
    ixe__dovi = ''
    for gxawq__yjpo in range(1, len(A) - 1, 2):
        zwr__xnz = 'if' if len(ixe__dovi) == 0 else 'elif'
        if A[gxawq__yjpo + 1] == bodo.none:
            ldvgx__xpzp = '   bodo.libs.array_kernels.setna(res, i)\n'
        elif bodo.utils.utils.is_array_typ(A[gxawq__yjpo + 1]):
            ldvgx__xpzp = (
                f'   if bodo.libs.array_kernels.isna({fcaxp__bfz[gxawq__yjpo + 1]}, i):\n'
                )
            ldvgx__xpzp += f'      bodo.libs.array_kernels.setna(res, i)\n'
            ldvgx__xpzp += f'   else:\n'
            ldvgx__xpzp += f'      res[i] = arg{gxawq__yjpo + 1}\n'
        else:
            ldvgx__xpzp = f'   res[i] = arg{gxawq__yjpo + 1}\n'
        if A[0] == bodo.none and (bodo.utils.utils.is_array_typ(A[
            gxawq__yjpo]) or A[gxawq__yjpo] == bodo.none):
            if A[gxawq__yjpo] == bodo.none:
                ixe__dovi += f'{zwr__xnz} True:\n'
                ixe__dovi += ldvgx__xpzp
                break
            else:
                ixe__dovi += f"""{zwr__xnz} bodo.libs.array_kernels.isna({fcaxp__bfz[gxawq__yjpo]}, i):
"""
                ixe__dovi += ldvgx__xpzp
        elif A[0] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[0]):
            if bodo.utils.utils.is_array_typ(A[gxawq__yjpo]):
                ixe__dovi += f"""{zwr__xnz} (bodo.libs.array_kernels.isna({fcaxp__bfz[0]}, i) and bodo.libs.array_kernels.isna({fcaxp__bfz[gxawq__yjpo]}, i)) or (not bodo.libs.array_kernels.isna({fcaxp__bfz[0]}, i) and not bodo.libs.array_kernels.isna({fcaxp__bfz[gxawq__yjpo]}, i) and arg0 == arg{gxawq__yjpo}):
"""
                ixe__dovi += ldvgx__xpzp
            elif A[gxawq__yjpo] == bodo.none:
                ixe__dovi += (
                    f'{zwr__xnz} bodo.libs.array_kernels.isna({fcaxp__bfz[0]}, i):\n'
                    )
                ixe__dovi += ldvgx__xpzp
            else:
                ixe__dovi += f"""{zwr__xnz} (not bodo.libs.array_kernels.isna({fcaxp__bfz[0]}, i)) and arg0 == arg{gxawq__yjpo}:
"""
                ixe__dovi += ldvgx__xpzp
        elif A[gxawq__yjpo] == bodo.none:
            pass
        elif bodo.utils.utils.is_array_typ(A[gxawq__yjpo]):
            ixe__dovi += f"""{zwr__xnz} (not bodo.libs.array_kernels.isna({fcaxp__bfz[gxawq__yjpo]}, i)) and arg0 == arg{gxawq__yjpo}:
"""
            ixe__dovi += ldvgx__xpzp
        else:
            ixe__dovi += f'{zwr__xnz} arg0 == arg{gxawq__yjpo}:\n'
            ixe__dovi += ldvgx__xpzp
    if len(ixe__dovi) > 0:
        ixe__dovi += 'else:\n'
    if len(A) % 2 == 0 and A[-1] != bodo.none:
        if bodo.utils.utils.is_array_typ(A[-1]):
            ixe__dovi += (
                f'   if bodo.libs.array_kernels.isna({fcaxp__bfz[-1]}, i):\n')
            ixe__dovi += '      bodo.libs.array_kernels.setna(res, i)\n'
            ixe__dovi += '   else:\n'
        ixe__dovi += f'      res[i] = arg{len(A) - 1}'
    else:
        ixe__dovi += '   bodo.libs.array_kernels.setna(res, i)'
    uawb__upw = 'A'
    mnib__jdo = {f'A{gxawq__yjpo}': f'A[{gxawq__yjpo}]' for gxawq__yjpo in
        range(len(A))}
    if len(eis__lhnd) % 2 == 0:
        gwtv__jacy = [eis__lhnd[0]] + eis__lhnd[1:-1:2]
        xtxx__fkqr = eis__lhnd[2::2] + [eis__lhnd[-1]]
    else:
        gwtv__jacy = [eis__lhnd[0]] + eis__lhnd[1::2]
        xtxx__fkqr = eis__lhnd[2::2]
    zeo__czv = get_common_broadcasted_type(gwtv__jacy, 'DECODE')
    gamm__iwei = get_common_broadcasted_type(xtxx__fkqr, 'DECODE')
    if gamm__iwei == bodo.none:
        gamm__iwei = zeo__czv
    jtmf__cmr = bodo.utils.utils.is_array_typ(A[0]
        ) and bodo.none not in gwtv__jacy and len(eis__lhnd) % 2 == 1
    return gen_vectorized(fcaxp__bfz, eis__lhnd, aqmcd__ptme, ixe__dovi,
        gamm__iwei, uawb__upw, mnib__jdo, support_dict_encoding=jtmf__cmr)


def concat_ws(A, sep):
    return


@overload(concat_ws)
def overload_concat_ws(A, sep):
    if not isinstance(A, (types.Tuple, types.UniTuple)):
        raise_bodo_error('concat_ws argument must be a tuple')
    for gxawq__yjpo in range(len(A)):
        if isinstance(A[gxawq__yjpo], types.optional):
            return unopt_argument('bodo.libs.bodosql_array_kernels.concat_ws',
                ['A', 'sep'], 0, container_arg=gxawq__yjpo,
                container_length=len(A))
    if isinstance(sep, types.optional):
        return unopt_argument('bodo.libs.bodosql_array_kernels.concat_ws',
            ['A', 'sep'], 1)

    def impl(A, sep):
        return concat_ws_util(A, sep)
    return impl


def concat_ws_util(A, sep):
    return


@overload(concat_ws_util, no_unliteral=True)
def overload_concat_ws_util(A, sep):
    if len(A) == 0:
        raise_bodo_error('Cannot concatenate 0 columns')
    fcaxp__bfz = []
    eis__lhnd = []
    for gxawq__yjpo, wmdw__xnum in enumerate(A):
        tghe__itdu = f'A{gxawq__yjpo}'
        verify_string_arg(wmdw__xnum, 'CONCAT_WS', tghe__itdu)
        fcaxp__bfz.append(tghe__itdu)
        eis__lhnd.append(wmdw__xnum)
    fcaxp__bfz.append('sep')
    verify_string_arg(sep, 'CONCAT_WS', 'sep')
    eis__lhnd.append(sep)
    aqmcd__ptme = [True] * len(fcaxp__bfz)
    gamm__iwei = bodo.string_array_type
    uawb__upw = 'A, sep'
    mnib__jdo = {f'A{gxawq__yjpo}': f'A[{gxawq__yjpo}]' for gxawq__yjpo in
        range(len(A))}
    gps__fzk = ','.join([f'arg{gxawq__yjpo}' for gxawq__yjpo in range(len(A))])
    ixe__dovi = f'  res[i] = arg{len(A)}.join([{gps__fzk}])\n'
    return gen_vectorized(fcaxp__bfz, eis__lhnd, aqmcd__ptme, ixe__dovi,
        gamm__iwei, uawb__upw, mnib__jdo)
