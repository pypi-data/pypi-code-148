"""
Class information for DataFrame iterators returned by pd.read_csv. This is used
to handle situations in which pd.read_csv is used to return chunks with separate
read calls instead of just a single read.
"""
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, ir_utils, types
from numba.core.imputils import RefType, impl_ret_borrowed, iternext_impl
from numba.core.typing.templates import signature
from numba.extending import intrinsic, lower_builtin, models, register_model
import bodo
import bodo.ir.connector
import bodo.ir.csv_ext
from bodo import objmode
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.table import Table, TableType
from bodo.io import csv_cpp
from bodo.ir.csv_ext import _gen_read_csv_objmode, astype
from bodo.utils.typing import ColNamesMetaType
from bodo.utils.utils import check_java_installation
from bodo.utils.utils import sanitize_varname
ll.add_symbol('update_csv_reader', csv_cpp.update_csv_reader)
ll.add_symbol('initialize_csv_reader', csv_cpp.initialize_csv_reader)


class CSVIteratorType(types.SimpleIteratorType):

    def __init__(self, df_type, out_colnames, out_types, usecols, sep,
        index_ind, index_arr_typ, index_name, escapechar, storage_options):
        assert isinstance(df_type, DataFrameType
            ), 'CSVIterator must return a DataFrame'
        awh__ovi = (
            f'CSVIteratorType({df_type}, {out_colnames}, {out_types}, {usecols}, {sep}, {index_ind}, {index_arr_typ}, {index_name}, {escapechar})'
            )
        super(types.SimpleIteratorType, self).__init__(awh__ovi)
        self._yield_type = df_type
        self._out_colnames = out_colnames
        self._out_types = out_types
        self._usecols = usecols
        self._sep = sep
        self._index_ind = index_ind
        self._index_arr_typ = index_arr_typ
        self._index_name = index_name
        self._escapechar = escapechar
        self._storage_options = storage_options

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(CSVIteratorType)
class CSVIteratorModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wqi__aor = [('csv_reader', types.stream_reader_type), ('index',
            types.EphemeralPointer(types.uintp))]
        super(CSVIteratorModel, self).__init__(dmm, fe_type, wqi__aor)


@lower_builtin('getiter', CSVIteratorType)
def getiter_csv_iterator(context, builder, sig, args):
    vyen__mtylb = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        value=args[0])
    gea__ctam = lir.FunctionType(lir.VoidType(), [lir.IntType(8).as_pointer()])
    ypw__wph = cgutils.get_or_insert_function(builder.module, gea__ctam,
        name='initialize_csv_reader')
    rya__wki = cgutils.create_struct_proxy(types.stream_reader_type)(context,
        builder, value=vyen__mtylb.csv_reader)
    builder.call(ypw__wph, [rya__wki.pyobj])
    builder.store(context.get_constant(types.uint64, 0), vyen__mtylb.index)
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@lower_builtin('iternext', CSVIteratorType)
@iternext_impl(RefType.NEW)
def iternext_csv_iterator(context, builder, sig, args, result):
    [vane__xmhwx] = sig.args
    [yyv__gswz] = args
    vyen__mtylb = cgutils.create_struct_proxy(vane__xmhwx)(context, builder,
        value=yyv__gswz)
    gea__ctam = lir.FunctionType(lir.IntType(1), [lir.IntType(8).as_pointer()])
    ypw__wph = cgutils.get_or_insert_function(builder.module, gea__ctam,
        name='update_csv_reader')
    rya__wki = cgutils.create_struct_proxy(types.stream_reader_type)(context,
        builder, value=vyen__mtylb.csv_reader)
    mssnh__hlyze = builder.call(ypw__wph, [rya__wki.pyobj])
    result.set_valid(mssnh__hlyze)
    with builder.if_then(mssnh__hlyze):
        jregx__tozar = builder.load(vyen__mtylb.index)
        fzl__mhbpu = types.Tuple([sig.return_type.first_type, types.int64])
        aqdh__sxmlm = gen_read_csv_objmode(sig.args[0])
        grfh__gqoch = signature(fzl__mhbpu, types.stream_reader_type, types
            .int64)
        vmrf__nev = context.compile_internal(builder, aqdh__sxmlm,
            grfh__gqoch, [vyen__mtylb.csv_reader, jregx__tozar])
        hzd__lnm, sybog__ethnv = cgutils.unpack_tuple(builder, vmrf__nev)
        xor__yxz = builder.add(jregx__tozar, sybog__ethnv, flags=['nsw'])
        builder.store(xor__yxz, vyen__mtylb.index)
        result.yield_(hzd__lnm)


@intrinsic
def init_csv_iterator(typingctx, csv_reader, csv_iterator_typeref):

    def codegen(context, builder, signature, args):
        zqb__fkzcs = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        context.nrt.incref(builder, signature.args[0], args[0])
        zqb__fkzcs.csv_reader = args[0]
        hkrs__awuya = context.get_constant(types.uintp, 0)
        zqb__fkzcs.index = cgutils.alloca_once_value(builder, hkrs__awuya)
        return zqb__fkzcs._getvalue()
    assert isinstance(csv_iterator_typeref, types.TypeRef
        ), 'Initializing a csv iterator requires a typeref'
    vqr__guftz = csv_iterator_typeref.instance_type
    sig = signature(vqr__guftz, csv_reader, csv_iterator_typeref)
    return sig, codegen


def gen_read_csv_objmode(csv_iterator_type):
    xiim__kjb = 'def read_csv_objmode(f_reader):\n'
    yml__kgos = [sanitize_varname(yhstw__xko) for yhstw__xko in
        csv_iterator_type._out_colnames]
    fkuyh__kbv = ir_utils.next_label()
    xke__qdus = globals()
    out_types = csv_iterator_type._out_types
    xke__qdus[f'table_type_{fkuyh__kbv}'] = TableType(tuple(out_types))
    xke__qdus[f'idx_array_typ'] = csv_iterator_type._index_arr_typ
    zzuq__nppkn = list(range(len(csv_iterator_type._usecols)))
    xiim__kjb += _gen_read_csv_objmode(csv_iterator_type._out_colnames,
        yml__kgos, out_types, csv_iterator_type._usecols, zzuq__nppkn,
        csv_iterator_type._sep, csv_iterator_type._escapechar,
        csv_iterator_type._storage_options, fkuyh__kbv, xke__qdus, parallel
        =False, check_parallel_runtime=True, idx_col_index=
        csv_iterator_type._index_ind, idx_col_typ=csv_iterator_type.
        _index_arr_typ)
    eaa__iwqau = bodo.ir.csv_ext._gen_parallel_flag_name(yml__kgos)
    vgdtq__ojjl = ['T'] + (['idx_arr'] if csv_iterator_type._index_ind is not
        None else []) + [eaa__iwqau]
    xiim__kjb += f"  return {', '.join(vgdtq__ojjl)}"
    xke__qdus = globals()
    owht__fjuo = {}
    exec(xiim__kjb, xke__qdus, owht__fjuo)
    pmjnd__gimz = owht__fjuo['read_csv_objmode']
    mrbhx__kapy = numba.njit(pmjnd__gimz)
    bodo.ir.csv_ext.compiled_funcs.append(mrbhx__kapy)
    ktfvo__zqkb = 'def read_func(reader, local_start):\n'
    ktfvo__zqkb += f"  {', '.join(vgdtq__ojjl)} = objmode_func(reader)\n"
    index_ind = csv_iterator_type._index_ind
    if index_ind is None:
        ktfvo__zqkb += f'  local_len = len(T)\n'
        ktfvo__zqkb += '  total_size = local_len\n'
        ktfvo__zqkb += f'  if ({eaa__iwqau}):\n'
        ktfvo__zqkb += """    local_start = local_start + bodo.libs.distributed_api.dist_exscan(local_len, _op)
"""
        ktfvo__zqkb += (
            '    total_size = bodo.libs.distributed_api.dist_reduce(local_len, _op)\n'
            )
        zun__wlf = (
            f'bodo.hiframes.pd_index_ext.init_range_index(local_start, local_start + local_len, 1, None)'
            )
    else:
        ktfvo__zqkb += '  total_size = 0\n'
        zun__wlf = (
            f'bodo.utils.conversion.convert_to_index({vgdtq__ojjl[1]}, {csv_iterator_type._index_name!r})'
            )
    ktfvo__zqkb += f"""  return (bodo.hiframes.pd_dataframe_ext.init_dataframe(({vgdtq__ojjl[0]},), {zun__wlf}, __col_name_meta_value_read_csv_objmode), total_size)
"""
    exec(ktfvo__zqkb, {'bodo': bodo, 'objmode_func': mrbhx__kapy, '_op': np
        .int32(bodo.libs.distributed_api.Reduce_Type.Sum.value),
        '__col_name_meta_value_read_csv_objmode': ColNamesMetaType(
        csv_iterator_type.yield_type.columns)}, owht__fjuo)
    return owht__fjuo['read_func']
