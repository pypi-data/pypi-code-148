"""File containing utility functions for supporting DataFrame operations with Table Format."""
from collections import defaultdict
from typing import Any, Dict, Set
import numba
import numpy as np
from numba.core import types
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.table import TableType
from bodo.utils.typing import get_castable_arr_dtype, get_overload_const_bool, get_overload_const_str, is_overload_constant_bool, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, raise_bodo_error


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_mappable_table_func(table, func_name, out_arr_typ, is_method,
    used_cols=None):
    if not is_overload_constant_str(func_name) and not is_overload_none(
        func_name):
        raise_bodo_error(
            'generate_mappable_table_func(): func_name must be a constant string'
            )
    if not is_overload_constant_bool(is_method):
        raise_bodo_error(
            'generate_mappable_table_func(): is_method must be a constant boolean'
            )
    rgcyd__hpum = not is_overload_none(func_name)
    if rgcyd__hpum:
        func_name = get_overload_const_str(func_name)
        eci__jrhqy = get_overload_const_bool(is_method)
    pjxl__fop = out_arr_typ.instance_type if isinstance(out_arr_typ, types.
        TypeRef) else out_arr_typ
    kyd__buc = pjxl__fop == types.none
    qhwd__nwsr = len(table.arr_types)
    if kyd__buc:
        lgo__qagh = table
    else:
        pjqjs__skm = tuple([pjxl__fop] * qhwd__nwsr)
        lgo__qagh = TableType(pjqjs__skm)
    zgo__akf = {'bodo': bodo, 'lst_dtype': pjxl__fop, 'table_typ': lgo__qagh}
    llc__uto = (
        'def impl(table, func_name, out_arr_typ, is_method, used_cols=None):\n'
        )
    if kyd__buc:
        llc__uto += (
            f'  out_table = bodo.hiframes.table.init_table(table, False)\n')
        llc__uto += f'  l = len(table)\n'
    else:
        llc__uto += f"""  out_list = bodo.hiframes.table.alloc_empty_list_type({qhwd__nwsr}, lst_dtype)
"""
    if not is_overload_none(used_cols):
        vugj__vpuwg = used_cols.instance_type
        ehfgz__kzosy = np.array(vugj__vpuwg.meta, dtype=np.int64)
        zgo__akf['used_cols_glbl'] = ehfgz__kzosy
        mpdpi__wdnwl = set([table.block_nums[isvkp__qkx] for isvkp__qkx in
            ehfgz__kzosy])
        llc__uto += f'  used_cols_set = set(used_cols_glbl)\n'
    else:
        llc__uto += f'  used_cols_set = None\n'
        ehfgz__kzosy = None
    llc__uto += (
        f'  bodo.hiframes.table.ensure_table_unboxed(table, used_cols_set)\n')
    for dqdk__sts in table.type_to_blk.values():
        llc__uto += (
            f'  blk_{dqdk__sts} = bodo.hiframes.table.get_table_block(table, {dqdk__sts})\n'
            )
        if kyd__buc:
            llc__uto += f"""  out_list_{dqdk__sts} = bodo.hiframes.table.alloc_list_like(blk_{dqdk__sts}, len(blk_{dqdk__sts}), False)
"""
            niiq__vizc = f'out_list_{dqdk__sts}'
        else:
            niiq__vizc = 'out_list'
        if ehfgz__kzosy is None or dqdk__sts in mpdpi__wdnwl:
            llc__uto += f'  for i in range(len(blk_{dqdk__sts})):\n'
            zgo__akf[f'col_indices_{dqdk__sts}'] = np.array(table.
                block_to_arr_ind[dqdk__sts], dtype=np.int64)
            llc__uto += f'    col_loc = col_indices_{dqdk__sts}[i]\n'
            if ehfgz__kzosy is not None:
                llc__uto += f'    if col_loc not in used_cols_set:\n'
                llc__uto += f'        continue\n'
            if kyd__buc:
                vtqyr__mrevk = 'i'
            else:
                vtqyr__mrevk = 'col_loc'
            if not rgcyd__hpum:
                llc__uto += (
                    f'    {niiq__vizc}[{vtqyr__mrevk}] = blk_{dqdk__sts}[i]\n')
            elif eci__jrhqy:
                llc__uto += (
                    f'    {niiq__vizc}[{vtqyr__mrevk}] = blk_{dqdk__sts}[i].{func_name}()\n'
                    )
            else:
                llc__uto += (
                    f'    {niiq__vizc}[{vtqyr__mrevk}] = {func_name}(blk_{dqdk__sts}[i])\n'
                    )
        if kyd__buc:
            llc__uto += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, {niiq__vizc}, {dqdk__sts})
"""
    if kyd__buc:
        llc__uto += (
            f'  out_table = bodo.hiframes.table.set_table_len(out_table, l)\n')
        llc__uto += '  return out_table\n'
    else:
        llc__uto += (
            '  return bodo.hiframes.table.init_table_from_lists((out_list,), table_typ)\n'
            )
    jcg__idjp = {}
    exec(llc__uto, zgo__akf, jcg__idjp)
    return jcg__idjp['impl']


def generate_mappable_table_func_equiv(self, scope, equiv_set, loc, args, kws):
    qorwn__ezrpm = args[0]
    if equiv_set.has_shape(qorwn__ezrpm):
        return ArrayAnalysis.AnalyzeResult(shape=qorwn__ezrpm, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_utils_table_utils_generate_mappable_table_func
    ) = generate_mappable_table_func_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def generate_table_nbytes(table, out_arr, start_offset, parallel=False):
    zgo__akf = {'bodo': bodo, 'sum_op': np.int32(bodo.libs.distributed_api.
        Reduce_Type.Sum.value)}
    llc__uto = 'def impl(table, out_arr, start_offset, parallel=False):\n'
    llc__uto += '  bodo.hiframes.table.ensure_table_unboxed(table, None)\n'
    for dqdk__sts in table.type_to_blk.values():
        llc__uto += (
            f'  blk = bodo.hiframes.table.get_table_block(table, {dqdk__sts})\n'
            )
        zgo__akf[f'col_indices_{dqdk__sts}'] = np.array(table.
            block_to_arr_ind[dqdk__sts], dtype=np.int64)
        llc__uto += '  for i in range(len(blk)):\n'
        llc__uto += f'    col_loc = col_indices_{dqdk__sts}[i]\n'
        llc__uto += '    out_arr[col_loc + start_offset] = blk[i].nbytes\n'
    llc__uto += '  if parallel:\n'
    llc__uto += '    for i in range(start_offset, len(out_arr)):\n'
    llc__uto += (
        '      out_arr[i] = bodo.libs.distributed_api.dist_reduce(out_arr[i], sum_op)\n'
        )
    jcg__idjp = {}
    exec(llc__uto, zgo__akf, jcg__idjp)
    return jcg__idjp['impl']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_concat(table, col_nums_meta, arr_type):
    arr_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type
    ngxj__rqjmd = table.type_to_blk[arr_type]
    zgo__akf: Dict[str, Any] = {'bodo': bodo}
    zgo__akf['col_indices'] = np.array(table.block_to_arr_ind[ngxj__rqjmd],
        dtype=np.int64)
    qqya__bbl = col_nums_meta.instance_type
    zgo__akf['col_nums'] = np.array(qqya__bbl.meta, np.int64)
    llc__uto = 'def impl(table, col_nums_meta, arr_type):\n'
    llc__uto += (
        f'  blk = bodo.hiframes.table.get_table_block(table, {ngxj__rqjmd})\n')
    llc__uto += (
        '  col_num_to_ind_in_blk = {c : i for i, c in enumerate(col_indices)}\n'
        )
    llc__uto += '  n = len(table)\n'
    kcw__aei = arr_type == bodo.string_array_type
    if kcw__aei:
        llc__uto += '  total_chars = 0\n'
        llc__uto += '  for c in col_nums:\n'
        llc__uto += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
        llc__uto += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
        llc__uto += (
            '    total_chars += bodo.libs.str_arr_ext.num_total_chars(arr)\n')
        llc__uto += """  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n * len(col_nums), total_chars)
"""
    else:
        llc__uto += (
            '  out_arr = bodo.utils.utils.alloc_type(n * len(col_nums), arr_type, (-1,))\n'
            )
    llc__uto += '  for i in range(len(col_nums)):\n'
    llc__uto += '    c = col_nums[i]\n'
    if not kcw__aei:
        llc__uto += """    bodo.hiframes.table.ensure_column_unboxed(table, blk, col_num_to_ind_in_blk[c], c)
"""
    llc__uto += '    arr = blk[col_num_to_ind_in_blk[c]]\n'
    llc__uto += '    off = i * n\n'
    llc__uto += '    for j in range(len(arr)):\n'
    llc__uto += '      if bodo.libs.array_kernels.isna(arr, j):\n'
    llc__uto += '        bodo.libs.array_kernels.setna(out_arr, off+j)\n'
    llc__uto += '      else:\n'
    llc__uto += '        out_arr[off+j] = arr[j]\n'
    llc__uto += '  return out_arr\n'
    eehbz__leuxk = {}
    exec(llc__uto, zgo__akf, eehbz__leuxk)
    qyqxt__rdo = eehbz__leuxk['impl']
    return qyqxt__rdo


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_astype(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):
    new_table_typ = new_table_typ.instance_type
    vuwgx__ahk = not is_overload_false(copy)
    pldng__ifur = is_overload_true(copy)
    zgo__akf: Dict[str, Any] = {'bodo': bodo}
    ora__oxvv = table.arr_types
    bvfto__xgdv = new_table_typ.arr_types
    zevkd__azv: Set[int] = set()
    fguy__bfoad: Dict[types.Type, Set[types.Type]] = defaultdict(set)
    pyv__sojxb: Set[types.Type] = set()
    for isvkp__qkx, usp__pinbh in enumerate(ora__oxvv):
        qlmzn__joee = bvfto__xgdv[isvkp__qkx]
        if usp__pinbh == qlmzn__joee:
            pyv__sojxb.add(usp__pinbh)
        else:
            zevkd__azv.add(isvkp__qkx)
            fguy__bfoad[qlmzn__joee].add(usp__pinbh)
    llc__uto = (
        'def impl(table, new_table_typ, copy, _bodo_nan_to_str, used_cols=None):\n'
        )
    llc__uto += (
        f'  out_table = bodo.hiframes.table.init_table(new_table_typ, False)\n'
        )
    llc__uto += (
        f'  out_table = bodo.hiframes.table.set_table_len(out_table, len(table))\n'
        )
    frjo__lyzin = set(range(len(ora__oxvv)))
    jmeg__ogac = frjo__lyzin - zevkd__azv
    if not is_overload_none(used_cols):
        vugj__vpuwg = used_cols.instance_type
        jvrtl__ooqll = set(vugj__vpuwg.meta)
        zevkd__azv = zevkd__azv & jvrtl__ooqll
        jmeg__ogac = jmeg__ogac & jvrtl__ooqll
        mpdpi__wdnwl = set([table.block_nums[isvkp__qkx] for isvkp__qkx in
            jvrtl__ooqll])
    else:
        jvrtl__ooqll = None
    xmbzq__yym = dict()
    for nlo__egce in zevkd__azv:
        btd__ghfcp = table.block_nums[nlo__egce]
        tnw__nctu = new_table_typ.block_nums[nlo__egce]
        if f'cast_cols_{btd__ghfcp}_{tnw__nctu}' in xmbzq__yym:
            xmbzq__yym[f'cast_cols_{btd__ghfcp}_{tnw__nctu}'].append(nlo__egce)
        else:
            xmbzq__yym[f'cast_cols_{btd__ghfcp}_{tnw__nctu}'] = [nlo__egce]
    for mtudf__jcbxq in table.blk_to_type:
        for tnw__nctu in new_table_typ.blk_to_type:
            nwtb__rqg = xmbzq__yym.get(f'cast_cols_{mtudf__jcbxq}_{tnw__nctu}',
                [])
            zgo__akf[f'cast_cols_{mtudf__jcbxq}_{tnw__nctu}'] = np.array(list
                (nwtb__rqg), dtype=np.int64)
            llc__uto += f"""  cast_cols_{mtudf__jcbxq}_{tnw__nctu}_set = set(cast_cols_{mtudf__jcbxq}_{tnw__nctu})
"""
    zgo__akf['copied_cols'] = np.array(list(jmeg__ogac), dtype=np.int64)
    llc__uto += f'  copied_cols_set = set(copied_cols)\n'
    for ohtxh__wkj, wwce__hyopb in new_table_typ.type_to_blk.items():
        zgo__akf[f'typ_list_{wwce__hyopb}'] = types.List(ohtxh__wkj)
        llc__uto += f"""  out_arr_list_{wwce__hyopb} = bodo.hiframes.table.alloc_list_like(typ_list_{wwce__hyopb}, {len(new_table_typ.block_to_arr_ind[wwce__hyopb])}, False)
"""
        if ohtxh__wkj in pyv__sojxb:
            fgrm__fcjat = table.type_to_blk[ohtxh__wkj]
            if jvrtl__ooqll is None or fgrm__fcjat in mpdpi__wdnwl:
                njftr__nxh = table.block_to_arr_ind[fgrm__fcjat]
                dtjfd__syfxw = [new_table_typ.block_offsets[nctom__iwaqq] for
                    nctom__iwaqq in njftr__nxh]
                zgo__akf[f'new_idx_{fgrm__fcjat}'] = np.array(dtjfd__syfxw,
                    np.int64)
                zgo__akf[f'orig_arr_inds_{fgrm__fcjat}'] = np.array(njftr__nxh,
                    np.int64)
                llc__uto += f"""  arr_list_{fgrm__fcjat} = bodo.hiframes.table.get_table_block(table, {fgrm__fcjat})
"""
                llc__uto += f'  for i in range(len(arr_list_{fgrm__fcjat})):\n'
                llc__uto += (
                    f'    arr_ind_{fgrm__fcjat} = orig_arr_inds_{fgrm__fcjat}[i]\n'
                    )
                llc__uto += (
                    f'    if arr_ind_{fgrm__fcjat} not in copied_cols_set:\n')
                llc__uto += f'      continue\n'
                llc__uto += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{fgrm__fcjat}, i, arr_ind_{fgrm__fcjat})
"""
                llc__uto += (
                    f'    out_idx_{wwce__hyopb}_{fgrm__fcjat} = new_idx_{fgrm__fcjat}[i]\n'
                    )
                llc__uto += (
                    f'    arr_val_{fgrm__fcjat} = arr_list_{fgrm__fcjat}[i]\n')
                if pldng__ifur:
                    llc__uto += (
                        f'    arr_val_{fgrm__fcjat} = arr_val_{fgrm__fcjat}.copy()\n'
                        )
                elif vuwgx__ahk:
                    llc__uto += f"""    arr_val_{fgrm__fcjat} = arr_val_{fgrm__fcjat}.copy() if copy else arr_val_{wwce__hyopb}
"""
                llc__uto += f"""    out_arr_list_{wwce__hyopb}[out_idx_{wwce__hyopb}_{fgrm__fcjat}] = arr_val_{fgrm__fcjat}
"""
    kwqjl__mxr = set()
    for ohtxh__wkj, wwce__hyopb in new_table_typ.type_to_blk.items():
        if ohtxh__wkj in fguy__bfoad:
            zgo__akf[f'typ_{wwce__hyopb}'] = get_castable_arr_dtype(ohtxh__wkj)
            ocw__dneyh = fguy__bfoad[ohtxh__wkj]
            for nxjtf__vqadc in ocw__dneyh:
                fgrm__fcjat = table.type_to_blk[nxjtf__vqadc]
                if jvrtl__ooqll is None or fgrm__fcjat in mpdpi__wdnwl:
                    if (nxjtf__vqadc not in pyv__sojxb and nxjtf__vqadc not in
                        kwqjl__mxr):
                        njftr__nxh = table.block_to_arr_ind[fgrm__fcjat]
                        dtjfd__syfxw = [new_table_typ.block_offsets[
                            nctom__iwaqq] for nctom__iwaqq in njftr__nxh]
                        zgo__akf[f'new_idx_{fgrm__fcjat}'] = np.array(
                            dtjfd__syfxw, np.int64)
                        zgo__akf[f'orig_arr_inds_{fgrm__fcjat}'] = np.array(
                            njftr__nxh, np.int64)
                        llc__uto += f"""  arr_list_{fgrm__fcjat} = bodo.hiframes.table.get_table_block(table, {fgrm__fcjat})
"""
                    kwqjl__mxr.add(nxjtf__vqadc)
                    llc__uto += (
                        f'  for i in range(len(arr_list_{fgrm__fcjat})):\n')
                    llc__uto += (
                        f'    arr_ind_{fgrm__fcjat} = orig_arr_inds_{fgrm__fcjat}[i]\n'
                        )
                    llc__uto += f"""    if arr_ind_{fgrm__fcjat} not in cast_cols_{fgrm__fcjat}_{wwce__hyopb}_set:
"""
                    llc__uto += f'      continue\n'
                    llc__uto += f"""    bodo.hiframes.table.ensure_column_unboxed(table, arr_list_{fgrm__fcjat}, i, arr_ind_{fgrm__fcjat})
"""
                    llc__uto += f"""    out_idx_{wwce__hyopb}_{fgrm__fcjat} = new_idx_{fgrm__fcjat}[i]
"""
                    llc__uto += f"""    arr_val_{wwce__hyopb} =  bodo.utils.conversion.fix_arr_dtype(arr_list_{fgrm__fcjat}[i], typ_{wwce__hyopb}, copy, nan_to_str=_bodo_nan_to_str, from_series=True)
"""
                    llc__uto += f"""    out_arr_list_{wwce__hyopb}[out_idx_{wwce__hyopb}_{fgrm__fcjat}] = arr_val_{wwce__hyopb}
"""
        llc__uto += f"""  out_table = bodo.hiframes.table.set_table_block(out_table, out_arr_list_{wwce__hyopb}, {wwce__hyopb})
"""
    llc__uto += '  return out_table\n'
    jcg__idjp = {}
    exec(llc__uto, zgo__akf, jcg__idjp)
    return jcg__idjp['impl']


def table_astype_equiv(self, scope, equiv_set, loc, args, kws):
    qorwn__ezrpm = args[0]
    if equiv_set.has_shape(qorwn__ezrpm):
        return ArrayAnalysis.AnalyzeResult(shape=qorwn__ezrpm, pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_utils_table_utils_table_astype = (
    table_astype_equiv)
