"""
Indexing support for pd.DataFrame type.
"""
import operator
import numpy as np
import pandas as pd
from numba.core import cgutils, types
from numba.core.typing.templates import AbstractTemplate, infer_global
from numba.extending import intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.utils.transform import gen_const_tup
from bodo.utils.typing import BodoError, get_overload_const_int, get_overload_const_list, get_overload_const_str, is_immutable_array, is_list_like_index_type, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, raise_bodo_error


@infer_global(operator.getitem)
class DataFrameGetItemTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        check_runtime_cols_unsupported(args[0], 'DataFrame getitem (df[])')
        if isinstance(args[0], DataFrameType):
            return self.typecheck_df_getitem(args)
        elif isinstance(args[0], DataFrameLocType):
            return self.typecheck_loc_getitem(args)
        else:
            return

    def typecheck_loc_getitem(self, args):
        I = args[0]
        idx = args[1]
        df = I.df_type
        if isinstance(df.columns[0], tuple):
            raise_bodo_error(
                'DataFrame.loc[] getitem (location-based indexing) with multi-indexed columns not supported yet'
                )
        if is_list_like_index_type(idx) and idx.dtype == types.bool_:
            npjx__mydtq = idx
            bor__hbzxj = df.data
            xmvv__fnxe = df.columns
            lqg__bhhn = self.replace_range_with_numeric_idx_if_needed(df,
                npjx__mydtq)
            dlyt__krqi = DataFrameType(bor__hbzxj, lqg__bhhn, xmvv__fnxe,
                is_table_format=df.is_table_format)
            return dlyt__krqi(*args)
        if isinstance(idx, types.BaseTuple) and len(idx) == 2:
            saui__kyfb = idx.types[0]
            vbkh__ovw = idx.types[1]
            if isinstance(saui__kyfb, types.Integer):
                if not isinstance(df.index, bodo.hiframes.pd_index_ext.
                    RangeIndexType):
                    raise_bodo_error(
                        'Dataframe.loc[int, col_ind] getitem only supported for dataframes with RangeIndexes'
                        )
                if is_overload_constant_str(vbkh__ovw):
                    krth__vmndw = get_overload_const_str(vbkh__ovw)
                    if krth__vmndw not in df.columns:
                        raise_bodo_error(
                            'dataframe {} does not include column {}'.
                            format(df, krth__vmndw))
                    ovm__rlxn = df.columns.index(krth__vmndw)
                    return df.data[ovm__rlxn].dtype(*args)
                if isinstance(vbkh__ovw, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                else:
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
                        )
            if is_list_like_index_type(saui__kyfb
                ) and saui__kyfb.dtype == types.bool_ or isinstance(saui__kyfb,
                types.SliceType):
                lqg__bhhn = self.replace_range_with_numeric_idx_if_needed(df,
                    saui__kyfb)
                if is_overload_constant_str(vbkh__ovw):
                    fvvo__fqz = get_overload_const_str(vbkh__ovw)
                    if fvvo__fqz not in df.columns:
                        raise_bodo_error(
                            f'dataframe {df} does not include column {fvvo__fqz}'
                            )
                    ovm__rlxn = df.columns.index(fvvo__fqz)
                    gqzm__oel = df.data[ovm__rlxn]
                    xnadw__aklq = gqzm__oel.dtype
                    laz__mtkk = types.literal(df.columns[ovm__rlxn])
                    dlyt__krqi = bodo.SeriesType(xnadw__aklq, gqzm__oel,
                        lqg__bhhn, laz__mtkk)
                    return dlyt__krqi(*args)
                if isinstance(vbkh__ovw, types.UnicodeType):
                    raise_bodo_error(
                        f'DataFrame.loc[] getitem (location-based indexing) requires constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                        )
                elif is_overload_constant_list(vbkh__ovw):
                    kxtja__iwoul = get_overload_const_list(vbkh__ovw)
                    exa__mysa = types.unliteral(vbkh__ovw)
                    if exa__mysa.dtype == types.bool_:
                        if len(df.columns) != len(kxtja__iwoul):
                            raise_bodo_error(
                                f'dataframe {df} has {len(df.columns)} columns, but boolean array used with DataFrame.loc[] {kxtja__iwoul} has {len(kxtja__iwoul)} values'
                                )
                        knsmv__klm = []
                        jcd__zbs = []
                        for lgdf__oza in range(len(kxtja__iwoul)):
                            if kxtja__iwoul[lgdf__oza]:
                                knsmv__klm.append(df.columns[lgdf__oza])
                                jcd__zbs.append(df.data[lgdf__oza])
                        brrvt__fzpv = tuple()
                        tcqkr__zeea = df.is_table_format and len(knsmv__klm
                            ) > 0 and len(knsmv__klm
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        dlyt__krqi = DataFrameType(tuple(jcd__zbs),
                            lqg__bhhn, tuple(knsmv__klm), is_table_format=
                            tcqkr__zeea)
                        return dlyt__krqi(*args)
                    elif exa__mysa.dtype == bodo.string_type:
                        brrvt__fzpv, jcd__zbs = (
                            get_df_getitem_kept_cols_and_data(df, kxtja__iwoul)
                            )
                        tcqkr__zeea = df.is_table_format and len(kxtja__iwoul
                            ) > 0 and len(kxtja__iwoul
                            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
                        dlyt__krqi = DataFrameType(jcd__zbs, lqg__bhhn,
                            brrvt__fzpv, is_table_format=tcqkr__zeea)
                        return dlyt__krqi(*args)
        raise_bodo_error(
            f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet. If you are trying to select a subset of the columns by passing a list of column names, that list must be a compile time constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def typecheck_df_getitem(self, args):
        df = args[0]
        ind = args[1]
        if is_overload_constant_str(ind) or is_overload_constant_int(ind):
            ind_val = get_overload_const_str(ind) if is_overload_constant_str(
                ind) else get_overload_const_int(ind)
            if isinstance(df.columns[0], tuple):
                knsmv__klm = []
                jcd__zbs = []
                for lgdf__oza, jsn__zahll in enumerate(df.columns):
                    if jsn__zahll[0] != ind_val:
                        continue
                    knsmv__klm.append(jsn__zahll[1] if len(jsn__zahll) == 2
                         else jsn__zahll[1:])
                    jcd__zbs.append(df.data[lgdf__oza])
                gqzm__oel = tuple(jcd__zbs)
                hry__wqwwh = df.index
                pkx__kmu = tuple(knsmv__klm)
                dlyt__krqi = DataFrameType(gqzm__oel, hry__wqwwh, pkx__kmu)
                return dlyt__krqi(*args)
            else:
                if ind_val not in df.columns:
                    raise_bodo_error('dataframe {} does not include column {}'
                        .format(df, ind_val))
                ovm__rlxn = df.columns.index(ind_val)
                gqzm__oel = df.data[ovm__rlxn]
                xnadw__aklq = gqzm__oel.dtype
                hry__wqwwh = df.index
                laz__mtkk = types.literal(df.columns[ovm__rlxn])
                dlyt__krqi = bodo.SeriesType(xnadw__aklq, gqzm__oel,
                    hry__wqwwh, laz__mtkk)
                return dlyt__krqi(*args)
        if isinstance(ind, types.Integer) or isinstance(ind, types.UnicodeType
            ):
            raise_bodo_error(
                'df[] getitem selecting a subset of columns requires providing constant column names. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        if is_list_like_index_type(ind
            ) and ind.dtype == types.bool_ or isinstance(ind, types.SliceType):
            gqzm__oel = df.data
            hry__wqwwh = self.replace_range_with_numeric_idx_if_needed(df, ind)
            pkx__kmu = df.columns
            dlyt__krqi = DataFrameType(gqzm__oel, hry__wqwwh, pkx__kmu,
                is_table_format=df.is_table_format)
            return dlyt__krqi(*args)
        elif is_overload_constant_list(ind):
            kajs__szxr = get_overload_const_list(ind)
            pkx__kmu, gqzm__oel = get_df_getitem_kept_cols_and_data(df,
                kajs__szxr)
            hry__wqwwh = df.index
            tcqkr__zeea = df.is_table_format and len(kajs__szxr) > 0 and len(
                kajs__szxr) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD
            dlyt__krqi = DataFrameType(gqzm__oel, hry__wqwwh, pkx__kmu,
                is_table_format=tcqkr__zeea)
            return dlyt__krqi(*args)
        raise_bodo_error(
            f'df[] getitem using {ind} not supported. If you are trying to select a subset of the columns, you must provide the column names you are selecting as a constant. See https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )

    def replace_range_with_numeric_idx_if_needed(self, df, ind):
        lqg__bhhn = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64,
            df.index.name_typ) if not isinstance(ind, types.SliceType
            ) and isinstance(df.index, bodo.hiframes.pd_index_ext.
            RangeIndexType) else df.index
        return lqg__bhhn


DataFrameGetItemTemplate._no_unliteral = True


def get_df_getitem_kept_cols_and_data(df, cols_to_keep_list):
    for hyo__rwpo in cols_to_keep_list:
        if hyo__rwpo not in df.column_index:
            raise_bodo_error('Column {} not found in dataframe columns {}'.
                format(hyo__rwpo, df.columns))
    pkx__kmu = tuple(cols_to_keep_list)
    gqzm__oel = tuple(df.data[df.column_index[alwng__mwuw]] for alwng__mwuw in
        pkx__kmu)
    return pkx__kmu, gqzm__oel


@lower_builtin(operator.getitem, DataFrameType, types.Any)
def getitem_df_lower(context, builder, sig, args):
    impl = df_getitem_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def df_getitem_overload(df, ind):
    if not isinstance(df, DataFrameType):
        return
    if is_overload_constant_str(ind) or is_overload_constant_int(ind):
        ind_val = get_overload_const_str(ind) if is_overload_constant_str(ind
            ) else get_overload_const_int(ind)
        if isinstance(df.columns[0], tuple):
            knsmv__klm = []
            jcd__zbs = []
            for lgdf__oza, jsn__zahll in enumerate(df.columns):
                if jsn__zahll[0] != ind_val:
                    continue
                knsmv__klm.append(jsn__zahll[1] if len(jsn__zahll) == 2 else
                    jsn__zahll[1:])
                jcd__zbs.append(
                    'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {})'
                    .format(lgdf__oza))
            nzin__xdze = 'def impl(df, ind):\n'
            nregb__vkucq = (
                'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
            return bodo.hiframes.dataframe_impl._gen_init_df(nzin__xdze,
                knsmv__klm, ', '.join(jcd__zbs), nregb__vkucq)
        if ind_val not in df.columns:
            raise_bodo_error('dataframe {} does not include column {}'.
                format(df, ind_val))
        col_no = df.columns.index(ind_val)
        return lambda df, ind: bodo.hiframes.pd_series_ext.init_series(bodo
            .hiframes.pd_dataframe_ext.get_dataframe_data(df, col_no), bodo
            .hiframes.pd_dataframe_ext.get_dataframe_index(df), ind_val)
    if is_overload_constant_list(ind):
        kajs__szxr = get_overload_const_list(ind)
        for hyo__rwpo in kajs__szxr:
            if hyo__rwpo not in df.column_index:
                raise_bodo_error('Column {} not found in dataframe columns {}'
                    .format(hyo__rwpo, df.columns))
        onn__wdpa = None
        if df.is_table_format and len(kajs__szxr) > 0 and len(kajs__szxr
            ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
            vatko__opz = [df.column_index[hyo__rwpo] for hyo__rwpo in
                kajs__szxr]
            onn__wdpa = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
                vatko__opz))}
            jcd__zbs = (
                f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, True)'
                )
        else:
            jcd__zbs = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[hyo__rwpo]}).copy()'
                 for hyo__rwpo in kajs__szxr)
        nzin__xdze = 'def impl(df, ind):\n'
        nregb__vkucq = 'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)'
        return bodo.hiframes.dataframe_impl._gen_init_df(nzin__xdze,
            kajs__szxr, jcd__zbs, nregb__vkucq, extra_globals=onn__wdpa)
    if is_list_like_index_type(ind) and ind.dtype == types.bool_ or isinstance(
        ind, types.SliceType):
        nzin__xdze = 'def impl(df, ind):\n'
        if not isinstance(ind, types.SliceType):
            nzin__xdze += (
                '  ind = bodo.utils.conversion.coerce_to_array(ind)\n')
        nregb__vkucq = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[ind]')
        if df.is_table_format:
            jcd__zbs = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[ind]')
        else:
            jcd__zbs = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[hyo__rwpo]})[ind]'
                 for hyo__rwpo in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(nzin__xdze, df.
            columns, jcd__zbs, nregb__vkucq)
    raise_bodo_error('df[] getitem using {} not supported'.format(ind))


@overload(operator.setitem, no_unliteral=True)
def df_setitem_overload(df, idx, val):
    check_runtime_cols_unsupported(df, 'DataFrame setitem (df[])')
    if not isinstance(df, DataFrameType):
        return
    raise_bodo_error('DataFrame setitem: transform necessary')


class DataFrameILocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        alwng__mwuw = 'DataFrameILocType({})'.format(df_type)
        super(DataFrameILocType, self).__init__(alwng__mwuw)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameILocType)
class DataFrameILocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wjhg__pwxwh = [('obj', fe_type.df_type)]
        super(DataFrameILocModel, self).__init__(dmm, fe_type, wjhg__pwxwh)


make_attribute_wrapper(DataFrameILocType, 'obj', '_obj')


@intrinsic
def init_dataframe_iloc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        otsj__rpjca, = args
        iwm__xwn = signature.return_type
        trfhc__xpmcl = cgutils.create_struct_proxy(iwm__xwn)(context, builder)
        trfhc__xpmcl.obj = otsj__rpjca
        context.nrt.incref(builder, signature.args[0], otsj__rpjca)
        return trfhc__xpmcl._getvalue()
    return DataFrameILocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iloc')
def overload_dataframe_iloc(df):
    check_runtime_cols_unsupported(df, 'DataFrame.iloc')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_iloc(df)


@overload(operator.getitem, no_unliteral=True)
def overload_iloc_getitem(I, idx):
    if not isinstance(I, DataFrameILocType):
        return
    df = I.df_type
    if isinstance(idx, types.Integer):
        return _gen_iloc_getitem_row_impl(df, df.columns, 'idx')
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and not isinstance(
        idx[1], types.SliceType):
        if not (is_overload_constant_list(idx.types[1]) or
            is_overload_constant_int(idx.types[1])):
            raise_bodo_error(
                'idx2 in df.iloc[idx1, idx2] should be a constant integer or constant list of integers. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        bhbga__izty = len(df.data)
        if is_overload_constant_int(idx.types[1]):
            is_out_series = True
            bgzb__xya = get_overload_const_int(idx.types[1])
            if bgzb__xya < 0 or bgzb__xya >= bhbga__izty:
                raise BodoError(
                    'df.iloc: column integer must refer to a valid column number'
                    )
            mcyua__xza = [bgzb__xya]
        else:
            is_out_series = False
            mcyua__xza = get_overload_const_list(idx.types[1])
            if any(not isinstance(ind, int) or ind < 0 or ind >=
                bhbga__izty for ind in mcyua__xza):
                raise BodoError(
                    'df.iloc: column list must be integers referring to a valid column number'
                    )
        col_names = tuple(pd.Series(df.columns, dtype=object)[mcyua__xza])
        if isinstance(idx.types[0], types.Integer):
            if isinstance(idx.types[1], types.Integer):
                bgzb__xya = mcyua__xza[0]

                def impl(I, idx):
                    df = I._obj
                    return bodo.utils.conversion.box_if_dt64(bodo.hiframes.
                        pd_dataframe_ext.get_dataframe_data(df, bgzb__xya)[
                        idx[0]])
                return impl
            return _gen_iloc_getitem_row_impl(df, col_names, 'idx[0]')
        if is_list_like_index_type(idx.types[0]) and isinstance(idx.types[0
            ].dtype, (types.Integer, types.Boolean)) or isinstance(idx.
            types[0], types.SliceType):
            return _gen_iloc_getitem_bool_slice_impl(df, col_names, idx.
                types[0], 'idx[0]', is_out_series)
    if is_list_like_index_type(idx) and isinstance(idx.dtype, (types.
        Integer, types.Boolean)) or isinstance(idx, types.SliceType):
        return _gen_iloc_getitem_bool_slice_impl(df, df.columns, idx, 'idx',
            False)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):
        raise_bodo_error(
            'slice2 in df.iloc[slice1,slice2] should be constant. For more information, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
            )
    raise_bodo_error(f'df.iloc[] getitem using {idx} not supported')


def _gen_iloc_getitem_bool_slice_impl(df, col_names, idx_typ, idx,
    is_out_series):
    nzin__xdze = 'def impl(I, idx):\n'
    nzin__xdze += '  df = I._obj\n'
    if isinstance(idx_typ, types.SliceType):
        nzin__xdze += f'  idx_t = {idx}\n'
    else:
        nzin__xdze += (
            f'  idx_t = bodo.utils.conversion.coerce_to_array({idx})\n')
    nregb__vkucq = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
    onn__wdpa = None
    if df.is_table_format and not is_out_series:
        vatko__opz = [df.column_index[hyo__rwpo] for hyo__rwpo in col_names]
        onn__wdpa = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            vatko__opz))}
        jcd__zbs = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx_t]'
            )
    else:
        jcd__zbs = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[hyo__rwpo]})[idx_t]'
             for hyo__rwpo in col_names)
    if is_out_series:
        hcj__loi = f"'{col_names[0]}'" if isinstance(col_names[0], str
            ) else f'{col_names[0]}'
        nzin__xdze += f"""  return bodo.hiframes.pd_series_ext.init_series({jcd__zbs}, {nregb__vkucq}, {hcj__loi})
"""
        byv__qplhf = {}
        exec(nzin__xdze, {'bodo': bodo}, byv__qplhf)
        return byv__qplhf['impl']
    return bodo.hiframes.dataframe_impl._gen_init_df(nzin__xdze, col_names,
        jcd__zbs, nregb__vkucq, extra_globals=onn__wdpa)


def _gen_iloc_getitem_row_impl(df, col_names, idx):
    nzin__xdze = 'def impl(I, idx):\n'
    nzin__xdze += '  df = I._obj\n'
    yvvk__xscf = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[hyo__rwpo]})[{idx}]'
         for hyo__rwpo in col_names)
    nzin__xdze += f"""  row_idx = bodo.hiframes.pd_index_ext.init_heter_index({gen_const_tup(col_names)}, None)
"""
    nzin__xdze += f"""  return bodo.hiframes.pd_series_ext.init_series(({yvvk__xscf},), row_idx, None)
"""
    byv__qplhf = {}
    exec(nzin__xdze, {'bodo': bodo}, byv__qplhf)
    impl = byv__qplhf['impl']
    return impl


@overload(operator.setitem, no_unliteral=True)
def df_iloc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameILocType):
        return
    raise_bodo_error(
        f'DataFrame.iloc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameLocType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        alwng__mwuw = 'DataFrameLocType({})'.format(df_type)
        super(DataFrameLocType, self).__init__(alwng__mwuw)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameLocType)
class DataFrameLocModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wjhg__pwxwh = [('obj', fe_type.df_type)]
        super(DataFrameLocModel, self).__init__(dmm, fe_type, wjhg__pwxwh)


make_attribute_wrapper(DataFrameLocType, 'obj', '_obj')


@intrinsic
def init_dataframe_loc(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        otsj__rpjca, = args
        gxowm__bzj = signature.return_type
        gjvv__upxe = cgutils.create_struct_proxy(gxowm__bzj)(context, builder)
        gjvv__upxe.obj = otsj__rpjca
        context.nrt.incref(builder, signature.args[0], otsj__rpjca)
        return gjvv__upxe._getvalue()
    return DataFrameLocType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'loc')
def overload_dataframe_loc(df):
    check_runtime_cols_unsupported(df, 'DataFrame.loc')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_loc(df)


@lower_builtin(operator.getitem, DataFrameLocType, types.Any)
def loc_getitem_lower(context, builder, sig, args):
    impl = overload_loc_getitem(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def overload_loc_getitem(I, idx):
    if not isinstance(I, DataFrameLocType):
        return
    df = I.df_type
    if is_list_like_index_type(idx) and idx.dtype == types.bool_:
        nzin__xdze = 'def impl(I, idx):\n'
        nzin__xdze += '  df = I._obj\n'
        nzin__xdze += '  idx_t = bodo.utils.conversion.coerce_to_array(idx)\n'
        nregb__vkucq = (
            'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx_t]')
        if df.is_table_format:
            jcd__zbs = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)[idx_t]'
                )
        else:
            jcd__zbs = ', '.join(
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {df.column_index[hyo__rwpo]})[idx_t]'
                 for hyo__rwpo in df.columns)
        return bodo.hiframes.dataframe_impl._gen_init_df(nzin__xdze, df.
            columns, jcd__zbs, nregb__vkucq)
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        mgef__nfs = idx.types[1]
        if is_overload_constant_str(mgef__nfs):
            lpofs__edkfr = get_overload_const_str(mgef__nfs)
            bgzb__xya = df.columns.index(lpofs__edkfr)

            def impl_col_name(I, idx):
                df = I._obj
                nregb__vkucq = (bodo.hiframes.pd_dataframe_ext.
                    get_dataframe_index(df))
                aimp__chv = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(
                    df, bgzb__xya)
                return bodo.hiframes.pd_series_ext.init_series(aimp__chv,
                    nregb__vkucq, lpofs__edkfr).loc[idx[0]]
            return impl_col_name
        if is_overload_constant_list(mgef__nfs):
            col_idx_list = get_overload_const_list(mgef__nfs)
            if len(col_idx_list) > 0 and not isinstance(col_idx_list[0], (
                bool, np.bool_)) and not all(hyo__rwpo in df.column_index for
                hyo__rwpo in col_idx_list):
                raise_bodo_error(
                    f'DataFrame.loc[]: invalid column list {col_idx_list}; not all in dataframe columns {df.columns}'
                    )
            return gen_df_loc_col_select_impl(df, col_idx_list)
    raise_bodo_error(
        f'DataFrame.loc[] getitem (location-based indexing) using {idx} not supported yet.'
        )


def gen_df_loc_col_select_impl(df, col_idx_list):
    col_names = []
    mcyua__xza = []
    if len(col_idx_list) > 0 and isinstance(col_idx_list[0], (bool, np.bool_)):
        for lgdf__oza, ace__vbd in enumerate(col_idx_list):
            if ace__vbd:
                mcyua__xza.append(lgdf__oza)
                col_names.append(df.columns[lgdf__oza])
    else:
        col_names = col_idx_list
        mcyua__xza = [df.column_index[hyo__rwpo] for hyo__rwpo in col_idx_list]
    onn__wdpa = None
    if df.is_table_format and len(col_idx_list) > 0 and len(col_idx_list
        ) >= bodo.hiframes.boxing.TABLE_FORMAT_THRESHOLD:
        onn__wdpa = {'col_nums_meta': bodo.utils.typing.MetaType(tuple(
            mcyua__xza))}
        jcd__zbs = (
            f'bodo.hiframes.table.table_subset(bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df), col_nums_meta, False)[idx[0]]'
            )
    else:
        jcd__zbs = ', '.join(
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {ind})[idx[0]]'
             for ind in mcyua__xza)
    nregb__vkucq = (
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)[idx[0]]')
    nzin__xdze = 'def impl(I, idx):\n'
    nzin__xdze += '  df = I._obj\n'
    return bodo.hiframes.dataframe_impl._gen_init_df(nzin__xdze, col_names,
        jcd__zbs, nregb__vkucq, extra_globals=onn__wdpa)


@overload(operator.setitem, no_unliteral=True)
def df_loc_setitem_overload(df, idx, val):
    if not isinstance(df, DataFrameLocType):
        return
    raise_bodo_error(
        f'DataFrame.loc setitem unsupported for dataframe {df.df_type}, index {idx}, value {val}'
        )


class DataFrameIatType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        alwng__mwuw = 'DataFrameIatType({})'.format(df_type)
        super(DataFrameIatType, self).__init__(alwng__mwuw)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)
    ndim = 2


@register_model(DataFrameIatType)
class DataFrameIatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        wjhg__pwxwh = [('obj', fe_type.df_type)]
        super(DataFrameIatModel, self).__init__(dmm, fe_type, wjhg__pwxwh)


make_attribute_wrapper(DataFrameIatType, 'obj', '_obj')


@intrinsic
def init_dataframe_iat(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        otsj__rpjca, = args
        cob__wplgy = signature.return_type
        fee__fuwsr = cgutils.create_struct_proxy(cob__wplgy)(context, builder)
        fee__fuwsr.obj = otsj__rpjca
        context.nrt.incref(builder, signature.args[0], otsj__rpjca)
        return fee__fuwsr._getvalue()
    return DataFrameIatType(obj)(obj), codegen


@overload_attribute(DataFrameType, 'iat')
def overload_dataframe_iat(df):
    check_runtime_cols_unsupported(df, 'DataFrame.iat')
    return lambda df: bodo.hiframes.dataframe_indexing.init_dataframe_iat(df)


@overload(operator.getitem, no_unliteral=True)
def overload_iat_getitem(I, idx):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat getitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        bgzb__xya = get_overload_const_int(idx.types[1])

        def impl_col_ind(I, idx):
            df = I._obj
            aimp__chv = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                bgzb__xya)
            return bodo.utils.conversion.box_if_dt64(aimp__chv[idx[0]])
        return impl_col_ind
    raise BodoError('df.iat[] getitem using {} not supported'.format(idx))


@overload(operator.setitem, no_unliteral=True)
def overload_iat_setitem(I, idx, val):
    if not isinstance(I, DataFrameIatType):
        return
    if isinstance(idx, types.BaseTuple) and len(idx) == 2:
        if not isinstance(idx.types[0], types.Integer):
            raise BodoError(
                'DataFrame.iat: iAt based indexing can only have integer indexers'
                )
        if not is_overload_constant_int(idx.types[1]):
            raise_bodo_error(
                'DataFrame.iat setitem: column index must be a constant integer. For more informaton, see https://docs.bodo.ai/latest/bodo_parallelism/typing_considerations/#require_constants.'
                )
        bgzb__xya = get_overload_const_int(idx.types[1])
        if is_immutable_array(I.df_type.data[bgzb__xya]):
            raise BodoError(
                f'DataFrame setitem not supported for column with immutable array type {I.df_type.data}'
                )

        def impl_col_ind(I, idx, val):
            df = I._obj
            aimp__chv = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df,
                bgzb__xya)
            aimp__chv[idx[0]
                ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(val)
        return impl_col_ind
    raise BodoError('df.iat[] setitem using {} not supported'.format(idx))


@lower_cast(DataFrameIatType, DataFrameIatType)
@lower_cast(DataFrameILocType, DataFrameILocType)
@lower_cast(DataFrameLocType, DataFrameLocType)
def cast_series_iat(context, builder, fromty, toty, val):
    fee__fuwsr = cgutils.create_struct_proxy(fromty)(context, builder, val)
    lbmj__xbmn = context.cast(builder, fee__fuwsr.obj, fromty.df_type, toty
        .df_type)
    fxzs__jfae = cgutils.create_struct_proxy(toty)(context, builder)
    fxzs__jfae.obj = lbmj__xbmn
    return fxzs__jfae._getvalue()
