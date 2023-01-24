import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir, ir_utils, typeinfer, types
from numba.core.ir_utils import compile_to_numba_ir, replace_arg_nodes
from numba.extending import intrinsic
import bodo
import bodo.ir.connector
from bodo import objmode
from bodo.io.fs_io import get_storage_options_pyobject, storage_options_dict_type
from bodo.libs.str_ext import string_type
from bodo.transforms import distributed_analysis, distributed_pass
from bodo.utils.utils import check_and_propagate_cpp_exception, check_java_installation, sanitize_varname


class JsonReader(ir.Stmt):

    def __init__(self, df_out, loc, out_vars, out_types, file_name,
        df_colnames, orient, convert_dates, precise_float, lines,
        compression, storage_options):
        self.connector_typ = 'json'
        self.df_out = df_out
        self.loc = loc
        self.out_vars = out_vars
        self.out_types = out_types
        self.file_name = file_name
        self.df_colnames = df_colnames
        self.orient = orient
        self.convert_dates = convert_dates
        self.precise_float = precise_float
        self.lines = lines
        self.compression = compression
        self.storage_options = storage_options

    def __repr__(self):
        return ('{} = ReadJson(file={}, col_names={}, types={}, vars={})'.
            format(self.df_out, self.file_name, self.df_colnames, self.
            out_types, self.out_vars))


import llvmlite.binding as ll
from bodo.io import json_cpp
ll.add_symbol('json_file_chunk_reader', json_cpp.json_file_chunk_reader)


@intrinsic
def json_file_chunk_reader(typingctx, fname_t, lines_t, is_parallel_t,
    nrows_t, compression_t, bucket_region_t, storage_options_t):
    assert storage_options_t == storage_options_dict_type, "Storage options don't match expected type"

    def codegen(context, builder, sig, args):
        bpoh__expu = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        wxcvf__mptw = cgutils.get_or_insert_function(builder.module,
            bpoh__expu, name='json_file_chunk_reader')
        cgtyq__mrkut = builder.call(wxcvf__mptw, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        hkx__mqvfp = cgutils.create_struct_proxy(types.stream_reader_type)(
            context, builder)
        vxuyh__vhzb = context.get_python_api(builder)
        hkx__mqvfp.meminfo = vxuyh__vhzb.nrt_meminfo_new_from_pyobject(context
            .get_constant_null(types.voidptr), cgtyq__mrkut)
        hkx__mqvfp.pyobj = cgtyq__mrkut
        vxuyh__vhzb.decref(cgtyq__mrkut)
        return hkx__mqvfp._getvalue()
    return types.stream_reader_type(types.voidptr, types.bool_, types.bool_,
        types.int64, types.voidptr, types.voidptr, storage_options_dict_type
        ), codegen


def remove_dead_json(json_node, lives_no_aliases, lives, arg_aliases,
    alias_map, func_ir, typemap):
    mwjva__mmqsg = []
    yrqc__uqiwd = []
    gscsk__jpodc = []
    for ryw__wqby, qhtq__mhuoz in enumerate(json_node.out_vars):
        if qhtq__mhuoz.name in lives:
            mwjva__mmqsg.append(json_node.df_colnames[ryw__wqby])
            yrqc__uqiwd.append(json_node.out_vars[ryw__wqby])
            gscsk__jpodc.append(json_node.out_types[ryw__wqby])
    json_node.df_colnames = mwjva__mmqsg
    json_node.out_vars = yrqc__uqiwd
    json_node.out_types = gscsk__jpodc
    if len(json_node.out_vars) == 0:
        return None
    return json_node


def json_distributed_run(json_node, array_dists, typemap, calltypes,
    typingctx, targetctx):
    if bodo.user_logging.get_verbose_level() >= 1:
        mqnp__ayz = (
            'Finish column pruning on read_json node:\n%s\nColumns loaded %s\n'
            )
        ropr__lwf = json_node.loc.strformat()
        hwq__fneg = json_node.df_colnames
        bodo.user_logging.log_message('Column Pruning', mqnp__ayz,
            ropr__lwf, hwq__fneg)
        lpqne__befdo = [wmrgp__xsp for ryw__wqby, wmrgp__xsp in enumerate(
            json_node.df_colnames) if isinstance(json_node.out_types[
            ryw__wqby], bodo.libs.dict_arr_ext.DictionaryArrayType)]
        if lpqne__befdo:
            hrjbd__rjmrs = """Finished optimized encoding on read_json node:
%s
Columns %s using dictionary encoding to reduce memory usage.
"""
            bodo.user_logging.log_message('Dictionary Encoding',
                hrjbd__rjmrs, ropr__lwf, lpqne__befdo)
    parallel = False
    if array_dists is not None:
        parallel = True
        for drzk__lpdna in json_node.out_vars:
            if array_dists[drzk__lpdna.name
                ] != distributed_pass.Distribution.OneD and array_dists[
                drzk__lpdna.name] != distributed_pass.Distribution.OneD_Var:
                parallel = False
    cggkv__xmtz = len(json_node.out_vars)
    ytm__avhea = ', '.join('arr' + str(ryw__wqby) for ryw__wqby in range(
        cggkv__xmtz))
    qlu__pptn = 'def json_impl(fname):\n'
    qlu__pptn += '    ({},) = _json_reader_py(fname)\n'.format(ytm__avhea)
    dnf__pzpii = {}
    exec(qlu__pptn, {}, dnf__pzpii)
    zpkn__tmam = dnf__pzpii['json_impl']
    aobvb__olcm = _gen_json_reader_py(json_node.df_colnames, json_node.
        out_types, typingctx, targetctx, parallel, json_node.orient,
        json_node.convert_dates, json_node.precise_float, json_node.lines,
        json_node.compression, json_node.storage_options)
    sawi__yjqw = compile_to_numba_ir(zpkn__tmam, {'_json_reader_py':
        aobvb__olcm}, typingctx=typingctx, targetctx=targetctx, arg_typs=(
        string_type,), typemap=typemap, calltypes=calltypes).blocks.popitem()[1
        ]
    replace_arg_nodes(sawi__yjqw, [json_node.file_name])
    ebpd__gwqo = sawi__yjqw.body[:-3]
    for ryw__wqby in range(len(json_node.out_vars)):
        ebpd__gwqo[-len(json_node.out_vars) + ryw__wqby
            ].target = json_node.out_vars[ryw__wqby]
    return ebpd__gwqo


numba.parfors.array_analysis.array_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_array_analysis
distributed_analysis.distributed_analysis_extensions[JsonReader
    ] = bodo.ir.connector.connector_distributed_analysis
typeinfer.typeinfer_extensions[JsonReader
    ] = bodo.ir.connector.connector_typeinfer
ir_utils.visit_vars_extensions[JsonReader
    ] = bodo.ir.connector.visit_vars_connector
ir_utils.remove_dead_extensions[JsonReader] = remove_dead_json
numba.core.analysis.ir_extension_usedefs[JsonReader
    ] = bodo.ir.connector.connector_usedefs
ir_utils.copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.get_copies_connector
ir_utils.apply_copy_propagate_extensions[JsonReader
    ] = bodo.ir.connector.apply_copies_connector
ir_utils.build_defs_extensions[JsonReader
    ] = bodo.ir.connector.build_connector_definitions
distributed_pass.distributed_run_extensions[JsonReader] = json_distributed_run
compiled_funcs = []


def _gen_json_reader_py(col_names, col_typs, typingctx, targetctx, parallel,
    orient, convert_dates, precise_float, lines, compression, storage_options):
    hvh__wtqm = [sanitize_varname(wmrgp__xsp) for wmrgp__xsp in col_names]
    dqaem__hsl = ', '.join(str(ryw__wqby) for ryw__wqby, iavx__mxu in
        enumerate(col_typs) if iavx__mxu.dtype == types.NPDatetime('ns'))
    lelu__vrm = ', '.join(["{}='{}'".format(ocgi__hrsg, bodo.ir.csv_ext.
        _get_dtype_str(iavx__mxu)) for ocgi__hrsg, iavx__mxu in zip(
        hvh__wtqm, col_typs)])
    qjxg__stby = ', '.join(["'{}':{}".format(ieex__fpg, bodo.ir.csv_ext.
        _get_pd_dtype_str(iavx__mxu)) for ieex__fpg, iavx__mxu in zip(
        col_names, col_typs)])
    if compression is None:
        compression = 'uncompressed'
    qlu__pptn = 'def json_reader_py(fname):\n'
    qlu__pptn += '  df_typeref_2 = df_typeref\n'
    qlu__pptn += '  check_java_installation(fname)\n'
    qlu__pptn += f"""  bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(fname, parallel={parallel})
"""
    if storage_options is None:
        storage_options = {}
    storage_options['bodo_dummy'] = 'dummy'
    qlu__pptn += (
        f'  storage_options_py = get_storage_options_pyobject({str(storage_options)})\n'
        )
    qlu__pptn += (
        '  f_reader = bodo.ir.json_ext.json_file_chunk_reader(bodo.libs.str_ext.unicode_to_utf8(fname), '
        )
    qlu__pptn += (
        """    {}, {}, -1, bodo.libs.str_ext.unicode_to_utf8('{}'), bodo.libs.str_ext.unicode_to_utf8(bucket_region), storage_options_py )
"""
        .format(lines, parallel, compression))
    qlu__pptn += '  if bodo.utils.utils.is_null_pointer(f_reader._pyobj):\n'
    qlu__pptn += "      raise FileNotFoundError('File does not exist')\n"
    qlu__pptn += f'  with objmode({lelu__vrm}):\n'
    qlu__pptn += f"    df = pd.read_json(f_reader, orient='{orient}',\n"
    qlu__pptn += f'       convert_dates = {convert_dates}, \n'
    qlu__pptn += f'       precise_float={precise_float}, \n'
    qlu__pptn += f'       lines={lines}, \n'
    qlu__pptn += '       dtype={{{}}},\n'.format(qjxg__stby)
    qlu__pptn += '       )\n'
    qlu__pptn += (
        '    bodo.ir.connector.cast_float_to_nullable(df, df_typeref_2)\n')
    for ocgi__hrsg, ieex__fpg in zip(hvh__wtqm, col_names):
        qlu__pptn += '    if len(df) > 0:\n'
        qlu__pptn += "        {} = df['{}'].values\n".format(ocgi__hrsg,
            ieex__fpg)
        qlu__pptn += '    else:\n'
        qlu__pptn += '        {} = np.array([])\n'.format(ocgi__hrsg)
    qlu__pptn += '  return ({},)\n'.format(', '.join(kto__obl for kto__obl in
        hvh__wtqm))
    xll__orwd = globals()
    xll__orwd.update({'bodo': bodo, 'pd': pd, 'np': np, 'objmode': objmode,
        'check_java_installation': check_java_installation, 'df_typeref':
        bodo.DataFrameType(tuple(col_typs), bodo.RangeIndexType(None),
        tuple(col_names)), 'get_storage_options_pyobject':
        get_storage_options_pyobject})
    dnf__pzpii = {}
    exec(qlu__pptn, xll__orwd, dnf__pzpii)
    aobvb__olcm = dnf__pzpii['json_reader_py']
    jjim__penr = numba.njit(aobvb__olcm)
    compiled_funcs.append(jjim__penr)
    return jjim__penr
