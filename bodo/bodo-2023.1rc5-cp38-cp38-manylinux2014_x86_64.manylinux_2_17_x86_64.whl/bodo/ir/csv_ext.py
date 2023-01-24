from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from mpi4py import MPI
from numba.core import cgutils, ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
from numba.extending import intrinsic
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.hiframes.datetime_date_ext import datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.table import Table, TableType
from bodo.io.fs_io import get_storage_options_pyobject, storage_options_dict_type
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import StringArrayType, string_array_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.transforms.table_column_del_pass import ir_extension_table_column_use, remove_dead_column_extensions
from bodo.utils.typing import BodoError
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import check_and_propagate_cpp_exception, sanitize_varname


class CsvReader(ir.Stmt):

    def __init__(self, file_name, df_out, sep, df_colnames, out_vars,
        out_types, usecols, loc, header, compression, nrows, skiprows,
        chunksize, is_skiprows_list, low_memory, escapechar,
        storage_options=None, index_column_index=None, index_column_typ=
        types.none):
        self.connector_typ = 'csv'
        self.file_name = file_name
        self.df_out = df_out
        self.sep = sep
        self.df_colnames = df_colnames
        self.out_vars = out_vars
        self.out_types = out_types
        self.usecols = usecols
        self.loc = loc
        self.skiprows = skiprows
        self.nrows = nrows
        self.header = header
        self.compression = compression
        self.chunksize = chunksize
        self.is_skiprows_list = is_skiprows_list
        self.pd_low_memory = low_memory
        self.escapechar = escapechar
        self.storage_options = storage_options
        self.index_column_index = index_column_index
        self.index_column_typ = index_column_typ
        self.out_used_cols = list(range(len(usecols)))

    def __repr__(self):
        return (
            '{} = ReadCsv(file={}, col_names={}, types={}, vars={}, nrows={}, skiprows={}, chunksize={}, is_skiprows_list={}, pd_low_memory={}, escapechar={}, storage_options={}, index_column_index={}, index_colum_typ = {}, out_used_colss={})'
            .format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars, self.nrows, self.skiprows, self.
            chunksize, self.is_skiprows_list, self.pd_low_memory, self.
            escapechar, self.storage_options, self.index_column_index, self
            .index_column_typ, self.out_used_cols))


def check_node_typing(node, typemap):
    ezvb__xtrke = typemap[node.file_name.name]
    if types.unliteral(ezvb__xtrke) != types.unicode_type:
        raise BodoError(
            f"pd.read_csv(): 'filepath_or_buffer' must be a string. Found type: {ezvb__xtrke}."
            , node.file_name.loc)
    if not isinstance(node.skiprows, ir.Const):
        otjs__orlr = typemap[node.skiprows.name]
        if isinstance(otjs__orlr, types.Dispatcher):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' callable not supported yet.",
                node.file_name.loc)
        elif not isinstance(otjs__orlr, types.Integer) and not (isinstance(
            otjs__orlr, (types.List, types.Tuple)) and isinstance(
            otjs__orlr.dtype, types.Integer)) and not isinstance(otjs__orlr,
            (types.LiteralList, bodo.utils.typing.ListLiteral)):
            raise BodoError(
                f"pd.read_csv(): 'skiprows' must be an integer or list of integers. Found type {otjs__orlr}."
                , loc=node.skiprows.loc)
        elif isinstance(otjs__orlr, (types.List, types.Tuple)):
            node.is_skiprows_list = True
    if not isinstance(node.nrows, ir.Const):
        jhp__ptzuq = typemap[node.nrows.name]
        if not isinstance(jhp__ptzuq, types.Integer):
            raise BodoError(
                f"pd.read_csv(): 'nrows' must be an integer. Found type {jhp__ptzuq}."
                , loc=node.nrows.loc)


import llvmlite.binding as ll
from bodo.io import csv_cpp
ll.add_symbol('csv_file_chunk_reader', csv_cpp.csv_file_chunk_reader)


@intrinsic
def csv_file_chunk_reader(typingctx, fname_t, is_parallel_t, skiprows_t,
    nrows_t, header_t, compression_t, bucket_region_t, storage_options_t,
    chunksize_t, is_skiprows_list_t, skiprows_list_len_t, pd_low_memory_t):
    assert storage_options_t == storage_options_dict_type, "Storage options don't match expected type"

    def codegen(context, builder, sig, args):
        grfj__vdl = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(1), lir.IntType(64),
            lir.IntType(1)])
        sgxvt__rqp = cgutils.get_or_insert_function(builder.module,
            grfj__vdl, name='csv_file_chunk_reader')
        ufirq__grs = builder.call(sgxvt__rqp, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        gomh__hmxl = cgutils.create_struct_proxy(types.stream_reader_type)(
            context, builder)
        ttxh__mxxt = context.get_python_api(builder)
        gomh__hmxl.meminfo = ttxh__mxxt.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), ufirq__grs)
        gomh__hmxl.pyobj = ufirq__grs
        ttxh__mxxt.decref(ufirq__grs)
        return gomh__hmxl._getvalue()
    return types.stream_reader_type(types.voidptr, types.bool_, types.
        voidptr, types.int64, types.bool_, types.voidptr, types.voidptr,
        storage_options_dict_type, types.int64, types.bool_, types.int64,
        types.bool_), codegen


def remove_dead_csv(csv_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    if csv_node.chunksize is not None:
        todr__tvl = csv_node.out_vars[0]
        if todr__tvl.name not in lives:
            return None
    else:
        ryds__wiqx = csv_node.out_vars[0]
        dhvex__wtw = csv_node.out_vars[1]
        if ryds__wiqx.name not in lives and dhvex__wtw.name not in lives:
            return None
        elif dhvex__wtw.name not in lives:
            csv_node.index_column_index = None
            csv_node.index_column_typ = types.none
        elif ryds__wiqx.name not in lives:
            csv_node.usecols = []
            csv_node.out_types = []
            csv_node.out_used_cols = []
    return csv_node


def csv_distributed_run(csv_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    otjs__orlr = types.int64 if isinstance(csv_node.skiprows, ir.Const
        ) else types.unliteral(typemap[csv_node.skiprows.name])
    if csv_node.chunksize is not None:
        parallel = False
        if bodo.user_logging.get_verbose_level() >= 1:
            pqtz__cgj = (
                'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n'
                )
            kbbb__eshdg = csv_node.loc.strformat()
            jcq__rhr = csv_node.df_colnames
            bodo.user_logging.log_message('Column Pruning', pqtz__cgj,
                kbbb__eshdg, jcq__rhr)
            rrfgy__rfw = csv_node.out_types[0].yield_type.data
            gap__eurg = [syakc__wsuh for ofe__jvv, syakc__wsuh in enumerate
                (csv_node.df_colnames) if isinstance(rrfgy__rfw[ofe__jvv],
                bodo.libs.dict_arr_ext.DictionaryArrayType)]
            if gap__eurg:
                xvq__eivvr = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
                bodo.user_logging.log_message('Dictionary Encoding',
                    xvq__eivvr, kbbb__eshdg, gap__eurg)
        if array_dists is not None:
            wnhgr__poh = csv_node.out_vars[0].name
            parallel = array_dists[wnhgr__poh] in (distributed_pass.
                Distribution.OneD, distributed_pass.Distribution.OneD_Var)
        gsb__dtdcf = 'def csv_iterator_impl(fname, nrows, skiprows):\n'
        gsb__dtdcf += (
            f'    reader = _csv_reader_init(fname, nrows, skiprows)\n')
        gsb__dtdcf += (
            f'    iterator = init_csv_iterator(reader, csv_iterator_type)\n')
        pxhu__rbavc = {}
        from bodo.io.csv_iterator_ext import init_csv_iterator
        exec(gsb__dtdcf, {}, pxhu__rbavc)
        kec__dcnmh = pxhu__rbavc['csv_iterator_impl']
        iima__uvxqk = 'def csv_reader_init(fname, nrows, skiprows):\n'
        iima__uvxqk += _gen_csv_file_reader_init(parallel, csv_node.header,
            csv_node.compression, csv_node.chunksize, csv_node.
            is_skiprows_list, csv_node.pd_low_memory, csv_node.storage_options)
        iima__uvxqk += '  return f_reader\n'
        exec(iima__uvxqk, globals(), pxhu__rbavc)
        wkny__mskt = pxhu__rbavc['csv_reader_init']
        gezh__awh = numba.njit(wkny__mskt)
        compiled_funcs.append(gezh__awh)
        fyfy__ydh = compile_to_numba_ir(kec__dcnmh, {'_csv_reader_init':
            gezh__awh, 'init_csv_iterator': init_csv_iterator,
            'csv_iterator_type': typemap[csv_node.out_vars[0].name]},
            typingctx=typingctx, targetctx=targetctx, arg_typs=(string_type,
            types.int64, otjs__orlr), typemap=typemap, calltypes=calltypes
            ).blocks.popitem()[1]
        replace_arg_nodes(fyfy__ydh, [csv_node.file_name, csv_node.nrows,
            csv_node.skiprows])
        lixx__emy = fyfy__ydh.body[:-3]
        lixx__emy[-1].target = csv_node.out_vars[0]
        return lixx__emy
    parallel = bodo.ir.connector.is_connector_table_parallel(csv_node,
        array_dists, typemap, 'CSVReader')
    gsb__dtdcf = 'def csv_impl(fname, nrows, skiprows):\n'
    gsb__dtdcf += (
        f'    (table_val, idx_col) = _csv_reader_py(fname, nrows, skiprows)\n')
    pxhu__rbavc = {}
    exec(gsb__dtdcf, {}, pxhu__rbavc)
    vri__coif = pxhu__rbavc['csv_impl']
    bcmc__epyzq = csv_node.usecols
    if bcmc__epyzq:
        bcmc__epyzq = [csv_node.usecols[ofe__jvv] for ofe__jvv in csv_node.
            out_used_cols]
    if bodo.user_logging.get_verbose_level() >= 1:
        pqtz__cgj = (
            'Finish column pruning on read_csv node:\n%s\nColumns loaded %s\n')
        kbbb__eshdg = csv_node.loc.strformat()
        jcq__rhr = []
        gap__eurg = []
        if bcmc__epyzq:
            for ofe__jvv in csv_node.out_used_cols:
                qyqot__onyhe = csv_node.df_colnames[ofe__jvv]
                jcq__rhr.append(qyqot__onyhe)
                if isinstance(csv_node.out_types[ofe__jvv], bodo.libs.
                    dict_arr_ext.DictionaryArrayType):
                    gap__eurg.append(qyqot__onyhe)
        bodo.user_logging.log_message('Column Pruning', pqtz__cgj,
            kbbb__eshdg, jcq__rhr)
        if gap__eurg:
            xvq__eivvr = """Finished optimized encoding on read_csv node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding', xvq__eivvr,
                kbbb__eshdg, gap__eurg)
    mjsw__xovbx = _gen_csv_reader_py(csv_node.df_colnames, csv_node.
        out_types, bcmc__epyzq, csv_node.out_used_cols, csv_node.sep,
        parallel, csv_node.header, csv_node.compression, csv_node.
        is_skiprows_list, csv_node.pd_low_memory, csv_node.escapechar,
        csv_node.storage_options, idx_col_index=csv_node.index_column_index,
        idx_col_typ=csv_node.index_column_typ)
    fyfy__ydh = compile_to_numba_ir(vri__coif, {'_csv_reader_py':
        mjsw__xovbx}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type, types.int64, otjs__orlr), typemap=typemap, calltypes=
        calltypes).blocks.popitem()[1]
    replace_arg_nodes(fyfy__ydh, [csv_node.file_name, csv_node.nrows,
        csv_node.skiprows, csv_node.is_skiprows_list])
    lixx__emy = fyfy__ydh.body[:-3]
    lixx__emy[-1].target = csv_node.out_vars[1]
    lixx__emy[-2].target = csv_node.out_vars[0]
    assert not (csv_node.index_column_index is None and not bcmc__epyzq
        ), 'At most one of table and index should be dead if the CSV IR node is live'
    if csv_node.index_column_index is None:
        lixx__emy.pop(-1)
    elif not bcmc__epyzq:
        lixx__emy.pop(-2)
    return lixx__emy


def csv_remove_dead_column(csv_node, column_live_map, equiv_vars, typemap):
    if csv_node.chunksize is not None:
        return False
    return bodo.ir.connector.base_connector_remove_dead_columns(csv_node,
        column_live_map, equiv_vars, typemap, 'CSVReader', csv_node.usecols)


numba.parfors.array_analysis.array_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[CsvReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[CsvReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[CsvReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[CsvReader] = remove_dead_csv
numba.core.analysis.ir_extension_usedefs[CsvReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[CsvReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[CsvReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[CsvReader] = csv_distributed_run
remove_dead_column_extensions[CsvReader] = csv_remove_dead_column
ir_extension_table_column_use[CsvReader
    ] = bodo.ir.connector.connector_table_column_use


def _get_dtype_str(t):
    nju__okeyl = t.dtype
    if isinstance(nju__okeyl, PDCategoricalDtype):
        hqahc__mzzdq = CategoricalArrayType(nju__okeyl)
        oyjr__woipx = 'CategoricalArrayType' + str(ir_utils.next_label())
        setattr(types, oyjr__woipx, hqahc__mzzdq)
        return oyjr__woipx
    if nju__okeyl == types.NPDatetime('ns'):
        nju__okeyl = 'NPDatetime("ns")'
    if t == string_array_type:
        types.string_array_type = string_array_type
        return 'string_array_type'
    if isinstance(t, IntegerArrayType):
        zytg__rprxa = 'int_arr_{}'.format(nju__okeyl)
        setattr(types, zytg__rprxa, t)
        return zytg__rprxa
    if t == boolean_array:
        types.boolean_array = boolean_array
        return 'boolean_array'
    if nju__okeyl == types.bool_:
        nju__okeyl = 'bool_'
    if nju__okeyl == datetime_date_type:
        return 'datetime_date_array_type'
    if isinstance(t, ArrayItemArrayType) and isinstance(nju__okeyl, (
        StringArrayType, ArrayItemArrayType)):
        wxb__xaezp = f'ArrayItemArrayType{str(ir_utils.next_label())}'
        setattr(types, wxb__xaezp, t)
        return wxb__xaezp
    return '{}[::1]'.format(nju__okeyl)


def _get_pd_dtype_str(t):
    nju__okeyl = t.dtype
    if isinstance(nju__okeyl, PDCategoricalDtype):
        return 'pd.CategoricalDtype({})'.format(nju__okeyl.categories)
    if nju__okeyl == types.NPDatetime('ns'):
        return 'str'
    if t == string_array_type or t == bodo.dict_str_arr_type:
        return 'str'
    if isinstance(t, IntegerArrayType):
        return '"{}Int{}"'.format('' if nju__okeyl.signed else 'U',
            nju__okeyl.bitwidth)
    if t == boolean_array:
        return 'np.bool_'
    if isinstance(t, ArrayItemArrayType) and isinstance(nju__okeyl, (
        StringArrayType, ArrayItemArrayType)):
        return 'object'
    return 'np.{}'.format(nju__okeyl)


compiled_funcs = []


@numba.njit
def check_nrows_skiprows_value(nrows, skiprows):
    if nrows < -1:
        raise ValueError('pd.read_csv: nrows must be integer >= 0.')
    if skiprows[0] < 0:
        raise ValueError('pd.read_csv: skiprows must be integer >= 0.')


def astype(df, typemap, parallel):
    pzjsv__vfiq = ''
    from collections import defaultdict
    wkpo__mqhr = defaultdict(list)
    for kdui__ime, edj__niaw in typemap.items():
        wkpo__mqhr[edj__niaw].append(kdui__ime)
    fnh__ryp = df.columns.to_list()
    hfo__eqed = []
    for edj__niaw, shcj__tqcx in wkpo__mqhr.items():
        try:
            hfo__eqed.append(df.loc[:, shcj__tqcx].astype(edj__niaw, copy=
                False))
            df = df.drop(shcj__tqcx, axis=1)
        except (ValueError, TypeError) as hjbuy__iysv:
            pzjsv__vfiq = (
                f"Caught the runtime error '{hjbuy__iysv}' on columns {shcj__tqcx}. Consider setting the 'dtype' argument in 'read_csv' or investigate if the data is corrupted."
                )
            break
    kptk__unpyq = bool(pzjsv__vfiq)
    if parallel:
        yfd__iwlb = MPI.COMM_WORLD
        kptk__unpyq = yfd__iwlb.allreduce(kptk__unpyq, op=MPI.LOR)
    if kptk__unpyq:
        jpmv__aalko = 'pd.read_csv(): Bodo could not infer dtypes correctly.'
        if pzjsv__vfiq:
            raise TypeError(f'{jpmv__aalko}\n{pzjsv__vfiq}')
        else:
            raise TypeError(
                f'{jpmv__aalko}\nPlease refer to errors on other ranks.')
    df = pd.concat(hfo__eqed + [df], axis=1)
    vht__qflo = df.loc[:, fnh__ryp]
    return vht__qflo


def _gen_csv_file_reader_init(parallel, header, compression, chunksize,
    is_skiprows_list, pd_low_memory, storage_options):
    rpj__njov = header == 0
    if compression is None:
        compression = 'uncompressed'
    if is_skiprows_list:
        gsb__dtdcf = '  skiprows = sorted(set(skiprows))\n'
    else:
        gsb__dtdcf = '  skiprows = [skiprows]\n'
    gsb__dtdcf += '  skiprows_list_len = len(skiprows)\n'
    gsb__dtdcf += '  check_nrows_skiprows_value(nrows, skiprows)\n'
    gsb__dtdcf += '  check_java_installation(fname)\n'
    gsb__dtdcf += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    gsb__dtdcf += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    gsb__dtdcf += (
        '  f_reader = bodo.ir.csv_ext.csv_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    gsb__dtdcf += (
        """    {}, bodo.utils.conversion.coerce_to_ndarray(skiprows, scalar_to_arr_len=1).ctypes, nrows, {}, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py, {}, {}, skiprows_list_len, {})
"""
        .format(parallel, rpj__njov, compression, chunksize,
        is_skiprows_list, pd_low_memory))
    gsb__dtdcf += '  if bodo.utils.utils.is_null_pointer(f_reader._pyobj):\n'
    gsb__dtdcf += "      raise FileNotFoundError('File does not exist')\n"
    return gsb__dtdcf


def _gen_read_csv_objmode(col_names, sanitized_cnames, col_typs, usecols,
    out_used_cols, sep, escapechar, storage_options, call_id, glbs,
    parallel, check_parallel_runtime, idx_col_index, idx_col_typ):
    rzxq__ofm = [str(ofe__jvv) for ofe__jvv, ocuh__chvkl in enumerate(
        usecols) if col_typs[out_used_cols[ofe__jvv]].dtype == types.
        NPDatetime('ns')]
    if idx_col_typ == types.NPDatetime('ns'):
        assert not idx_col_index is None
        rzxq__ofm.append(str(idx_col_index))
    myq__ohb = ', '.join(rzxq__ofm)
    wiz__mzaub = _gen_parallel_flag_name(sanitized_cnames)
    uqo__vqeka = f"{wiz__mzaub}='bool_'" if check_parallel_runtime else ''
    nyw__lvf = [_get_pd_dtype_str(col_typs[out_used_cols[ofe__jvv]]) for
        ofe__jvv in range(len(usecols))]
    kfurj__mtxsv = None if idx_col_index is None else _get_pd_dtype_str(
        idx_col_typ)
    cond__kpm = [ocuh__chvkl for ofe__jvv, ocuh__chvkl in enumerate(usecols
        ) if nyw__lvf[ofe__jvv] == 'str']
    if idx_col_index is not None and kfurj__mtxsv == 'str':
        cond__kpm.append(idx_col_index)
    gbqb__ile = np.array(cond__kpm, dtype=np.int64)
    glbs[f'str_col_nums_{call_id}'] = gbqb__ile
    gsb__dtdcf = f'  str_col_nums_{call_id}_2 = str_col_nums_{call_id}\n'
    msfai__pux = np.array(usecols + ([idx_col_index] if idx_col_index is not
        None else []), dtype=np.int64)
    glbs[f'usecols_arr_{call_id}'] = msfai__pux
    gsb__dtdcf += f'  usecols_arr_{call_id}_2 = usecols_arr_{call_id}\n'
    snzb__onpnz = np.array(out_used_cols, dtype=np.int64)
    if usecols:
        glbs[f'type_usecols_offsets_arr_{call_id}'] = snzb__onpnz
        gsb__dtdcf += f"""  type_usecols_offsets_arr_{call_id}_2 = type_usecols_offsets_arr_{call_id}
"""
    ijikt__sge = defaultdict(list)
    for ofe__jvv, ocuh__chvkl in enumerate(usecols):
        if nyw__lvf[ofe__jvv] == 'str':
            continue
        ijikt__sge[nyw__lvf[ofe__jvv]].append(ocuh__chvkl)
    if idx_col_index is not None and kfurj__mtxsv != 'str':
        ijikt__sge[kfurj__mtxsv].append(idx_col_index)
    for ofe__jvv, mxjv__ihrf in enumerate(ijikt__sge.values()):
        glbs[f't_arr_{ofe__jvv}_{call_id}'] = np.asarray(mxjv__ihrf)
        gsb__dtdcf += (
            f'  t_arr_{ofe__jvv}_{call_id}_2 = t_arr_{ofe__jvv}_{call_id}\n')
    if idx_col_index != None:
        gsb__dtdcf += f"""  with objmode(T=table_type_{call_id}, idx_arr=idx_array_typ, {uqo__vqeka}):
"""
    else:
        gsb__dtdcf += (
            f'  with objmode(T=table_type_{call_id}, {uqo__vqeka}):\n')
    gsb__dtdcf += f'    typemap = {{}}\n'
    for ofe__jvv, fgw__ahx in enumerate(ijikt__sge.keys()):
        gsb__dtdcf += f"""    typemap.update({{i:{fgw__ahx} for i in t_arr_{ofe__jvv}_{call_id}_2}})
"""
    gsb__dtdcf += '    if f_reader.get_chunk_size() == 0:\n'
    gsb__dtdcf += (
        f'      df = pd.DataFrame(columns=usecols_arr_{call_id}_2, dtype=str)\n'
        )
    gsb__dtdcf += '    else:\n'
    gsb__dtdcf += '      df = pd.read_csv(f_reader,\n'
    gsb__dtdcf += '        header=None,\n'
    gsb__dtdcf += '        parse_dates=[{}],\n'.format(myq__ohb)
    gsb__dtdcf += (
        f"        dtype={{i:'string[pyarrow]' for i in str_col_nums_{call_id}_2}},\n"
        )
    gsb__dtdcf += f"""        usecols=usecols_arr_{call_id}_2, sep={sep!r}, low_memory=False, escapechar={escapechar!r})
"""
    if check_parallel_runtime:
        gsb__dtdcf += f'    {wiz__mzaub} = f_reader.is_parallel()\n'
    else:
        gsb__dtdcf += f'    {wiz__mzaub} = {parallel}\n'
    gsb__dtdcf += f'    df = astype(df, typemap, {wiz__mzaub})\n'
    if idx_col_index != None:
        bxrg__eiqxe = sorted(msfai__pux).index(idx_col_index)
        gsb__dtdcf += f'    idx_arr = df.iloc[:, {bxrg__eiqxe}].values\n'
        gsb__dtdcf += (
            f'    df.drop(columns=df.columns[{bxrg__eiqxe}], inplace=True)\n')
    if len(usecols) == 0:
        gsb__dtdcf += f'    T = None\n'
    else:
        gsb__dtdcf += f'    arrs = []\n'
        gsb__dtdcf += f'    for i in range(df.shape[1]):\n'
        gsb__dtdcf += f'      arrs.append(df.iloc[:, i].values)\n'
        gsb__dtdcf += f"""    T = Table(arrs, type_usecols_offsets_arr_{call_id}_2, {len(col_names)})
"""
    return gsb__dtdcf


def _gen_parallel_flag_name(sanitized_cnames):
    wiz__mzaub = '_parallel_value'
    while wiz__mzaub in sanitized_cnames:
        wiz__mzaub = '_' + wiz__mzaub
    return wiz__mzaub


def _gen_csv_reader_py(col_names, col_typs, usecols, out_used_cols, sep,
    parallel, header, compression, is_skiprows_list, pd_low_memory,
    escapechar, storage_options, idx_col_index=None, idx_col_typ=types.none):
    sanitized_cnames = [sanitize_varname(syakc__wsuh) for syakc__wsuh in
        col_names]
    gsb__dtdcf = 'def csv_reader_py(fname, nrows, skiprows):\n'
    gsb__dtdcf += _gen_csv_file_reader_init(parallel, header, compression, 
        -1, is_skiprows_list, pd_low_memory, storage_options)
    call_id = ir_utils.next_label()
    kupg__rcf = globals()
    if idx_col_typ != types.none:
        kupg__rcf[f'idx_array_typ'] = idx_col_typ
    if len(usecols) == 0:
        kupg__rcf[f'table_type_{call_id}'] = types.none
    else:
        kupg__rcf[f'table_type_{call_id}'] = TableType(tuple(col_typs))
    gsb__dtdcf += _gen_read_csv_objmode(col_names, sanitized_cnames,
        col_typs, usecols, out_used_cols, sep, escapechar, storage_options,
        call_id, kupg__rcf, parallel=parallel, check_parallel_runtime=False,
        idx_col_index=idx_col_index, idx_col_typ=idx_col_typ)
    if idx_col_index != None:
        gsb__dtdcf += '  return (T, idx_arr)\n'
    else:
        gsb__dtdcf += '  return (T, None)\n'
    pxhu__rbavc = {}
    kupg__rcf['get_storage_options_pyobject'] = get_storage_options_pyobject
    exec(gsb__dtdcf, kupg__rcf, pxhu__rbavc)
    mjsw__xovbx = pxhu__rbavc['csv_reader_py']
    gezh__awh = numba.njit(mjsw__xovbx)
    compiled_funcs.append(gezh__awh)
    return gezh__awh
