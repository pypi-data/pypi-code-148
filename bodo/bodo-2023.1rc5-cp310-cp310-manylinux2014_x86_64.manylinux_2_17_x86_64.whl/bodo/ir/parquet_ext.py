"""IR node for the parquet data access"""
from typing import List
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from numba.core import ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, get_definition, guard, mk_unique_var, next_label, replace_arg_nodes
from numba.extending import NativeValue, models, register_model, unbox
import bodo
import bodo.ir.connector
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.table import Table, TableType
from bodo.io.fs_io import get_storage_options_pyobject, storage_options_dict_type
from bodo.io.helpers import is_nullable, numba_to_pyarrow_schema, pyarrow_table_schema_type
from bodo.io.parquet_pio import ParquetFileInfo, get_filters_pyobject, parquet_file_schema, parquet_predicate_type
from bodo.libs.array import cpp_table_to_py_table, delete_table, info_from_table, info_to_array, table_type
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.str_ext import unicode_to_utf8
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.transform import get_const_value
from bodo.utils.typing import BodoError, FilenameType
from bodo.utils.utils import check_and_propagate_cpp_exception, numba_to_c_type, sanitize_varname


class ReadParquetFilepathType(types.Opaque):

    def __init__(self):
        super(ReadParquetFilepathType, self).__init__(name=
            'ReadParquetFilepathType')


read_parquet_fpath_type = ReadParquetFilepathType()
types.read_parquet_fpath_type = read_parquet_fpath_type
register_model(ReadParquetFilepathType)(models.OpaqueModel)


@unbox(ReadParquetFilepathType)
def unbox_read_parquet_fpath_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


class ParquetHandler:

    def __init__(self, func_ir, typingctx, args, _locals):
        self.func_ir = func_ir
        self.typingctx = typingctx
        self.args = args
        self.locals = _locals

    def gen_parquet_read(self, file_name, lhs, columns, storage_options=
        None, input_file_name_col=None, read_as_dict_cols=None, use_hive=True):
        nxj__kqql = lhs.scope
        loc = lhs.loc
        zdofl__ziiyg = None
        if lhs.name in self.locals:
            zdofl__ziiyg = self.locals[lhs.name]
            self.locals.pop(lhs.name)
        fyeps__daw = {}
        if lhs.name + ':convert' in self.locals:
            fyeps__daw = self.locals[lhs.name + ':convert']
            self.locals.pop(lhs.name + ':convert')
        if zdofl__ziiyg is None:
            ghbm__mltu = (
                'Parquet schema not available. Either path argument should be constant for Bodo to look at the file at compile time or schema should be provided. For more information, see: https://docs.bodo.ai/latest/file_io/#parquet-section.'
                )
            kuxa__zze = get_const_value(file_name, self.func_ir, ghbm__mltu,
                arg_types=self.args, file_info=ParquetFileInfo(columns,
                storage_options=storage_options, input_file_name_col=
                input_file_name_col, read_as_dict_cols=read_as_dict_cols,
                use_hive=use_hive))
            flzr__eclg = guard(get_definition, self.func_ir, file_name)
            if isinstance(flzr__eclg, ir.Arg) and isinstance(self.args[
                flzr__eclg.index], FilenameType):
                typ: FilenameType = self.args[flzr__eclg.index]
                (col_names, eyd__cke, hxxt__zhq, col_indices,
                    partition_names, unsupported_columns,
                    unsupported_arrow_types, arrow_schema) = typ.schema
            else:
                (col_names, eyd__cke, hxxt__zhq, col_indices,
                    partition_names, unsupported_columns,
                    unsupported_arrow_types, arrow_schema) = (
                    parquet_file_schema(kuxa__zze, columns, storage_options,
                    input_file_name_col, read_as_dict_cols, use_hive))
        else:
            cvef__lahlr: List[str] = list(zdofl__ziiyg.keys())
            xvg__mkonc = {c: phcj__smwnx for phcj__smwnx, c in enumerate(
                cvef__lahlr)}
            quaha__bqgcg = [czwag__arys for czwag__arys in zdofl__ziiyg.
                values()]
            col_names: List[str] = cvef__lahlr if columns is None else columns
            col_indices = [xvg__mkonc[c] for c in col_names]
            eyd__cke = [quaha__bqgcg[xvg__mkonc[c]] for c in col_names]
            hxxt__zhq = next((fhv__ildy for fhv__ildy in col_names if
                fhv__ildy.startswith('__index_level_')), None)
            partition_names = []
            unsupported_columns = []
            unsupported_arrow_types = []
            arrow_schema = numba_to_pyarrow_schema(DataFrameType(data=tuple
                (eyd__cke), columns=tuple(col_names)))
        bpfn__ejowr = None if isinstance(hxxt__zhq, dict
            ) or hxxt__zhq is None else hxxt__zhq
        index_column_index = None
        index_column_type = types.none
        if bpfn__ejowr:
            yxo__xen = col_names.index(bpfn__ejowr)
            index_column_index = col_indices.pop(yxo__xen)
            index_column_type = eyd__cke.pop(yxo__xen)
            col_names.pop(yxo__xen)
        for phcj__smwnx, c in enumerate(col_names):
            if c in fyeps__daw:
                eyd__cke[phcj__smwnx] = fyeps__daw[c]
        kzmzx__yozmu = [ir.Var(nxj__kqql, mk_unique_var('pq_table'), loc),
            ir.Var(nxj__kqql, mk_unique_var('pq_index'), loc)]
        kwa__fgap = [ParquetReader(file_name, lhs.name, col_names,
            col_indices, eyd__cke, kzmzx__yozmu, loc, partition_names,
            storage_options, index_column_index, index_column_type,
            input_file_name_col, unsupported_columns,
            unsupported_arrow_types, arrow_schema, use_hive)]
        return (col_names, kzmzx__yozmu, hxxt__zhq, kwa__fgap, eyd__cke,
            index_column_type)


class ParquetReader(ir.Stmt):

    def __init__(self, file_name, df_out, col_names, col_indices, out_types,
        out_vars, loc, partition_names, storage_options, index_column_index,
        index_column_type, input_file_name_col, unsupported_columns,
        unsupported_arrow_types, arrow_schema, use_hive):
        self.connector_typ = 'parquet'
        self.file_name = file_name
        self.df_out = df_out
        self.df_colnames = col_names
        self.col_indices = col_indices
        self.out_types = out_types
        self.original_out_types = out_types
        self.original_df_colnames = col_names
        self.out_vars = out_vars
        self.loc = loc
        self.partition_names = partition_names
        self.filters = None
        self.storage_options = storage_options
        self.index_column_index = index_column_index
        self.index_column_type = index_column_type
        self.out_used_cols = list(range(len(col_indices)))
        self.input_file_name_col = input_file_name_col
        self.unsupported_columns = unsupported_columns
        self.unsupported_arrow_types = unsupported_arrow_types
        self.arrow_schema = arrow_schema
        self.is_live_table = True
        self.use_hive = use_hive

    def __repr__(self):
        return (
            '({}) = ReadParquet({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'
            .format(self.df_out, self.file_name.name, self.df_colnames,
            self.col_indices, self.out_types, self.original_out_types, self
            .original_df_colnames, self.out_vars, self.partition_names,
            self.filters, self.storage_options, self.index_column_index,
            self.index_column_type, self.out_used_cols, self.
            input_file_name_col, self.unsupported_columns, self.
            unsupported_arrow_types, self.arrow_schema))


def remove_dead_pq(pq_node, lives_no_aliases, lives, arg_aliases, alias_map,
    func_ir, typemap):
    nkcoo__epzam = pq_node.out_vars[0].name
    mskag__qam = pq_node.out_vars[1].name
    if nkcoo__epzam not in lives and mskag__qam not in lives:
        return None
    elif nkcoo__epzam not in lives:
        pq_node.col_indices = []
        pq_node.df_colnames = []
        pq_node.out_used_cols = []
        pq_node.is_live_table = False
    elif mskag__qam not in lives:
        pq_node.index_column_index = None
        pq_node.index_column_type = types.none
    return pq_node


def pq_remove_dead_column(pq_node, column_live_map, equiv_vars, typemap):
    return bodo.ir.connector.base_connector_remove_dead_columns(pq_node,
        column_live_map, equiv_vars, typemap, 'ParquetReader', pq_node.
        col_indices, require_one_column=False)


def pq_distributed_run(pq_node, array_dists, typemap, calltypes, typingctx,
    targetctx, is_independent=False, meta_head_only_info=None):
    wzx__roxa = len(pq_node.out_vars)
    dnf_filter_str = 'None'
    expr_filter_str = 'None'
    kkunr__tzpwr, jjs__fpv = bodo.ir.connector.generate_filter_map(pq_node.
        filters)
    extra_args = ', '.join(kkunr__tzpwr.values())
    dnf_filter_str, expr_filter_str = bodo.ir.connector.generate_arrow_filters(
        pq_node.filters, kkunr__tzpwr, jjs__fpv, pq_node.
        original_df_colnames, pq_node.partition_names, pq_node.
        original_out_types, typemap, 'parquet', output_dnf=False)
    xijn__unbe = ', '.join(f'out{phcj__smwnx}' for phcj__smwnx in range(
        wzx__roxa))
    yhkq__lsgq = f'def pq_impl(fname, {extra_args}):\n'
    yhkq__lsgq += (
        f'    (total_rows, {xijn__unbe},) = _pq_reader_py(fname, {extra_args})\n'
        )
    nthxf__elz = {}
    exec(yhkq__lsgq, {}, nthxf__elz)
    fhmn__wmjw = nthxf__elz['pq_impl']
    if bodo.user_logging.get_verbose_level() >= 1:
        wfkv__mrh = pq_node.loc.strformat()
        rwjr__had = []
        zytr__rjhf = []
        for phcj__smwnx in pq_node.out_used_cols:
            ptod__jgti = pq_node.df_colnames[phcj__smwnx]
            rwjr__had.append(ptod__jgti)
            if isinstance(pq_node.out_types[phcj__smwnx], bodo.libs.
                dict_arr_ext.DictionaryArrayType):
                zytr__rjhf.append(ptod__jgti)
        qhb__ggtgo = (
            'Finish column pruning on read_parquet node:\n%s\nColumns loaded %s\n'
            )
        bodo.user_logging.log_message('Column Pruning', qhb__ggtgo,
            wfkv__mrh, rwjr__had)
        if zytr__rjhf:
            mxik__ryksf = """Finished optimized encoding on read_parquet node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                mxik__ryksf, wfkv__mrh, zytr__rjhf)
    mpve__ljh = bodo.ir.connector.is_connector_table_parallel(pq_node,
        array_dists, typemap, 'ParquetReader')
    if pq_node.unsupported_columns:
        ihsjv__fhwkn = set(pq_node.out_used_cols)
        sey__jjrq = set(pq_node.unsupported_columns)
        znlqn__wicjl = ihsjv__fhwkn & sey__jjrq
        if znlqn__wicjl:
            nbez__lpch = sorted(znlqn__wicjl)
            cvko__esj = [
                f'pandas.read_parquet(): 1 or more columns found with Arrow types that are not supported in Bodo and could not be eliminated. '
                 +
                "Please manually remove these columns from your read_parquet with the 'columns' argument. If these "
                 +
                'columns are needed, you will need to modify your dataset to use a supported type.'
                , 'Unsupported Columns:']
            qow__geqrc = 0
            for ndmgs__qgt in nbez__lpch:
                while pq_node.unsupported_columns[qow__geqrc] != ndmgs__qgt:
                    qow__geqrc += 1
                cvko__esj.append(
                    f"Column '{pq_node.df_colnames[ndmgs__qgt]}' with unsupported arrow type {pq_node.unsupported_arrow_types[qow__geqrc]}"
                    )
                qow__geqrc += 1
            cduo__qcfqv = '\n'.join(cvko__esj)
            raise BodoError(cduo__qcfqv, loc=pq_node.loc)
    qdu__jiv = _gen_pq_reader_py(pq_node.df_colnames, pq_node.col_indices,
        pq_node.out_used_cols, pq_node.out_types, pq_node.storage_options,
        pq_node.partition_names, dnf_filter_str, expr_filter_str,
        extra_args, mpve__ljh, meta_head_only_info, pq_node.
        index_column_index, pq_node.index_column_type, pq_node.
        input_file_name_col, not pq_node.is_live_table, pq_node.
        arrow_schema, pq_node.use_hive)
    six__kiqh = typemap[pq_node.file_name.name]
    ilm__wdbs = (six__kiqh,) + tuple(typemap[pnxvx__vuyc.name] for
        pnxvx__vuyc in jjs__fpv)
    mplfa__ptcx = compile_to_numba_ir(fhmn__wmjw, {'_pq_reader_py':
        qdu__jiv}, typingctx=typingctx, targetctx=targetctx, arg_typs=
        ilm__wdbs, typemap=typemap, calltypes=calltypes).blocks.popitem()[1]
    replace_arg_nodes(mplfa__ptcx, [pq_node.file_name] + jjs__fpv)
    kwa__fgap = mplfa__ptcx.body[:-3]
    if meta_head_only_info:
        kwa__fgap[-3].target = meta_head_only_info[1]
    kwa__fgap[-2].target = pq_node.out_vars[0]
    kwa__fgap[-1].target = pq_node.out_vars[1]
    assert not (pq_node.index_column_index is None and not pq_node.
        is_live_table
        ), 'At most one of table and index should be dead if the Parquet IR node is live'
    if pq_node.index_column_index is None:
        kwa__fgap.pop(-1)
    elif not pq_node.is_live_table:
        kwa__fgap.pop(-2)
    return kwa__fgap


def _gen_pq_reader_py(col_names, col_indices, out_used_cols, out_types,
    storage_options, partition_names, dnf_filter_str, expr_filter_str,
    extra_args, is_parallel, meta_head_only_info, index_column_index,
    index_column_type, input_file_name_col, is_dead_table, pyarrow_schema:
    pa.Schema, use_hive: bool):
    uldhp__jguo = next_label()
    syl__bkimu = ',' if extra_args else ''
    yhkq__lsgq = f'def pq_reader_py(fname,{extra_args}):\n'
    yhkq__lsgq += (
        f"    ev = bodo.utils.tracing.Event('read_parquet', {is_parallel})\n")
    yhkq__lsgq += f"    ev.add_attribute('g_fname', fname)\n"
    yhkq__lsgq += f"""    dnf_filters, expr_filters = get_filters_pyobject("{dnf_filter_str}", "{expr_filter_str}", ({extra_args}{syl__bkimu}))
"""
    yhkq__lsgq += '    fname_py = get_fname_pyobject(fname)\n'
    storage_options['bodo_dummy'] = 'dummy'
    yhkq__lsgq += (
        f'    storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    jejss__fkv = -1
    if meta_head_only_info and meta_head_only_info[0] is not None:
        jejss__fkv = meta_head_only_info[0]
    idfzk__ndwcd = [sanitize_varname(c) for c in col_names]
    partition_names = [sanitize_varname(c) for c in partition_names]
    input_file_name_col = sanitize_varname(input_file_name_col
        ) if input_file_name_col is not None and col_names.index(
        input_file_name_col) in out_used_cols else None
    eni__rwu = {c: phcj__smwnx for phcj__smwnx, c in enumerate(col_indices)}
    fju__poqhu = {c: phcj__smwnx for phcj__smwnx, c in enumerate(idfzk__ndwcd)}
    xakm__rwqjs = []
    lgpr__ejmw = set()
    gan__ijuk = partition_names + [input_file_name_col]
    for phcj__smwnx in out_used_cols:
        if idfzk__ndwcd[phcj__smwnx] not in gan__ijuk:
            xakm__rwqjs.append(col_indices[phcj__smwnx])
        elif not input_file_name_col or idfzk__ndwcd[phcj__smwnx
            ] != input_file_name_col:
            lgpr__ejmw.add(col_indices[phcj__smwnx])
    if index_column_index is not None:
        xakm__rwqjs.append(index_column_index)
    xakm__rwqjs = sorted(xakm__rwqjs)
    lmjft__tja = {c: phcj__smwnx for phcj__smwnx, c in enumerate(xakm__rwqjs)}
    qgfxq__iteti = [(int(is_nullable(out_types[eni__rwu[frsy__shu]])) if 
        frsy__shu != index_column_index else int(is_nullable(
        index_column_type))) for frsy__shu in xakm__rwqjs]
    pxqnk__wruf = []
    for frsy__shu in xakm__rwqjs:
        if frsy__shu == index_column_index:
            czwag__arys = index_column_type
        else:
            czwag__arys = out_types[eni__rwu[frsy__shu]]
        if czwag__arys == dict_str_arr_type:
            pxqnk__wruf.append(frsy__shu)
    ppw__itmy = []
    nit__plx = {}
    tlsdc__ifw = []
    himp__ymjaz = []
    for phcj__smwnx, zghi__ihofr in enumerate(partition_names):
        try:
            ndj__anvcu = fju__poqhu[zghi__ihofr]
            if col_indices[ndj__anvcu] not in lgpr__ejmw:
                continue
        except (KeyError, ValueError) as kat__dvw:
            continue
        nit__plx[zghi__ihofr] = len(ppw__itmy)
        ppw__itmy.append(zghi__ihofr)
        tlsdc__ifw.append(phcj__smwnx)
        hnn__zsq = out_types[ndj__anvcu].dtype
        wzea__pksx = bodo.hiframes.pd_categorical_ext.get_categories_int_type(
            hnn__zsq)
        himp__ymjaz.append(numba_to_c_type(wzea__pksx))
    yhkq__lsgq += f"""    total_rows_np = np.array([0], dtype=np.int64)
    out_table = pq_read(
        fname_py,
        {is_parallel},
        dnf_filters,
        expr_filters,
        storage_options_py,
        pyarrow_schema_{uldhp__jguo},
        {jejss__fkv},
        selected_cols_arr_{uldhp__jguo}.ctypes,
        {len(xakm__rwqjs)},
        nullable_cols_arr_{uldhp__jguo}.ctypes,
"""
    if len(tlsdc__ifw) > 0:
        yhkq__lsgq += f"""        np.array({tlsdc__ifw}, dtype=np.int32).ctypes,
        np.array({himp__ymjaz}, dtype=np.int32).ctypes,
        {len(tlsdc__ifw)},
"""
    else:
        yhkq__lsgq += f'        0, 0, 0,\n'
    if len(pxqnk__wruf) > 0:
        yhkq__lsgq += f"""        np.array({pxqnk__wruf}, dtype=np.int32).ctypes, {len(pxqnk__wruf)},
"""
    else:
        yhkq__lsgq += f'        0, 0,\n'
    yhkq__lsgq += f'        total_rows_np.ctypes,\n'
    yhkq__lsgq += f'        {input_file_name_col is not None},\n'
    yhkq__lsgq += f'        {use_hive},\n'
    yhkq__lsgq += f'    )\n'
    yhkq__lsgq += f'    check_and_propagate_cpp_exception()\n'
    yhkq__lsgq += f'    total_rows = total_rows_np[0]\n'
    if is_parallel:
        yhkq__lsgq += f"""    local_rows = get_node_portion(total_rows, bodo.get_size(), bodo.get_rank())
"""
    else:
        yhkq__lsgq += f'    local_rows = total_rows\n'
    tqe__khj = index_column_type
    ryfjf__lzd = TableType(tuple(out_types))
    if is_dead_table:
        ryfjf__lzd = types.none
    if is_dead_table:
        wfll__wvmaj = None
    else:
        wfll__wvmaj = []
        gjwm__yrwud = 0
        qnwzv__kjn = col_indices[col_names.index(input_file_name_col)
            ] if input_file_name_col is not None else None
        for phcj__smwnx, ndmgs__qgt in enumerate(col_indices):
            if gjwm__yrwud < len(out_used_cols
                ) and phcj__smwnx == out_used_cols[gjwm__yrwud]:
                jxpy__cma = col_indices[phcj__smwnx]
                if qnwzv__kjn and jxpy__cma == qnwzv__kjn:
                    wfll__wvmaj.append(len(xakm__rwqjs) + len(ppw__itmy))
                elif jxpy__cma in lgpr__ejmw:
                    caw__cevc = idfzk__ndwcd[phcj__smwnx]
                    wfll__wvmaj.append(len(xakm__rwqjs) + nit__plx[caw__cevc])
                else:
                    wfll__wvmaj.append(lmjft__tja[ndmgs__qgt])
                gjwm__yrwud += 1
            else:
                wfll__wvmaj.append(-1)
        wfll__wvmaj = np.array(wfll__wvmaj, dtype=np.int64)
    if is_dead_table:
        yhkq__lsgq += '    T = None\n'
    else:
        yhkq__lsgq += f"""    T = cpp_table_to_py_table(out_table, table_idx_{uldhp__jguo}, py_table_type_{uldhp__jguo})
"""
        if len(out_used_cols) == 0:
            yhkq__lsgq += f'    T = set_table_len(T, local_rows)\n'
    if index_column_index is None:
        yhkq__lsgq += '    index_arr = None\n'
    else:
        gsclx__pdiji = lmjft__tja[index_column_index]
        yhkq__lsgq += f"""    index_arr = info_to_array(info_from_table(out_table, {gsclx__pdiji}), index_arr_type)
"""
    yhkq__lsgq += f'    delete_table(out_table)\n'
    yhkq__lsgq += f'    ev.finalize()\n'
    yhkq__lsgq += f'    return (total_rows, T, index_arr)\n'
    nthxf__elz = {}
    eckll__xeglf = {f'py_table_type_{uldhp__jguo}': ryfjf__lzd,
        f'table_idx_{uldhp__jguo}': wfll__wvmaj,
        f'selected_cols_arr_{uldhp__jguo}': np.array(xakm__rwqjs, np.int32),
        f'nullable_cols_arr_{uldhp__jguo}': np.array(qgfxq__iteti, np.int32
        ), f'pyarrow_schema_{uldhp__jguo}': pyarrow_schema.remove_metadata(
        ), 'index_arr_type': tqe__khj, 'cpp_table_to_py_table':
        cpp_table_to_py_table, 'info_to_array': info_to_array,
        'info_from_table': info_from_table, 'delete_table': delete_table,
        'check_and_propagate_cpp_exception':
        check_and_propagate_cpp_exception, 'pq_read': _pq_read,
        'unicode_to_utf8': unicode_to_utf8, 'get_filters_pyobject':
        get_filters_pyobject, 'get_storage_options_pyobject':
        get_storage_options_pyobject, 'get_fname_pyobject':
        get_fname_pyobject, 'np': np, 'pd': pd, 'bodo': bodo,
        'get_node_portion': bodo.libs.distributed_api.get_node_portion,
        'set_table_len': bodo.hiframes.table.set_table_len}
    exec(yhkq__lsgq, eckll__xeglf, nthxf__elz)
    qdu__jiv = nthxf__elz['pq_reader_py']
    mttjd__ziymp = numba.njit(qdu__jiv, no_cpython_wrapper=True)
    return mttjd__ziymp


@numba.njit
def get_fname_pyobject(fname):
    with numba.objmode(fname_py='read_parquet_fpath_type'):
        fname_py = fname
    return fname_py


numba.parfors.array_analysis.array_analysis_extensions[ParquetReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[ParquetReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[ParquetReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[ParquetReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[ParquetReader] = remove_dead_pq
numba.core.analysis.ir_extension_usedefs[ParquetReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[ParquetReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[ParquetReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[ParquetReader
    ] = bodo.ir.connector.build_connector_definitions
remove_dead_column_extensions[ParquetReader] = pq_remove_dead_column
ir_extension_table_column_use[ParquetReader
    ] = bodo.ir.connector.connector_table_column_use
distributed_pass.distributed_run_extensions[ParquetReader] = pq_distributed_run
if bodo.utils.utils.has_pyarrow():
    from bodo.io import arrow_cpp
    ll.add_symbol('pq_read', arrow_cpp.pq_read)
_pq_read = types.ExternalFunction('pq_read', table_type(
    read_parquet_fpath_type, types.boolean, parquet_predicate_type,
    parquet_predicate_type, storage_options_dict_type,
    pyarrow_table_schema_type, types.int64, types.voidptr, types.int32,
    types.voidptr, types.voidptr, types.voidptr, types.int32, types.voidptr,
    types.int32, types.voidptr, types.boolean, types.boolean))
