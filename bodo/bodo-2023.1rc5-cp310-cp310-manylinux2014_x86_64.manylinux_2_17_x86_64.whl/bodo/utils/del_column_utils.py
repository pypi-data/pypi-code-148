"""Helper information to keep table column deletion
pass organized. This contains information about all
table operations for optimizations.
"""
from typing import Dict, Tuple
from numba.core import ir, types
from bodo.hiframes.table import TableType
table_usecol_funcs = {('get_table_data', 'bodo.hiframes.table'), (
    'table_filter', 'bodo.hiframes.table'), ('table_subset',
    'bodo.hiframes.table'), ('set_table_data', 'bodo.hiframes.table'), (
    'set_table_data_null', 'bodo.hiframes.table'), (
    'generate_mappable_table_func', 'bodo.utils.table_utils'), (
    'table_astype', 'bodo.utils.table_utils'), ('generate_table_nbytes',
    'bodo.utils.table_utils'), ('table_concat', 'bodo.utils.table_utils'),
    ('py_data_to_cpp_table', 'bodo.libs.array'), ('logical_table_to_table',
    'bodo.hiframes.table')}


def is_table_use_column_ops(fdef: Tuple[str, str], args, typemap):
    return fdef in table_usecol_funcs and len(args) > 0 and isinstance(typemap
        [args[0].name], TableType)


def get_table_used_columns(fdef: Tuple[str, str], call_expr: ir.Expr,
    typemap: Dict[str, types.Type]):
    if fdef == ('get_table_data', 'bodo.hiframes.table'):
        codnn__glxb = typemap[call_expr.args[1].name].literal_value
        return {codnn__glxb}
    elif fdef in {('table_filter', 'bodo.hiframes.table'), ('table_astype',
        'bodo.utils.table_utils'), ('generate_mappable_table_func',
        'bodo.utils.table_utils'), ('set_table_data', 'bodo.hiframes.table'
        ), ('set_table_data_null', 'bodo.hiframes.table')}:
        dxnr__jsm = dict(call_expr.kws)
        if 'used_cols' in dxnr__jsm:
            isxcq__hey = dxnr__jsm['used_cols']
            fgwh__jdr = typemap[isxcq__hey.name]
            fgwh__jdr = fgwh__jdr.instance_type
            return set(fgwh__jdr.meta)
    elif fdef == ('table_concat', 'bodo.utils.table_utils'):
        isxcq__hey = call_expr.args[1]
        fgwh__jdr = typemap[isxcq__hey.name]
        fgwh__jdr = fgwh__jdr.instance_type
        return set(fgwh__jdr.meta)
    elif fdef == ('table_subset', 'bodo.hiframes.table'):
        wfi__jlrn = call_expr.args[1]
        fok__qwzxc = typemap[wfi__jlrn.name]
        fok__qwzxc = fok__qwzxc.instance_type
        agfya__nep = fok__qwzxc.meta
        dxnr__jsm = dict(call_expr.kws)
        if 'used_cols' in dxnr__jsm:
            isxcq__hey = dxnr__jsm['used_cols']
            fgwh__jdr = typemap[isxcq__hey.name]
            fgwh__jdr = fgwh__jdr.instance_type
            cle__ijtat = set(fgwh__jdr.meta)
            nhlts__mmmt = set()
            for iow__cbsn, snmjc__eveok in enumerate(agfya__nep):
                if iow__cbsn in cle__ijtat:
                    nhlts__mmmt.add(snmjc__eveok)
            return nhlts__mmmt
        else:
            return set(agfya__nep)
    elif fdef == ('py_data_to_cpp_table', 'bodo.libs.array'):
        ycf__sclsd = typemap[call_expr.args[2].name].instance_type.meta
        pqvxb__oylde = len(typemap[call_expr.args[0].name].arr_types)
        return set(iow__cbsn for iow__cbsn in ycf__sclsd if iow__cbsn <
            pqvxb__oylde)
    elif fdef == ('logical_table_to_table', 'bodo.hiframes.table'):
        pqp__jnh = typemap[call_expr.args[2].name].instance_type.meta
        nng__cyhk = len(typemap[call_expr.args[0].name].arr_types)
        dxnr__jsm = dict(call_expr.kws)
        if 'used_cols' in dxnr__jsm:
            cle__ijtat = set(typemap[dxnr__jsm['used_cols'].name].
                instance_type.meta)
            pwnlm__emmx = set()
            for ujpsc__nir, jvunn__bmgp in enumerate(pqp__jnh):
                if ujpsc__nir in cle__ijtat and jvunn__bmgp < nng__cyhk:
                    pwnlm__emmx.add(jvunn__bmgp)
            return pwnlm__emmx
        else:
            return set(iow__cbsn for iow__cbsn in pqp__jnh if iow__cbsn <
                nng__cyhk)
    return None
