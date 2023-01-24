"""
Implement pd.DataFrame typing and data model handling.
"""
import json
import operator
import time
from functools import cached_property
from typing import Optional, Sequence
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
import pyarrow as pa
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed, lower_constant
from numba.core.typing.templates import AbstractTemplate, bound_function, infer_global, signature
from numba.cpython.listobj import ListInstance
from numba.extending import infer_getattr, intrinsic, lower_builtin, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType
from bodo.hiframes.pd_index_ext import HeterogeneousIndexType, NumericIndexType, RangeIndexType, is_pd_index_type
from bodo.hiframes.pd_multi_index_ext import MultiIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.series_indexing import SeriesIlocType
from bodo.hiframes.table import Table, TableType, decode_if_dict_table, get_table_data, set_table_data_codegen
from bodo.hiframes.time_ext import TimeArrayType
from bodo.io import json_cpp
from bodo.libs.array import arr_info_list_to_table, array_to_info, delete_info_decref_array, delete_table, delete_table_decref_arrays, info_from_table, info_to_array, py_table_to_cpp_table, shuffle_table
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import str_arr_from_sequence
from bodo.libs.str_ext import string_type, unicode_to_utf8
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils import tracing
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.conversion import fix_arr_dtype, index_to_array
from bodo.utils.templates import OverloadedKeyAttributeTemplate
from bodo.utils.transform import get_const_func_output_type
from bodo.utils.typing import BodoError, BodoWarning, ColNamesMetaType, check_unsupported_args, create_unsupported_overload, decode_if_dict_array, dtype_to_array_type, get_index_data_arr_types, get_literal_value, get_overload_const, get_overload_const_bool, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_udf_error_msg, get_udf_out_arr_type, is_heterogeneous_tuple_type, is_iterable_type, is_literal_type, is_overload_bool, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_str, is_overload_false, is_overload_int, is_overload_none, is_overload_true, is_str_arr_type, is_tuple_like_type, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array
from bodo.utils.utils import is_null_pointer
_json_write = types.ExternalFunction('json_write', types.void(types.voidptr,
    types.voidptr, types.int64, types.int64, types.bool_, types.bool_,
    types.voidptr, types.voidptr))
ll.add_symbol('json_write', json_cpp.json_write)


class DataFrameType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, data: Optional[Sequence['types.Array']]=None, index=
        None, columns: Optional[Sequence[str]]=None, dist=None,
        is_table_format=False):
        from bodo.transforms.distributed_analysis import Distribution
        self.data = data
        if index is None:
            index = RangeIndexType(types.none)
        self.index = index
        self.columns = columns
        dist = Distribution.OneD_Var if dist is None else dist
        self.dist = dist
        self.is_table_format = is_table_format
        if columns is None:
            assert is_table_format, 'Determining columns at runtime is only supported for DataFrame with table format'
            self.table_type = TableType(tuple(data[:-1]), True)
        else:
            self.table_type = TableType(data) if is_table_format else None
        super(DataFrameType, self).__init__(name=
            f'dataframe({data}, {index}, {columns}, {dist}, {is_table_format}, {self.has_runtime_cols})'
            )

    def __str__(self):
        if not self.has_runtime_cols and len(self.columns) > 20:
            hok__qjxn = f'{len(self.data)} columns of types {set(self.data)}'
            fnsg__frs = (
                f"('{self.columns[0]}', '{self.columns[1]}', ..., '{self.columns[-1]}')"
                )
            sdni__qcduh = str(hash(super().__str__()))
            return (
                f'dataframe({hok__qjxn}, {self.index}, {fnsg__frs}, {self.dist}, {self.is_table_format}, {self.has_runtime_cols}, key_hash={sdni__qcduh})'
                )
        return super().__str__()

    def copy(self, data=None, index=None, columns=None, dist=None,
        is_table_format=None):
        if data is None:
            data = self.data
        if columns is None:
            columns = self.columns
        if index is None:
            index = self.index
        if dist is None:
            dist = self.dist
        if is_table_format is None:
            is_table_format = self.is_table_format
        return DataFrameType(data, index, columns, dist, is_table_format)

    @property
    def has_runtime_cols(self):
        return self.columns is None

    @cached_property
    def column_index(self):
        return {qqoy__lyyaj: i for i, qqoy__lyyaj in enumerate(self.columns)}

    @property
    def runtime_colname_typ(self):
        return self.data[-1] if self.has_runtime_cols else None

    @property
    def runtime_data_types(self):
        return self.data[:-1] if self.has_runtime_cols else self.data

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    @property
    def key(self):
        return (self.data, self.index, self.columns, self.dist, self.
            is_table_format)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)

    def unify(self, typingctx, other):
        from bodo.transforms.distributed_analysis import Distribution
        if (isinstance(other, DataFrameType) and len(other.data) == len(
            self.data) and other.columns == self.columns and other.
            has_runtime_cols == self.has_runtime_cols):
            whlz__brt = (self.index if self.index == other.index else self.
                index.unify(typingctx, other.index))
            data = tuple(ncgs__ulz.unify(typingctx, jsjf__ixyaw) if 
                ncgs__ulz != jsjf__ixyaw else ncgs__ulz for ncgs__ulz,
                jsjf__ixyaw in zip(self.data, other.data))
            dist = Distribution(min(self.dist.value, other.dist.value))
            if whlz__brt is not None and None not in data:
                return DataFrameType(data, whlz__brt, self.columns, dist,
                    self.is_table_format)
        if isinstance(other, DataFrameType) and len(self.data
            ) == 0 and not self.has_runtime_cols:
            return other

    def can_convert_to(self, typingctx, other):
        from numba.core.typeconv import Conversion
        if (isinstance(other, DataFrameType) and self.data == other.data and
            self.index == other.index and self.columns == other.columns and
            self.dist != other.dist and self.has_runtime_cols == other.
            has_runtime_cols):
            return Conversion.safe

    def is_precise(self):
        return all(ncgs__ulz.is_precise() for ncgs__ulz in self.data
            ) and self.index.is_precise()

    def replace_col_type(self, col_name, new_type):
        if col_name not in self.columns:
            raise ValueError(
                f"DataFrameType.replace_col_type replaced column must be found in the DataFrameType. '{col_name}' not found in DataFrameType with columns {self.columns}"
                )
        updmz__kmqp = self.columns.index(col_name)
        wxu__suy = tuple(list(self.data[:updmz__kmqp]) + [new_type] + list(
            self.data[updmz__kmqp + 1:]))
        return DataFrameType(wxu__suy, self.index, self.columns, self.dist,
            self.is_table_format)


def check_runtime_cols_unsupported(df, func_name):
    if isinstance(df, DataFrameType) and df.has_runtime_cols:
        raise BodoError(
            f'{func_name} on DataFrames with columns determined at runtime is not yet supported. Please return the DataFrame to regular Python to update typing information.'
            )


class DataFramePayloadType(types.Type):

    def __init__(self, df_type):
        self.df_type = df_type
        super(DataFramePayloadType, self).__init__(name=
            f'DataFramePayloadType({df_type})')

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(DataFramePayloadType)
class DataFramePayloadModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        data_typ = types.Tuple(fe_type.df_type.data)
        if fe_type.df_type.is_table_format:
            data_typ = types.Tuple([fe_type.df_type.table_type])
        cynjg__nqexu = [('data', data_typ), ('index', fe_type.df_type.index
            ), ('parent', types.pyobject)]
        if fe_type.df_type.has_runtime_cols:
            cynjg__nqexu.append(('columns', fe_type.df_type.
                runtime_colname_typ))
        super(DataFramePayloadModel, self).__init__(dmm, fe_type, cynjg__nqexu)


@register_model(DataFrameType)
class DataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        payload_type = DataFramePayloadType(fe_type)
        cynjg__nqexu = [('meminfo', types.MemInfoPointer(payload_type)), (
            'parent', types.pyobject)]
        super(DataFrameModel, self).__init__(dmm, fe_type, cynjg__nqexu)


make_attribute_wrapper(DataFrameType, 'meminfo', '_meminfo')


@infer_getattr
class DataFrameAttribute(OverloadedKeyAttributeTemplate):
    key = DataFrameType

    def resolve_shape(self, df):
        return types.Tuple([types.int64, types.int64])

    @bound_function('df.head')
    def resolve_head(self, df, args, kws):
        func_name = 'DataFrame.head'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        tiv__myfob = 'n',
        qioc__qnu = {'n': 5}
        zdkur__imig, qvsxc__exy = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, tiv__myfob, qioc__qnu)
        jqg__ffc = qvsxc__exy[0]
        if not is_overload_int(jqg__ffc):
            raise BodoError(f"{func_name}(): 'n' must be an Integer")
        qwz__abl = df.copy()
        return qwz__abl(*qvsxc__exy).replace(pysig=zdkur__imig)

    @bound_function('df.corr')
    def resolve_corr(self, df, args, kws):
        func_name = 'DataFrame.corr'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        sfkel__qkf = (df,) + args
        tiv__myfob = 'df', 'method', 'min_periods'
        qioc__qnu = {'method': 'pearson', 'min_periods': 1}
        esxwq__phe = 'method',
        zdkur__imig, qvsxc__exy = bodo.utils.typing.fold_typing_args(func_name,
            sfkel__qkf, kws, tiv__myfob, qioc__qnu, esxwq__phe)
        jteq__lzp = qvsxc__exy[2]
        if not is_overload_int(jteq__lzp):
            raise BodoError(f"{func_name}(): 'min_periods' must be an Integer")
        njue__wuz = []
        zsq__frr = []
        for qqoy__lyyaj, wmhj__myjkl in zip(df.columns, df.data):
            if bodo.utils.typing._is_pandas_numeric_dtype(wmhj__myjkl.dtype):
                njue__wuz.append(qqoy__lyyaj)
                zsq__frr.append(types.Array(types.float64, 1, 'A'))
        if len(njue__wuz) == 0:
            raise_bodo_error('DataFrame.corr(): requires non-empty dataframe')
        zsq__frr = tuple(zsq__frr)
        njue__wuz = tuple(njue__wuz)
        index_typ = bodo.utils.typing.type_col_to_index(njue__wuz)
        qwz__abl = DataFrameType(zsq__frr, index_typ, njue__wuz)
        return qwz__abl(*qvsxc__exy).replace(pysig=zdkur__imig)

    @bound_function('df.pipe', no_unliteral=True)
    def resolve_pipe(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.pipe()')
        return bodo.hiframes.pd_groupby_ext.resolve_obj_pipe(self, df, args,
            kws, 'DataFrame')

    @bound_function('df.apply', no_unliteral=True)
    def resolve_apply(self, df, args, kws):
        check_runtime_cols_unsupported(df, 'DataFrame.apply()')
        kws = dict(kws)
        jroy__qne = args[0] if len(args) > 0 else kws.pop('func', None)
        axis = args[1] if len(args) > 1 else kws.pop('axis', types.literal(0))
        yfx__hxqmh = args[2] if len(args) > 2 else kws.pop('raw', types.
            literal(False))
        flty__boki = args[3] if len(args) > 3 else kws.pop('result_type',
            types.none)
        upu__sgkdy = args[4] if len(args) > 4 else kws.pop('args', types.
            Tuple([]))
        xsc__kmgai = dict(raw=yfx__hxqmh, result_type=flty__boki)
        ndfbt__dlas = dict(raw=False, result_type=None)
        check_unsupported_args('Dataframe.apply', xsc__kmgai, ndfbt__dlas,
            package_name='pandas', module_name='DataFrame')
        hzdc__dggyh = True
        if types.unliteral(jroy__qne) == types.unicode_type:
            if not is_overload_constant_str(jroy__qne):
                raise BodoError(
                    f'DataFrame.apply(): string argument (for builtins) must be a compile time constant'
                    )
            hzdc__dggyh = False
        if not is_overload_constant_int(axis):
            raise BodoError(
                'Dataframe.apply(): axis argument must be a compile time constant.'
                )
        mtnfx__vrxq = get_overload_const_int(axis)
        if hzdc__dggyh and mtnfx__vrxq != 1:
            raise BodoError(
                'Dataframe.apply(): only axis=1 supported for user-defined functions'
                )
        elif mtnfx__vrxq not in (0, 1):
            raise BodoError('Dataframe.apply(): axis must be either 0 or 1')
        neh__fes = []
        for arr_typ in df.data:
            hib__wdhk = SeriesType(arr_typ.dtype, arr_typ, df.index,
                string_type)
            vuiwu__rzup = self.context.resolve_function_type(operator.
                getitem, (SeriesIlocType(hib__wdhk), types.int64), {}
                ).return_type
            neh__fes.append(vuiwu__rzup)
        fakc__idp = types.none
        gmjjj__qoe = HeterogeneousIndexType(types.BaseTuple.from_types(
            tuple(types.literal(qqoy__lyyaj) for qqoy__lyyaj in df.columns)
            ), None)
        aghl__vkf = types.BaseTuple.from_types(neh__fes)
        tesyg__psmsa = types.Tuple([types.bool_] * len(aghl__vkf))
        ayy__wbu = bodo.NullableTupleType(aghl__vkf, tesyg__psmsa)
        dsld__ool = df.index.dtype
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(df.index,
            'DataFrame.apply()')
        if dsld__ool == types.NPDatetime('ns'):
            dsld__ool = bodo.pd_timestamp_tz_naive_type
        if dsld__ool == types.NPTimedelta('ns'):
            dsld__ool = bodo.pd_timedelta_type
        if is_heterogeneous_tuple_type(aghl__vkf):
            dkjkb__olr = HeterogeneousSeriesType(ayy__wbu, gmjjj__qoe,
                dsld__ool)
        else:
            dkjkb__olr = SeriesType(aghl__vkf.dtype, ayy__wbu, gmjjj__qoe,
                dsld__ool)
        waqvt__paip = dkjkb__olr,
        if upu__sgkdy is not None:
            waqvt__paip += tuple(upu__sgkdy.types)
        try:
            if not hzdc__dggyh:
                glfg__lagqq = bodo.utils.transform.get_udf_str_return_type(df,
                    get_overload_const_str(jroy__qne), self.context,
                    'DataFrame.apply', axis if mtnfx__vrxq == 1 else None)
            else:
                glfg__lagqq = get_const_func_output_type(jroy__qne,
                    waqvt__paip, kws, self.context, numba.core.registry.
                    cpu_target.target_context)
        except Exception as hzmi__oqidc:
            raise_bodo_error(get_udf_error_msg('DataFrame.apply()',
                hzmi__oqidc))
        if hzdc__dggyh:
            if not (is_overload_constant_int(axis) and 
                get_overload_const_int(axis) == 1):
                raise BodoError(
                    'Dataframe.apply(): only user-defined functions with axis=1 supported'
                    )
            if isinstance(glfg__lagqq, (SeriesType, HeterogeneousSeriesType)
                ) and glfg__lagqq.const_info is None:
                raise BodoError(
                    'Invalid Series output in UDF (Series with constant length and constant Index value expected)'
                    )
            if isinstance(glfg__lagqq, HeterogeneousSeriesType):
                gbc__dkw, zgd__dlau = glfg__lagqq.const_info
                if isinstance(glfg__lagqq.data, bodo.libs.
                    nullable_tuple_ext.NullableTupleType):
                    satg__ull = glfg__lagqq.data.tuple_typ.types
                elif isinstance(glfg__lagqq.data, types.Tuple):
                    satg__ull = glfg__lagqq.data.types
                else:
                    raise_bodo_error(
                        'df.apply(): Unexpected Series return type for Heterogeneous data'
                        )
                evaec__zqii = tuple(to_nullable_type(dtype_to_array_type(
                    fimmx__moe)) for fimmx__moe in satg__ull)
                ypi__llhat = DataFrameType(evaec__zqii, df.index, zgd__dlau)
            elif isinstance(glfg__lagqq, SeriesType):
                ejrr__owany, zgd__dlau = glfg__lagqq.const_info
                evaec__zqii = tuple(to_nullable_type(dtype_to_array_type(
                    glfg__lagqq.dtype)) for gbc__dkw in range(ejrr__owany))
                ypi__llhat = DataFrameType(evaec__zqii, df.index, zgd__dlau)
            else:
                zme__ubk = get_udf_out_arr_type(glfg__lagqq)
                ypi__llhat = SeriesType(zme__ubk.dtype, zme__ubk, df.index,
                    None)
        else:
            ypi__llhat = glfg__lagqq
        hyjj__ysj = ', '.join("{} = ''".format(ncgs__ulz) for ncgs__ulz in
            kws.keys())
        dxh__ulce = f"""def apply_stub(func, axis=0, raw=False, result_type=None, args=(), {hyjj__ysj}):
"""
        dxh__ulce += '    pass\n'
        kdchp__xde = {}
        exec(dxh__ulce, {}, kdchp__xde)
        ajcuk__jgyyp = kdchp__xde['apply_stub']
        zdkur__imig = numba.core.utils.pysignature(ajcuk__jgyyp)
        kkv__iatzu = (jroy__qne, axis, yfx__hxqmh, flty__boki, upu__sgkdy
            ) + tuple(kws.values())
        return signature(ypi__llhat, *kkv__iatzu).replace(pysig=zdkur__imig)

    @bound_function('df.plot', no_unliteral=True)
    def resolve_plot(self, df, args, kws):
        func_name = 'DataFrame.plot'
        check_runtime_cols_unsupported(df, f'{func_name}()')
        tiv__myfob = ('x', 'y', 'kind', 'figsize', 'ax', 'subplots',
            'sharex', 'sharey', 'layout', 'use_index', 'title', 'grid',
            'legend', 'style', 'logx', 'logy', 'loglog', 'xticks', 'yticks',
            'xlim', 'ylim', 'rot', 'fontsize', 'colormap', 'table', 'yerr',
            'xerr', 'secondary_y', 'sort_columns', 'xlabel', 'ylabel',
            'position', 'stacked', 'mark_right', 'include_bool', 'backend')
        qioc__qnu = {'x': None, 'y': None, 'kind': 'line', 'figsize': None,
            'ax': None, 'subplots': False, 'sharex': None, 'sharey': False,
            'layout': None, 'use_index': True, 'title': None, 'grid': None,
            'legend': True, 'style': None, 'logx': False, 'logy': False,
            'loglog': False, 'xticks': None, 'yticks': None, 'xlim': None,
            'ylim': None, 'rot': None, 'fontsize': None, 'colormap': None,
            'table': False, 'yerr': None, 'xerr': None, 'secondary_y': 
            False, 'sort_columns': False, 'xlabel': None, 'ylabel': None,
            'position': 0.5, 'stacked': False, 'mark_right': True,
            'include_bool': False, 'backend': None}
        esxwq__phe = ('subplots', 'sharex', 'sharey', 'layout', 'use_index',
            'grid', 'style', 'logx', 'logy', 'loglog', 'xlim', 'ylim',
            'rot', 'colormap', 'table', 'yerr', 'xerr', 'sort_columns',
            'secondary_y', 'colorbar', 'position', 'stacked', 'mark_right',
            'include_bool', 'backend')
        zdkur__imig, qvsxc__exy = bodo.utils.typing.fold_typing_args(func_name,
            args, kws, tiv__myfob, qioc__qnu, esxwq__phe)
        xuezx__npmsr = qvsxc__exy[2]
        if not is_overload_constant_str(xuezx__npmsr):
            raise BodoError(
                f"{func_name}: kind must be a constant string and one of ('line', 'scatter')."
                )
        xflce__bevk = qvsxc__exy[0]
        if not is_overload_none(xflce__bevk) and not (is_overload_int(
            xflce__bevk) or is_overload_constant_str(xflce__bevk)):
            raise BodoError(
                f'{func_name}: x must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(xflce__bevk):
            lav__laqt = get_overload_const_str(xflce__bevk)
            if lav__laqt not in df.columns:
                raise BodoError(f'{func_name}: {lav__laqt} column not found.')
        elif is_overload_int(xflce__bevk):
            bll__wstk = get_overload_const_int(xflce__bevk)
            if bll__wstk > len(df.columns):
                raise BodoError(
                    f'{func_name}: x: {bll__wstk} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            xflce__bevk = df.columns[xflce__bevk]
        zkncu__ozehw = qvsxc__exy[1]
        if not is_overload_none(zkncu__ozehw) and not (is_overload_int(
            zkncu__ozehw) or is_overload_constant_str(zkncu__ozehw)):
            raise BodoError(
                'df.plot(): y must be a constant column name, constant integer, or None.'
                )
        if is_overload_constant_str(zkncu__ozehw):
            zfy__jdxij = get_overload_const_str(zkncu__ozehw)
            if zfy__jdxij not in df.columns:
                raise BodoError(f'{func_name}: {zfy__jdxij} column not found.')
        elif is_overload_int(zkncu__ozehw):
            yoaz__mootg = get_overload_const_int(zkncu__ozehw)
            if yoaz__mootg > len(df.columns):
                raise BodoError(
                    f'{func_name}: y: {yoaz__mootg} is out of bounds for axis 0 with size {len(df.columns)}'
                    )
            zkncu__ozehw = df.columns[zkncu__ozehw]
        bcz__gei = qvsxc__exy[3]
        if not is_overload_none(bcz__gei) and not is_tuple_like_type(bcz__gei):
            raise BodoError(
                f'{func_name}: figsize must be a constant numeric tuple (width, height) or None.'
                )
        qpr__leb = qvsxc__exy[10]
        if not is_overload_none(qpr__leb) and not is_overload_constant_str(
            qpr__leb):
            raise BodoError(
                f'{func_name}: title must be a constant string or None.')
        ewf__zrk = qvsxc__exy[12]
        if not is_overload_bool(ewf__zrk):
            raise BodoError(f'{func_name}: legend must be a boolean type.')
        pwy__vom = qvsxc__exy[17]
        if not is_overload_none(pwy__vom) and not is_tuple_like_type(pwy__vom):
            raise BodoError(
                f'{func_name}: xticks must be a constant tuple or None.')
        btisx__bwduz = qvsxc__exy[18]
        if not is_overload_none(btisx__bwduz) and not is_tuple_like_type(
            btisx__bwduz):
            raise BodoError(
                f'{func_name}: yticks must be a constant tuple or None.')
        cnmxp__usgi = qvsxc__exy[22]
        if not is_overload_none(cnmxp__usgi) and not is_overload_int(
            cnmxp__usgi):
            raise BodoError(
                f'{func_name}: fontsize must be an integer or None.')
        dadjb__kxb = qvsxc__exy[29]
        if not is_overload_none(dadjb__kxb) and not is_overload_constant_str(
            dadjb__kxb):
            raise BodoError(
                f'{func_name}: xlabel must be a constant string or None.')
        dss__dupma = qvsxc__exy[30]
        if not is_overload_none(dss__dupma) and not is_overload_constant_str(
            dss__dupma):
            raise BodoError(
                f'{func_name}: ylabel must be a constant string or None.')
        bxh__whyc = types.List(types.mpl_line_2d_type)
        xuezx__npmsr = get_overload_const_str(xuezx__npmsr)
        if xuezx__npmsr == 'scatter':
            if is_overload_none(xflce__bevk) and is_overload_none(zkncu__ozehw
                ):
                raise BodoError(
                    f'{func_name}: {xuezx__npmsr} requires an x and y column.')
            elif is_overload_none(xflce__bevk):
                raise BodoError(
                    f'{func_name}: {xuezx__npmsr} x column is missing.')
            elif is_overload_none(zkncu__ozehw):
                raise BodoError(
                    f'{func_name}: {xuezx__npmsr} y column is missing.')
            bxh__whyc = types.mpl_path_collection_type
        elif xuezx__npmsr != 'line':
            raise BodoError(
                f'{func_name}: {xuezx__npmsr} plot is not supported.')
        return signature(bxh__whyc, *qvsxc__exy).replace(pysig=zdkur__imig)

    def generic_resolve(self, df, attr):
        if self._is_existing_attr(attr):
            return
        check_runtime_cols_unsupported(df,
            'Acessing DataFrame columns by attribute')
        if attr in df.columns:
            sfar__yal = df.columns.index(attr)
            arr_typ = df.data[sfar__yal]
            return SeriesType(arr_typ.dtype, arr_typ, df.index, types.
                StringLiteral(attr))
        if len(df.columns) > 0 and isinstance(df.columns[0], tuple):
            qjdih__tujjw = []
            wxu__suy = []
            zox__tjdm = False
            for i, lwy__euvm in enumerate(df.columns):
                if lwy__euvm[0] != attr:
                    continue
                zox__tjdm = True
                qjdih__tujjw.append(lwy__euvm[1] if len(lwy__euvm) == 2 else
                    lwy__euvm[1:])
                wxu__suy.append(df.data[i])
            if zox__tjdm:
                return DataFrameType(tuple(wxu__suy), df.index, tuple(
                    qjdih__tujjw))


DataFrameAttribute._no_unliteral = True


@overload(operator.getitem, no_unliteral=True)
def namedtuple_getitem_overload(tup, idx):
    if isinstance(tup, types.BaseNamedTuple) and is_overload_constant_str(idx):
        pqhms__tgngh = get_overload_const_str(idx)
        val_ind = tup.instance_class._fields.index(pqhms__tgngh)
        return lambda tup, idx: tup[val_ind]


def decref_df_data(context, builder, payload, df_type):
    if df_type.is_table_format:
        context.nrt.decref(builder, df_type.table_type, builder.
            extract_value(payload.data, 0))
        context.nrt.decref(builder, df_type.index, payload.index)
        if df_type.has_runtime_cols:
            context.nrt.decref(builder, df_type.data[-1], payload.columns)
        return
    for i in range(len(df_type.data)):
        ivb__wamy = builder.extract_value(payload.data, i)
        context.nrt.decref(builder, df_type.data[i], ivb__wamy)
    context.nrt.decref(builder, df_type.index, payload.index)


def define_df_dtor(context, builder, df_type, payload_type):
    hoo__hrs = builder.module
    kqhoi__zhnkl = lir.FunctionType(lir.VoidType(), [cgutils.voidptr_t])
    tfvz__omz = cgutils.get_or_insert_function(hoo__hrs, kqhoi__zhnkl, name
        ='.dtor.df.{}'.format(df_type))
    if not tfvz__omz.is_declaration:
        return tfvz__omz
    tfvz__omz.linkage = 'linkonce_odr'
    builder = lir.IRBuilder(tfvz__omz.append_basic_block())
    sgdc__wcxp = tfvz__omz.args[0]
    swy__qetkl = context.get_value_type(payload_type).as_pointer()
    zxya__exele = builder.bitcast(sgdc__wcxp, swy__qetkl)
    payload = context.make_helper(builder, payload_type, ref=zxya__exele)
    decref_df_data(context, builder, payload, df_type)
    has_parent = cgutils.is_not_null(builder, payload.parent)
    with builder.if_then(has_parent):
        yko__eqb = context.get_python_api(builder)
        gjwx__bgjc = yko__eqb.gil_ensure()
        yko__eqb.decref(payload.parent)
        yko__eqb.gil_release(gjwx__bgjc)
    builder.ret_void()
    return tfvz__omz


def construct_dataframe(context, builder, df_type, data_tup, index_val,
    parent=None, colnames=None):
    payload_type = DataFramePayloadType(df_type)
    bqw__fvdye = cgutils.create_struct_proxy(payload_type)(context, builder)
    bqw__fvdye.data = data_tup
    bqw__fvdye.index = index_val
    if colnames is not None:
        assert df_type.has_runtime_cols, 'construct_dataframe can only provide colnames if columns are determined at runtime'
        bqw__fvdye.columns = colnames
    dntmw__msbev = context.get_value_type(payload_type)
    tiixn__pijyo = context.get_abi_sizeof(dntmw__msbev)
    htfl__glro = define_df_dtor(context, builder, df_type, payload_type)
    wvks__osygz = context.nrt.meminfo_alloc_dtor(builder, context.
        get_constant(types.uintp, tiixn__pijyo), htfl__glro)
    ghbx__ulq = context.nrt.meminfo_data(builder, wvks__osygz)
    spwk__msjyh = builder.bitcast(ghbx__ulq, dntmw__msbev.as_pointer())
    csh__ulnki = cgutils.create_struct_proxy(df_type)(context, builder)
    csh__ulnki.meminfo = wvks__osygz
    if parent is None:
        csh__ulnki.parent = cgutils.get_null_value(csh__ulnki.parent.type)
    else:
        csh__ulnki.parent = parent
        bqw__fvdye.parent = parent
        has_parent = cgutils.is_not_null(builder, parent)
        with builder.if_then(has_parent):
            yko__eqb = context.get_python_api(builder)
            gjwx__bgjc = yko__eqb.gil_ensure()
            yko__eqb.incref(parent)
            yko__eqb.gil_release(gjwx__bgjc)
    builder.store(bqw__fvdye._getvalue(), spwk__msjyh)
    return csh__ulnki._getvalue()


@intrinsic
def init_runtime_cols_dataframe(typingctx, data_typ, index_typ,
    colnames_index_typ=None):
    assert isinstance(data_typ, types.BaseTuple) and isinstance(data_typ.
        dtype, TableType
        ) and data_typ.dtype.has_runtime_cols, 'init_runtime_cols_dataframe must be called with a table that determines columns at runtime.'
    assert bodo.hiframes.pd_index_ext.is_pd_index_type(colnames_index_typ
        ) or isinstance(colnames_index_typ, bodo.hiframes.
        pd_multi_index_ext.MultiIndexType), 'Column names must be an index'
    if isinstance(data_typ.dtype.arr_types, types.UniTuple):
        lukm__apuhv = [data_typ.dtype.arr_types.dtype] * len(data_typ.dtype
            .arr_types)
    else:
        lukm__apuhv = [fimmx__moe for fimmx__moe in data_typ.dtype.arr_types]
    mmka__zqp = DataFrameType(tuple(lukm__apuhv + [colnames_index_typ]),
        index_typ, None, is_table_format=True)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup, index, col_names = args
        parent = None
        dbsq__cxq = construct_dataframe(context, builder, df_type, data_tup,
            index, parent, col_names)
        context.nrt.incref(builder, data_typ, data_tup)
        context.nrt.incref(builder, index_typ, index)
        context.nrt.incref(builder, colnames_index_typ, col_names)
        return dbsq__cxq
    sig = signature(mmka__zqp, data_typ, index_typ, colnames_index_typ)
    return sig, codegen


@intrinsic
def init_dataframe(typingctx, data_tup_typ, index_typ, col_names_typ):
    assert is_pd_index_type(index_typ) or isinstance(index_typ, MultiIndexType
        ), 'init_dataframe(): invalid index type'
    ejrr__owany = len(data_tup_typ.types)
    if ejrr__owany == 0:
        column_names = ()
    kbmo__bdua = col_names_typ.instance_type if isinstance(col_names_typ,
        types.TypeRef) else col_names_typ
    assert isinstance(kbmo__bdua, ColNamesMetaType) and isinstance(kbmo__bdua
        .meta, tuple
        ), 'Third argument to init_dataframe must be of type ColNamesMetaType, and must contain a tuple of column names'
    column_names = kbmo__bdua.meta
    if ejrr__owany == 1 and isinstance(data_tup_typ.types[0], TableType):
        ejrr__owany = len(data_tup_typ.types[0].arr_types)
    assert len(column_names
        ) == ejrr__owany, 'init_dataframe(): number of column names does not match number of columns'
    is_table_format = False
    nldcs__ohohy = data_tup_typ.types
    if ejrr__owany != 0 and isinstance(data_tup_typ.types[0], TableType):
        nldcs__ohohy = data_tup_typ.types[0].arr_types
        is_table_format = True
    mmka__zqp = DataFrameType(nldcs__ohohy, index_typ, column_names,
        is_table_format=is_table_format)

    def codegen(context, builder, signature, args):
        df_type = signature.return_type
        data_tup = args[0]
        index_val = args[1]
        parent = None
        if is_table_format:
            get__zrfaa = cgutils.create_struct_proxy(mmka__zqp.table_type)(
                context, builder, builder.extract_value(data_tup, 0))
            parent = get__zrfaa.parent
        dbsq__cxq = construct_dataframe(context, builder, df_type, data_tup,
            index_val, parent, None)
        context.nrt.incref(builder, data_tup_typ, data_tup)
        context.nrt.incref(builder, index_typ, index_val)
        return dbsq__cxq
    sig = signature(mmka__zqp, data_tup_typ, index_typ, col_names_typ)
    return sig, codegen


@intrinsic
def has_parent(typingctx, df=None):
    check_runtime_cols_unsupported(df, 'has_parent')

    def codegen(context, builder, sig, args):
        csh__ulnki = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        return cgutils.is_not_null(builder, csh__ulnki.parent)
    return signature(types.bool_, df), codegen


@intrinsic
def _column_needs_unboxing(typingctx, df_typ, i_typ=None):
    check_runtime_cols_unsupported(df_typ, '_column_needs_unboxing')
    assert isinstance(df_typ, DataFrameType) and is_overload_constant_int(i_typ
        )

    def codegen(context, builder, sig, args):
        bqw__fvdye = get_dataframe_payload(context, builder, df_typ, args[0])
        bsm__kfap = get_overload_const_int(i_typ)
        arr_typ = df_typ.data[bsm__kfap]
        if df_typ.is_table_format:
            get__zrfaa = cgutils.create_struct_proxy(df_typ.table_type)(context
                , builder, builder.extract_value(bqw__fvdye.data, 0))
            yirt__lrrxu = df_typ.table_type.type_to_blk[arr_typ]
            dae__mgg = getattr(get__zrfaa, f'block_{yirt__lrrxu}')
            hwhq__zvpe = ListInstance(context, builder, types.List(arr_typ),
                dae__mgg)
            bwki__appse = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[bsm__kfap])
            ivb__wamy = hwhq__zvpe.getitem(bwki__appse)
        else:
            ivb__wamy = builder.extract_value(bqw__fvdye.data, bsm__kfap)
        wcfx__facnl = cgutils.alloca_once_value(builder, ivb__wamy)
        arg__godm = cgutils.alloca_once_value(builder, context.
            get_constant_null(arr_typ))
        return is_ll_eq(builder, wcfx__facnl, arg__godm)
    return signature(types.bool_, df_typ, i_typ), codegen


def get_dataframe_payload(context, builder, df_type, value):
    wvks__osygz = cgutils.create_struct_proxy(df_type)(context, builder, value
        ).meminfo
    payload_type = DataFramePayloadType(df_type)
    payload = context.nrt.meminfo_data(builder, wvks__osygz)
    swy__qetkl = context.get_value_type(payload_type).as_pointer()
    payload = builder.bitcast(payload, swy__qetkl)
    return context.make_helper(builder, payload_type, ref=payload)


@intrinsic
def _get_dataframe_data(typingctx, df_typ=None):
    check_runtime_cols_unsupported(df_typ, '_get_dataframe_data')
    mmka__zqp = types.Tuple(df_typ.data)
    if df_typ.is_table_format:
        mmka__zqp = types.Tuple([TableType(df_typ.data)])
    sig = signature(mmka__zqp, df_typ)

    def codegen(context, builder, signature, args):
        bqw__fvdye = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, signature.return_type,
            bqw__fvdye.data)
    return sig, codegen


@intrinsic
def get_dataframe_index(typingctx, df_typ=None):

    def codegen(context, builder, signature, args):
        bqw__fvdye = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.index, bqw__fvdye
            .index)
    mmka__zqp = df_typ.index
    sig = signature(mmka__zqp, df_typ)
    return sig, codegen


def get_dataframe_data(df, i):
    return df[i]


@infer_global(get_dataframe_data)
class GetDataFrameDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 2
        if not is_overload_constant_int(args[1]):
            raise_bodo_error(
                'Selecting a DataFrame column requires a constant column label'
                )
        df = args[0]
        check_runtime_cols_unsupported(df, 'get_dataframe_data')
        i = get_overload_const_int(args[1])
        qwz__abl = df.data[i]
        return qwz__abl(*args)


GetDataFrameDataInfer.prefer_literal = True


def get_dataframe_data_impl(df, i):
    if df.is_table_format:

        def _impl(df, i):
            if has_parent(df) and _column_needs_unboxing(df, i):
                bodo.hiframes.boxing.unbox_dataframe_column(df, i)
            return get_table_data(_get_dataframe_data(df)[0], i)
        return _impl

    def _impl(df, i):
        if has_parent(df) and _column_needs_unboxing(df, i):
            bodo.hiframes.boxing.unbox_dataframe_column(df, i)
        return _get_dataframe_data(df)[i]
    return _impl


@intrinsic
def get_dataframe_table(typingctx, df_typ=None):
    assert df_typ.is_table_format, 'get_dataframe_table() expects table format'

    def codegen(context, builder, signature, args):
        bqw__fvdye = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.table_type,
            builder.extract_value(bqw__fvdye.data, 0))
    return df_typ.table_type(df_typ), codegen


def get_dataframe_all_data(df):
    return df.data


def get_dataframe_all_data_impl(df):
    if df.is_table_format:

        def _impl(df):
            return get_dataframe_table(df)
        return _impl
    data = ', '.join(
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})' for i in
        range(len(df.columns)))
    jcnjh__eqlex = ',' if len(df.columns) > 1 else ''
    return eval(f'lambda df: ({data}{jcnjh__eqlex})', {'bodo': bodo})


@infer_global(get_dataframe_all_data)
class GetDataFrameAllDataInfer(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        df_type = args[0]
        check_runtime_cols_unsupported(df_type, 'get_dataframe_data')
        qwz__abl = (df_type.table_type if df_type.is_table_format else
            types.BaseTuple.from_types(df_type.data))
        return qwz__abl(*args)


@lower_builtin(get_dataframe_all_data, DataFrameType)
def lower_get_dataframe_all_data(context, builder, sig, args):
    impl = get_dataframe_all_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


@intrinsic
def get_dataframe_column_names(typingctx, df_typ=None):
    assert df_typ.has_runtime_cols, 'get_dataframe_column_names() expects columns to be determined at runtime'

    def codegen(context, builder, signature, args):
        bqw__fvdye = get_dataframe_payload(context, builder, signature.args
            [0], args[0])
        return impl_ret_borrowed(context, builder, df_typ.
            runtime_colname_typ, bqw__fvdye.columns)
    return df_typ.runtime_colname_typ(df_typ), codegen


@lower_builtin(get_dataframe_data, DataFrameType, types.IntegerLiteral)
def lower_get_dataframe_data(context, builder, sig, args):
    impl = get_dataframe_data_impl(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['get_dataframe_data',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_index',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_table',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_dataframe_all_data',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_dummy_func


def alias_ext_init_dataframe(lhs_name, args, alias_map, arg_aliases):
    assert len(args) == 3
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)
    numba.core.ir_utils._add_alias(lhs_name, args[1].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_dataframe',
    'bodo.hiframes.pd_dataframe_ext'] = alias_ext_init_dataframe


def init_dataframe_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 3 and not kws
    data_tup = args[0]
    index = args[1]
    aghl__vkf = self.typemap[data_tup.name]
    if any(is_tuple_like_type(fimmx__moe) for fimmx__moe in aghl__vkf.types):
        return None
    if equiv_set.has_shape(data_tup):
        alvnl__vrsyz = equiv_set.get_shape(data_tup)
        if len(alvnl__vrsyz) > 1:
            equiv_set.insert_equiv(*alvnl__vrsyz)
        if len(alvnl__vrsyz) > 0:
            gmjjj__qoe = self.typemap[index.name]
            if not isinstance(gmjjj__qoe, HeterogeneousIndexType
                ) and equiv_set.has_shape(index):
                equiv_set.insert_equiv(alvnl__vrsyz[0], index)
            return ArrayAnalysis.AnalyzeResult(shape=(alvnl__vrsyz[0], len(
                alvnl__vrsyz)), pre=[])
    return None


(ArrayAnalysis._analyze_op_call_bodo_hiframes_pd_dataframe_ext_init_dataframe
    ) = init_dataframe_equiv


def get_dataframe_data_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    zvt__jva = args[0]
    data_types = self.typemap[zvt__jva.name].data
    if any(is_tuple_like_type(fimmx__moe) for fimmx__moe in data_types):
        return None
    if equiv_set.has_shape(zvt__jva):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            zvt__jva)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_data
    ) = get_dataframe_data_equiv


def get_dataframe_index_equiv(self, scope, equiv_set, loc, args, kws):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    assert len(args) == 1 and not kws
    zvt__jva = args[0]
    gmjjj__qoe = self.typemap[zvt__jva.name].index
    if isinstance(gmjjj__qoe, HeterogeneousIndexType):
        return None
    if equiv_set.has_shape(zvt__jva):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            zvt__jva)[0], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_index
    ) = get_dataframe_index_equiv


def get_dataframe_table_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    zvt__jva = args[0]
    if equiv_set.has_shape(zvt__jva):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            zvt__jva), pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_table
    ) = get_dataframe_table_equiv


def get_dataframe_column_names_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 1 and not kws
    zvt__jva = args[0]
    if equiv_set.has_shape(zvt__jva):
        return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
            zvt__jva)[1], pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_dataframe_ext_get_dataframe_column_names
    ) = get_dataframe_column_names_equiv


@intrinsic
def set_dataframe_data(typingctx, df_typ, c_ind_typ, arr_typ=None):
    check_runtime_cols_unsupported(df_typ, 'set_dataframe_data')
    assert is_overload_constant_int(c_ind_typ)
    bsm__kfap = get_overload_const_int(c_ind_typ)
    if df_typ.data[bsm__kfap] != arr_typ:
        raise BodoError(
            'Changing dataframe column data type inplace is not supported in conditionals/loops or for dataframe arguments'
            )

    def codegen(context, builder, signature, args):
        vibzz__aqsjy, gbc__dkw, ysdfh__zva = args
        bqw__fvdye = get_dataframe_payload(context, builder, df_typ,
            vibzz__aqsjy)
        if df_typ.is_table_format:
            get__zrfaa = cgutils.create_struct_proxy(df_typ.table_type)(context
                , builder, builder.extract_value(bqw__fvdye.data, 0))
            yirt__lrrxu = df_typ.table_type.type_to_blk[arr_typ]
            dae__mgg = getattr(get__zrfaa, f'block_{yirt__lrrxu}')
            hwhq__zvpe = ListInstance(context, builder, types.List(arr_typ),
                dae__mgg)
            bwki__appse = context.get_constant(types.int64, df_typ.
                table_type.block_offsets[bsm__kfap])
            hwhq__zvpe.setitem(bwki__appse, ysdfh__zva, True)
        else:
            ivb__wamy = builder.extract_value(bqw__fvdye.data, bsm__kfap)
            context.nrt.decref(builder, df_typ.data[bsm__kfap], ivb__wamy)
            bqw__fvdye.data = builder.insert_value(bqw__fvdye.data,
                ysdfh__zva, bsm__kfap)
            context.nrt.incref(builder, arr_typ, ysdfh__zva)
        csh__ulnki = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=vibzz__aqsjy)
        payload_type = DataFramePayloadType(df_typ)
        zxya__exele = context.nrt.meminfo_data(builder, csh__ulnki.meminfo)
        swy__qetkl = context.get_value_type(payload_type).as_pointer()
        zxya__exele = builder.bitcast(zxya__exele, swy__qetkl)
        builder.store(bqw__fvdye._getvalue(), zxya__exele)
        return impl_ret_borrowed(context, builder, df_typ, vibzz__aqsjy)
    sig = signature(df_typ, df_typ, c_ind_typ, arr_typ)
    return sig, codegen


@intrinsic
def set_df_index(typingctx, df_t, index_t=None):
    check_runtime_cols_unsupported(df_t, 'set_df_index')

    def codegen(context, builder, signature, args):
        esz__ardym = args[0]
        index_val = args[1]
        df_typ = signature.args[0]
        ihzs__seng = cgutils.create_struct_proxy(df_typ)(context, builder,
            value=esz__ardym)
        wyzhy__rwept = get_dataframe_payload(context, builder, df_typ,
            esz__ardym)
        csh__ulnki = construct_dataframe(context, builder, signature.
            return_type, wyzhy__rwept.data, index_val, ihzs__seng.parent, None)
        context.nrt.incref(builder, index_t, index_val)
        context.nrt.incref(builder, types.Tuple(df_t.data), wyzhy__rwept.data)
        return csh__ulnki
    mmka__zqp = DataFrameType(df_t.data, index_t, df_t.columns, df_t.dist,
        df_t.is_table_format)
    sig = signature(mmka__zqp, df_t, index_t)
    return sig, codegen


@intrinsic
def set_df_column_with_reflect(typingctx, df_type, cname_type, arr_type=None):
    check_runtime_cols_unsupported(df_type, 'set_df_column_with_reflect')
    assert is_literal_type(cname_type), 'constant column name expected'
    col_name = get_literal_value(cname_type)
    ejrr__owany = len(df_type.columns)
    juh__mkqgh = ejrr__owany
    hoj__xnk = df_type.data
    column_names = df_type.columns
    index_typ = df_type.index
    ykk__vcwm = col_name not in df_type.columns
    bsm__kfap = ejrr__owany
    if ykk__vcwm:
        hoj__xnk += arr_type,
        column_names += col_name,
        juh__mkqgh += 1
    else:
        bsm__kfap = df_type.columns.index(col_name)
        hoj__xnk = tuple(arr_type if i == bsm__kfap else hoj__xnk[i] for i in
            range(ejrr__owany))

    def codegen(context, builder, signature, args):
        vibzz__aqsjy, gbc__dkw, ysdfh__zva = args
        in_dataframe_payload = get_dataframe_payload(context, builder,
            df_type, vibzz__aqsjy)
        hke__ias = cgutils.create_struct_proxy(df_type)(context, builder,
            value=vibzz__aqsjy)
        if df_type.is_table_format:
            hydys__ptycr = df_type.table_type
            agh__oexng = builder.extract_value(in_dataframe_payload.data, 0)
            duz__kzz = TableType(hoj__xnk)
            fyrx__bdt = set_table_data_codegen(context, builder,
                hydys__ptycr, agh__oexng, duz__kzz, arr_type, ysdfh__zva,
                bsm__kfap, ykk__vcwm)
            data_tup = context.make_tuple(builder, types.Tuple([duz__kzz]),
                [fyrx__bdt])
        else:
            nldcs__ohohy = [(builder.extract_value(in_dataframe_payload.
                data, i) if i != bsm__kfap else ysdfh__zva) for i in range(
                ejrr__owany)]
            if ykk__vcwm:
                nldcs__ohohy.append(ysdfh__zva)
            for zvt__jva, xgq__fsbgf in zip(nldcs__ohohy, hoj__xnk):
                context.nrt.incref(builder, xgq__fsbgf, zvt__jva)
            data_tup = context.make_tuple(builder, types.Tuple(hoj__xnk),
                nldcs__ohohy)
        index_val = in_dataframe_payload.index
        context.nrt.incref(builder, index_typ, index_val)
        qyvv__aac = construct_dataframe(context, builder, signature.
            return_type, data_tup, index_val, hke__ias.parent, None)
        if not ykk__vcwm and arr_type == df_type.data[bsm__kfap]:
            decref_df_data(context, builder, in_dataframe_payload, df_type)
            payload_type = DataFramePayloadType(df_type)
            zxya__exele = context.nrt.meminfo_data(builder, hke__ias.meminfo)
            swy__qetkl = context.get_value_type(payload_type).as_pointer()
            zxya__exele = builder.bitcast(zxya__exele, swy__qetkl)
            qrpp__fuywf = get_dataframe_payload(context, builder, df_type,
                qyvv__aac)
            builder.store(qrpp__fuywf._getvalue(), zxya__exele)
            context.nrt.incref(builder, index_typ, index_val)
            if df_type.is_table_format:
                context.nrt.incref(builder, duz__kzz, builder.extract_value
                    (data_tup, 0))
            else:
                for zvt__jva, xgq__fsbgf in zip(nldcs__ohohy, hoj__xnk):
                    context.nrt.incref(builder, xgq__fsbgf, zvt__jva)
        has_parent = cgutils.is_not_null(builder, hke__ias.parent)
        with builder.if_then(has_parent):
            yko__eqb = context.get_python_api(builder)
            gjwx__bgjc = yko__eqb.gil_ensure()
            jjp__juv = context.get_env_manager(builder)
            context.nrt.incref(builder, arr_type, ysdfh__zva)
            qqoy__lyyaj = numba.core.pythonapi._BoxContext(context, builder,
                yko__eqb, jjp__juv)
            ummu__tbe = qqoy__lyyaj.pyapi.from_native_value(arr_type,
                ysdfh__zva, qqoy__lyyaj.env_manager)
            if isinstance(col_name, str):
                yuv__zqm = context.insert_const_string(builder.module, col_name
                    )
                fsasn__ebji = yko__eqb.string_from_string(yuv__zqm)
            else:
                assert isinstance(col_name, int)
                fsasn__ebji = yko__eqb.long_from_longlong(context.
                    get_constant(types.intp, col_name))
            yko__eqb.object_setitem(hke__ias.parent, fsasn__ebji, ummu__tbe)
            yko__eqb.decref(ummu__tbe)
            yko__eqb.decref(fsasn__ebji)
            yko__eqb.gil_release(gjwx__bgjc)
        return qyvv__aac
    mmka__zqp = DataFrameType(hoj__xnk, index_typ, column_names, df_type.
        dist, df_type.is_table_format)
    sig = signature(mmka__zqp, df_type, cname_type, arr_type)
    return sig, codegen


@lower_constant(DataFrameType)
def lower_constant_dataframe(context, builder, df_type, pyval):
    check_runtime_cols_unsupported(df_type, 'lowering a constant DataFrame')
    ejrr__owany = len(pyval.columns)
    nldcs__ohohy = []
    for i in range(ejrr__owany):
        thx__tntr = pyval.iloc[:, i]
        if isinstance(df_type.data[i], bodo.DatetimeArrayType):
            ummu__tbe = thx__tntr.array
        else:
            ummu__tbe = thx__tntr.values
        nldcs__ohohy.append(ummu__tbe)
    nldcs__ohohy = tuple(nldcs__ohohy)
    if df_type.is_table_format:
        get__zrfaa = context.get_constant_generic(builder, df_type.
            table_type, Table(nldcs__ohohy))
        data_tup = lir.Constant.literal_struct([get__zrfaa])
    else:
        data_tup = lir.Constant.literal_struct([context.
            get_constant_generic(builder, df_type.data[i], lwy__euvm) for i,
            lwy__euvm in enumerate(nldcs__ohohy)])
    index_val = context.get_constant_generic(builder, df_type.index, pyval.
        index)
    hqp__hyn = context.get_constant_null(types.pyobject)
    payload = lir.Constant.literal_struct([data_tup, index_val, hqp__hyn])
    payload = cgutils.global_constant(builder, '.const.payload', payload
        ).bitcast(cgutils.voidptr_t)
    iht__gagsk = context.get_constant(types.int64, -1)
    qksz__oeabe = context.get_constant_null(types.voidptr)
    wvks__osygz = lir.Constant.literal_struct([iht__gagsk, qksz__oeabe,
        qksz__oeabe, payload, iht__gagsk])
    wvks__osygz = cgutils.global_constant(builder, '.const.meminfo',
        wvks__osygz).bitcast(cgutils.voidptr_t)
    return lir.Constant.literal_struct([wvks__osygz, hqp__hyn])


@lower_cast(DataFrameType, DataFrameType)
def cast_df_to_df(context, builder, fromty, toty, val):
    if (fromty.data == toty.data and fromty.index == toty.index and fromty.
        columns == toty.columns and fromty.is_table_format == toty.
        is_table_format and fromty.dist != toty.dist and fromty.
        has_runtime_cols == toty.has_runtime_cols):
        return val
    if not fromty.has_runtime_cols and not toty.has_runtime_cols and len(fromty
        .data) == 0 and len(toty.columns):
        return _cast_empty_df(context, builder, toty)
    if len(fromty.data) != len(toty.data) or fromty.data != toty.data and any(
        context.typing_context.unify_pairs(fromty.data[i], toty.data[i]) is
        None for i in range(len(fromty.data))
        ) or fromty.has_runtime_cols != toty.has_runtime_cols:
        raise BodoError(f'Invalid dataframe cast from {fromty} to {toty}')
    in_dataframe_payload = get_dataframe_payload(context, builder, fromty, val)
    if isinstance(fromty.index, RangeIndexType) and isinstance(toty.index,
        NumericIndexType):
        whlz__brt = context.cast(builder, in_dataframe_payload.index,
            fromty.index, toty.index)
    else:
        whlz__brt = in_dataframe_payload.index
        context.nrt.incref(builder, fromty.index, whlz__brt)
    if (fromty.is_table_format == toty.is_table_format and fromty.data ==
        toty.data):
        wxu__suy = in_dataframe_payload.data
        if fromty.is_table_format:
            context.nrt.incref(builder, types.Tuple([fromty.table_type]),
                wxu__suy)
        else:
            context.nrt.incref(builder, types.BaseTuple.from_types(fromty.
                data), wxu__suy)
    elif not fromty.is_table_format and toty.is_table_format:
        wxu__suy = _cast_df_data_to_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and not toty.is_table_format:
        wxu__suy = _cast_df_data_to_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    elif fromty.is_table_format and toty.is_table_format:
        wxu__suy = _cast_df_data_keep_table_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    else:
        wxu__suy = _cast_df_data_keep_tuple_format(context, builder, fromty,
            toty, val, in_dataframe_payload)
    return construct_dataframe(context, builder, toty, wxu__suy, whlz__brt,
        in_dataframe_payload.parent, None)


def _cast_empty_df(context, builder, toty):
    rpbxk__dgs = {}
    if isinstance(toty.index, RangeIndexType):
        index = 'bodo.hiframes.pd_index_ext.init_range_index(0, 0, 1, None)'
    else:
        lxv__xuo = get_index_data_arr_types(toty.index)[0]
        vgahn__hhxnx = bodo.utils.transform.get_type_alloc_counts(lxv__xuo) - 1
        izip__xmph = ', '.join('0' for gbc__dkw in range(vgahn__hhxnx))
        index = (
            'bodo.utils.conversion.index_from_array(bodo.utils.utils.alloc_type(0, index_arr_type, ({}{})))'
            .format(izip__xmph, ', ' if vgahn__hhxnx == 1 else ''))
        rpbxk__dgs['index_arr_type'] = lxv__xuo
    tshsf__iusv = []
    for i, arr_typ in enumerate(toty.data):
        vgahn__hhxnx = bodo.utils.transform.get_type_alloc_counts(arr_typ) - 1
        izip__xmph = ', '.join('0' for gbc__dkw in range(vgahn__hhxnx))
        gqweg__kzhu = ('bodo.utils.utils.alloc_type(0, arr_type{}, ({}{}))'
            .format(i, izip__xmph, ', ' if vgahn__hhxnx == 1 else ''))
        tshsf__iusv.append(gqweg__kzhu)
        rpbxk__dgs[f'arr_type{i}'] = arr_typ
    tshsf__iusv = ', '.join(tshsf__iusv)
    dxh__ulce = 'def impl():\n'
    fgk__douw = bodo.hiframes.dataframe_impl._gen_init_df(dxh__ulce, toty.
        columns, tshsf__iusv, index, rpbxk__dgs)
    df = context.compile_internal(builder, fgk__douw, toty(), [])
    return df


def _cast_df_data_to_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame to table format')
    oqfqd__uvmra = toty.table_type
    get__zrfaa = cgutils.create_struct_proxy(oqfqd__uvmra)(context, builder)
    get__zrfaa.parent = in_dataframe_payload.parent
    for fimmx__moe, yirt__lrrxu in oqfqd__uvmra.type_to_blk.items():
        hyytr__cha = context.get_constant(types.int64, len(oqfqd__uvmra.
            block_to_arr_ind[yirt__lrrxu]))
        gbc__dkw, pvwgz__mzyv = ListInstance.allocate_ex(context, builder,
            types.List(fimmx__moe), hyytr__cha)
        pvwgz__mzyv.size = hyytr__cha
        setattr(get__zrfaa, f'block_{yirt__lrrxu}', pvwgz__mzyv.value)
    for i, fimmx__moe in enumerate(fromty.data):
        fnvin__vst = toty.data[i]
        if fimmx__moe != fnvin__vst:
            bghga__lxrk = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*bghga__lxrk)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        ivb__wamy = builder.extract_value(in_dataframe_payload.data, i)
        if fimmx__moe != fnvin__vst:
            vynq__cvfot = context.cast(builder, ivb__wamy, fimmx__moe,
                fnvin__vst)
            mqpk__fruxd = False
        else:
            vynq__cvfot = ivb__wamy
            mqpk__fruxd = True
        yirt__lrrxu = oqfqd__uvmra.type_to_blk[fimmx__moe]
        dae__mgg = getattr(get__zrfaa, f'block_{yirt__lrrxu}')
        hwhq__zvpe = ListInstance(context, builder, types.List(fimmx__moe),
            dae__mgg)
        bwki__appse = context.get_constant(types.int64, oqfqd__uvmra.
            block_offsets[i])
        hwhq__zvpe.setitem(bwki__appse, vynq__cvfot, mqpk__fruxd)
    data_tup = context.make_tuple(builder, types.Tuple([oqfqd__uvmra]), [
        get__zrfaa._getvalue()])
    return data_tup


def _cast_df_data_keep_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting traditional DataFrame columns')
    nldcs__ohohy = []
    for i in range(len(fromty.data)):
        if fromty.data[i] != toty.data[i]:
            bghga__lxrk = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*bghga__lxrk)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
            ivb__wamy = builder.extract_value(in_dataframe_payload.data, i)
            vynq__cvfot = context.cast(builder, ivb__wamy, fromty.data[i],
                toty.data[i])
            mqpk__fruxd = False
        else:
            vynq__cvfot = builder.extract_value(in_dataframe_payload.data, i)
            mqpk__fruxd = True
        if mqpk__fruxd:
            context.nrt.incref(builder, toty.data[i], vynq__cvfot)
        nldcs__ohohy.append(vynq__cvfot)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), nldcs__ohohy
        )
    return data_tup


def _cast_df_data_keep_table_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(toty,
        'casting table format DataFrame columns')
    hydys__ptycr = fromty.table_type
    agh__oexng = cgutils.create_struct_proxy(hydys__ptycr)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    duz__kzz = toty.table_type
    fyrx__bdt = cgutils.create_struct_proxy(duz__kzz)(context, builder)
    fyrx__bdt.parent = in_dataframe_payload.parent
    for fimmx__moe, yirt__lrrxu in duz__kzz.type_to_blk.items():
        hyytr__cha = context.get_constant(types.int64, len(duz__kzz.
            block_to_arr_ind[yirt__lrrxu]))
        gbc__dkw, pvwgz__mzyv = ListInstance.allocate_ex(context, builder,
            types.List(fimmx__moe), hyytr__cha)
        pvwgz__mzyv.size = hyytr__cha
        setattr(fyrx__bdt, f'block_{yirt__lrrxu}', pvwgz__mzyv.value)
    for i in range(len(fromty.data)):
        kld__ocufw = fromty.data[i]
        fnvin__vst = toty.data[i]
        if kld__ocufw != fnvin__vst:
            bghga__lxrk = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*bghga__lxrk)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        bvyw__mep = hydys__ptycr.type_to_blk[kld__ocufw]
        evcqr__inbvq = getattr(agh__oexng, f'block_{bvyw__mep}')
        dkf__arf = ListInstance(context, builder, types.List(kld__ocufw),
            evcqr__inbvq)
        zfcee__eipj = context.get_constant(types.int64, hydys__ptycr.
            block_offsets[i])
        ivb__wamy = dkf__arf.getitem(zfcee__eipj)
        if kld__ocufw != fnvin__vst:
            vynq__cvfot = context.cast(builder, ivb__wamy, kld__ocufw,
                fnvin__vst)
            mqpk__fruxd = False
        else:
            vynq__cvfot = ivb__wamy
            mqpk__fruxd = True
        jbbmu__xkgi = duz__kzz.type_to_blk[fimmx__moe]
        pvwgz__mzyv = getattr(fyrx__bdt, f'block_{jbbmu__xkgi}')
        ehn__mdu = ListInstance(context, builder, types.List(fnvin__vst),
            pvwgz__mzyv)
        fxp__rcq = context.get_constant(types.int64, duz__kzz.block_offsets[i])
        ehn__mdu.setitem(fxp__rcq, vynq__cvfot, mqpk__fruxd)
    data_tup = context.make_tuple(builder, types.Tuple([duz__kzz]), [
        fyrx__bdt._getvalue()])
    return data_tup


def _cast_df_data_to_tuple_format(context, builder, fromty, toty, df,
    in_dataframe_payload):
    check_runtime_cols_unsupported(fromty,
        'casting table format to traditional DataFrame')
    oqfqd__uvmra = fromty.table_type
    get__zrfaa = cgutils.create_struct_proxy(oqfqd__uvmra)(context, builder,
        builder.extract_value(in_dataframe_payload.data, 0))
    nldcs__ohohy = []
    for i, fimmx__moe in enumerate(toty.data):
        kld__ocufw = fromty.data[i]
        if fimmx__moe != kld__ocufw:
            bghga__lxrk = fromty, types.literal(i)
            impl = lambda df, i: bodo.hiframes.boxing.unbox_col_if_needed(df, i
                )
            sig = types.none(*bghga__lxrk)
            args = df, context.get_constant(types.int64, i)
            context.compile_internal(builder, impl, sig, args)
        yirt__lrrxu = oqfqd__uvmra.type_to_blk[kld__ocufw]
        dae__mgg = getattr(get__zrfaa, f'block_{yirt__lrrxu}')
        hwhq__zvpe = ListInstance(context, builder, types.List(kld__ocufw),
            dae__mgg)
        bwki__appse = context.get_constant(types.int64, oqfqd__uvmra.
            block_offsets[i])
        ivb__wamy = hwhq__zvpe.getitem(bwki__appse)
        if fimmx__moe != kld__ocufw:
            vynq__cvfot = context.cast(builder, ivb__wamy, kld__ocufw,
                fimmx__moe)
        else:
            vynq__cvfot = ivb__wamy
            context.nrt.incref(builder, fimmx__moe, vynq__cvfot)
        nldcs__ohohy.append(vynq__cvfot)
    data_tup = context.make_tuple(builder, types.Tuple(toty.data), nldcs__ohohy
        )
    return data_tup


@overload(pd.DataFrame, inline='always', no_unliteral=True)
def pd_dataframe_overload(data=None, index=None, columns=None, dtype=None,
    copy=False):
    if not is_overload_constant_bool(copy):
        raise BodoError(
            "pd.DataFrame(): 'copy' argument should be a constant boolean")
    copy = get_overload_const(copy)
    cch__snm, tshsf__iusv, index_arg = _get_df_args(data, index, columns,
        dtype, copy)
    obo__zfrs = ColNamesMetaType(tuple(cch__snm))
    dxh__ulce = (
        'def _init_df(data=None, index=None, columns=None, dtype=None, copy=False):\n'
        )
    dxh__ulce += (
        """  return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, {}, __col_name_meta_value_pd_overload)
"""
        .format(tshsf__iusv, index_arg))
    kdchp__xde = {}
    exec(dxh__ulce, {'bodo': bodo, 'np': np,
        '__col_name_meta_value_pd_overload': obo__zfrs}, kdchp__xde)
    ayw__nrqb = kdchp__xde['_init_df']
    return ayw__nrqb


@intrinsic
def _tuple_to_table_format_decoded(typingctx, df_typ):
    assert not df_typ.is_table_format, '_tuple_to_table_format requires a tuple format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    mmka__zqp = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ
        .index, df_typ.columns, dist=df_typ.dist, is_table_format=True)
    sig = signature(mmka__zqp, df_typ)
    return sig, codegen


@intrinsic
def _table_to_tuple_format_decoded(typingctx, df_typ):
    assert df_typ.is_table_format, '_tuple_to_table_format requires a table format input'

    def codegen(context, builder, signature, args):
        return context.cast(builder, args[0], signature.args[0], signature.
            return_type)
    mmka__zqp = DataFrameType(to_str_arr_if_dict_array(df_typ.data), df_typ
        .index, df_typ.columns, dist=df_typ.dist, is_table_format=False)
    sig = signature(mmka__zqp, df_typ)
    return sig, codegen


def _get_df_args(data, index, columns, dtype, copy):
    lzd__nkq = ''
    if not is_overload_none(dtype):
        lzd__nkq = '.astype(dtype)'
    index_is_none = is_overload_none(index)
    index_arg = 'bodo.utils.conversion.convert_to_index(index)'
    if isinstance(data, types.BaseTuple):
        if not data.types[0] == types.StringLiteral('__bodo_tup'):
            raise BodoError('pd.DataFrame tuple input data not supported yet')
        assert len(data.types) % 2 == 1, 'invalid const dict tuple structure'
        ejrr__owany = (len(data.types) - 1) // 2
        jwawy__mbwj = [fimmx__moe.literal_value for fimmx__moe in data.
            types[1:ejrr__owany + 1]]
        data_val_types = dict(zip(jwawy__mbwj, data.types[ejrr__owany + 1:]))
        nldcs__ohohy = ['data[{}]'.format(i) for i in range(ejrr__owany + 1,
            2 * ejrr__owany + 1)]
        data_dict = dict(zip(jwawy__mbwj, nldcs__ohohy))
        if is_overload_none(index):
            for i, fimmx__moe in enumerate(data.types[ejrr__owany + 1:]):
                if isinstance(fimmx__moe, SeriesType):
                    index_arg = (
                        'bodo.hiframes.pd_series_ext.get_series_index(data[{}])'
                        .format(ejrr__owany + 1 + i))
                    index_is_none = False
                    break
    elif is_overload_none(data):
        data_dict = {}
        data_val_types = {}
    else:
        if not (isinstance(data, types.Array) and data.ndim == 2):
            raise BodoError(
                'pd.DataFrame() only supports constant dictionary and array input'
                )
        if is_overload_none(columns):
            raise BodoError(
                "pd.DataFrame() 'columns' argument is required when an array is passed as data"
                )
        xwo__sczn = '.copy()' if copy else ''
        iko__hucl = get_overload_const_list(columns)
        ejrr__owany = len(iko__hucl)
        data_val_types = {qqoy__lyyaj: data.copy(ndim=1) for qqoy__lyyaj in
            iko__hucl}
        nldcs__ohohy = ['data[:,{}]{}'.format(i, xwo__sczn) for i in range(
            ejrr__owany)]
        data_dict = dict(zip(iko__hucl, nldcs__ohohy))
    if is_overload_none(columns):
        col_names = data_dict.keys()
    else:
        col_names = get_overload_const_list(columns)
    df_len = _get_df_len_from_info(data_dict, data_val_types, col_names,
        index_is_none, index_arg)
    _fill_null_arrays(data_dict, col_names, df_len, dtype)
    if index_is_none:
        if is_overload_none(data):
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_binary_str_index(bodo.libs.str_arr_ext.pre_alloc_string_array(0, 0))'
                )
        else:
            index_arg = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, {}, 1, None)'
                .format(df_len))
    tshsf__iusv = '({},)'.format(', '.join(
        'bodo.utils.conversion.coerce_to_array({}, True, scalar_to_arr_len={}){}'
        .format(data_dict[qqoy__lyyaj], df_len, lzd__nkq) for qqoy__lyyaj in
        col_names))
    if len(col_names) == 0:
        tshsf__iusv = '()'
    return col_names, tshsf__iusv, index_arg


def _get_df_len_from_info(data_dict, data_val_types, col_names,
    index_is_none, index_arg):
    df_len = '0'
    for qqoy__lyyaj in col_names:
        if qqoy__lyyaj in data_dict and is_iterable_type(data_val_types[
            qqoy__lyyaj]):
            df_len = 'len({})'.format(data_dict[qqoy__lyyaj])
            break
    if df_len == '0':
        if not index_is_none:
            df_len = f'len({index_arg})'
        elif data_dict:
            raise BodoError(
                'Internal Error: Unable to determine length of DataFrame Index. If this is unexpected, please try passing an index value.'
                )
    return df_len


def _fill_null_arrays(data_dict, col_names, df_len, dtype):
    if all(qqoy__lyyaj in data_dict for qqoy__lyyaj in col_names):
        return
    if is_overload_none(dtype):
        dtype = 'bodo.string_array_type'
    else:
        dtype = 'bodo.utils.conversion.array_type_from_dtype(dtype)'
    ucuyz__xqpic = 'bodo.libs.array_kernels.gen_na_array({}, {})'.format(df_len
        , dtype)
    for qqoy__lyyaj in col_names:
        if qqoy__lyyaj not in data_dict:
            data_dict[qqoy__lyyaj] = ucuyz__xqpic


@infer_global(len)
class LenTemplate(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        assert len(args) == 1
        if isinstance(args[0], (DataFrameType, bodo.TableType)):
            return types.int64(*args)


@lower_builtin(len, DataFrameType)
def table_len_lower(context, builder, sig, args):
    impl = df_len_overload(*sig.args)
    return context.compile_internal(builder, impl, sig, args)


def df_len_overload(df):
    if not isinstance(df, DataFrameType):
        return
    if df.has_runtime_cols:

        def impl(df):
            if is_null_pointer(df._meminfo):
                return 0
            fimmx__moe = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            return len(fimmx__moe)
        return impl
    if len(df.columns) == 0:

        def impl(df):
            if is_null_pointer(df._meminfo):
                return 0
            return len(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df))
        return impl

    def impl(df):
        if is_null_pointer(df._meminfo):
            return 0
        return len(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, 0))
    return impl


@infer_global(operator.getitem)
class GetItemTuple(AbstractTemplate):
    key = operator.getitem

    def generic(self, args, kws):
        tup, idx = args
        if not isinstance(tup, types.BaseTuple) or not isinstance(idx,
            types.IntegerLiteral):
            return
        lqup__lzjt = idx.literal_value
        if isinstance(lqup__lzjt, int):
            qwz__abl = tup.types[lqup__lzjt]
        elif isinstance(lqup__lzjt, slice):
            qwz__abl = types.BaseTuple.from_types(tup.types[lqup__lzjt])
        return signature(qwz__abl, *args)


GetItemTuple.prefer_literal = True


@lower_builtin(operator.getitem, types.BaseTuple, types.IntegerLiteral)
@lower_builtin(operator.getitem, types.BaseTuple, types.SliceLiteral)
def getitem_tuple_lower(context, builder, sig, args):
    iovwq__vkf, idx = sig.args
    idx = idx.literal_value
    tup, gbc__dkw = args
    if isinstance(idx, int):
        if idx < 0:
            idx += len(iovwq__vkf)
        if not 0 <= idx < len(iovwq__vkf):
            raise IndexError('cannot index at %d in %s' % (idx, iovwq__vkf))
        sxrxm__swf = builder.extract_value(tup, idx)
    elif isinstance(idx, slice):
        lshx__dnzy = cgutils.unpack_tuple(builder, tup)[idx]
        sxrxm__swf = context.make_tuple(builder, sig.return_type, lshx__dnzy)
    else:
        raise NotImplementedError('unexpected index %r for %s' % (idx, sig.
            args[0]))
    return impl_ret_borrowed(context, builder, sig.return_type, sxrxm__swf)


def join_dummy(left_df, right_df, left_on, right_on, how, suffix_x,
    suffix_y, is_join, indicator, _bodo_na_equal, gen_cond):
    return left_df


@infer_global(join_dummy)
class JoinTyper(AbstractTemplate):

    def generic(self, args, kws):
        from bodo.hiframes.pd_dataframe_ext import DataFrameType
        from bodo.utils.typing import is_overload_str
        assert not kws
        (left_df, right_df, left_on, right_on, yhknb__aapmf, suffix_x,
            suffix_y, is_join, indicator, gbc__dkw, gbc__dkw) = args
        how = get_overload_const_str(yhknb__aapmf)
        if how == 'cross':
            data = left_df.data + right_df.data
            columns = left_df.columns + right_df.columns
            cfzsh__trm = DataFrameType(data, RangeIndexType(types.none),
                columns, is_table_format=True)
            return signature(cfzsh__trm, *args)
        left_on = get_overload_const_list(left_on)
        right_on = get_overload_const_list(right_on)
        igjw__efxi = {qqoy__lyyaj: i for i, qqoy__lyyaj in enumerate(left_on)}
        wdya__ashht = {qqoy__lyyaj: i for i, qqoy__lyyaj in enumerate(right_on)
            }
        qzmwn__wlg = set(left_on) & set(right_on)
        tybi__drpp = set(left_df.columns) & set(right_df.columns)
        tezbi__aucu = tybi__drpp - qzmwn__wlg
        conlo__xvsza = '$_bodo_index_' in left_on
        lvl__ubtui = '$_bodo_index_' in right_on
        wtby__yjv = how in {'left', 'outer'}
        vpdf__ebbqy = how in {'right', 'outer'}
        columns = []
        data = []
        if conlo__xvsza or lvl__ubtui:
            if conlo__xvsza:
                lpur__egwon = bodo.utils.typing.get_index_data_arr_types(
                    left_df.index)[0]
            else:
                lpur__egwon = left_df.data[left_df.column_index[left_on[0]]]
            if lvl__ubtui:
                jrksq__zigyf = bodo.utils.typing.get_index_data_arr_types(
                    right_df.index)[0]
            else:
                jrksq__zigyf = right_df.data[right_df.column_index[right_on[0]]
                    ]
        if conlo__xvsza and not lvl__ubtui and not is_join.literal_value:
            mbo__uls = right_on[0]
            if mbo__uls in left_df.column_index:
                columns.append(mbo__uls)
                if (jrksq__zigyf == bodo.dict_str_arr_type and lpur__egwon ==
                    bodo.string_array_type):
                    yvd__suoq = bodo.string_array_type
                else:
                    yvd__suoq = jrksq__zigyf
                data.append(yvd__suoq)
        if lvl__ubtui and not conlo__xvsza and not is_join.literal_value:
            feq__duog = left_on[0]
            if feq__duog in right_df.column_index:
                columns.append(feq__duog)
                if (lpur__egwon == bodo.dict_str_arr_type and jrksq__zigyf ==
                    bodo.string_array_type):
                    yvd__suoq = bodo.string_array_type
                else:
                    yvd__suoq = lpur__egwon
                data.append(yvd__suoq)
        for kld__ocufw, thx__tntr in zip(left_df.data, left_df.columns):
            columns.append(str(thx__tntr) + suffix_x.literal_value if 
                thx__tntr in tezbi__aucu else thx__tntr)
            if thx__tntr in qzmwn__wlg:
                if kld__ocufw == bodo.dict_str_arr_type:
                    kld__ocufw = right_df.data[right_df.column_index[thx__tntr]
                        ]
                data.append(kld__ocufw)
            else:
                if (kld__ocufw == bodo.dict_str_arr_type and thx__tntr in
                    igjw__efxi):
                    if lvl__ubtui:
                        kld__ocufw = jrksq__zigyf
                    else:
                        pqvc__mfpg = igjw__efxi[thx__tntr]
                        cfjl__fga = right_on[pqvc__mfpg]
                        kld__ocufw = right_df.data[right_df.column_index[
                            cfjl__fga]]
                if vpdf__ebbqy:
                    kld__ocufw = to_nullable_type(kld__ocufw)
                data.append(kld__ocufw)
        for kld__ocufw, thx__tntr in zip(right_df.data, right_df.columns):
            if thx__tntr not in qzmwn__wlg:
                columns.append(str(thx__tntr) + suffix_y.literal_value if 
                    thx__tntr in tezbi__aucu else thx__tntr)
                if (kld__ocufw == bodo.dict_str_arr_type and thx__tntr in
                    wdya__ashht):
                    if conlo__xvsza:
                        kld__ocufw = lpur__egwon
                    else:
                        pqvc__mfpg = wdya__ashht[thx__tntr]
                        mzth__dpgx = left_on[pqvc__mfpg]
                        kld__ocufw = left_df.data[left_df.column_index[
                            mzth__dpgx]]
                if wtby__yjv:
                    kld__ocufw = to_nullable_type(kld__ocufw)
                data.append(kld__ocufw)
        xjzs__aumb = get_overload_const_bool(indicator)
        if xjzs__aumb:
            columns.append('_merge')
            data.append(bodo.CategoricalArrayType(bodo.PDCategoricalDtype((
                'left_only', 'right_only', 'both'), bodo.string_type, False)))
        index_typ = RangeIndexType(types.none)
        zmm__walhh = False
        if conlo__xvsza and lvl__ubtui and not is_overload_str(how, 'asof'):
            index_typ = left_df.index
            zmm__walhh = True
        elif conlo__xvsza and not lvl__ubtui:
            index_typ = right_df.index
            zmm__walhh = True
        elif lvl__ubtui and not conlo__xvsza:
            index_typ = left_df.index
            zmm__walhh = True
        if zmm__walhh and isinstance(index_typ, bodo.hiframes.pd_index_ext.
            RangeIndexType):
            index_typ = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64
                )
        cfzsh__trm = DataFrameType(tuple(data), index_typ, tuple(columns),
            is_table_format=True)
        return signature(cfzsh__trm, *args)


JoinTyper._no_unliteral = True


@lower_builtin(join_dummy, types.VarArg(types.Any))
def lower_join_dummy(context, builder, sig, args):
    csh__ulnki = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return csh__ulnki._getvalue()


@overload(pd.concat, inline='always', no_unliteral=True)
def concat_overload(objs, axis=0, join='outer', join_axes=None,
    ignore_index=False, keys=None, levels=None, names=None,
    verify_integrity=False, sort=None, copy=True):
    if not is_overload_constant_int(axis):
        raise BodoError("pd.concat(): 'axis' should be a constant integer")
    if not is_overload_constant_bool(ignore_index):
        raise BodoError(
            "pd.concat(): 'ignore_index' should be a constant boolean")
    axis = get_overload_const_int(axis)
    ignore_index = is_overload_true(ignore_index)
    xsc__kmgai = dict(join=join, join_axes=join_axes, keys=keys, levels=
        levels, names=names, verify_integrity=verify_integrity, sort=sort,
        copy=copy)
    qioc__qnu = dict(join='outer', join_axes=None, keys=None, levels=None,
        names=None, verify_integrity=False, sort=None, copy=True)
    check_unsupported_args('pandas.concat', xsc__kmgai, qioc__qnu,
        package_name='pandas', module_name='General')
    dxh__ulce = """def impl(objs, axis=0, join='outer', join_axes=None, ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=None, copy=True):
"""
    if axis == 1:
        if not isinstance(objs, types.BaseTuple):
            raise_bodo_error(
                'Only tuple argument for pd.concat(axis=1) expected')
        index = (
            'bodo.hiframes.pd_index_ext.init_range_index(0, len(objs[0]), 1, None)'
            )
        zmjh__anz = 0
        tshsf__iusv = []
        names = []
        for i, tsfbu__qnte in enumerate(objs.types):
            assert isinstance(tsfbu__qnte, (SeriesType, DataFrameType))
            check_runtime_cols_unsupported(tsfbu__qnte, 'pandas.concat()')
            if isinstance(tsfbu__qnte, SeriesType):
                names.append(str(zmjh__anz))
                zmjh__anz += 1
                tshsf__iusv.append(
                    'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'
                    .format(i))
            else:
                names.extend(tsfbu__qnte.columns)
                for itmwb__bzlpj in range(len(tsfbu__qnte.data)):
                    tshsf__iusv.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, itmwb__bzlpj))
        return bodo.hiframes.dataframe_impl._gen_init_df(dxh__ulce, names,
            ', '.join(tshsf__iusv), index)
    if axis != 0:
        raise_bodo_error('pd.concat(): axis must be 0 or 1')
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        DataFrameType):
        assert all(isinstance(fimmx__moe, DataFrameType) for fimmx__moe in
            objs.types)
        twwz__yyh = []
        for df in objs.types:
            check_runtime_cols_unsupported(df, 'pandas.concat()')
            twwz__yyh.extend(df.columns)
        twwz__yyh = list(dict.fromkeys(twwz__yyh).keys())
        lukm__apuhv = {}
        for zmjh__anz, qqoy__lyyaj in enumerate(twwz__yyh):
            for i, df in enumerate(objs.types):
                if qqoy__lyyaj in df.column_index:
                    lukm__apuhv[f'arr_typ{zmjh__anz}'] = df.data[df.
                        column_index[qqoy__lyyaj]]
                    break
        assert len(lukm__apuhv) == len(twwz__yyh)
        jmfy__ddgqn = []
        for zmjh__anz, qqoy__lyyaj in enumerate(twwz__yyh):
            args = []
            for i, df in enumerate(objs.types):
                if qqoy__lyyaj in df.column_index:
                    bsm__kfap = df.column_index[qqoy__lyyaj]
                    args.append(
                        'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(objs[{}], {})'
                        .format(i, bsm__kfap))
                else:
                    args.append(
                        'bodo.libs.array_kernels.gen_na_array(len(objs[{}]), arr_typ{})'
                        .format(i, zmjh__anz))
            dxh__ulce += ('  A{} = bodo.libs.array_kernels.concat(({},))\n'
                .format(zmjh__anz, ', '.join(args)))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(A0), 1, None)'
                )
        else:
            index = (
                """bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)) if len(objs[i].
                columns) > 0)))
        return bodo.hiframes.dataframe_impl._gen_init_df(dxh__ulce,
            twwz__yyh, ', '.join('A{}'.format(i) for i in range(len(
            twwz__yyh))), index, lukm__apuhv)
    if isinstance(objs, types.BaseTuple) and isinstance(objs.types[0],
        SeriesType):
        assert all(isinstance(fimmx__moe, SeriesType) for fimmx__moe in
            objs.types)
        dxh__ulce += ('  out_arr = bodo.libs.array_kernels.concat(({},))\n'
            .format(', '.join(
            'bodo.hiframes.pd_series_ext.get_series_data(objs[{}])'.format(
            i) for i in range(len(objs.types)))))
        if ignore_index:
            dxh__ulce += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            dxh__ulce += (
                """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(({},)))
"""
                .format(', '.join(
                'bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(objs[{}]))'
                .format(i) for i in range(len(objs.types)))))
        dxh__ulce += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        kdchp__xde = {}
        exec(dxh__ulce, {'bodo': bodo, 'np': np, 'numba': numba}, kdchp__xde)
        return kdchp__xde['impl']
    if isinstance(objs, types.List) and isinstance(objs.dtype, DataFrameType):
        check_runtime_cols_unsupported(objs.dtype, 'pandas.concat()')
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(objs.
            dtype, 'pandas.concat()')
        df_type = objs.dtype
        for zmjh__anz, qqoy__lyyaj in enumerate(df_type.columns):
            dxh__ulce += '  arrs{} = []\n'.format(zmjh__anz)
            dxh__ulce += '  for i in range(len(objs)):\n'
            dxh__ulce += '    df = objs[i]\n'
            dxh__ulce += (
                """    arrs{0}.append(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {0}))
"""
                .format(zmjh__anz))
            dxh__ulce += (
                '  out_arr{0} = bodo.libs.array_kernels.concat(arrs{0})\n'.
                format(zmjh__anz))
        if ignore_index:
            index = (
                'bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr0), 1, None)'
                )
        else:
            dxh__ulce += '  arrs_index = []\n'
            dxh__ulce += '  for i in range(len(objs)):\n'
            dxh__ulce += '    df = objs[i]\n'
            dxh__ulce += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
            if objs.dtype.index.name_typ == types.none:
                name = None
            else:
                name = objs.dtype.index.name_typ.literal_value
            index = f"""bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index), {name!r})
"""
        return bodo.hiframes.dataframe_impl._gen_init_df(dxh__ulce, df_type
            .columns, ', '.join('out_arr{}'.format(i) for i in range(len(
            df_type.columns))), index)
    if isinstance(objs, types.List) and isinstance(objs.dtype, SeriesType):
        dxh__ulce += '  arrs = []\n'
        dxh__ulce += '  for i in range(len(objs)):\n'
        dxh__ulce += (
            '    arrs.append(bodo.hiframes.pd_series_ext.get_series_data(objs[i]))\n'
            )
        dxh__ulce += '  out_arr = bodo.libs.array_kernels.concat(arrs)\n'
        if ignore_index:
            dxh__ulce += """  index = bodo.hiframes.pd_index_ext.init_range_index(0, len(out_arr), 1, None)
"""
        else:
            dxh__ulce += '  arrs_index = []\n'
            dxh__ulce += '  for i in range(len(objs)):\n'
            dxh__ulce += '    S = objs[i]\n'
            dxh__ulce += """    arrs_index.append(bodo.utils.conversion.index_to_array(bodo.hiframes.pd_series_ext.get_series_index(S)))
"""
            dxh__ulce += """  index = bodo.utils.conversion.index_from_array(bodo.libs.array_kernels.concat(arrs_index))
"""
        dxh__ulce += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index)\n'
            )
        kdchp__xde = {}
        exec(dxh__ulce, {'bodo': bodo, 'np': np, 'numba': numba}, kdchp__xde)
        return kdchp__xde['impl']
    raise BodoError('pd.concat(): input type {} not supported yet'.format(objs)
        )


def sort_values_dummy(df, by, ascending, inplace, na_position,
    _bodo_chunk_bounds):
    pass


@infer_global(sort_values_dummy)
class SortDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df = args[0]
        index = df.index
        if isinstance(index, bodo.hiframes.pd_index_ext.RangeIndexType):
            index = bodo.hiframes.pd_index_ext.NumericIndexType(types.int64)
        mmka__zqp = df.copy(index=index)
        return signature(mmka__zqp, *args)


SortDummyTyper._no_unliteral = True


@lower_builtin(sort_values_dummy, types.VarArg(types.Any))
def lower_sort_values_dummy(context, builder, sig, args):
    if sig.return_type == types.none:
        return
    sjlpm__nfq = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return sjlpm__nfq._getvalue()


@overload_method(DataFrameType, 'itertuples', inline='always', no_unliteral
    =True)
def itertuples_overload(df, index=True, name='Pandas'):
    check_runtime_cols_unsupported(df, 'DataFrame.itertuples()')
    xsc__kmgai = dict(index=index, name=name)
    qioc__qnu = dict(index=True, name='Pandas')
    check_unsupported_args('DataFrame.itertuples', xsc__kmgai, qioc__qnu,
        package_name='pandas', module_name='DataFrame')

    def _impl(df, index=True, name='Pandas'):
        return bodo.hiframes.pd_dataframe_ext.itertuples_dummy(df)
    return _impl


def itertuples_dummy(df):
    return df


@infer_global(itertuples_dummy)
class ItertuplesDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        df, = args
        assert 'Index' not in df.columns
        columns = ('Index',) + df.columns
        lukm__apuhv = (types.Array(types.int64, 1, 'C'),) + df.data
        caqe__mvzpu = bodo.hiframes.dataframe_impl.DataFrameTupleIterator(
            columns, lukm__apuhv)
        return signature(caqe__mvzpu, *args)


@lower_builtin(itertuples_dummy, types.VarArg(types.Any))
def lower_itertuples_dummy(context, builder, sig, args):
    sjlpm__nfq = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return sjlpm__nfq._getvalue()


def query_dummy(df, expr):
    return df.eval(expr)


@infer_global(query_dummy)
class QueryDummyTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=RangeIndexType(types
            .none)), *args)


@lower_builtin(query_dummy, types.VarArg(types.Any))
def lower_query_dummy(context, builder, sig, args):
    sjlpm__nfq = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return sjlpm__nfq._getvalue()


def val_isin_dummy(S, vals):
    return S in vals


def val_notin_dummy(S, vals):
    return S not in vals


@infer_global(val_isin_dummy)
@infer_global(val_notin_dummy)
class ValIsinTyper(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        return signature(SeriesType(types.bool_, index=args[0].index), *args)


@lower_builtin(val_isin_dummy, types.VarArg(types.Any))
@lower_builtin(val_notin_dummy, types.VarArg(types.Any))
def lower_val_isin_dummy(context, builder, sig, args):
    sjlpm__nfq = cgutils.create_struct_proxy(sig.return_type)(context, builder)
    return sjlpm__nfq._getvalue()


@numba.generated_jit(nopython=True)
def pivot_impl(index_tup, columns_tup, values_tup, pivot_values,
    index_names, columns_name, value_names, check_duplicates=True,
    is_already_shuffled=False, _constant_pivot_values=None, parallel=False):
    if not is_overload_constant_bool(check_duplicates):
        raise BodoError(
            'pivot_impl(): check_duplicates must be a constant boolean')
    fsxd__dqaao = get_overload_const_bool(check_duplicates)
    xbi__nxnfx = not get_overload_const_bool(is_already_shuffled)
    qpo__abvxp = not is_overload_none(_constant_pivot_values)
    index_names = index_names.instance_type if isinstance(index_names,
        types.TypeRef) else index_names
    columns_name = columns_name.instance_type if isinstance(columns_name,
        types.TypeRef) else columns_name
    value_names = value_names.instance_type if isinstance(value_names,
        types.TypeRef) else value_names
    _constant_pivot_values = (_constant_pivot_values.instance_type if
        isinstance(_constant_pivot_values, types.TypeRef) else
        _constant_pivot_values)
    wku__pey = len(value_names) > 1
    rioes__pvcz = None
    yhyk__jnsk = None
    qnw__pzma = None
    dni__ercyc = None
    ybb__gwp = isinstance(values_tup, types.UniTuple)
    if ybb__gwp:
        vmwct__alvpn = [to_str_arr_if_dict_array(to_nullable_type(
            values_tup.dtype))]
    else:
        vmwct__alvpn = [to_str_arr_if_dict_array(to_nullable_type(
            xgq__fsbgf)) for xgq__fsbgf in values_tup]
    dxh__ulce = 'def impl(\n'
    dxh__ulce += """    index_tup, columns_tup, values_tup, pivot_values, index_names, columns_name, value_names, check_duplicates=True, is_already_shuffled=False, _constant_pivot_values=None, parallel=False
"""
    dxh__ulce += '):\n'
    dxh__ulce += "    ev = tracing.Event('pivot_impl', is_parallel=parallel)\n"
    if xbi__nxnfx:
        dxh__ulce += '    if parallel:\n'
        dxh__ulce += (
            "        ev_shuffle = tracing.Event('shuffle_pivot_index')\n")
        uifr__yoz = ', '.join([f'array_to_info(index_tup[{i}])' for i in
            range(len(index_tup))] + [f'array_to_info(columns_tup[{i}])' for
            i in range(len(columns_tup))] + [
            f'array_to_info(values_tup[{i}])' for i in range(len(values_tup))])
        dxh__ulce += f'        info_list = [{uifr__yoz}]\n'
        dxh__ulce += '        cpp_table = arr_info_list_to_table(info_list)\n'
        dxh__ulce += f"""        out_cpp_table = shuffle_table(cpp_table, {len(index_tup)}, parallel, 0)
"""
        gfo__wut = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i}), index_tup[{i}])'
             for i in range(len(index_tup))])
        wqznh__hhtsb = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup)}), columns_tup[{i}])'
             for i in range(len(columns_tup))])
        ltile__nbp = ', '.join([
            f'info_to_array(info_from_table(out_cpp_table, {i + len(index_tup) + len(columns_tup)}), values_tup[{i}])'
             for i in range(len(values_tup))])
        dxh__ulce += f'        index_tup = ({gfo__wut},)\n'
        dxh__ulce += f'        columns_tup = ({wqznh__hhtsb},)\n'
        dxh__ulce += f'        values_tup = ({ltile__nbp},)\n'
        dxh__ulce += '        delete_table(cpp_table)\n'
        dxh__ulce += '        delete_table(out_cpp_table)\n'
        dxh__ulce += '        ev_shuffle.finalize()\n'
    dxh__ulce += '    columns_arr = columns_tup[0]\n'
    if ybb__gwp:
        dxh__ulce += '    values_arrs = [arr for arr in values_tup]\n'
    dxh__ulce += (
        "    ev_unique = tracing.Event('pivot_unique_index_map', is_parallel=parallel)\n"
        )
    dxh__ulce += """    unique_index_arr_tup, row_vector = bodo.libs.array_ops.array_unique_vector_map(
"""
    dxh__ulce += '        index_tup\n'
    dxh__ulce += '    )\n'
    dxh__ulce += '    n_rows = len(unique_index_arr_tup[0])\n'
    dxh__ulce += '    num_values_arrays = len(values_tup)\n'
    dxh__ulce += '    n_unique_pivots = len(pivot_values)\n'
    if ybb__gwp:
        dxh__ulce += '    n_cols = num_values_arrays * n_unique_pivots\n'
    else:
        dxh__ulce += '    n_cols = n_unique_pivots\n'
    dxh__ulce += '    col_map = {}\n'
    dxh__ulce += '    for i in range(n_unique_pivots):\n'
    dxh__ulce += '        if bodo.libs.array_kernels.isna(pivot_values, i):\n'
    dxh__ulce += '            raise ValueError(\n'
    dxh__ulce += """                "DataFrame.pivot(): NA values in 'columns' array not supported\"
"""
    dxh__ulce += '            )\n'
    dxh__ulce += '        col_map[pivot_values[i]] = i\n'
    dxh__ulce += '    ev_unique.finalize()\n'
    dxh__ulce += (
        "    ev_alloc = tracing.Event('pivot_alloc', is_parallel=parallel)\n")
    ezb__cvazv = False
    for i, bofct__bnf in enumerate(vmwct__alvpn):
        if is_str_arr_type(bofct__bnf):
            ezb__cvazv = True
            dxh__ulce += (
                f'    len_arrs_{i} = [np.zeros(n_rows, np.int64) for _ in range(n_cols)]\n'
                )
            dxh__ulce += f'    total_lens_{i} = np.zeros(n_cols, np.int64)\n'
    if ezb__cvazv:
        if fsxd__dqaao:
            dxh__ulce += '    nbytes = (n_rows + 7) >> 3\n'
            dxh__ulce += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
        dxh__ulce += '    for i in range(len(columns_arr)):\n'
        dxh__ulce += '        col_name = columns_arr[i]\n'
        dxh__ulce += '        pivot_idx = col_map[col_name]\n'
        dxh__ulce += '        row_idx = row_vector[i]\n'
        if fsxd__dqaao:
            dxh__ulce += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
            dxh__ulce += """        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):
"""
            dxh__ulce += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
            dxh__ulce += '        else:\n'
            dxh__ulce += """            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)
"""
        if ybb__gwp:
            dxh__ulce += '        for j in range(num_values_arrays):\n'
            dxh__ulce += (
                '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
            dxh__ulce += '            len_arr = len_arrs_0[col_idx]\n'
            dxh__ulce += '            values_arr = values_arrs[j]\n'
            dxh__ulce += (
                '            if not bodo.libs.array_kernels.isna(values_arr, i):\n'
                )
            dxh__ulce += """                str_val_len = bodo.libs.str_arr_ext.get_str_arr_item_length(values_arr, i)
"""
            dxh__ulce += '                len_arr[row_idx] = str_val_len\n'
            dxh__ulce += (
                '                total_lens_0[col_idx] += str_val_len\n')
        else:
            for i, bofct__bnf in enumerate(vmwct__alvpn):
                if is_str_arr_type(bofct__bnf):
                    dxh__ulce += f"""        if not bodo.libs.array_kernels.isna(values_tup[{i}], i):
"""
                    dxh__ulce += f"""            str_val_len_{i} = bodo.libs.str_arr_ext.get_str_arr_item_length(values_tup[{i}], i)
"""
                    dxh__ulce += (
                        f'            len_arrs_{i}[pivot_idx][row_idx] = str_val_len_{i}\n'
                        )
                    dxh__ulce += (
                        f'            total_lens_{i}[pivot_idx] += str_val_len_{i}\n'
                        )
    dxh__ulce += f"    ev_alloc.add_attribute('num_rows', n_rows)\n"
    for i, bofct__bnf in enumerate(vmwct__alvpn):
        if is_str_arr_type(bofct__bnf):
            dxh__ulce += f'    data_arrs_{i} = [\n'
            dxh__ulce += (
                '        bodo.libs.str_arr_ext.gen_na_str_array_lens(\n')
            dxh__ulce += (
                f'            n_rows, total_lens_{i}[i], len_arrs_{i}[i]\n')
            dxh__ulce += '        )\n'
            dxh__ulce += '        for i in range(n_cols)\n'
            dxh__ulce += '    ]\n'
            dxh__ulce += f'    if tracing.is_tracing():\n'
            dxh__ulce += '         for i in range(n_cols):\n'
            dxh__ulce += f"""            ev_alloc.add_attribute('total_str_chars_out_column_{i}_' + str(i), total_lens_{i}[i])
"""
        else:
            dxh__ulce += f'    data_arrs_{i} = [\n'
            dxh__ulce += (
                f'        bodo.libs.array_kernels.gen_na_array(n_rows, data_arr_typ_{i})\n'
                )
            dxh__ulce += '        for _ in range(n_cols)\n'
            dxh__ulce += '    ]\n'
    if not ezb__cvazv and fsxd__dqaao:
        dxh__ulce += '    nbytes = (n_rows + 7) >> 3\n'
        dxh__ulce += """    seen_bitmaps = [np.zeros(nbytes, np.int8) for _ in range(n_unique_pivots)]
"""
    dxh__ulce += '    ev_alloc.finalize()\n'
    dxh__ulce += (
        "    ev_fill = tracing.Event('pivot_fill_data', is_parallel=parallel)\n"
        )
    dxh__ulce += '    for i in range(len(columns_arr)):\n'
    dxh__ulce += '        col_name = columns_arr[i]\n'
    dxh__ulce += '        pivot_idx = col_map[col_name]\n'
    dxh__ulce += '        row_idx = row_vector[i]\n'
    if not ezb__cvazv and fsxd__dqaao:
        dxh__ulce += '        seen_bitmap = seen_bitmaps[pivot_idx]\n'
        dxh__ulce += (
            '        if bodo.libs.int_arr_ext.get_bit_bitmap_arr(seen_bitmap, row_idx):\n'
            )
        dxh__ulce += """            raise ValueError("DataFrame.pivot(): 'index' contains duplicate entries for the same output column")
"""
        dxh__ulce += '        else:\n'
        dxh__ulce += (
            '            bodo.libs.int_arr_ext.set_bit_to_arr(seen_bitmap, row_idx, 1)\n'
            )
    if ybb__gwp:
        dxh__ulce += '        for j in range(num_values_arrays):\n'
        dxh__ulce += (
            '            col_idx = (j * len(pivot_values)) + pivot_idx\n')
        dxh__ulce += '            col_arr = data_arrs_0[col_idx]\n'
        dxh__ulce += '            values_arr = values_arrs[j]\n'
        dxh__ulce += """            bodo.libs.array_kernels.copy_array_element(col_arr, row_idx, values_arr, i)
"""
    else:
        for i, bofct__bnf in enumerate(vmwct__alvpn):
            dxh__ulce += f'        col_arr_{i} = data_arrs_{i}[pivot_idx]\n'
            dxh__ulce += f"""        bodo.libs.array_kernels.copy_array_element(col_arr_{i}, row_idx, values_tup[{i}], i)
"""
    if len(index_names) == 1:
        dxh__ulce += """    index = bodo.utils.conversion.index_from_array(unique_index_arr_tup[0], index_names_lit)
"""
        rioes__pvcz = index_names.meta[0]
    else:
        dxh__ulce += """    index = bodo.hiframes.pd_multi_index_ext.init_multi_index(unique_index_arr_tup, index_names_lit, None)
"""
        rioes__pvcz = tuple(index_names.meta)
    dxh__ulce += f'    if tracing.is_tracing():\n'
    dxh__ulce += f'        index_nbytes = index.nbytes\n'
    dxh__ulce += f"        ev.add_attribute('index_nbytes', index_nbytes)\n"
    if not qpo__abvxp:
        qnw__pzma = columns_name.meta[0]
        if wku__pey:
            dxh__ulce += (
                f'    num_rows = {len(value_names)} * len(pivot_values)\n')
            yhyk__jnsk = value_names.meta
            if all(isinstance(qqoy__lyyaj, str) for qqoy__lyyaj in yhyk__jnsk):
                yhyk__jnsk = pd.array(yhyk__jnsk, 'string')
            elif all(isinstance(qqoy__lyyaj, int) for qqoy__lyyaj in yhyk__jnsk
                ):
                yhyk__jnsk = np.array(yhyk__jnsk, 'int64')
            else:
                raise BodoError(
                    f"pivot(): column names selected for 'values' must all share a common int or string type. Please convert your names to a common type using DataFrame.rename()"
                    )
            if isinstance(yhyk__jnsk.dtype, pd.StringDtype):
                dxh__ulce += '    total_chars = 0\n'
                dxh__ulce += f'    for i in range({len(value_names)}):\n'
                dxh__ulce += """        value_name_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(value_names_lit, i)
"""
                dxh__ulce += '        total_chars += value_name_str_len\n'
                dxh__ulce += """    new_value_names = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * len(pivot_values))
"""
            else:
                dxh__ulce += """    new_value_names = bodo.utils.utils.alloc_type(num_rows, value_names_lit, (-1,))
"""
            if is_str_arr_type(pivot_values):
                dxh__ulce += '    total_chars = 0\n'
                dxh__ulce += '    for i in range(len(pivot_values)):\n'
                dxh__ulce += """        pivot_val_str_len = bodo.libs.str_arr_ext.get_str_arr_item_length(pivot_values, i)
"""
                dxh__ulce += '        total_chars += pivot_val_str_len\n'
                dxh__ulce += f"""    new_pivot_values = bodo.libs.str_arr_ext.pre_alloc_string_array(num_rows, total_chars * {len(value_names)})
"""
            else:
                dxh__ulce += """    new_pivot_values = bodo.utils.utils.alloc_type(num_rows, pivot_values, (-1,))
"""
            dxh__ulce += f'    for i in range({len(value_names)}):\n'
            dxh__ulce += '        for j in range(len(pivot_values)):\n'
            dxh__ulce += """            new_value_names[(i * len(pivot_values)) + j] = value_names_lit[i]
"""
            dxh__ulce += """            new_pivot_values[(i * len(pivot_values)) + j] = pivot_values[j]
"""
            dxh__ulce += """    column_index = bodo.hiframes.pd_multi_index_ext.init_multi_index((new_value_names, new_pivot_values), (None, columns_name_lit), None)
"""
        else:
            dxh__ulce += """    column_index =  bodo.utils.conversion.index_from_array(pivot_values, columns_name_lit)
"""
    dxh__ulce += '    ev_fill.finalize()\n'
    oqfqd__uvmra = None
    if qpo__abvxp:
        if wku__pey:
            iygvw__qyms = []
            for sxcrz__ogyqt in _constant_pivot_values.meta:
                for hzzr__ekpci in value_names.meta:
                    iygvw__qyms.append((sxcrz__ogyqt, hzzr__ekpci))
            column_names = tuple(iygvw__qyms)
        else:
            column_names = tuple(_constant_pivot_values.meta)
        dni__ercyc = ColNamesMetaType(column_names)
        aqkng__vrqy = []
        for xgq__fsbgf in vmwct__alvpn:
            aqkng__vrqy.extend([xgq__fsbgf] * len(_constant_pivot_values))
        ipy__xjjd = tuple(aqkng__vrqy)
        oqfqd__uvmra = TableType(ipy__xjjd)
        dxh__ulce += (
            f'    table = bodo.hiframes.table.init_table(table_type, False)\n')
        dxh__ulce += (
            f'    table = bodo.hiframes.table.set_table_len(table, n_rows)\n')
        for i, xgq__fsbgf in enumerate(vmwct__alvpn):
            dxh__ulce += f"""    table = bodo.hiframes.table.set_table_block(table, data_arrs_{i}, {oqfqd__uvmra.type_to_blk[xgq__fsbgf]})
"""
        dxh__ulce += (
            '    result = bodo.hiframes.pd_dataframe_ext.init_dataframe(\n')
        dxh__ulce += '        (table,), index, columns_typ\n'
        dxh__ulce += '    )\n'
    else:
        gdoo__kabnh = ', '.join(f'data_arrs_{i}' for i in range(len(
            vmwct__alvpn)))
        dxh__ulce += f"""    table = bodo.hiframes.table.init_runtime_table_from_lists(({gdoo__kabnh},), n_rows)
"""
        dxh__ulce += (
            '    result = bodo.hiframes.pd_dataframe_ext.init_runtime_cols_dataframe(\n'
            )
        dxh__ulce += '        (table,), index, column_index\n'
        dxh__ulce += '    )\n'
    dxh__ulce += '    ev.finalize()\n'
    dxh__ulce += '    return result\n'
    kdchp__xde = {}
    fgx__ljd = {f'data_arr_typ_{i}': bofct__bnf for i, bofct__bnf in
        enumerate(vmwct__alvpn)}
    ppi__jrt = {'bodo': bodo, 'np': np, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table, 'shuffle_table':
        shuffle_table, 'info_to_array': info_to_array, 'delete_table':
        delete_table, 'info_from_table': info_from_table, 'table_type':
        oqfqd__uvmra, 'columns_typ': dni__ercyc, 'index_names_lit':
        rioes__pvcz, 'value_names_lit': yhyk__jnsk, 'columns_name_lit':
        qnw__pzma, **fgx__ljd, 'tracing': tracing}
    exec(dxh__ulce, ppi__jrt, kdchp__xde)
    impl = kdchp__xde['impl']
    return impl


def gen_pandas_parquet_metadata(column_names, data_types, index,
    write_non_range_index_to_metadata, write_rangeindex_to_metadata,
    partition_cols=None, is_runtime_columns=False):
    wmny__kqs = {}
    wmny__kqs['columns'] = []
    if partition_cols is None:
        partition_cols = []
    for col_name, tfk__zzuzk in zip(column_names, data_types):
        if col_name in partition_cols:
            continue
        gcf__bey = None
        if isinstance(tfk__zzuzk, bodo.DatetimeArrayType):
            lcjtq__irc = 'datetimetz'
            ipb__haboh = 'datetime64[ns]'
            if isinstance(tfk__zzuzk.tz, int):
                jnlee__xjvbs = (bodo.libs.pd_datetime_arr_ext.
                    nanoseconds_to_offset(tfk__zzuzk.tz))
            else:
                jnlee__xjvbs = pd.DatetimeTZDtype(tz=tfk__zzuzk.tz).tz
            gcf__bey = {'timezone': pa.lib.tzinfo_to_string(jnlee__xjvbs)}
        elif isinstance(tfk__zzuzk, types.Array
            ) or tfk__zzuzk == boolean_array:
            lcjtq__irc = ipb__haboh = tfk__zzuzk.dtype.name
            if ipb__haboh.startswith('datetime'):
                lcjtq__irc = 'datetime'
        elif is_str_arr_type(tfk__zzuzk):
            lcjtq__irc = 'unicode'
            ipb__haboh = 'object'
        elif tfk__zzuzk == binary_array_type:
            lcjtq__irc = 'bytes'
            ipb__haboh = 'object'
        elif isinstance(tfk__zzuzk, DecimalArrayType):
            lcjtq__irc = ipb__haboh = 'object'
        elif isinstance(tfk__zzuzk, IntegerArrayType):
            vkz__dyiw = tfk__zzuzk.dtype.name
            if vkz__dyiw.startswith('int'):
                ipb__haboh = 'Int' + vkz__dyiw[3:]
            elif vkz__dyiw.startswith('uint'):
                ipb__haboh = 'UInt' + vkz__dyiw[4:]
            else:
                if is_runtime_columns:
                    col_name = 'Runtime determined column of type'
                raise BodoError(
                    'to_parquet(): unknown dtype in nullable Integer column {} {}'
                    .format(col_name, tfk__zzuzk))
            lcjtq__irc = tfk__zzuzk.dtype.name
        elif isinstance(tfk__zzuzk, bodo.FloatingArrayType):
            vkz__dyiw = tfk__zzuzk.dtype.name
            lcjtq__irc = vkz__dyiw
            ipb__haboh = vkz__dyiw.capitalize()
        elif tfk__zzuzk == datetime_date_array_type:
            lcjtq__irc = 'datetime'
            ipb__haboh = 'object'
        elif isinstance(tfk__zzuzk, TimeArrayType):
            lcjtq__irc = 'datetime'
            ipb__haboh = 'object'
        elif isinstance(tfk__zzuzk, (StructArrayType, ArrayItemArrayType)):
            lcjtq__irc = 'object'
            ipb__haboh = 'object'
        else:
            if is_runtime_columns:
                col_name = 'Runtime determined column of type'
            raise BodoError(
                'to_parquet(): unsupported column type for metadata generation : {} {}'
                .format(col_name, tfk__zzuzk))
        odgnp__elq = {'name': col_name, 'field_name': col_name,
            'pandas_type': lcjtq__irc, 'numpy_type': ipb__haboh, 'metadata':
            gcf__bey}
        wmny__kqs['columns'].append(odgnp__elq)
    if write_non_range_index_to_metadata:
        if isinstance(index, MultiIndexType):
            raise BodoError('to_parquet: MultiIndex not supported yet')
        if 'none' in index.name:
            ogh__ghko = '__index_level_0__'
            fhhbi__utzxv = None
        else:
            ogh__ghko = '%s'
            fhhbi__utzxv = '%s'
        wmny__kqs['index_columns'] = [ogh__ghko]
        wmny__kqs['columns'].append({'name': fhhbi__utzxv, 'field_name':
            ogh__ghko, 'pandas_type': index.pandas_type_name, 'numpy_type':
            index.numpy_type_name, 'metadata': None})
    elif write_rangeindex_to_metadata:
        wmny__kqs['index_columns'] = [{'kind': 'range', 'name': '%s',
            'start': '%d', 'stop': '%d', 'step': '%d'}]
    else:
        wmny__kqs['index_columns'] = []
    wmny__kqs['pandas_version'] = pd.__version__
    return wmny__kqs


@overload_method(DataFrameType, 'to_parquet', no_unliteral=True)
def to_parquet_overload(df, path, engine='auto', compression='snappy',
    index=None, partition_cols=None, storage_options=None, row_group_size=-
    1, _bodo_file_prefix='part-', _bodo_timestamp_tz=None, _is_parallel=False):
    check_unsupported_args('DataFrame.to_parquet', {'storage_options':
        storage_options}, {'storage_options': None}, package_name='pandas',
        module_name='IO')
    if df.has_runtime_cols and not is_overload_none(partition_cols):
        raise BodoError(
            f"DataFrame.to_parquet(): Providing 'partition_cols' on DataFrames with columns determined at runtime is not yet supported. Please return the DataFrame to regular Python to update typing information."
            )
    if not is_overload_none(engine) and get_overload_const_str(engine) not in (
        'auto', 'pyarrow'):
        raise BodoError('DataFrame.to_parquet(): only pyarrow engine supported'
            )
    if not is_overload_none(compression) and get_overload_const_str(compression
        ) not in {'snappy', 'gzip', 'brotli'}:
        raise BodoError('to_parquet(): Unsupported compression: ' + str(
            get_overload_const_str(compression)))
    if not is_overload_none(partition_cols):
        partition_cols = get_overload_const_list(partition_cols)
        skw__pzh = []
        for eqfm__tfgim in partition_cols:
            try:
                idx = df.columns.index(eqfm__tfgim)
            except ValueError as hoitw__wxhzk:
                raise BodoError(
                    f'Partition column {eqfm__tfgim} is not in dataframe')
            skw__pzh.append(idx)
    else:
        partition_cols = None
    if not is_overload_none(index) and not is_overload_constant_bool(index):
        raise BodoError('to_parquet(): index must be a constant bool or None')
    if not is_overload_int(row_group_size):
        raise BodoError('to_parquet(): row_group_size must be integer')
    if not is_overload_none(_bodo_timestamp_tz) and (not
        is_overload_constant_str(_bodo_timestamp_tz) or not
        get_overload_const_str(_bodo_timestamp_tz)):
        raise BodoError(
            'to_parquet(): _bodo_timestamp_tz must be None or a constant string'
            )
    from bodo.io.parquet_pio import parquet_write_table_cpp, parquet_write_table_partitioned_cpp
    tjm__gfgh = isinstance(df.index, bodo.hiframes.pd_index_ext.RangeIndexType)
    yhghn__rhp = df.index is not None and (is_overload_true(_is_parallel) or
        not is_overload_true(_is_parallel) and not tjm__gfgh)
    write_non_range_index_to_metadata = is_overload_true(index
        ) or is_overload_none(index) and (not tjm__gfgh or is_overload_true
        (_is_parallel))
    write_rangeindex_to_metadata = is_overload_none(index
        ) and tjm__gfgh and not is_overload_true(_is_parallel)
    if df.has_runtime_cols:
        if isinstance(df.runtime_colname_typ, MultiIndexType):
            raise BodoError(
                'DataFrame.to_parquet(): Not supported with MultiIndex runtime column names. Please return the DataFrame to regular Python to update typing information.'
                )
        if not isinstance(df.runtime_colname_typ, bodo.hiframes.
            pd_index_ext.StringIndexType):
            raise BodoError(
                'DataFrame.to_parquet(): parquet must have string column names. Please return the DataFrame with runtime column names to regular Python to modify column names.'
                )
        cde__insn = df.runtime_data_types
        dozl__owi = len(cde__insn)
        gcf__bey = gen_pandas_parquet_metadata([''] * dozl__owi, cde__insn,
            df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=True)
        iluhy__ckk = gcf__bey['columns'][:dozl__owi]
        gcf__bey['columns'] = gcf__bey['columns'][dozl__owi:]
        iluhy__ckk = [json.dumps(xflce__bevk).replace('""', '{0}') for
            xflce__bevk in iluhy__ckk]
        lzqtr__huo = json.dumps(gcf__bey)
        wdcor__ykqti = '"columns": ['
        ayhv__mpzg = lzqtr__huo.find(wdcor__ykqti)
        if ayhv__mpzg == -1:
            raise BodoError(
                'DataFrame.to_parquet(): Unexpected metadata string for runtime columns.  Please return the DataFrame to regular Python to update typing information.'
                )
        fcl__npun = ayhv__mpzg + len(wdcor__ykqti)
        qma__uscz = lzqtr__huo[:fcl__npun]
        lzqtr__huo = lzqtr__huo[fcl__npun:]
        vicqr__sqjb = len(gcf__bey['columns'])
    else:
        lzqtr__huo = json.dumps(gen_pandas_parquet_metadata(df.columns, df.
            data, df.index, write_non_range_index_to_metadata,
            write_rangeindex_to_metadata, partition_cols=partition_cols,
            is_runtime_columns=False))
    if not is_overload_true(_is_parallel) and tjm__gfgh:
        lzqtr__huo = lzqtr__huo.replace('"%d"', '%d')
        if df.index.name == 'RangeIndexType(none)':
            lzqtr__huo = lzqtr__huo.replace('"%s"', '%s')
    if not df.is_table_format:
        tshsf__iusv = ', '.join(
            'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {}))'
            .format(i) for i in range(len(df.columns)))
    dxh__ulce = """def df_to_parquet(df, path, engine='auto', compression='snappy', index=None, partition_cols=None, storage_options=None, row_group_size=-1, _bodo_file_prefix='part-', _bodo_timestamp_tz=None, _is_parallel=False):
"""
    if df.is_table_format:
        dxh__ulce += '    py_table = get_dataframe_table(df)\n'
        dxh__ulce += (
            '    table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        dxh__ulce += '    info_list = [{}]\n'.format(tshsf__iusv)
        dxh__ulce += '    table = arr_info_list_to_table(info_list)\n'
    if df.has_runtime_cols:
        dxh__ulce += '    columns_index = get_dataframe_column_names(df)\n'
        dxh__ulce += '    names_arr = index_to_array(columns_index)\n'
        dxh__ulce += '    col_names = array_to_info(names_arr)\n'
    else:
        dxh__ulce += '    col_names = array_to_info(col_names_arr)\n'
    if is_overload_true(index) or is_overload_none(index) and yhghn__rhp:
        dxh__ulce += """    index_col = array_to_info(index_to_array(bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)))
"""
        fkhcl__dkhh = True
    else:
        dxh__ulce += '    index_col = array_to_info(np.empty(0))\n'
        fkhcl__dkhh = False
    if df.has_runtime_cols:
        dxh__ulce += '    columns_lst = []\n'
        dxh__ulce += '    num_cols = 0\n'
        for i in range(len(df.runtime_data_types)):
            dxh__ulce += f'    for _ in range(len(py_table.block_{i})):\n'
            dxh__ulce += f"""        columns_lst.append({iluhy__ckk[i]!r}.replace('{{0}}', '"' + names_arr[num_cols] + '"'))
"""
            dxh__ulce += '        num_cols += 1\n'
        if vicqr__sqjb:
            dxh__ulce += "    columns_lst.append('')\n"
        dxh__ulce += '    columns_str = ", ".join(columns_lst)\n'
        dxh__ulce += ('    metadata = """' + qma__uscz +
            '""" + columns_str + """' + lzqtr__huo + '"""\n')
    else:
        dxh__ulce += '    metadata = """' + lzqtr__huo + '"""\n'
    dxh__ulce += '    if compression is None:\n'
    dxh__ulce += "        compression = 'none'\n"
    dxh__ulce += '    if _bodo_timestamp_tz is None:\n'
    dxh__ulce += "        _bodo_timestamp_tz = ''\n"
    dxh__ulce += '    if df.index.name is not None:\n'
    dxh__ulce += '        name_ptr = df.index.name\n'
    dxh__ulce += '    else:\n'
    dxh__ulce += "        name_ptr = 'null'\n"
    dxh__ulce += f"""    bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(path, parallel=_is_parallel)
"""
    sqap__jzj = None
    if partition_cols:
        sqap__jzj = pd.array([col_name for col_name in df.columns if 
            col_name not in partition_cols])
        lez__zly = ', '.join(
            f'array_to_info(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i}).dtype.categories.values)'
             for i in range(len(df.columns)) if isinstance(df.data[i],
            CategoricalArrayType) and i in skw__pzh)
        if lez__zly:
            dxh__ulce += '    cat_info_list = [{}]\n'.format(lez__zly)
            dxh__ulce += (
                '    cat_table = arr_info_list_to_table(cat_info_list)\n')
        else:
            dxh__ulce += '    cat_table = table\n'
        dxh__ulce += (
            '    col_names_no_partitions = array_to_info(col_names_no_parts_arr)\n'
            )
        dxh__ulce += (
            f'    part_cols_idxs = np.array({skw__pzh}, dtype=np.int32)\n')
        dxh__ulce += (
            '    parquet_write_table_partitioned_cpp(unicode_to_utf8(path),\n')
        dxh__ulce += """                            table, col_names, col_names_no_partitions, cat_table,
"""
        dxh__ulce += (
            '                            part_cols_idxs.ctypes, len(part_cols_idxs),\n'
            )
        dxh__ulce += (
            '                            unicode_to_utf8(compression),\n')
        dxh__ulce += '                            _is_parallel,\n'
        dxh__ulce += (
            '                            unicode_to_utf8(bucket_region),\n')
        dxh__ulce += '                            row_group_size,\n'
        dxh__ulce += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        dxh__ulce += (
            '                            unicode_to_utf8(_bodo_timestamp_tz))\n'
            )
        dxh__ulce += '    delete_table_decref_arrays(table)\n'
        dxh__ulce += '    delete_info_decref_array(index_col)\n'
        dxh__ulce += '    delete_info_decref_array(col_names_no_partitions)\n'
        dxh__ulce += '    delete_info_decref_array(col_names)\n'
        if lez__zly:
            dxh__ulce += '    delete_table_decref_arrays(cat_table)\n'
    elif write_rangeindex_to_metadata:
        dxh__ulce += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        dxh__ulce += (
            '                            table, col_names, index_col,\n')
        dxh__ulce += '                            ' + str(fkhcl__dkhh) + ',\n'
        dxh__ulce += '                            unicode_to_utf8(metadata),\n'
        dxh__ulce += (
            '                            unicode_to_utf8(compression),\n')
        dxh__ulce += (
            '                            _is_parallel, 1, df.index.start,\n')
        dxh__ulce += (
            '                            df.index.stop, df.index.step,\n')
        dxh__ulce += '                            unicode_to_utf8(name_ptr),\n'
        dxh__ulce += (
            '                            unicode_to_utf8(bucket_region),\n')
        dxh__ulce += '                            row_group_size,\n'
        dxh__ulce += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        dxh__ulce += '                              False,\n'
        dxh__ulce += (
            '                            unicode_to_utf8(_bodo_timestamp_tz),\n'
            )
        dxh__ulce += '                              False)\n'
        dxh__ulce += '    delete_table_decref_arrays(table)\n'
        dxh__ulce += '    delete_info_decref_array(index_col)\n'
        dxh__ulce += '    delete_info_decref_array(col_names)\n'
    else:
        dxh__ulce += '    parquet_write_table_cpp(unicode_to_utf8(path),\n'
        dxh__ulce += (
            '                            table, col_names, index_col,\n')
        dxh__ulce += '                            ' + str(fkhcl__dkhh) + ',\n'
        dxh__ulce += '                            unicode_to_utf8(metadata),\n'
        dxh__ulce += (
            '                            unicode_to_utf8(compression),\n')
        dxh__ulce += '                            _is_parallel, 0, 0, 0, 0,\n'
        dxh__ulce += '                            unicode_to_utf8(name_ptr),\n'
        dxh__ulce += (
            '                            unicode_to_utf8(bucket_region),\n')
        dxh__ulce += '                            row_group_size,\n'
        dxh__ulce += (
            '                            unicode_to_utf8(_bodo_file_prefix),\n'
            )
        dxh__ulce += '                              False,\n'
        dxh__ulce += (
            '                            unicode_to_utf8(_bodo_timestamp_tz),\n'
            )
        dxh__ulce += '                              False)\n'
        dxh__ulce += '    delete_table_decref_arrays(table)\n'
        dxh__ulce += '    delete_info_decref_array(index_col)\n'
        dxh__ulce += '    delete_info_decref_array(col_names)\n'
    kdchp__xde = {}
    if df.has_runtime_cols:
        jthd__epu = None
    else:
        for thx__tntr in df.columns:
            if not isinstance(thx__tntr, str):
                raise BodoError(
                    'DataFrame.to_parquet(): parquet must have string column names'
                    )
        jthd__epu = pd.array(df.columns)
    exec(dxh__ulce, {'np': np, 'bodo': bodo, 'unicode_to_utf8':
        unicode_to_utf8, 'array_to_info': array_to_info,
        'arr_info_list_to_table': arr_info_list_to_table,
        'str_arr_from_sequence': str_arr_from_sequence,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'parquet_write_table_partitioned_cpp':
        parquet_write_table_partitioned_cpp, 'index_to_array':
        index_to_array, 'delete_info_decref_array':
        delete_info_decref_array, 'delete_table_decref_arrays':
        delete_table_decref_arrays, 'col_names_arr': jthd__epu,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'get_dataframe_table': get_dataframe_table,
        'col_names_no_parts_arr': sqap__jzj, 'get_dataframe_column_names':
        get_dataframe_column_names, 'fix_arr_dtype': fix_arr_dtype,
        'decode_if_dict_array': decode_if_dict_array,
        'decode_if_dict_table': decode_if_dict_table}, kdchp__xde)
    rdkbr__edre = kdchp__xde['df_to_parquet']
    return rdkbr__edre


def to_sql_exception_guard(df, name, con, schema=None, if_exists='fail',
    index=True, index_label=None, chunksize=None, dtype=None, method=None,
    _is_table_create=False, _is_parallel=False):
    olvye__klh = tracing.Event('to_sql_exception_guard', is_parallel=
        _is_parallel)
    myzw__ltz = 'all_ok'
    ixvu__ojxev, dwn__nkyej = bodo.ir.sql_ext.parse_dbtype(con)
    if _is_parallel and bodo.get_rank() == 0:
        dgrwm__xuk = 100
        if chunksize is None:
            ruvq__plze = dgrwm__xuk
        else:
            ruvq__plze = min(chunksize, dgrwm__xuk)
        if _is_table_create:
            df = df.iloc[:ruvq__plze, :]
        else:
            df = df.iloc[ruvq__plze:, :]
            if len(df) == 0:
                return myzw__ltz
    qgv__vfq = df.columns
    try:
        if ixvu__ojxev == 'oracle':
            import os
            import sqlalchemy as sa
            from sqlalchemy.dialects.oracle import VARCHAR2
            kgsh__jcy = os.environ.get('BODO_DISABLE_ORACLE_VARCHAR2', None)
            bnbns__dgiug = bodo.typeof(df)
            ekb__wfbzz = {}
            for qqoy__lyyaj, jdnii__mcf in zip(bnbns__dgiug.columns,
                bnbns__dgiug.data):
                if df[qqoy__lyyaj].dtype == 'object':
                    if jdnii__mcf == datetime_date_array_type:
                        ekb__wfbzz[qqoy__lyyaj] = sa.types.Date
                    elif jdnii__mcf in (bodo.string_array_type, bodo.
                        dict_str_arr_type) and (not kgsh__jcy or kgsh__jcy ==
                        '0'):
                        ekb__wfbzz[qqoy__lyyaj] = VARCHAR2(4000)
            dtype = ekb__wfbzz
        try:
            uis__tpqb = tracing.Event('df_to_sql', is_parallel=_is_parallel)
            df.to_sql(name, con, schema, if_exists, index, index_label,
                chunksize, dtype, method)
            uis__tpqb.finalize()
        except Exception as hzmi__oqidc:
            myzw__ltz = hzmi__oqidc.args[0]
            if ixvu__ojxev == 'oracle' and 'ORA-12899' in myzw__ltz:
                myzw__ltz += """
                String is larger than VARCHAR2 maximum length.
                Please set environment variable `BODO_DISABLE_ORACLE_VARCHAR2` to
                disable Bodo's optimziation use of VARCHA2.
                NOTE: Oracle `to_sql` with CLOB datatypes is known to be really slow.
                """
        return myzw__ltz
    finally:
        df.columns = qgv__vfq
        olvye__klh.finalize()


@numba.njit
def to_sql_exception_guard_encaps(df, name, con, schema=None, if_exists=
    'fail', index=True, index_label=None, chunksize=None, dtype=None,
    method=None, _is_table_create=False, _is_parallel=False):
    olvye__klh = tracing.Event('to_sql_exception_guard_encaps', is_parallel
        =_is_parallel)
    with numba.objmode(out='unicode_type'):
        urb__bilom = tracing.Event('to_sql_exception_guard_encaps:objmode',
            is_parallel=_is_parallel)
        out = to_sql_exception_guard(df, name, con, schema, if_exists,
            index, index_label, chunksize, dtype, method, _is_table_create,
            _is_parallel)
        urb__bilom.finalize()
    olvye__klh.finalize()
    return out


@overload_method(DataFrameType, 'to_sql')
def to_sql_overload(df, name, con, schema=None, if_exists='fail', index=
    True, index_label=None, chunksize=None, dtype=None, method=None,
    _bodo_allow_downcasting=False, _is_parallel=False):
    import warnings
    check_runtime_cols_unsupported(df, 'DataFrame.to_sql()')
    df: DataFrameType = df
    assert df.columns is not None and df.data is not None
    if is_overload_none(schema):
        if bodo.get_rank() == 0:
            warnings.warn(BodoWarning(
                f'DataFrame.to_sql(): schema argument is recommended to avoid permission issues when writing the table.'
                ))
    if not (is_overload_none(chunksize) or isinstance(chunksize, types.Integer)
        ):
        raise BodoError(
            "DataFrame.to_sql(): 'chunksize' argument must be an integer if provided."
            )
    from bodo.io.helpers import exception_propagating_thread_type
    from bodo.io.parquet_pio import parquet_write_table_cpp
    from bodo.io.snowflake import snowflake_connector_cursor_python_type
    for thx__tntr in df.columns:
        if not isinstance(thx__tntr, str):
            raise BodoError(
                'DataFrame.to_sql(): input dataframe must have string column names. Please return the DataFrame with runtime column names to regular Python to modify column names.'
                )
    jthd__epu = pd.array(df.columns)
    dxh__ulce = """def df_to_sql(
    df, name, con,
    schema=None, if_exists='fail', index=True,
    index_label=None, chunksize=None, dtype=None,
    method=None, _bodo_allow_downcasting=False,
    _is_parallel=False,
):
"""
    dxh__ulce += """    if con.startswith('iceberg'):
        con_str = bodo.io.iceberg.format_iceberg_conn_njit(con)
        if schema is None:
            raise ValueError('DataFrame.to_sql(): schema must be provided when writing to an Iceberg table.')
        if chunksize is not None:
            raise ValueError('DataFrame.to_sql(): chunksize not supported for Iceberg tables.')
        if index and bodo.get_rank() == 0:
            warnings.warn('index is not supported for Iceberg tables.')      
        if index_label is not None and bodo.get_rank() == 0:
            warnings.warn('index_label is not supported for Iceberg tables.')
"""
    if df.is_table_format:
        dxh__ulce += f'        py_table = get_dataframe_table(df)\n'
        dxh__ulce += (
            f'        table = py_table_to_cpp_table(py_table, py_table_typ)\n')
    else:
        tshsf__iusv = ', '.join(
            f'array_to_info(get_dataframe_data(df, {i}))' for i in range(
            len(df.columns)))
        dxh__ulce += f'        info_list = [{tshsf__iusv}]\n'
        dxh__ulce += f'        table = arr_info_list_to_table(info_list)\n'
    dxh__ulce += """        col_names = array_to_info(col_names_arr)
        bodo.io.iceberg.iceberg_write(
            name, con_str, schema, table, col_names,
            if_exists, _is_parallel, pyarrow_table_schema,
            _bodo_allow_downcasting,
        )
        delete_table_decref_arrays(table)
        delete_info_decref_array(col_names)
"""
    dxh__ulce += "    elif con.startswith('snowflake'):\n"
    dxh__ulce += """        if index and bodo.get_rank() == 0:
            warnings.warn('index is not supported for Snowflake tables.')      
        if index_label is not None and bodo.get_rank() == 0:
            warnings.warn('index_label is not supported for Snowflake tables.')
        if _bodo_allow_downcasting and bodo.get_rank() == 0:
            warnings.warn('_bodo_allow_downcasting is not supported for Snowflake tables.')
        ev = tracing.Event('snowflake_write_impl', sync=False)
"""
    dxh__ulce += "        location = ''\n"
    if not is_overload_none(schema):
        dxh__ulce += '        location += \'"\' + schema + \'".\'\n'
    dxh__ulce += '        location += name\n'
    dxh__ulce += '        my_rank = bodo.get_rank()\n'
    dxh__ulce += """        with bodo.objmode(
            cursor='snowflake_connector_cursor_type',
            tmp_folder='temporary_directory_type',
            stage_name='unicode_type',
            parquet_path='unicode_type',
            upload_using_snowflake_put='boolean',
            old_creds='DictType(unicode_type, unicode_type)',
            azure_stage_direct_upload='boolean',
            old_core_site='unicode_type',
            old_sas_token='unicode_type',
        ):
            (
                cursor, tmp_folder, stage_name, parquet_path, upload_using_snowflake_put, old_creds, azure_stage_direct_upload, old_core_site, old_sas_token,
            ) = bodo.io.snowflake.connect_and_get_upload_info(con)
"""
    dxh__ulce += '        bodo.barrier()\n'
    dxh__ulce += '        if azure_stage_direct_upload:\n'
    dxh__ulce += (
        '            bodo.libs.distributed_api.disconnect_hdfs_njit()\n')
    dxh__ulce += '        if chunksize is None:\n'
    dxh__ulce += """            ev_estimate_chunksize = tracing.Event('estimate_chunksize')          
"""
    if df.is_table_format and len(df.columns) > 0:
        dxh__ulce += f"""            nbytes_arr = np.empty({len(df.columns)}, np.int64)
            table = bodo.hiframes.pd_dataframe_ext.get_dataframe_table(df)
            bodo.utils.table_utils.generate_table_nbytes(table, nbytes_arr, 0)
            memory_usage = np.sum(nbytes_arr)
"""
    else:
        data = ', '.join(
            f'bodo.libs.array_ops.array_op_nbytes(get_dataframe_data(df, {i}))'
             for i in range(len(df.columns)))
        jcnjh__eqlex = ',' if len(df.columns) == 1 else ''
        dxh__ulce += f"""            memory_usage = np.array(({data}{jcnjh__eqlex}), np.int64).sum()
"""
    dxh__ulce += """            nsplits = int(max(1, memory_usage / bodo.io.snowflake.SF_WRITE_PARQUET_CHUNK_SIZE))
            chunksize = max(1, (len(df) + nsplits - 1) // nsplits)
            ev_estimate_chunksize.finalize()
"""
    if df.has_runtime_cols:
        dxh__ulce += '        columns_index = get_dataframe_column_names(df)\n'
        dxh__ulce += '        names_arr = index_to_array(columns_index)\n'
        dxh__ulce += '        col_names = array_to_info(names_arr)\n'
    else:
        dxh__ulce += '        col_names = array_to_info(col_names_arr)\n'
    dxh__ulce += '        index_col = array_to_info(np.empty(0))\n'
    dxh__ulce += """        bucket_region = bodo.io.fs_io.get_s3_bucket_region_njit(parquet_path, parallel=_is_parallel)
"""
    dxh__ulce += """        ev_upload_df = tracing.Event('upload_df', is_parallel=False)           
"""
    dxh__ulce += '        upload_threads_in_progress = []\n'
    dxh__ulce += """        for chunk_idx, i in enumerate(range(0, len(df), chunksize)):           
"""
    dxh__ulce += """            chunk_name = f'file{chunk_idx}_rank{my_rank}_{bodo.io.helpers.uuid4_helper()}.parquet'
"""
    dxh__ulce += '            chunk_path = parquet_path + chunk_name\n'
    dxh__ulce += (
        '            chunk_path = chunk_path.replace("\\\\", "\\\\\\\\")\n')
    dxh__ulce += (
        '            chunk_path = chunk_path.replace("\'", "\\\\\'")\n')
    dxh__ulce += """            ev_to_df_table = tracing.Event(f'to_df_table_{chunk_idx}', is_parallel=False)
"""
    dxh__ulce += '            chunk = df.iloc[i : i + chunksize]\n'
    if df.is_table_format:
        dxh__ulce += (
            '            py_table_chunk = get_dataframe_table(chunk)\n')
        dxh__ulce += """            table_chunk = py_table_to_cpp_table(py_table_chunk, py_table_typ)
"""
    else:
        zdoef__auazw = ', '.join(
            f'array_to_info(get_dataframe_data(chunk, {i}))' for i in range
            (len(df.columns)))
        dxh__ulce += (
            f'            table_chunk = arr_info_list_to_table([{zdoef__auazw}])     \n'
            )
    dxh__ulce += '            ev_to_df_table.finalize()\n'
    dxh__ulce += """            ev_pq_write_cpp = tracing.Event(f'pq_write_cpp_{chunk_idx}', is_parallel=False)
            ev_pq_write_cpp.add_attribute('chunk_start', i)
            ev_pq_write_cpp.add_attribute('chunk_end', i + len(chunk))
            ev_pq_write_cpp.add_attribute('chunk_size', len(chunk))
            ev_pq_write_cpp.add_attribute('chunk_path', chunk_path)
            parquet_write_table_cpp(
                unicode_to_utf8(chunk_path),
                table_chunk, col_names, index_col,
                False,
                unicode_to_utf8('null'),
                unicode_to_utf8(bodo.io.snowflake.SF_WRITE_PARQUET_COMPRESSION),
                False,
                0,
                0, 0, 0,
                unicode_to_utf8('null'),
                unicode_to_utf8(bucket_region),
                chunksize,
                unicode_to_utf8('null'),
                True,
                unicode_to_utf8('UTC'),
                True,
            )
            ev_pq_write_cpp.finalize()
            delete_table_decref_arrays(table_chunk)
            if upload_using_snowflake_put:
                with bodo.objmode(upload_thread='types.optional(exception_propagating_thread_type)'):
                    upload_thread = bodo.io.snowflake.do_upload_and_cleanup(
                        cursor, chunk_idx, chunk_path, stage_name,
                    )
                if bodo.io.snowflake.SF_WRITE_OVERLAP_UPLOAD:
                    upload_threads_in_progress.append(upload_thread)
        delete_info_decref_array(index_col)
        delete_info_decref_array(col_names)
        if bodo.io.snowflake.SF_WRITE_OVERLAP_UPLOAD:
            with bodo.objmode():
                bodo.io.helpers.join_all_threads(upload_threads_in_progress)
        ev_upload_df.finalize()
"""
    dxh__ulce += '        bodo.barrier()\n'
    pyj__ewafo = bodo.io.snowflake.gen_snowflake_schema(df.columns, df.data)
    dxh__ulce += f"""        with bodo.objmode():
            bodo.io.snowflake.create_table_copy_into(
                cursor, stage_name, location, {pyj__ewafo},
                if_exists, old_creds, tmp_folder,
                azure_stage_direct_upload, old_core_site,
                old_sas_token,
            )
"""
    dxh__ulce += '        if azure_stage_direct_upload:\n'
    dxh__ulce += (
        '            bodo.libs.distributed_api.disconnect_hdfs_njit()\n')
    dxh__ulce += '        ev.finalize()\n'
    dxh__ulce += '    else:\n'
    dxh__ulce += (
        '        if _bodo_allow_downcasting and bodo.get_rank() == 0:\n')
    dxh__ulce += """            warnings.warn('_bodo_allow_downcasting is not supported for SQL tables.')
"""
    dxh__ulce += '        rank = bodo.libs.distributed_api.get_rank()\n'
    dxh__ulce += "        err_msg = 'unset'\n"
    dxh__ulce += '        if rank != 0:\n'
    dxh__ulce += """            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          
"""
    dxh__ulce += '        elif rank == 0:\n'
    dxh__ulce += '            err_msg = to_sql_exception_guard_encaps(\n'
    dxh__ulce += """                          df, name, con, schema, if_exists, index, index_label,
"""
    dxh__ulce += '                          chunksize, dtype, method,\n'
    dxh__ulce += '                          True, _is_parallel,\n'
    dxh__ulce += '                      )\n'
    dxh__ulce += """            err_msg = bodo.libs.distributed_api.bcast_scalar(err_msg)          
"""
    dxh__ulce += "        if_exists = 'append'\n"
    dxh__ulce += "        if _is_parallel and err_msg == 'all_ok':\n"
    dxh__ulce += '            err_msg = to_sql_exception_guard_encaps(\n'
    dxh__ulce += """                          df, name, con, schema, if_exists, index, index_label,
"""
    dxh__ulce += '                          chunksize, dtype, method,\n'
    dxh__ulce += '                          False, _is_parallel,\n'
    dxh__ulce += '                      )\n'
    dxh__ulce += "        if err_msg != 'all_ok':\n"
    dxh__ulce += "            print('err_msg=', err_msg)\n"
    dxh__ulce += (
        "            raise ValueError('error in to_sql() operation')\n")
    kdchp__xde = {}
    ppi__jrt = globals().copy()
    ppi__jrt.update({'arr_info_list_to_table': arr_info_list_to_table,
        'array_to_info': array_to_info, 'bodo': bodo, 'col_names_arr':
        jthd__epu, 'delete_info_decref_array': delete_info_decref_array,
        'delete_table_decref_arrays': delete_table_decref_arrays,
        'get_dataframe_column_names': get_dataframe_column_names,
        'get_dataframe_data': get_dataframe_data, 'get_dataframe_table':
        get_dataframe_table, 'index_to_array': index_to_array, 'np': np,
        'parquet_write_table_cpp': parquet_write_table_cpp,
        'py_table_to_cpp_table': py_table_to_cpp_table, 'py_table_typ': df.
        table_type, 'pyarrow_table_schema': bodo.io.helpers.
        numba_to_pyarrow_schema(df, is_iceberg=True), 'time': time,
        'to_sql_exception_guard_encaps': to_sql_exception_guard_encaps,
        'tracing': tracing, 'unicode_to_utf8': unicode_to_utf8, 'warnings':
        warnings})
    exec(dxh__ulce, ppi__jrt, kdchp__xde)
    _impl = kdchp__xde['df_to_sql']
    return _impl


@overload_method(DataFrameType, 'to_csv', no_unliteral=True)
def to_csv_overload(df, path_or_buf=None, sep=',', na_rep='', float_format=
    None, columns=None, header=True, index=True, index_label=None, mode='w',
    encoding=None, compression=None, quoting=None, quotechar='"',
    line_terminator=None, chunksize=None, date_format=None, doublequote=
    True, escapechar=None, decimal='.', errors='strict', storage_options=
    None, _bodo_file_prefix='part-'):
    check_runtime_cols_unsupported(df, 'DataFrame.to_csv()')
    check_unsupported_args('DataFrame.to_csv', {'encoding': encoding,
        'mode': mode, 'errors': errors, 'storage_options': storage_options},
        {'encoding': None, 'mode': 'w', 'errors': 'strict',
        'storage_options': None}, package_name='pandas', module_name='IO')
    if not (is_overload_none(path_or_buf) or is_overload_constant_str(
        path_or_buf) or path_or_buf == string_type):
        raise BodoError(
            "DataFrame.to_csv(): 'path_or_buf' argument should be None or string"
            )
    if not is_overload_none(compression):
        raise BodoError(
            "DataFrame.to_csv(): 'compression' argument supports only None, which is the default in JIT code."
            )
    if is_overload_constant_str(path_or_buf):
        adzg__xui = get_overload_const_str(path_or_buf)
        if adzg__xui.endswith(('.gz', '.bz2', '.zip', '.xz')):
            import warnings
            from bodo.utils.typing import BodoWarning
            warnings.warn(BodoWarning(
                "DataFrame.to_csv(): 'compression' argument defaults to None in JIT code, which is the only supported value."
                ))
    if not (is_overload_none(columns) or isinstance(columns, (types.List,
        types.Tuple))):
        raise BodoError(
            "DataFrame.to_csv(): 'columns' argument must be list a or tuple type."
            )
    if is_overload_none(path_or_buf):

        def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=
            None, columns=None, header=True, index=True, index_label=None,
            mode='w', encoding=None, compression=None, quoting=None,
            quotechar='"', line_terminator=None, chunksize=None,
            date_format=None, doublequote=True, escapechar=None, decimal=
            '.', errors='strict', storage_options=None, _bodo_file_prefix=
            'part-'):
            with numba.objmode(D='unicode_type'):
                D = df.to_csv(path_or_buf, sep, na_rep, float_format,
                    columns, header, index, index_label, mode, encoding,
                    compression, quoting, quotechar, line_terminator,
                    chunksize, date_format, doublequote, escapechar,
                    decimal, errors, storage_options)
            return D
        return _impl

    def _impl(df, path_or_buf=None, sep=',', na_rep='', float_format=None,
        columns=None, header=True, index=True, index_label=None, mode='w',
        encoding=None, compression=None, quoting=None, quotechar='"',
        line_terminator=None, chunksize=None, date_format=None, doublequote
        =True, escapechar=None, decimal='.', errors='strict',
        storage_options=None, _bodo_file_prefix='part-'):
        with numba.objmode(D='unicode_type'):
            D = df.to_csv(None, sep, na_rep, float_format, columns, header,
                index, index_label, mode, encoding, compression, quoting,
                quotechar, line_terminator, chunksize, date_format,
                doublequote, escapechar, decimal, errors, storage_options)
        bodo.io.fs_io.csv_write(path_or_buf, D, _bodo_file_prefix)
    return _impl


@overload_method(DataFrameType, 'to_json', no_unliteral=True)
def to_json_overload(df, path_or_buf=None, orient='records', date_format=
    None, double_precision=10, force_ascii=True, date_unit='ms',
    default_handler=None, lines=True, compression='infer', index=True,
    indent=None, storage_options=None, _bodo_file_prefix='part-'):
    check_runtime_cols_unsupported(df, 'DataFrame.to_json()')
    check_unsupported_args('DataFrame.to_json', {'storage_options':
        storage_options}, {'storage_options': None}, package_name='pandas',
        module_name='IO')
    if path_or_buf is None or path_or_buf == types.none:

        def _impl(df, path_or_buf=None, orient='records', date_format=None,
            double_precision=10, force_ascii=True, date_unit='ms',
            default_handler=None, lines=True, compression='infer', index=
            True, indent=None, storage_options=None, _bodo_file_prefix='part-'
            ):
            with numba.objmode(D='unicode_type'):
                D = df.to_json(path_or_buf, orient, date_format,
                    double_precision, force_ascii, date_unit,
                    default_handler, lines, compression, index, indent,
                    storage_options)
            return D
        return _impl

    def _impl(df, path_or_buf=None, orient='records', date_format=None,
        double_precision=10, force_ascii=True, date_unit='ms',
        default_handler=None, lines=True, compression='infer', index=True,
        indent=None, storage_options=None, _bodo_file_prefix='part-'):
        with numba.objmode(D='unicode_type'):
            D = df.to_json(None, orient, date_format, double_precision,
                force_ascii, date_unit, default_handler, lines, compression,
                index, indent, storage_options)
        rvkh__vob = bodo.io.fs_io.get_s3_bucket_region_njit(path_or_buf,
            parallel=False)
        if lines and orient == 'records':
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, True,
                unicode_to_utf8(rvkh__vob), unicode_to_utf8(_bodo_file_prefix))
            bodo.utils.utils.check_and_propagate_cpp_exception()
        else:
            bodo.hiframes.pd_dataframe_ext._json_write(unicode_to_utf8(
                path_or_buf), unicode_to_utf8(D), 0, len(D), False, False,
                unicode_to_utf8(rvkh__vob), unicode_to_utf8(_bodo_file_prefix))
            bodo.utils.utils.check_and_propagate_cpp_exception()
    return _impl


@overload(pd.get_dummies, inline='always', no_unliteral=True)
def get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=
    None, sparse=False, drop_first=False, dtype=None):
    gxuaw__saklu = {'prefix': prefix, 'prefix_sep': prefix_sep, 'dummy_na':
        dummy_na, 'columns': columns, 'sparse': sparse, 'drop_first':
        drop_first, 'dtype': dtype}
    syjel__tkjim = {'prefix': None, 'prefix_sep': '_', 'dummy_na': False,
        'columns': None, 'sparse': False, 'drop_first': False, 'dtype': None}
    check_unsupported_args('pandas.get_dummies', gxuaw__saklu, syjel__tkjim,
        package_name='pandas', module_name='General')
    if not categorical_can_construct_dataframe(data):
        raise BodoError(
            'pandas.get_dummies() only support categorical data types with explicitly known categories'
            )
    dxh__ulce = """def impl(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None,):
"""
    if isinstance(data, SeriesType):
        yci__csc = data.data.dtype.categories
        dxh__ulce += (
            '  data_values = bodo.hiframes.pd_series_ext.get_series_data(data)\n'
            )
    else:
        yci__csc = data.dtype.categories
        dxh__ulce += '  data_values = data\n'
    ejrr__owany = len(yci__csc)
    dxh__ulce += """  codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(data_values)
"""
    dxh__ulce += '  numba.parfors.parfor.init_prange()\n'
    dxh__ulce += '  n = len(data_values)\n'
    for i in range(ejrr__owany):
        dxh__ulce += '  data_arr_{} = np.empty(n, np.uint8)\n'.format(i)
    dxh__ulce += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    dxh__ulce += '      if bodo.libs.array_kernels.isna(data_values, i):\n'
    for itmwb__bzlpj in range(ejrr__owany):
        dxh__ulce += '          data_arr_{}[i] = 0\n'.format(itmwb__bzlpj)
    dxh__ulce += '      else:\n'
    for prss__hrzv in range(ejrr__owany):
        dxh__ulce += '          data_arr_{0}[i] = codes[i] == {0}\n'.format(
            prss__hrzv)
    tshsf__iusv = ', '.join(f'data_arr_{i}' for i in range(ejrr__owany))
    index = 'bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)'
    if isinstance(yci__csc[0], np.datetime64):
        yci__csc = tuple(pd.Timestamp(qqoy__lyyaj) for qqoy__lyyaj in yci__csc)
    elif isinstance(yci__csc[0], np.timedelta64):
        yci__csc = tuple(pd.Timedelta(qqoy__lyyaj) for qqoy__lyyaj in yci__csc)
    return bodo.hiframes.dataframe_impl._gen_init_df(dxh__ulce, yci__csc,
        tshsf__iusv, index)


def categorical_can_construct_dataframe(val):
    if isinstance(val, CategoricalArrayType):
        return val.dtype.categories is not None
    elif isinstance(val, SeriesType) and isinstance(val.data,
        CategoricalArrayType):
        return val.data.dtype.categories is not None
    return False


def handle_inplace_df_type_change(inplace, _bodo_transformed, func_name):
    if is_overload_false(_bodo_transformed
        ) and bodo.transforms.typing_pass.in_partial_typing and (
        is_overload_true(inplace) or not is_overload_constant_bool(inplace)):
        bodo.transforms.typing_pass.typing_transform_required = True
        raise Exception('DataFrame.{}(): transform necessary for inplace'.
            format(func_name))


pd_unsupported = (pd.read_pickle, pd.read_table, pd.read_fwf, pd.
    read_clipboard, pd.ExcelFile, pd.read_html, pd.read_xml, pd.read_hdf,
    pd.read_feather, pd.read_orc, pd.read_sas, pd.read_spss, pd.
    read_sql_query, pd.read_gbq, pd.read_stata, pd.ExcelWriter, pd.
    json_normalize, pd.merge_ordered, pd.factorize, pd.wide_to_long, pd.
    bdate_range, pd.period_range, pd.infer_freq, pd.interval_range, pd.eval,
    pd.test, pd.Grouper)
pd_util_unsupported = pd.util.hash_array, pd.util.hash_pandas_object
dataframe_unsupported = ['set_flags', 'convert_dtypes', 'bool', '__iter__',
    'items', 'iteritems', 'keys', 'iterrows', 'lookup', 'pop', 'xs', 'get',
    'add', 'sub', 'mul', 'div', 'truediv', 'floordiv', 'mod', 'pow', 'dot',
    'radd', 'rsub', 'rmul', 'rdiv', 'rtruediv', 'rfloordiv', 'rmod', 'rpow',
    'lt', 'gt', 'le', 'ge', 'ne', 'eq', 'combine', 'combine_first',
    'subtract', 'divide', 'multiply', 'applymap', 'agg', 'aggregate',
    'transform', 'expanding', 'ewm', 'all', 'any', 'clip', 'corrwith',
    'cummax', 'cummin', 'eval', 'kurt', 'kurtosis', 'mad', 'mode', 'round',
    'sem', 'skew', 'value_counts', 'add_prefix', 'add_suffix', 'align',
    'at_time', 'between_time', 'equals', 'reindex', 'reindex_like',
    'rename_axis', 'set_axis', 'truncate', 'backfill', 'bfill', 'ffill',
    'interpolate', 'pad', 'droplevel', 'reorder_levels', 'nlargest',
    'nsmallest', 'swaplevel', 'stack', 'unstack', 'swapaxes', 'squeeze',
    'to_xarray', 'T', 'transpose', 'compare', 'update', 'asfreq', 'asof',
    'slice_shift', 'tshift', 'first_valid_index', 'last_valid_index',
    'resample', 'to_period', 'to_timestamp', 'tz_convert', 'tz_localize',
    'boxplot', 'hist', 'from_dict', 'from_records', 'to_pickle', 'to_hdf',
    'to_dict', 'to_excel', 'to_html', 'to_feather', 'to_latex', 'to_stata',
    'to_gbq', 'to_records', 'to_clipboard', 'to_markdown', 'to_xml']
dataframe_unsupported_attrs = ['at', 'attrs', 'axes', 'flags', 'style',
    'sparse']


def _install_pd_unsupported(mod_name, pd_unsupported):
    for mmd__kxai in pd_unsupported:
        qgsuc__xqsk = mod_name + '.' + mmd__kxai.__name__
        overload(mmd__kxai, no_unliteral=True)(create_unsupported_overload(
            qgsuc__xqsk))


def _install_dataframe_unsupported():
    for fbd__uuh in dataframe_unsupported_attrs:
        vzqw__mqsxs = 'DataFrame.' + fbd__uuh
        overload_attribute(DataFrameType, fbd__uuh)(create_unsupported_overload
            (vzqw__mqsxs))
    for qgsuc__xqsk in dataframe_unsupported:
        vzqw__mqsxs = 'DataFrame.' + qgsuc__xqsk + '()'
        overload_method(DataFrameType, qgsuc__xqsk)(create_unsupported_overload
            (vzqw__mqsxs))


_install_pd_unsupported('pandas', pd_unsupported)
_install_pd_unsupported('pandas.util', pd_util_unsupported)
_install_dataframe_unsupported()
