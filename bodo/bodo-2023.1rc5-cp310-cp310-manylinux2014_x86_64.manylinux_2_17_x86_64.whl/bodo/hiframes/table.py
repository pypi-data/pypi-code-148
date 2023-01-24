"""Table data type for storing dataframe column arrays. Supports storing many columns
(e.g. >10k) efficiently.
"""
import operator
from collections import defaultdict
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.ir_utils import guard
from numba.core.typing.templates import signature
from numba.cpython.listobj import ListInstance
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, lower_getattr, make_attribute_wrapper, models, overload, register_model, typeof_impl, unbox
from numba.np.arrayobj import _getitem_array_single_int
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.typing import BodoError, MetaType, decode_if_dict_array, get_overload_const_int, is_list_like_index_type, is_overload_constant_bool, is_overload_constant_int, is_overload_none, is_overload_true, raise_bodo_error, to_str_arr_if_dict_array, unwrap_typeref
from bodo.utils.utils import is_whole_slice


class Table:

    def __init__(self, arrs, usecols=None, num_arrs=-1):
        if usecols is not None:
            assert num_arrs != -1, 'num_arrs must be provided if usecols is not None'
            rkzfn__pqmv = 0
            mpor__cadwk = []
            for i in range(usecols[-1] + 1):
                if i == usecols[rkzfn__pqmv]:
                    mpor__cadwk.append(arrs[rkzfn__pqmv])
                    rkzfn__pqmv += 1
                else:
                    mpor__cadwk.append(None)
            for zzp__lock in range(usecols[-1] + 1, num_arrs):
                mpor__cadwk.append(None)
            self.arrays = mpor__cadwk
        else:
            self.arrays = arrs
        self.block_0 = arrs

    def __eq__(self, other):
        return isinstance(other, Table) and len(self.arrays) == len(other.
            arrays) and all((vpbls__szf == uubh__fslk).all() for vpbls__szf,
            uubh__fslk in zip(self.arrays, other.arrays))

    def __str__(self) ->str:
        return str(self.arrays)

    def to_pandas(self, index=None):
        lbjzb__ghvne = len(self.arrays)
        zgucf__gznoi = dict(zip(range(lbjzb__ghvne), self.arrays))
        df = pd.DataFrame(zgucf__gznoi, index)
        return df


class TableType(types.ArrayCompatible):

    def __init__(self, arr_types, has_runtime_cols=False):
        self.arr_types = arr_types
        self.has_runtime_cols = has_runtime_cols
        qgn__jfod = []
        gkwqj__zqa = []
        kpfs__awk = {}
        ftblk__jvpo = {}
        ety__zpgg = defaultdict(int)
        mrtr__egr = defaultdict(list)
        if not has_runtime_cols:
            for i, t in enumerate(arr_types):
                if t not in kpfs__awk:
                    pedsb__ocp = len(kpfs__awk)
                    kpfs__awk[t] = pedsb__ocp
                    ftblk__jvpo[pedsb__ocp] = t
                bxphb__txg = kpfs__awk[t]
                qgn__jfod.append(bxphb__txg)
                gkwqj__zqa.append(ety__zpgg[bxphb__txg])
                ety__zpgg[bxphb__txg] += 1
                mrtr__egr[bxphb__txg].append(i)
        self.block_nums = qgn__jfod
        self.block_offsets = gkwqj__zqa
        self.type_to_blk = kpfs__awk
        self.blk_to_type = ftblk__jvpo
        self.block_to_arr_ind = mrtr__egr
        super(TableType, self).__init__(name=
            f'TableType({arr_types}, {has_runtime_cols})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    @property
    def key(self):
        return self.arr_types, self.has_runtime_cols

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(Table)
def typeof_table(val, c):
    return TableType(tuple(numba.typeof(arr) for arr in val.arrays))


@register_model(TableType)
class TableTypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        if fe_type.has_runtime_cols:
            sqjp__yfkme = [(f'block_{i}', types.List(t)) for i, t in
                enumerate(fe_type.arr_types)]
        else:
            sqjp__yfkme = [(f'block_{bxphb__txg}', types.List(t)) for t,
                bxphb__txg in fe_type.type_to_blk.items()]
        sqjp__yfkme.append(('parent', types.pyobject))
        sqjp__yfkme.append(('len', types.int64))
        super(TableTypeModel, self).__init__(dmm, fe_type, sqjp__yfkme)


make_attribute_wrapper(TableType, 'block_0', 'block_0')
make_attribute_wrapper(TableType, 'len', '_len')


@infer_getattr
class TableTypeAttribute(OverloadedKeyAttributeTemplate):
    key = TableType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])


@unbox(TableType)
def unbox_table(typ, val, c):
    fdwrq__kdqub = c.pyapi.object_getattr_string(val, 'arrays')
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    table.parent = cgutils.get_null_value(table.parent.type)
    itfmh__bil = c.pyapi.make_none()
    tll__bkc = c.context.get_constant(types.int64, 0)
    zqtlj__rrixn = cgutils.alloca_once_value(c.builder, tll__bkc)
    for t, bxphb__txg in typ.type_to_blk.items():
        erv__sslk = c.context.get_constant(types.int64, len(typ.
            block_to_arr_ind[bxphb__txg]))
        zzp__lock, zso__lau = ListInstance.allocate_ex(c.context, c.builder,
            types.List(t), erv__sslk)
        zso__lau.size = erv__sslk
        cjav__ddlaj = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[bxphb__txg],
            dtype=np.int64))
        adsk__kdjx = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, cjav__ddlaj)
        with cgutils.for_range(c.builder, erv__sslk) as ghjvh__uxel:
            i = ghjvh__uxel.index
            nkj__jnvhc = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), adsk__kdjx, i)
            gjcl__uae = c.pyapi.long_from_longlong(nkj__jnvhc)
            lrzf__opik = c.pyapi.object_getitem(fdwrq__kdqub, gjcl__uae)
            fhxzp__gyshz = c.builder.icmp_unsigned('==', lrzf__opik, itfmh__bil
                )
            with c.builder.if_else(fhxzp__gyshz) as (zes__ahf, oud__mxmp):
                with zes__ahf:
                    qmuj__pbazu = c.context.get_constant_null(t)
                    zso__lau.inititem(i, qmuj__pbazu, incref=False)
                with oud__mxmp:
                    ose__qrs = c.pyapi.call_method(lrzf__opik, '__len__', ())
                    wycz__abu = c.pyapi.long_as_longlong(ose__qrs)
                    c.builder.store(wycz__abu, zqtlj__rrixn)
                    c.pyapi.decref(ose__qrs)
                    arr = c.pyapi.to_native_value(t, lrzf__opik).value
                    zso__lau.inititem(i, arr, incref=False)
            c.pyapi.decref(lrzf__opik)
            c.pyapi.decref(gjcl__uae)
        setattr(table, f'block_{bxphb__txg}', zso__lau.value)
    table.len = c.builder.load(zqtlj__rrixn)
    c.pyapi.decref(fdwrq__kdqub)
    c.pyapi.decref(itfmh__bil)
    fhlwc__les = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(table._getvalue(), is_error=fhlwc__les)


@box(TableType)
def box_table(typ, val, c, ensure_unboxed=None):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    table = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    if typ.has_runtime_cols:
        esr__vxq = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            mpor__cadwk = getattr(table, f'block_{i}')
            ygm__cbp = ListInstance(c.context, c.builder, types.List(t),
                mpor__cadwk)
            esr__vxq = c.builder.add(esr__vxq, ygm__cbp.size)
        oazb__wgba = c.pyapi.list_new(esr__vxq)
        ame__pihi = c.context.get_constant(types.int64, 0)
        for i, t in enumerate(typ.arr_types):
            mpor__cadwk = getattr(table, f'block_{i}')
            ygm__cbp = ListInstance(c.context, c.builder, types.List(t),
                mpor__cadwk)
            with cgutils.for_range(c.builder, ygm__cbp.size) as ghjvh__uxel:
                i = ghjvh__uxel.index
                arr = ygm__cbp.getitem(i)
                c.context.nrt.incref(c.builder, t, arr)
                idx = c.builder.add(ame__pihi, i)
                c.pyapi.list_setitem(oazb__wgba, idx, c.pyapi.
                    from_native_value(t, arr, c.env_manager))
            ame__pihi = c.builder.add(ame__pihi, ygm__cbp.size)
        eqgl__dqgl = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
        wfl__kcep = c.pyapi.call_function_objargs(eqgl__dqgl, (oazb__wgba,))
        c.pyapi.decref(eqgl__dqgl)
        c.pyapi.decref(oazb__wgba)
        c.context.nrt.decref(c.builder, typ, val)
        return wfl__kcep
    oazb__wgba = c.pyapi.list_new(c.context.get_constant(types.int64, len(
        typ.arr_types)))
    bvp__nnu = cgutils.is_not_null(c.builder, table.parent)
    if ensure_unboxed is None:
        ensure_unboxed = c.context.get_constant(types.bool_, False)
    for t, bxphb__txg in typ.type_to_blk.items():
        mpor__cadwk = getattr(table, f'block_{bxphb__txg}')
        ygm__cbp = ListInstance(c.context, c.builder, types.List(t),
            mpor__cadwk)
        cjav__ddlaj = c.context.make_constant_array(c.builder, types.Array(
            types.int64, 1, 'C'), np.array(typ.block_to_arr_ind[bxphb__txg],
            dtype=np.int64))
        adsk__kdjx = c.context.make_array(types.Array(types.int64, 1, 'C'))(c
            .context, c.builder, cjav__ddlaj)
        with cgutils.for_range(c.builder, ygm__cbp.size) as ghjvh__uxel:
            i = ghjvh__uxel.index
            nkj__jnvhc = _getitem_array_single_int(c.context, c.builder,
                types.int64, types.Array(types.int64, 1, 'C'), adsk__kdjx, i)
            arr = ygm__cbp.getitem(i)
            ysuua__wlcp = cgutils.alloca_once_value(c.builder, arr)
            xdq__sqta = cgutils.alloca_once_value(c.builder, c.context.
                get_constant_null(t))
            is_null = is_ll_eq(c.builder, ysuua__wlcp, xdq__sqta)
            with c.builder.if_else(c.builder.and_(is_null, c.builder.not_(
                ensure_unboxed))) as (zes__ahf, oud__mxmp):
                with zes__ahf:
                    itfmh__bil = c.pyapi.make_none()
                    c.pyapi.list_setitem(oazb__wgba, nkj__jnvhc, itfmh__bil)
                with oud__mxmp:
                    lrzf__opik = cgutils.alloca_once(c.builder, c.context.
                        get_value_type(types.pyobject))
                    with c.builder.if_else(c.builder.and_(is_null, bvp__nnu)
                        ) as (hvsa__uau, gbbst__jxz):
                        with hvsa__uau:
                            axbzv__jnmrh = get_df_obj_column_codegen(c.
                                context, c.builder, c.pyapi, table.parent,
                                nkj__jnvhc, t)
                            c.builder.store(axbzv__jnmrh, lrzf__opik)
                        with gbbst__jxz:
                            c.context.nrt.incref(c.builder, t, arr)
                            c.builder.store(c.pyapi.from_native_value(t,
                                arr, c.env_manager), lrzf__opik)
                    c.pyapi.list_setitem(oazb__wgba, nkj__jnvhc, c.builder.
                        load(lrzf__opik))
    eqgl__dqgl = c.pyapi.unserialize(c.pyapi.serialize_object(Table))
    wfl__kcep = c.pyapi.call_function_objargs(eqgl__dqgl, (oazb__wgba,))
    c.pyapi.decref(eqgl__dqgl)
    c.pyapi.decref(oazb__wgba)
    c.context.nrt.decref(c.builder, typ, val)
    return wfl__kcep


@lower_builtin(len, TableType)
def table_len_lower(context, builder, sig, args):
    impl = table_len_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def table_len_overload(T):
    if not isinstance(T, TableType):
        return

    def impl(T):
        return T._len
    return impl


@lower_getattr(TableType, 'shape')
def lower_table_shape(context, builder, typ, val):
    impl = table_shape_overload(typ)
    return context.compile_internal(builder, impl, types.Tuple([types.int64,
        types.int64])(typ), (val,))


def table_shape_overload(T):
    if T.has_runtime_cols:

        def impl(T):
            return T._len, compute_num_runtime_columns(T)
        return impl
    ncols = len(T.arr_types)
    return lambda T: (T._len, types.int64(ncols))


@intrinsic
def compute_num_runtime_columns(typingctx, table_type):
    assert isinstance(table_type, TableType)

    def codegen(context, builder, sig, args):
        table_arg, = args
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        ktvm__mser = context.get_constant(types.int64, 0)
        for i, t in enumerate(table_type.arr_types):
            mpor__cadwk = getattr(table, f'block_{i}')
            ygm__cbp = ListInstance(context, builder, types.List(t),
                mpor__cadwk)
            ktvm__mser = builder.add(ktvm__mser, ygm__cbp.size)
        return ktvm__mser
    sig = types.int64(table_type)
    return sig, codegen


def get_table_data_codegen(context, builder, table_arg, col_ind, table_type):
    arr_type = table_type.arr_types[col_ind]
    table = cgutils.create_struct_proxy(table_type)(context, builder, table_arg
        )
    bxphb__txg = table_type.block_nums[col_ind]
    nue__pxm = table_type.block_offsets[col_ind]
    mpor__cadwk = getattr(table, f'block_{bxphb__txg}')
    nvg__izf = types.none(table_type, types.List(arr_type), types.int64,
        types.int64)
    lmhr__vewj = context.get_constant(types.int64, col_ind)
    zgk__whinw = context.get_constant(types.int64, nue__pxm)
    yahaj__xgrqd = table_arg, mpor__cadwk, zgk__whinw, lmhr__vewj
    ensure_column_unboxed_codegen(context, builder, nvg__izf, yahaj__xgrqd)
    ygm__cbp = ListInstance(context, builder, types.List(arr_type), mpor__cadwk
        )
    arr = ygm__cbp.getitem(nue__pxm)
    return arr


@intrinsic
def get_table_data(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType)
    assert is_overload_constant_int(ind_typ)
    col_ind = get_overload_const_int(ind_typ)
    arr_type = table_type.arr_types[col_ind]

    def codegen(context, builder, sig, args):
        table_arg, zzp__lock = args
        arr = get_table_data_codegen(context, builder, table_arg, col_ind,
            table_type)
        return impl_ret_borrowed(context, builder, arr_type, arr)
    sig = arr_type(table_type, ind_typ)
    return sig, codegen


@intrinsic
def del_column(typingctx, table_type, ind_typ):
    assert isinstance(table_type, TableType
        ), 'Can only delete columns from a table'
    assert isinstance(ind_typ, types.TypeRef) and isinstance(ind_typ.
        instance_type, MetaType), 'ind_typ must be a typeref for a meta type'
    gpqyp__fhxaq = list(ind_typ.instance_type.meta)
    ttk__mtkq = defaultdict(list)
    for ind in gpqyp__fhxaq:
        ttk__mtkq[table_type.block_nums[ind]].append(table_type.
            block_offsets[ind])

    def codegen(context, builder, sig, args):
        table_arg, zzp__lock = args
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        for bxphb__txg, jqp__wqy in ttk__mtkq.items():
            arr_type = table_type.blk_to_type[bxphb__txg]
            mpor__cadwk = getattr(table, f'block_{bxphb__txg}')
            ygm__cbp = ListInstance(context, builder, types.List(arr_type),
                mpor__cadwk)
            qmuj__pbazu = context.get_constant_null(arr_type)
            if len(jqp__wqy) == 1:
                nue__pxm = jqp__wqy[0]
                arr = ygm__cbp.getitem(nue__pxm)
                context.nrt.decref(builder, arr_type, arr)
                ygm__cbp.inititem(nue__pxm, qmuj__pbazu, incref=False)
            else:
                erv__sslk = context.get_constant(types.int64, len(jqp__wqy))
                arr__opgr = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(jqp__wqy, dtype=np
                    .int64))
                kspn__cfn = context.make_array(types.Array(types.int64, 1, 'C')
                    )(context, builder, arr__opgr)
                with cgutils.for_range(builder, erv__sslk) as ghjvh__uxel:
                    i = ghjvh__uxel.index
                    nue__pxm = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        kspn__cfn, i)
                    arr = ygm__cbp.getitem(nue__pxm)
                    context.nrt.decref(builder, arr_type, arr)
                    ygm__cbp.inititem(nue__pxm, qmuj__pbazu, incref=False)
    sig = types.void(table_type, ind_typ)
    return sig, codegen


def set_table_data_codegen(context, builder, in_table_type, in_table,
    out_table_type, arr_type, arr_arg, col_ind, is_new_col):
    in_table = cgutils.create_struct_proxy(in_table_type)(context, builder,
        in_table)
    out_table = cgutils.create_struct_proxy(out_table_type)(context, builder)
    out_table.len = in_table.len
    out_table.parent = in_table.parent
    tll__bkc = context.get_constant(types.int64, 0)
    lwzf__wsp = context.get_constant(types.int64, 1)
    dceo__byifp = arr_type not in in_table_type.type_to_blk
    for t, bxphb__txg in out_table_type.type_to_blk.items():
        if t in in_table_type.type_to_blk:
            tqwe__nxk = in_table_type.type_to_blk[t]
            zso__lau = ListInstance(context, builder, types.List(t),
                getattr(in_table, f'block_{tqwe__nxk}'))
            context.nrt.incref(builder, types.List(t), zso__lau.value)
            setattr(out_table, f'block_{bxphb__txg}', zso__lau.value)
    if dceo__byifp:
        zzp__lock, zso__lau = ListInstance.allocate_ex(context, builder,
            types.List(arr_type), lwzf__wsp)
        zso__lau.size = lwzf__wsp
        zso__lau.inititem(tll__bkc, arr_arg, incref=True)
        bxphb__txg = out_table_type.type_to_blk[arr_type]
        setattr(out_table, f'block_{bxphb__txg}', zso__lau.value)
        if not is_new_col:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
    else:
        bxphb__txg = out_table_type.type_to_blk[arr_type]
        zso__lau = ListInstance(context, builder, types.List(arr_type),
            getattr(out_table, f'block_{bxphb__txg}'))
        if is_new_col:
            n = zso__lau.size
            fywt__ssi = builder.add(n, lwzf__wsp)
            zso__lau.resize(fywt__ssi)
            zso__lau.inititem(n, arr_arg, incref=True)
        elif arr_type == in_table_type.arr_types[col_ind]:
            qyqi__ixd = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            zso__lau.setitem(qyqi__ixd, arr_arg, incref=True)
        else:
            _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
                context, builder)
            qyqi__ixd = context.get_constant(types.int64, out_table_type.
                block_offsets[col_ind])
            n = zso__lau.size
            fywt__ssi = builder.add(n, lwzf__wsp)
            zso__lau.resize(fywt__ssi)
            context.nrt.incref(builder, arr_type, zso__lau.getitem(qyqi__ixd))
            zso__lau.move(builder.add(qyqi__ixd, lwzf__wsp), qyqi__ixd,
                builder.sub(n, qyqi__ixd))
            zso__lau.setitem(qyqi__ixd, arr_arg, incref=True)
    return out_table._getvalue()


def _rm_old_array(col_ind, out_table_type, out_table, in_table_type,
    context, builder):
    hhl__ixy = in_table_type.arr_types[col_ind]
    if hhl__ixy in out_table_type.type_to_blk:
        bxphb__txg = out_table_type.type_to_blk[hhl__ixy]
        qptn__wmy = getattr(out_table, f'block_{bxphb__txg}')
        jeywp__mehg = types.List(hhl__ixy)
        qyqi__ixd = context.get_constant(types.int64, in_table_type.
            block_offsets[col_ind])
        fqvmo__gwa = jeywp__mehg.dtype(jeywp__mehg, types.intp)
        etxp__edcph = context.compile_internal(builder, lambda lst, i: lst.
            pop(i), fqvmo__gwa, (qptn__wmy, qyqi__ixd))
        context.nrt.decref(builder, hhl__ixy, etxp__edcph)


def generate_set_table_data_code(table, ind, arr_type, used_cols, is_null=False
    ):
    ilt__kza = list(table.arr_types)
    if ind == len(ilt__kza):
        bhjsl__pfcph = None
        ilt__kza.append(arr_type)
    else:
        bhjsl__pfcph = table.arr_types[ind]
        ilt__kza[ind] = arr_type
    gryfc__mdcdh = TableType(tuple(ilt__kza))
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'set_table_block': set_table_block, 'set_table_len': set_table_len,
        'set_table_parent': set_table_parent, 'alloc_list_like':
        alloc_list_like, 'out_table_typ': gryfc__mdcdh}
    wtpkb__eac = 'def set_table_data(table, ind, arr, used_cols=None):\n'
    wtpkb__eac += f'  T2 = init_table(out_table_typ, False)\n'
    wtpkb__eac += f'  T2 = set_table_len(T2, len(table))\n'
    wtpkb__eac += f'  T2 = set_table_parent(T2, table)\n'
    for typ, bxphb__txg in gryfc__mdcdh.type_to_blk.items():
        if typ in table.type_to_blk:
            glp__fkwqm = table.type_to_blk[typ]
            wtpkb__eac += (
                f'  arr_list_{bxphb__txg} = get_table_block(table, {glp__fkwqm})\n'
                )
            wtpkb__eac += f"""  out_arr_list_{bxphb__txg} = alloc_list_like(arr_list_{bxphb__txg}, {len(gryfc__mdcdh.block_to_arr_ind[bxphb__txg])}, False)
"""
            if used_cols is None or set(table.block_to_arr_ind[glp__fkwqm]
                ) & used_cols:
                wtpkb__eac += (
                    f'  for i in range(len(arr_list_{bxphb__txg})):\n')
                if typ not in (bhjsl__pfcph, arr_type):
                    wtpkb__eac += (
                        f'    out_arr_list_{bxphb__txg}[i] = arr_list_{bxphb__txg}[i]\n'
                        )
                else:
                    ljp__begj = table.block_to_arr_ind[glp__fkwqm]
                    mvt__wen = np.empty(len(ljp__begj), np.int64)
                    vlotq__hmysl = False
                    for tcoop__rms, nkj__jnvhc in enumerate(ljp__begj):
                        if nkj__jnvhc != ind:
                            mkhu__qxzlm = gryfc__mdcdh.block_offsets[nkj__jnvhc
                                ]
                        else:
                            mkhu__qxzlm = -1
                            vlotq__hmysl = True
                        mvt__wen[tcoop__rms] = mkhu__qxzlm
                    glbls[f'out_idxs_{bxphb__txg}'] = np.array(mvt__wen, np
                        .int64)
                    wtpkb__eac += f'    out_idx = out_idxs_{bxphb__txg}[i]\n'
                    if vlotq__hmysl:
                        wtpkb__eac += f'    if out_idx == -1:\n'
                        wtpkb__eac += f'      continue\n'
                    wtpkb__eac += f"""    out_arr_list_{bxphb__txg}[out_idx] = arr_list_{bxphb__txg}[i]
"""
            if typ == arr_type and not is_null:
                wtpkb__eac += f"""  out_arr_list_{bxphb__txg}[{gryfc__mdcdh.block_offsets[ind]}] = arr
"""
        else:
            glbls[f'arr_list_typ_{bxphb__txg}'] = types.List(arr_type)
            wtpkb__eac += f"""  out_arr_list_{bxphb__txg} = alloc_list_like(arr_list_typ_{bxphb__txg}, 1, False)
"""
            if not is_null:
                wtpkb__eac += f'  out_arr_list_{bxphb__txg}[0] = arr\n'
        wtpkb__eac += (
            f'  T2 = set_table_block(T2, out_arr_list_{bxphb__txg}, {bxphb__txg})\n'
            )
    wtpkb__eac += f'  return T2\n'
    ziupv__lovo = {}
    exec(wtpkb__eac, glbls, ziupv__lovo)
    return ziupv__lovo['set_table_data']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data(table, ind, arr, used_cols=None):
    if is_overload_none(used_cols):
        cgcuz__zdy = None
    else:
        cgcuz__zdy = set(used_cols.instance_type.meta)
    julfu__odlp = get_overload_const_int(ind)
    return generate_set_table_data_code(table, julfu__odlp, arr, cgcuz__zdy)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def set_table_data_null(table, ind, arr, used_cols=None):
    julfu__odlp = get_overload_const_int(ind)
    arr_type = arr.instance_type
    if is_overload_none(used_cols):
        cgcuz__zdy = None
    else:
        cgcuz__zdy = set(used_cols.instance_type.meta)
    return generate_set_table_data_code(table, julfu__odlp, arr_type,
        cgcuz__zdy, is_null=True)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_table_data',
    'bodo.hiframes.table'] = alias_ext_dummy_func


def get_table_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    luvhv__nyh = args[0]
    if equiv_set.has_shape(luvhv__nyh):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            luvhv__nyh)[0], pre=[])


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_get_table_data = (
    get_table_data_equiv)


@lower_constant(TableType)
def lower_constant_table(context, builder, table_type, pyval):
    lsb__twi = []
    for t, bxphb__txg in table_type.type_to_blk.items():
        nfwk__pbl = len(table_type.block_to_arr_ind[bxphb__txg])
        kkpom__bghv = []
        for i in range(nfwk__pbl):
            nkj__jnvhc = table_type.block_to_arr_ind[bxphb__txg][i]
            kkpom__bghv.append(pyval.arrays[nkj__jnvhc])
        lsb__twi.append(context.get_constant_generic(builder, types.List(t),
            kkpom__bghv))
    hgmj__lijv = context.get_constant_null(types.pyobject)
    svwxe__son = context.get_constant(types.int64, 0 if len(pyval.arrays) ==
        0 else len(pyval.arrays[0]))
    return lir.Constant.literal_struct(lsb__twi + [hgmj__lijv, svwxe__son])


def get_init_table_output_type(table_type, to_str_if_dict_t):
    out_table_type = table_type.instance_type if isinstance(table_type,
        types.TypeRef) else table_type
    assert isinstance(out_table_type, TableType
        ), 'table type or typeref expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    if is_overload_true(to_str_if_dict_t):
        out_table_type = to_str_arr_if_dict_array(out_table_type)
    return out_table_type


@intrinsic
def init_table(typingctx, table_type, to_str_if_dict_t):
    out_table_type = get_init_table_output_type(table_type, to_str_if_dict_t)

    def codegen(context, builder, sig, args):
        table = cgutils.create_struct_proxy(out_table_type)(context, builder)
        for t, bxphb__txg in out_table_type.type_to_blk.items():
            tmev__hoqw = context.get_constant_null(types.List(t))
            setattr(table, f'block_{bxphb__txg}', tmev__hoqw)
        return table._getvalue()
    sig = out_table_type(table_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def init_table_from_lists(typingctx, tuple_of_lists_type, table_type):
    assert isinstance(tuple_of_lists_type, types.BaseTuple
        ), 'Tuple of data expected'
    ban__vzq = {}
    for i, typ in enumerate(tuple_of_lists_type):
        assert isinstance(typ, types.List), 'Each tuple element must be a list'
        ban__vzq[typ.dtype] = i
    xvm__zupk = table_type.instance_type if isinstance(table_type, types.
        TypeRef) else table_type
    assert isinstance(xvm__zupk, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        lsila__nlyya, zzp__lock = args
        table = cgutils.create_struct_proxy(xvm__zupk)(context, builder)
        for t, bxphb__txg in xvm__zupk.type_to_blk.items():
            idx = ban__vzq[t]
            xyo__yzv = signature(types.List(t), tuple_of_lists_type, types.
                literal(idx))
            hsv__sjkm = lsila__nlyya, idx
            prn__rnfyz = numba.cpython.tupleobj.static_getitem_tuple(context,
                builder, xyo__yzv, hsv__sjkm)
            setattr(table, f'block_{bxphb__txg}', prn__rnfyz)
        return table._getvalue()
    sig = xvm__zupk(tuple_of_lists_type, table_type)
    return sig, codegen


@intrinsic
def get_table_block(typingctx, table_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert is_overload_constant_int(blk_type)
    bxphb__txg = get_overload_const_int(blk_type)
    arr_type = None
    for t, uubh__fslk in table_type.type_to_blk.items():
        if uubh__fslk == bxphb__txg:
            arr_type = t
            break
    assert arr_type is not None, 'invalid table type block'
    wlul__smaul = types.List(arr_type)

    def codegen(context, builder, sig, args):
        table = cgutils.create_struct_proxy(table_type)(context, builder,
            args[0])
        mpor__cadwk = getattr(table, f'block_{bxphb__txg}')
        return impl_ret_borrowed(context, builder, wlul__smaul, mpor__cadwk)
    sig = wlul__smaul(table_type, blk_type)
    return sig, codegen


@intrinsic
def ensure_table_unboxed(typingctx, table_type, used_cols_typ):

    def codegen(context, builder, sig, args):
        table_arg, fjvtm__sfp = args
        mtcih__mnb = context.get_python_api(builder)
        ipdsp__cvku = used_cols_typ == types.none
        if not ipdsp__cvku:
            eolbi__dosky = numba.cpython.setobj.SetInstance(context,
                builder, types.Set(types.int64), fjvtm__sfp)
        table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
            table_arg)
        for t, bxphb__txg in table_type.type_to_blk.items():
            erv__sslk = context.get_constant(types.int64, len(table_type.
                block_to_arr_ind[bxphb__txg]))
            cjav__ddlaj = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(table_type.block_to_arr_ind[
                bxphb__txg], dtype=np.int64))
            adsk__kdjx = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, cjav__ddlaj)
            mpor__cadwk = getattr(table, f'block_{bxphb__txg}')
            with cgutils.for_range(builder, erv__sslk) as ghjvh__uxel:
                i = ghjvh__uxel.index
                nkj__jnvhc = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    adsk__kdjx, i)
                nvg__izf = types.none(table_type, types.List(t), types.
                    int64, types.int64)
                yahaj__xgrqd = table_arg, mpor__cadwk, i, nkj__jnvhc
                if ipdsp__cvku:
                    ensure_column_unboxed_codegen(context, builder,
                        nvg__izf, yahaj__xgrqd)
                else:
                    fhb__nmnku = eolbi__dosky.contains(nkj__jnvhc)
                    with builder.if_then(fhb__nmnku):
                        ensure_column_unboxed_codegen(context, builder,
                            nvg__izf, yahaj__xgrqd)
    assert isinstance(table_type, TableType), 'table type expected'
    sig = types.none(table_type, used_cols_typ)
    return sig, codegen


@intrinsic
def ensure_column_unboxed(typingctx, table_type, arr_list_t, ind_t, arr_ind_t):
    assert isinstance(table_type, TableType), 'table type expected'
    sig = types.none(table_type, arr_list_t, ind_t, arr_ind_t)
    return sig, ensure_column_unboxed_codegen


def ensure_column_unboxed_codegen(context, builder, sig, args):
    from bodo.hiframes.boxing import get_df_obj_column_codegen
    table_arg, orcd__iyx, sbahz__vdasz, livkd__dmj = args
    mtcih__mnb = context.get_python_api(builder)
    table = cgutils.create_struct_proxy(sig.args[0])(context, builder,
        table_arg)
    bvp__nnu = cgutils.is_not_null(builder, table.parent)
    ygm__cbp = ListInstance(context, builder, sig.args[1], orcd__iyx)
    uzv__spghi = ygm__cbp.getitem(sbahz__vdasz)
    ysuua__wlcp = cgutils.alloca_once_value(builder, uzv__spghi)
    xdq__sqta = cgutils.alloca_once_value(builder, context.
        get_constant_null(sig.args[1].dtype))
    is_null = is_ll_eq(builder, ysuua__wlcp, xdq__sqta)
    with builder.if_then(is_null):
        with builder.if_else(bvp__nnu) as (zes__ahf, oud__mxmp):
            with zes__ahf:
                lrzf__opik = get_df_obj_column_codegen(context, builder,
                    mtcih__mnb, table.parent, livkd__dmj, sig.args[1].dtype)
                arr = mtcih__mnb.to_native_value(sig.args[1].dtype, lrzf__opik
                    ).value
                ygm__cbp.inititem(sbahz__vdasz, arr, incref=False)
                mtcih__mnb.decref(lrzf__opik)
            with oud__mxmp:
                context.call_conv.return_user_exc(builder, BodoError, (
                    'unexpected null table column',))


@intrinsic
def set_table_block(typingctx, table_type, arr_list_type, blk_type):
    assert isinstance(table_type, TableType), 'table type expected'
    assert isinstance(arr_list_type, types.List), 'list type expected'
    assert is_overload_constant_int(blk_type), 'blk should be const int'
    bxphb__txg = get_overload_const_int(blk_type)

    def codegen(context, builder, sig, args):
        table_arg, ags__afrhb, zzp__lock = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        setattr(in_table, f'block_{bxphb__txg}', ags__afrhb)
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, arr_list_type, blk_type)
    return sig, codegen


@intrinsic
def set_table_len(typingctx, table_type, l_type):
    assert isinstance(table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        table_arg, hni__fiql = args
        in_table = cgutils.create_struct_proxy(table_type)(context, builder,
            table_arg)
        in_table.len = hni__fiql
        return impl_ret_borrowed(context, builder, table_type, in_table.
            _getvalue())
    sig = table_type(table_type, l_type)
    return sig, codegen


@intrinsic
def set_table_parent(typingctx, out_table_type, in_table_type):
    assert isinstance(in_table_type, TableType), 'table type expected'
    assert isinstance(out_table_type, TableType), 'table type expected'

    def codegen(context, builder, sig, args):
        kufx__git, aeip__dhois = args
        in_table = cgutils.create_struct_proxy(in_table_type)(context,
            builder, aeip__dhois)
        out_table = cgutils.create_struct_proxy(out_table_type)(context,
            builder, kufx__git)
        out_table.parent = in_table.parent
        context.nrt.incref(builder, types.pyobject, out_table.parent)
        return impl_ret_borrowed(context, builder, out_table_type,
            out_table._getvalue())
    sig = out_table_type(out_table_type, in_table_type)
    return sig, codegen


@intrinsic
def alloc_list_like(typingctx, list_type, len_type, to_str_if_dict_t):
    wlul__smaul = list_type.instance_type if isinstance(list_type, types.
        TypeRef) else list_type
    assert isinstance(wlul__smaul, types.List), 'list type or typeref expected'
    assert isinstance(len_type, types.Integer), 'integer type expected'
    assert is_overload_constant_bool(to_str_if_dict_t
        ), 'constant to_str_if_dict_t expected'
    if is_overload_true(to_str_if_dict_t):
        wlul__smaul = types.List(to_str_arr_if_dict_array(wlul__smaul.dtype))

    def codegen(context, builder, sig, args):
        kvp__nkjg = args[1]
        zzp__lock, zso__lau = ListInstance.allocate_ex(context, builder,
            wlul__smaul, kvp__nkjg)
        zso__lau.size = kvp__nkjg
        return zso__lau.value
    sig = wlul__smaul(list_type, len_type, to_str_if_dict_t)
    return sig, codegen


@intrinsic
def alloc_empty_list_type(typingctx, size_typ, data_typ):
    assert isinstance(size_typ, types.Integer), 'Size must be an integer'
    qofb__bdni = data_typ.instance_type if isinstance(data_typ, types.TypeRef
        ) else data_typ
    list_type = types.List(qofb__bdni)

    def codegen(context, builder, sig, args):
        kvp__nkjg, zzp__lock = args
        zzp__lock, zso__lau = ListInstance.allocate_ex(context, builder,
            list_type, kvp__nkjg)
        zso__lau.size = kvp__nkjg
        return zso__lau.value
    sig = list_type(size_typ, data_typ)
    return sig, codegen


def _get_idx_length(idx):
    pass


@overload(_get_idx_length)
def overload_get_idx_length(idx, n):
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        return lambda idx, n: idx.sum()
    assert isinstance(idx, types.SliceType), 'slice index expected'

    def impl(idx, n):
        fxd__odcp = numba.cpython.unicode._normalize_slice(idx, n)
        return numba.cpython.unicode._slice_span(fxd__odcp)
    return impl


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_filter(T, idx, used_cols=None):
    from bodo.utils.conversion import ensure_contig_if_np
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'set_table_block':
        set_table_block, 'set_table_len': set_table_len, 'alloc_list_like':
        alloc_list_like, '_get_idx_length': _get_idx_length,
        'ensure_contig_if_np': ensure_contig_if_np}
    if not is_overload_none(used_cols):
        igltz__tkw = used_cols.instance_type
        ixb__mlx = np.array(igltz__tkw.meta, dtype=np.int64)
        glbls['used_cols_vals'] = ixb__mlx
        tpjd__kftn = set([T.block_nums[i] for i in ixb__mlx])
    else:
        ixb__mlx = None
    wtpkb__eac = 'def table_filter_func(T, idx, used_cols=None):\n'
    wtpkb__eac += f'  T2 = init_table(T, False)\n'
    wtpkb__eac += f'  l = 0\n'
    if ixb__mlx is not None and len(ixb__mlx) == 0:
        wtpkb__eac += f'  l = _get_idx_length(idx, len(T))\n'
        wtpkb__eac += f'  T2 = set_table_len(T2, l)\n'
        wtpkb__eac += f'  return T2\n'
        ziupv__lovo = {}
        exec(wtpkb__eac, glbls, ziupv__lovo)
        return ziupv__lovo['table_filter_func']
    if ixb__mlx is not None:
        wtpkb__eac += f'  used_set = set(used_cols_vals)\n'
    for bxphb__txg in T.type_to_blk.values():
        wtpkb__eac += (
            f'  arr_list_{bxphb__txg} = get_table_block(T, {bxphb__txg})\n')
        wtpkb__eac += f"""  out_arr_list_{bxphb__txg} = alloc_list_like(arr_list_{bxphb__txg}, len(arr_list_{bxphb__txg}), False)
"""
        if ixb__mlx is None or bxphb__txg in tpjd__kftn:
            glbls[f'arr_inds_{bxphb__txg}'] = np.array(T.block_to_arr_ind[
                bxphb__txg], dtype=np.int64)
            wtpkb__eac += f'  for i in range(len(arr_list_{bxphb__txg})):\n'
            wtpkb__eac += (
                f'    arr_ind_{bxphb__txg} = arr_inds_{bxphb__txg}[i]\n')
            if ixb__mlx is not None:
                wtpkb__eac += (
                    f'    if arr_ind_{bxphb__txg} not in used_set: continue\n')
            wtpkb__eac += f"""    ensure_column_unboxed(T, arr_list_{bxphb__txg}, i, arr_ind_{bxphb__txg})
"""
            wtpkb__eac += f"""    out_arr_{bxphb__txg} = ensure_contig_if_np(arr_list_{bxphb__txg}[i][idx])
"""
            wtpkb__eac += f'    l = len(out_arr_{bxphb__txg})\n'
            wtpkb__eac += (
                f'    out_arr_list_{bxphb__txg}[i] = out_arr_{bxphb__txg}\n')
        wtpkb__eac += (
            f'  T2 = set_table_block(T2, out_arr_list_{bxphb__txg}, {bxphb__txg})\n'
            )
    wtpkb__eac += f'  T2 = set_table_len(T2, l)\n'
    wtpkb__eac += f'  return T2\n'
    ziupv__lovo = {}
    exec(wtpkb__eac, glbls, ziupv__lovo)
    return ziupv__lovo['table_filter_func']


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def table_subset(T, idx, copy_arrs, used_cols=None):
    hfn__swwwn = list(idx.instance_type.meta)
    ilt__kza = tuple(np.array(T.arr_types, dtype=object)[hfn__swwwn])
    gryfc__mdcdh = TableType(ilt__kza)
    if not is_overload_constant_bool(copy_arrs):
        raise_bodo_error('table_subset(): copy_arrs must be a constant')
    xbmnd__aoy = is_overload_true(copy_arrs)
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'set_table_block':
        set_table_block, 'set_table_len': set_table_len, 'alloc_list_like':
        alloc_list_like, 'out_table_typ': gryfc__mdcdh}
    if not is_overload_none(used_cols):
        kept_cols = used_cols.instance_type.meta
        yvrmr__omv = set(kept_cols)
        glbls['kept_cols'] = np.array(kept_cols, np.int64)
        uixjd__sstf = True
    else:
        uixjd__sstf = False
    yuz__xmi = {i: c for i, c in enumerate(hfn__swwwn)}
    wtpkb__eac = 'def table_subset(T, idx, copy_arrs, used_cols=None):\n'
    wtpkb__eac += f'  T2 = init_table(out_table_typ, False)\n'
    wtpkb__eac += f'  T2 = set_table_len(T2, len(T))\n'
    if uixjd__sstf and len(yvrmr__omv) == 0:
        wtpkb__eac += f'  return T2\n'
        ziupv__lovo = {}
        exec(wtpkb__eac, glbls, ziupv__lovo)
        return ziupv__lovo['table_subset']
    if uixjd__sstf:
        wtpkb__eac += f'  kept_cols_set = set(kept_cols)\n'
    for typ, bxphb__txg in gryfc__mdcdh.type_to_blk.items():
        glp__fkwqm = T.type_to_blk[typ]
        wtpkb__eac += (
            f'  arr_list_{bxphb__txg} = get_table_block(T, {glp__fkwqm})\n')
        wtpkb__eac += f"""  out_arr_list_{bxphb__txg} = alloc_list_like(arr_list_{bxphb__txg}, {len(gryfc__mdcdh.block_to_arr_ind[bxphb__txg])}, False)
"""
        bttx__zrex = True
        if uixjd__sstf:
            gne__pntcg = set(gryfc__mdcdh.block_to_arr_ind[bxphb__txg])
            gkbff__gjr = gne__pntcg & yvrmr__omv
            bttx__zrex = len(gkbff__gjr) > 0
        if bttx__zrex:
            glbls[f'out_arr_inds_{bxphb__txg}'] = np.array(gryfc__mdcdh.
                block_to_arr_ind[bxphb__txg], dtype=np.int64)
            wtpkb__eac += (
                f'  for i in range(len(out_arr_list_{bxphb__txg})):\n')
            wtpkb__eac += (
                f'    out_arr_ind_{bxphb__txg} = out_arr_inds_{bxphb__txg}[i]\n'
                )
            if uixjd__sstf:
                wtpkb__eac += (
                    f'    if out_arr_ind_{bxphb__txg} not in kept_cols_set: continue\n'
                    )
            pqd__jorzo = []
            xijzc__fjyob = []
            for vpp__audk in gryfc__mdcdh.block_to_arr_ind[bxphb__txg]:
                ltxty__ijeqs = yuz__xmi[vpp__audk]
                pqd__jorzo.append(ltxty__ijeqs)
                zfqcy__mke = T.block_offsets[ltxty__ijeqs]
                xijzc__fjyob.append(zfqcy__mke)
            glbls[f'in_logical_idx_{bxphb__txg}'] = np.array(pqd__jorzo,
                dtype=np.int64)
            glbls[f'in_physical_idx_{bxphb__txg}'] = np.array(xijzc__fjyob,
                dtype=np.int64)
            wtpkb__eac += (
                f'    logical_idx_{bxphb__txg} = in_logical_idx_{bxphb__txg}[i]\n'
                )
            wtpkb__eac += (
                f'    physical_idx_{bxphb__txg} = in_physical_idx_{bxphb__txg}[i]\n'
                )
            wtpkb__eac += f"""    ensure_column_unboxed(T, arr_list_{bxphb__txg}, physical_idx_{bxphb__txg}, logical_idx_{bxphb__txg})
"""
            xaaha__hxxtr = '.copy()' if xbmnd__aoy else ''
            wtpkb__eac += f"""    out_arr_list_{bxphb__txg}[i] = arr_list_{bxphb__txg}[physical_idx_{bxphb__txg}]{xaaha__hxxtr}
"""
        wtpkb__eac += (
            f'  T2 = set_table_block(T2, out_arr_list_{bxphb__txg}, {bxphb__txg})\n'
            )
    wtpkb__eac += f'  return T2\n'
    ziupv__lovo = {}
    exec(wtpkb__eac, glbls, ziupv__lovo)
    return ziupv__lovo['table_subset']


def table_filter_equiv(self, scope, equiv_set, loc, args, kws):
    luvhv__nyh = args[0]
    if equiv_set.has_shape(luvhv__nyh):
        if guard(is_whole_slice, self.typemap, self.func_ir, args[1]):
            return ArrayAnalysis.AnalyzeResult(shape=luvhv__nyh, pre=[])
        return ArrayAnalysis.AnalyzeResult(shape=(None, equiv_set.get_shape
            (luvhv__nyh)[1]), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_filter = (
    table_filter_equiv)


def table_subset_equiv(self, scope, equiv_set, loc, args, kws):
    luvhv__nyh = args[0]
    if equiv_set.has_shape(luvhv__nyh):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            luvhv__nyh)[0], None), pre=[])
    return None


ArrayAnalysis._analyze_op_call_bodo_hiframes_table_table_subset = (
    table_subset_equiv)


def gen_str_and_dict_enc_cols_to_one_block_fn_txt(in_table_type,
    out_table_type, glbls, is_gatherv=False):
    assert bodo.string_array_type in in_table_type.type_to_blk and bodo.string_array_type in in_table_type.type_to_blk, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: Table type {in_table_type} does not contain both a string, and encoded string column'
    nkbj__lufe = in_table_type.type_to_blk[bodo.string_array_type]
    twwzp__lyg = in_table_type.type_to_blk[bodo.dict_str_arr_type]
    efvr__tvfj = in_table_type.block_to_arr_ind.get(nkbj__lufe)
    bmr__apls = in_table_type.block_to_arr_ind.get(twwzp__lyg)
    whrrc__ndz = []
    kopfc__wwl = []
    swbfb__jtucb = 0
    juv__oplxz = 0
    for gxux__eze in range(len(efvr__tvfj) + len(bmr__apls)):
        if swbfb__jtucb == len(efvr__tvfj):
            kopfc__wwl.append(gxux__eze)
            continue
        elif juv__oplxz == len(bmr__apls):
            whrrc__ndz.append(gxux__eze)
            continue
        zrzhf__jkcey = efvr__tvfj[swbfb__jtucb]
        kvan__abbs = bmr__apls[juv__oplxz]
        if zrzhf__jkcey < kvan__abbs:
            whrrc__ndz.append(gxux__eze)
            swbfb__jtucb += 1
        else:
            kopfc__wwl.append(gxux__eze)
            juv__oplxz += 1
    assert 'output_table_str_arr_offsets_in_combined_block' not in glbls, "Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: key 'output_table_str_arr_idxs_in_combined_block' already present as a global variable"
    glbls['output_table_str_arr_offsets_in_combined_block'] = np.array(
        whrrc__ndz)
    assert 'output_table_dict_enc_str_arr_offsets_in_combined_block' not in glbls, "Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: key 'output_table_str_arr_idxs_in_combined_block' already present as a global variable"
    glbls['output_table_dict_enc_str_arr_offsets_in_combined_block'
        ] = np.array(kopfc__wwl)
    glbls['decode_if_dict_array'] = decode_if_dict_array
    zvsx__fpwlh = out_table_type.type_to_blk[bodo.string_array_type]
    assert f'arr_inds_{nkbj__lufe}' not in glbls, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: arr_inds_{nkbj__lufe} already present in global variables'
    glbls[f'arr_inds_{nkbj__lufe}'] = np.array(in_table_type.
        block_to_arr_ind[nkbj__lufe], dtype=np.int64)
    assert f'arr_inds_{twwzp__lyg}' not in glbls, f'Error in gen_str_and_dict_enc_cols_to_one_block_fn_txt: arr_inds_{twwzp__lyg} already present in global variables'
    glbls[f'arr_inds_{twwzp__lyg}'] = np.array(in_table_type.
        block_to_arr_ind[twwzp__lyg], dtype=np.int64)
    wtpkb__eac = f'  input_str_arr_list = get_table_block(T, {nkbj__lufe})\n'
    wtpkb__eac += (
        f'  input_dict_enc_str_arr_list = get_table_block(T, {twwzp__lyg})\n')
    wtpkb__eac += f"""  out_arr_list_{zvsx__fpwlh} = alloc_list_like(input_str_arr_list, {len(whrrc__ndz) + len(kopfc__wwl)}, True)
"""
    wtpkb__eac += f"""  for input_str_ary_idx, output_str_arr_offset in enumerate(output_table_str_arr_offsets_in_combined_block):
"""
    wtpkb__eac += (
        f'    arr_ind_str = arr_inds_{nkbj__lufe}[input_str_ary_idx]\n')
    wtpkb__eac += f"""    ensure_column_unboxed(T, input_str_arr_list, input_str_ary_idx, arr_ind_str)
"""
    wtpkb__eac += f'    out_arr_str = input_str_arr_list[input_str_ary_idx]\n'
    if is_gatherv:
        wtpkb__eac += (
            f'    out_arr_str = bodo.gatherv(out_arr_str, allgather, warn_if_rep, root)\n'
            )
    wtpkb__eac += (
        f'    out_arr_list_{zvsx__fpwlh}[output_str_arr_offset] = out_arr_str\n'
        )
    wtpkb__eac += f"""  for input_dict_enc_str_ary_idx, output_dict_enc_str_arr_offset in enumerate(output_table_dict_enc_str_arr_offsets_in_combined_block):
"""
    wtpkb__eac += (
        f'    arr_ind_dict_enc_str = arr_inds_{twwzp__lyg}[input_dict_enc_str_ary_idx]\n'
        )
    wtpkb__eac += f"""    ensure_column_unboxed(T, input_dict_enc_str_arr_list, input_dict_enc_str_ary_idx, arr_ind_dict_enc_str)
"""
    wtpkb__eac += f"""    out_arr_dict_enc_str = decode_if_dict_array(input_dict_enc_str_arr_list[input_dict_enc_str_ary_idx])
"""
    if is_gatherv:
        wtpkb__eac += f"""    out_arr_dict_enc_str = bodo.gatherv(out_arr_dict_enc_str, allgather, warn_if_rep, root)
"""
    wtpkb__eac += f"""    out_arr_list_{zvsx__fpwlh}[output_dict_enc_str_arr_offset] = out_arr_dict_enc_str
"""
    wtpkb__eac += (
        f'  T2 = set_table_block(T2, out_arr_list_{zvsx__fpwlh}, {zvsx__fpwlh})\n'
        )
    return wtpkb__eac


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def decode_if_dict_table(T):
    wtpkb__eac = 'def impl(T):\n'
    wtpkb__eac += f'  T2 = init_table(T, True)\n'
    wtpkb__eac += f'  l = len(T)\n'
    glbls = {'init_table': init_table, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'set_table_block':
        set_table_block, 'set_table_len': set_table_len, 'alloc_list_like':
        alloc_list_like, 'decode_if_dict_array': decode_if_dict_array}
    out_table_type = bodo.hiframes.table.get_init_table_output_type(T, True)
    xxxla__omu = (bodo.string_array_type in T.type_to_blk and bodo.
        dict_str_arr_type in T.type_to_blk)
    if xxxla__omu:
        wtpkb__eac += gen_str_and_dict_enc_cols_to_one_block_fn_txt(T,
            out_table_type, glbls)
    for typ, uftqu__vzenn in T.type_to_blk.items():
        if xxxla__omu and typ in (bodo.string_array_type, bodo.
            dict_str_arr_type):
            continue
        if typ == bodo.dict_str_arr_type:
            assert bodo.string_array_type in out_table_type.type_to_blk, 'Error in decode_if_dict_table: If encoded string type is present in the input, then non-encoded string type should be present in the output'
            zgjya__lbtu = out_table_type.type_to_blk[bodo.string_array_type]
        else:
            assert typ in out_table_type.type_to_blk, 'Error in decode_if_dict_table: All non-encoded string types present in the input should be present in the output'
            zgjya__lbtu = out_table_type.type_to_blk[typ]
        glbls[f'arr_inds_{uftqu__vzenn}'] = np.array(T.block_to_arr_ind[
            uftqu__vzenn], dtype=np.int64)
        wtpkb__eac += (
            f'  arr_list_{uftqu__vzenn} = get_table_block(T, {uftqu__vzenn})\n'
            )
        wtpkb__eac += f"""  out_arr_list_{uftqu__vzenn} = alloc_list_like(arr_list_{uftqu__vzenn}, len(arr_list_{uftqu__vzenn}), True)
"""
        wtpkb__eac += f'  for i in range(len(arr_list_{uftqu__vzenn})):\n'
        wtpkb__eac += (
            f'    arr_ind_{uftqu__vzenn} = arr_inds_{uftqu__vzenn}[i]\n')
        wtpkb__eac += f"""    ensure_column_unboxed(T, arr_list_{uftqu__vzenn}, i, arr_ind_{uftqu__vzenn})
"""
        wtpkb__eac += f"""    out_arr_{uftqu__vzenn} = decode_if_dict_array(arr_list_{uftqu__vzenn}[i])
"""
        wtpkb__eac += (
            f'    out_arr_list_{uftqu__vzenn}[i] = out_arr_{uftqu__vzenn}\n')
        wtpkb__eac += (
            f'  T2 = set_table_block(T2, out_arr_list_{uftqu__vzenn}, {zgjya__lbtu})\n'
            )
    wtpkb__eac += f'  T2 = set_table_len(T2, l)\n'
    wtpkb__eac += f'  return T2\n'
    ziupv__lovo = {}
    exec(wtpkb__eac, glbls, ziupv__lovo)
    return ziupv__lovo['impl']


@overload(operator.getitem, no_unliteral=True, inline='always')
def overload_table_getitem(T, idx):
    if not isinstance(T, TableType):
        return
    return lambda T, idx: table_filter(T, idx)


@intrinsic
def init_runtime_table_from_lists(typingctx, arr_list_tup_typ, nrows_typ=None):
    assert isinstance(arr_list_tup_typ, types.BaseTuple
        ), 'init_runtime_table_from_lists requires a tuple of list of arrays'
    if isinstance(arr_list_tup_typ, types.UniTuple):
        if arr_list_tup_typ.dtype.dtype == types.undefined:
            return
        wbzt__tcano = [arr_list_tup_typ.dtype.dtype] * len(arr_list_tup_typ)
    else:
        wbzt__tcano = []
        for typ in arr_list_tup_typ:
            if typ.dtype == types.undefined:
                return
            wbzt__tcano.append(typ.dtype)
    assert isinstance(nrows_typ, types.Integer
        ), 'init_runtime_table_from_lists requires an integer length'

    def codegen(context, builder, sig, args):
        jfdro__zqet, ilte__pfqu = args
        table = cgutils.create_struct_proxy(table_type)(context, builder)
        table.len = ilte__pfqu
        lsb__twi = cgutils.unpack_tuple(builder, jfdro__zqet)
        for i, mpor__cadwk in enumerate(lsb__twi):
            setattr(table, f'block_{i}', mpor__cadwk)
            context.nrt.incref(builder, types.List(wbzt__tcano[i]), mpor__cadwk
                )
        return table._getvalue()
    table_type = TableType(tuple(wbzt__tcano), True)
    sig = table_type(arr_list_tup_typ, nrows_typ)
    return sig, codegen


def _to_arr_if_series(t):
    return t.data if isinstance(t, SeriesType) else t


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def logical_table_to_table(in_table_t, extra_arrs_t, in_col_inds_t,
    n_table_cols_t, out_table_type_t=None, used_cols=None):
    in_col_inds = in_col_inds_t.instance_type.meta
    assert isinstance(in_table_t, (TableType, types.BaseTuple, types.NoneType)
        ), 'logical_table_to_table: input table must be a TableType or tuple of arrays or None (for dead table)'
    glbls = {}
    if not is_overload_none(used_cols):
        kept_cols = set(used_cols.instance_type.meta)
        glbls['kept_cols'] = np.array(list(kept_cols), np.int64)
        uixjd__sstf = True
    else:
        kept_cols = set(np.arange(len(in_col_inds)))
        uixjd__sstf = False
    extra_arrs_no_series = ', '.join(f'get_series_data(extra_arrs_t[{i}])' if
        isinstance(extra_arrs_t[i], SeriesType) else f'extra_arrs_t[{i}]' for
        i in range(len(extra_arrs_t)))
    extra_arrs_no_series = (
        f"({extra_arrs_no_series}{',' if len(extra_arrs_t) == 1 else ''})")
    if isinstance(in_table_t, (types.BaseTuple, types.NoneType)):
        return _logical_tuple_table_to_table_codegen(in_table_t,
            extra_arrs_t, in_col_inds, kept_cols, n_table_cols_t,
            out_table_type_t, extra_arrs_no_series)
    dadie__wqog = len(in_table_t.arr_types)
    out_table_type = TableType(tuple(in_table_t.arr_types[i] if i <
        dadie__wqog else _to_arr_if_series(extra_arrs_t.types[i -
        dadie__wqog]) for i in in_col_inds)) if is_overload_none(
        out_table_type_t) else unwrap_typeref(out_table_type_t)
    glbls.update({'init_table': init_table, 'set_table_len': set_table_len,
        'out_table_type': out_table_type})
    wtpkb__eac = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        wtpkb__eac += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    wtpkb__eac += f'  T1 = in_table_t\n'
    wtpkb__eac += f'  T2 = init_table(out_table_type, False)\n'
    wtpkb__eac += f'  T2 = set_table_len(T2, len(T1))\n'
    if uixjd__sstf and len(kept_cols) == 0:
        wtpkb__eac += f'  return T2\n'
        ziupv__lovo = {}
        exec(wtpkb__eac, glbls, ziupv__lovo)
        return ziupv__lovo['impl']
    if uixjd__sstf:
        wtpkb__eac += f'  kept_cols_set = set(kept_cols)\n'
    for typ, bxphb__txg in out_table_type.type_to_blk.items():
        glbls[f'arr_list_typ_{bxphb__txg}'] = types.List(typ)
        erv__sslk = len(out_table_type.block_to_arr_ind[bxphb__txg])
        wtpkb__eac += f"""  out_arr_list_{bxphb__txg} = alloc_list_like(arr_list_typ_{bxphb__txg}, {erv__sslk}, False)
"""
        if typ in in_table_t.type_to_blk:
            irj__cbohn = in_table_t.type_to_blk[typ]
            knywr__reld = []
            xmoe__yjpi = []
            for pkv__juh in out_table_type.block_to_arr_ind[bxphb__txg]:
                oncbc__rneo = in_col_inds[pkv__juh]
                if oncbc__rneo < dadie__wqog:
                    knywr__reld.append(in_table_t.block_offsets[oncbc__rneo])
                    xmoe__yjpi.append(oncbc__rneo)
                else:
                    knywr__reld.append(-1)
                    xmoe__yjpi.append(-1)
            glbls[f'in_idxs_{bxphb__txg}'] = np.array(knywr__reld, np.int64)
            glbls[f'in_arr_inds_{bxphb__txg}'] = np.array(xmoe__yjpi, np.int64)
            if uixjd__sstf:
                glbls[f'out_arr_inds_{bxphb__txg}'] = np.array(out_table_type
                    .block_to_arr_ind[bxphb__txg], dtype=np.int64)
            wtpkb__eac += (
                f'  in_arr_list_{bxphb__txg} = get_table_block(T1, {irj__cbohn})\n'
                )
            wtpkb__eac += (
                f'  for i in range(len(out_arr_list_{bxphb__txg})):\n')
            wtpkb__eac += (
                f'    in_offset_{bxphb__txg} = in_idxs_{bxphb__txg}[i]\n')
            wtpkb__eac += f'    if in_offset_{bxphb__txg} == -1:\n'
            wtpkb__eac += f'      continue\n'
            wtpkb__eac += (
                f'    in_arr_ind_{bxphb__txg} = in_arr_inds_{bxphb__txg}[i]\n')
            if uixjd__sstf:
                wtpkb__eac += f"""    if out_arr_inds_{bxphb__txg}[i] not in kept_cols_set: continue
"""
            wtpkb__eac += f"""    ensure_column_unboxed(T1, in_arr_list_{bxphb__txg}, in_offset_{bxphb__txg}, in_arr_ind_{bxphb__txg})
"""
            wtpkb__eac += f"""    out_arr_list_{bxphb__txg}[i] = in_arr_list_{bxphb__txg}[in_offset_{bxphb__txg}]
"""
        for i, pkv__juh in enumerate(out_table_type.block_to_arr_ind[
            bxphb__txg]):
            if pkv__juh not in kept_cols:
                continue
            oncbc__rneo = in_col_inds[pkv__juh]
            if oncbc__rneo >= dadie__wqog:
                wtpkb__eac += f"""  out_arr_list_{bxphb__txg}[{i}] = extra_arrs_t[{oncbc__rneo - dadie__wqog}]
"""
        wtpkb__eac += (
            f'  T2 = set_table_block(T2, out_arr_list_{bxphb__txg}, {bxphb__txg})\n'
            )
    wtpkb__eac += f'  return T2\n'
    glbls.update({'alloc_list_like': alloc_list_like, 'set_table_block':
        set_table_block, 'get_table_block': get_table_block,
        'ensure_column_unboxed': ensure_column_unboxed, 'get_series_data':
        bodo.hiframes.pd_series_ext.get_series_data})
    ziupv__lovo = {}
    exec(wtpkb__eac, glbls, ziupv__lovo)
    return ziupv__lovo['impl']


def _logical_tuple_table_to_table_codegen(in_table_t, extra_arrs_t,
    in_col_inds, kept_cols, n_table_cols_t, out_table_type_t,
    extra_arrs_no_series):
    dadie__wqog = get_overload_const_int(n_table_cols_t
        ) if is_overload_constant_int(n_table_cols_t) else len(in_table_t.types
        )
    out_table_type = TableType(tuple(in_table_t.types[i] if i < dadie__wqog
         else _to_arr_if_series(extra_arrs_t.types[i - dadie__wqog]) for i in
        in_col_inds)) if is_overload_none(out_table_type_t
        ) else unwrap_typeref(out_table_type_t)
    cxc__nmr = None
    if not is_overload_none(in_table_t):
        for i, t in enumerate(in_table_t.types):
            if t != types.none:
                cxc__nmr = f'in_table_t[{i}]'
                break
    if cxc__nmr is None:
        for i, t in enumerate(extra_arrs_t.types):
            if t != types.none:
                cxc__nmr = f'extra_arrs_t[{i}]'
                break
    assert cxc__nmr is not None, 'no array found in input data'
    wtpkb__eac = """def impl(in_table_t, extra_arrs_t, in_col_inds_t, n_table_cols_t, out_table_type_t=None, used_cols=None):
"""
    if any(isinstance(t, SeriesType) for t in extra_arrs_t.types):
        wtpkb__eac += f'  extra_arrs_t = {extra_arrs_no_series}\n'
    wtpkb__eac += f'  T1 = in_table_t\n'
    wtpkb__eac += f'  T2 = init_table(out_table_type, False)\n'
    wtpkb__eac += f'  T2 = set_table_len(T2, len({cxc__nmr}))\n'
    glbls = {}
    for typ, bxphb__txg in out_table_type.type_to_blk.items():
        glbls[f'arr_list_typ_{bxphb__txg}'] = types.List(typ)
        erv__sslk = len(out_table_type.block_to_arr_ind[bxphb__txg])
        wtpkb__eac += f"""  out_arr_list_{bxphb__txg} = alloc_list_like(arr_list_typ_{bxphb__txg}, {erv__sslk}, False)
"""
        for i, pkv__juh in enumerate(out_table_type.block_to_arr_ind[
            bxphb__txg]):
            if pkv__juh not in kept_cols:
                continue
            oncbc__rneo = in_col_inds[pkv__juh]
            if oncbc__rneo < dadie__wqog:
                wtpkb__eac += (
                    f'  out_arr_list_{bxphb__txg}[{i}] = T1[{oncbc__rneo}]\n')
            else:
                wtpkb__eac += f"""  out_arr_list_{bxphb__txg}[{i}] = extra_arrs_t[{oncbc__rneo - dadie__wqog}]
"""
        wtpkb__eac += (
            f'  T2 = set_table_block(T2, out_arr_list_{bxphb__txg}, {bxphb__txg})\n'
            )
    wtpkb__eac += f'  return T2\n'
    glbls.update({'init_table': init_table, 'alloc_list_like':
        alloc_list_like, 'set_table_block': set_table_block,
        'set_table_len': set_table_len, 'out_table_type': out_table_type,
        'get_series_data': bodo.hiframes.pd_series_ext.get_series_data})
    ziupv__lovo = {}
    exec(wtpkb__eac, glbls, ziupv__lovo)
    return ziupv__lovo['impl']


def logical_table_to_table_equiv(self, scope, equiv_set, loc, args, kws):
    cmtvl__pka = args[0]
    vpcd__vcqiz = args[1]
    if equiv_set.has_shape(cmtvl__pka):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            cmtvl__pka)[0], None), pre=[])
    if equiv_set.has_shape(vpcd__vcqiz):
        return ArrayAnalysis.AnalyzeResult(shape=(equiv_set.get_shape(
            vpcd__vcqiz)[0], None), pre=[])


(ArrayAnalysis._analyze_op_call_bodo_hiframes_table_logical_table_to_table
    ) = logical_table_to_table_equiv


def alias_ext_logical_table_to_table(lhs_name, args, alias_map, arg_aliases):
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['logical_table_to_table',
    'bodo.hiframes.table'] = alias_ext_logical_table_to_table
