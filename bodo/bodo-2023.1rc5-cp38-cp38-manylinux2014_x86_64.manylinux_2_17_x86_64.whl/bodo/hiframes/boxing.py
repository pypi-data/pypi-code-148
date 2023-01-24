"""
Boxing and unboxing support for DataFrame, Series, etc.
"""
import datetime
import decimal
import warnings
from enum import Enum
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.ir_utils import GuardException, guard
from numba.core.typing import signature
from numba.cpython.listobj import ListInstance
from numba.extending import NativeValue, box, intrinsic, typeof_impl, unbox
from numba.np.arrayobj import _getitem_array_single_int
from numba.typed.typeddict import Dict
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_array_type
from bodo.hiframes.pd_categorical_ext import PDCategoricalDtype
from bodo.hiframes.pd_dataframe_ext import DataFramePayloadType, DataFrameType, check_runtime_cols_unsupported, construct_dataframe
from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, RangeIndexType, StringIndexType, TimedeltaIndexType
from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
from bodo.hiframes.split_impl import string_array_split_view_type
from bodo.hiframes.time_ext import TimeArrayType
from bodo.libs import hstr_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.libs.float_arr_ext import FloatDtype, FloatingArrayType
from bodo.libs.int_arr_ext import IntDtype, IntegerArrayType
from bodo.libs.map_arr_ext import MapArrayType
from bodo.libs.str_arr_ext import string_array_type, string_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType, StructType
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.cg_helpers import is_ll_eq
from bodo.utils.typing import BodoError, BodoWarning, dtype_to_array_type, get_overload_const_bool, get_overload_const_int, get_overload_const_str, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_str, raise_bodo_error, to_nullable_type, to_str_arr_if_dict_array
ll.add_symbol('is_np_array', hstr_ext.is_np_array)
ll.add_symbol('array_size', hstr_ext.array_size)
ll.add_symbol('array_getptr1', hstr_ext.array_getptr1)
TABLE_FORMAT_THRESHOLD = 20
_use_dict_str_type = False


def _set_bodo_meta_in_pandas():
    if '_bodo_meta' not in pd.Series._metadata:
        pd.Series._metadata.append('_bodo_meta')
    if '_bodo_meta' not in pd.DataFrame._metadata:
        pd.DataFrame._metadata.append('_bodo_meta')


_set_bodo_meta_in_pandas()


@typeof_impl.register(pd.DataFrame)
def typeof_pd_dataframe(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    lpfhx__srqc = tuple(val.columns.to_list())
    wadit__ers = get_hiframes_dtypes(val)
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and len(val._bodo_meta['type_metadata'
        ][1]) == len(val.columns) and val._bodo_meta['type_metadata'][0] is not
        None):
        jjaq__zykeb = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        jjaq__zykeb = numba.typeof(val.index)
    fiftj__zgy = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    lsea__vhyfl = len(wadit__ers) >= TABLE_FORMAT_THRESHOLD
    return DataFrameType(wadit__ers, jjaq__zykeb, lpfhx__srqc, fiftj__zgy,
        is_table_format=lsea__vhyfl)


@typeof_impl.register(pd.Series)
def typeof_pd_series(val, c):
    from bodo.transforms.distributed_analysis import Distribution
    fiftj__zgy = Distribution(val._bodo_meta['dist']) if hasattr(val,
        '_bodo_meta') and val._bodo_meta is not None else Distribution.REP
    if (len(val.index) == 0 and val.index.dtype == np.dtype('O') and
        hasattr(val, '_bodo_meta') and val._bodo_meta is not None and 
        'type_metadata' in val._bodo_meta and val._bodo_meta[
        'type_metadata'] is not None and val._bodo_meta['type_metadata'][0]
         is not None):
        zenb__knzst = _dtype_from_type_enum_list(val._bodo_meta[
            'type_metadata'][0])
    else:
        zenb__knzst = numba.typeof(val.index)
    knnc__ncwww = _infer_series_arr_type(val)
    if _use_dict_str_type and knnc__ncwww == string_array_type:
        knnc__ncwww = bodo.dict_str_arr_type
    return SeriesType(knnc__ncwww.dtype, data=knnc__ncwww, index=
        zenb__knzst, name_typ=numba.typeof(val.name), dist=fiftj__zgy)


@unbox(DataFrameType)
def unbox_dataframe(typ, val, c):
    check_runtime_cols_unsupported(typ, 'Unboxing')
    tcxsz__pjz = c.pyapi.object_getattr_string(val, 'index')
    jydgy__hvie = c.pyapi.to_native_value(typ.index, tcxsz__pjz).value
    c.pyapi.decref(tcxsz__pjz)
    if typ.is_table_format:
        zhfxi__xky = cgutils.create_struct_proxy(typ.table_type)(c.context,
            c.builder)
        zhfxi__xky.parent = val
        for puoe__jng, nipj__mtr in typ.table_type.type_to_blk.items():
            kdrlw__tbl = c.context.get_constant(types.int64, len(typ.
                table_type.block_to_arr_ind[nipj__mtr]))
            xlzjk__aewx, whx__nly = ListInstance.allocate_ex(c.context, c.
                builder, types.List(puoe__jng), kdrlw__tbl)
            whx__nly.size = kdrlw__tbl
            setattr(zhfxi__xky, f'block_{nipj__mtr}', whx__nly.value)
        tzo__jyaz = c.pyapi.call_method(val, '__len__', ())
        ctue__lexfx = c.pyapi.long_as_longlong(tzo__jyaz)
        c.pyapi.decref(tzo__jyaz)
        zhfxi__xky.len = ctue__lexfx
        whu__dcn = c.context.make_tuple(c.builder, types.Tuple([typ.
            table_type]), [zhfxi__xky._getvalue()])
    else:
        qich__heda = [c.context.get_constant_null(puoe__jng) for puoe__jng in
            typ.data]
        whu__dcn = c.context.make_tuple(c.builder, types.Tuple(typ.data),
            qich__heda)
    idgn__hxdz = construct_dataframe(c.context, c.builder, typ, whu__dcn,
        jydgy__hvie, val, None)
    return NativeValue(idgn__hxdz)


def get_hiframes_dtypes(df):
    if (hasattr(df, '_bodo_meta') and df._bodo_meta is not None and 
        'type_metadata' in df._bodo_meta and df._bodo_meta['type_metadata']
         is not None and len(df._bodo_meta['type_metadata'][1]) == len(df.
        columns)):
        uffp__nbs = df._bodo_meta['type_metadata'][1]
    else:
        uffp__nbs = [None] * len(df.columns)
    cqbhj__gud = [_infer_series_arr_type(df.iloc[:, i], array_metadata=
        uffp__nbs[i]) for i in range(len(df.columns))]
    cqbhj__gud = [(bodo.dict_str_arr_type if _use_dict_str_type and 
        puoe__jng == string_array_type else puoe__jng) for puoe__jng in
        cqbhj__gud]
    return tuple(cqbhj__gud)


class SeriesDtypeEnum(Enum):
    Int8 = 0
    UInt8 = 1
    Int32 = 2
    UInt32 = 3
    Int64 = 4
    UInt64 = 7
    Float32 = 5
    Float64 = 6
    Int16 = 8
    UInt16 = 9
    STRING = 10
    Bool = 11
    Decimal = 12
    Datime_Date = 13
    NP_Datetime64ns = 14
    NP_Timedelta64ns = 15
    Int128 = 16
    LIST = 18
    STRUCT = 19
    BINARY = 21
    ARRAY = 22
    PD_nullable_Int8 = 23
    PD_nullable_UInt8 = 24
    PD_nullable_Int16 = 25
    PD_nullable_UInt16 = 26
    PD_nullable_Int32 = 27
    PD_nullable_UInt32 = 28
    PD_nullable_Int64 = 29
    PD_nullable_UInt64 = 30
    PD_nullable_bool = 31
    CategoricalType = 32
    NoneType = 33
    Literal = 34
    IntegerArray = 35
    RangeIndexType = 36
    DatetimeIndexType = 37
    NumericIndexType = 38
    PeriodIndexType = 39
    IntervalIndexType = 40
    CategoricalIndexType = 41
    StringIndexType = 42
    BinaryIndexType = 43
    TimedeltaIndexType = 44
    LiteralType = 45
    PD_nullable_Float32 = 46
    PD_nullable_Float64 = 47
    FloatingArray = 48


_one_to_one_type_to_enum_map = {types.int8: SeriesDtypeEnum.Int8.value,
    types.uint8: SeriesDtypeEnum.UInt8.value, types.int32: SeriesDtypeEnum.
    Int32.value, types.uint32: SeriesDtypeEnum.UInt32.value, types.int64:
    SeriesDtypeEnum.Int64.value, types.uint64: SeriesDtypeEnum.UInt64.value,
    types.float32: SeriesDtypeEnum.Float32.value, types.float64:
    SeriesDtypeEnum.Float64.value, types.NPDatetime('ns'): SeriesDtypeEnum.
    NP_Datetime64ns.value, types.NPTimedelta('ns'): SeriesDtypeEnum.
    NP_Timedelta64ns.value, types.bool_: SeriesDtypeEnum.Bool.value, types.
    int16: SeriesDtypeEnum.Int16.value, types.uint16: SeriesDtypeEnum.
    UInt16.value, types.Integer('int128', 128): SeriesDtypeEnum.Int128.
    value, bodo.hiframes.datetime_date_ext.datetime_date_type:
    SeriesDtypeEnum.Datime_Date.value, IntDtype(types.int8):
    SeriesDtypeEnum.PD_nullable_Int8.value, IntDtype(types.uint8):
    SeriesDtypeEnum.PD_nullable_UInt8.value, IntDtype(types.int16):
    SeriesDtypeEnum.PD_nullable_Int16.value, IntDtype(types.uint16):
    SeriesDtypeEnum.PD_nullable_UInt16.value, IntDtype(types.int32):
    SeriesDtypeEnum.PD_nullable_Int32.value, IntDtype(types.uint32):
    SeriesDtypeEnum.PD_nullable_UInt32.value, IntDtype(types.int64):
    SeriesDtypeEnum.PD_nullable_Int64.value, IntDtype(types.uint64):
    SeriesDtypeEnum.PD_nullable_UInt64.value, FloatDtype(types.float32):
    SeriesDtypeEnum.PD_nullable_Float32.value, FloatDtype(types.float64):
    SeriesDtypeEnum.PD_nullable_Float64.value, bytes_type: SeriesDtypeEnum.
    BINARY.value, string_type: SeriesDtypeEnum.STRING.value, bodo.bool_:
    SeriesDtypeEnum.Bool.value, types.none: SeriesDtypeEnum.NoneType.value}
_one_to_one_enum_to_type_map = {SeriesDtypeEnum.Int8.value: types.int8,
    SeriesDtypeEnum.UInt8.value: types.uint8, SeriesDtypeEnum.Int32.value:
    types.int32, SeriesDtypeEnum.UInt32.value: types.uint32,
    SeriesDtypeEnum.Int64.value: types.int64, SeriesDtypeEnum.UInt64.value:
    types.uint64, SeriesDtypeEnum.Float32.value: types.float32,
    SeriesDtypeEnum.Float64.value: types.float64, SeriesDtypeEnum.
    NP_Datetime64ns.value: types.NPDatetime('ns'), SeriesDtypeEnum.
    NP_Timedelta64ns.value: types.NPTimedelta('ns'), SeriesDtypeEnum.Int16.
    value: types.int16, SeriesDtypeEnum.UInt16.value: types.uint16,
    SeriesDtypeEnum.Int128.value: types.Integer('int128', 128),
    SeriesDtypeEnum.Datime_Date.value: bodo.hiframes.datetime_date_ext.
    datetime_date_type, SeriesDtypeEnum.PD_nullable_Int8.value: IntDtype(
    types.int8), SeriesDtypeEnum.PD_nullable_UInt8.value: IntDtype(types.
    uint8), SeriesDtypeEnum.PD_nullable_Int16.value: IntDtype(types.int16),
    SeriesDtypeEnum.PD_nullable_UInt16.value: IntDtype(types.uint16),
    SeriesDtypeEnum.PD_nullable_Int32.value: IntDtype(types.int32),
    SeriesDtypeEnum.PD_nullable_UInt32.value: IntDtype(types.uint32),
    SeriesDtypeEnum.PD_nullable_Int64.value: IntDtype(types.int64),
    SeriesDtypeEnum.PD_nullable_UInt64.value: IntDtype(types.uint64),
    SeriesDtypeEnum.PD_nullable_Float32.value: FloatDtype(types.float32),
    SeriesDtypeEnum.PD_nullable_Float64.value: FloatDtype(types.float64),
    SeriesDtypeEnum.BINARY.value: bytes_type, SeriesDtypeEnum.STRING.value:
    string_type, SeriesDtypeEnum.Bool.value: bodo.bool_, SeriesDtypeEnum.
    NoneType.value: types.none}


def _dtype_from_type_enum_list(typ_enum_list):
    ste__zgr, typ = _dtype_from_type_enum_list_recursor(typ_enum_list)
    if len(ste__zgr) != 0:
        raise_bodo_error(
            f"""Unexpected Internal Error while converting typing metadata: Dtype list was not fully consumed.
 Input typ_enum_list: {typ_enum_list}.
Remainder: {ste__zgr}. Please file the error here: https://github.com/Bodo-inc/Feedback"""
            )
    return typ


def _dtype_from_type_enum_list_recursor(typ_enum_list):
    if len(typ_enum_list) == 0:
        raise_bodo_error('Unable to infer dtype from empty typ_enum_list')
    elif typ_enum_list[0] in _one_to_one_enum_to_type_map:
        return typ_enum_list[1:], _one_to_one_enum_to_type_map[typ_enum_list[0]
            ]
    elif typ_enum_list[0] == SeriesDtypeEnum.IntegerArray.value:
        pgurf__eicfe, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return pgurf__eicfe, IntegerArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.FloatingArray.value:
        pgurf__eicfe, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return pgurf__eicfe, FloatingArrayType(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.ARRAY.value:
        pgurf__eicfe, typ = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        return pgurf__eicfe, dtype_to_array_type(typ)
    elif typ_enum_list[0] == SeriesDtypeEnum.Decimal.value:
        lcmd__grm = typ_enum_list[1]
        yaae__uldbt = typ_enum_list[2]
        return typ_enum_list[3:], Decimal128Type(lcmd__grm, yaae__uldbt)
    elif typ_enum_list[0] == SeriesDtypeEnum.STRUCT.value:
        lrvld__lytj = typ_enum_list[1]
        ohx__ysrkz = tuple(typ_enum_list[2:2 + lrvld__lytj])
        pnteh__aln = typ_enum_list[2 + lrvld__lytj:]
        jrmn__dupqq = []
        for i in range(lrvld__lytj):
            pnteh__aln, xkfmv__ztqcu = _dtype_from_type_enum_list_recursor(
                pnteh__aln)
            jrmn__dupqq.append(xkfmv__ztqcu)
        return pnteh__aln, StructType(tuple(jrmn__dupqq), ohx__ysrkz)
    elif typ_enum_list[0] == SeriesDtypeEnum.Literal.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'Literal' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        roiu__rsj = typ_enum_list[1]
        pnteh__aln = typ_enum_list[2:]
        return pnteh__aln, roiu__rsj
    elif typ_enum_list[0] == SeriesDtypeEnum.LiteralType.value:
        if len(typ_enum_list) == 1:
            raise_bodo_error(
                f"Unexpected Internal Error while converting typing metadata: Encountered 'LiteralType' internal enum value with no value following it. Please file the error here: https://github.com/Bodo-inc/Feedback"
                )
        roiu__rsj = typ_enum_list[1]
        pnteh__aln = typ_enum_list[2:]
        return pnteh__aln, numba.types.literal(roiu__rsj)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalType.value:
        pnteh__aln, lmvel__mukpb = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        pnteh__aln, kpcpe__riak = _dtype_from_type_enum_list_recursor(
            pnteh__aln)
        pnteh__aln, jdzrl__pcfz = _dtype_from_type_enum_list_recursor(
            pnteh__aln)
        pnteh__aln, uonz__jxs = _dtype_from_type_enum_list_recursor(pnteh__aln)
        pnteh__aln, jrr__wkmk = _dtype_from_type_enum_list_recursor(pnteh__aln)
        return pnteh__aln, PDCategoricalDtype(lmvel__mukpb, kpcpe__riak,
            jdzrl__pcfz, uonz__jxs, jrr__wkmk)
    elif typ_enum_list[0] == SeriesDtypeEnum.DatetimeIndexType.value:
        pnteh__aln, mya__rnts = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return pnteh__aln, DatetimeIndexType(mya__rnts)
    elif typ_enum_list[0] == SeriesDtypeEnum.NumericIndexType.value:
        pnteh__aln, dtype = _dtype_from_type_enum_list_recursor(typ_enum_list
            [1:])
        pnteh__aln, mya__rnts = _dtype_from_type_enum_list_recursor(pnteh__aln)
        pnteh__aln, uonz__jxs = _dtype_from_type_enum_list_recursor(pnteh__aln)
        return pnteh__aln, NumericIndexType(dtype, mya__rnts, uonz__jxs)
    elif typ_enum_list[0] == SeriesDtypeEnum.PeriodIndexType.value:
        pnteh__aln, ywmnp__lzxa = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        pnteh__aln, mya__rnts = _dtype_from_type_enum_list_recursor(pnteh__aln)
        return pnteh__aln, PeriodIndexType(ywmnp__lzxa, mya__rnts)
    elif typ_enum_list[0] == SeriesDtypeEnum.CategoricalIndexType.value:
        pnteh__aln, uonz__jxs = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        pnteh__aln, mya__rnts = _dtype_from_type_enum_list_recursor(pnteh__aln)
        return pnteh__aln, CategoricalIndexType(uonz__jxs, mya__rnts)
    elif typ_enum_list[0] == SeriesDtypeEnum.RangeIndexType.value:
        pnteh__aln, mya__rnts = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return pnteh__aln, RangeIndexType(mya__rnts)
    elif typ_enum_list[0] == SeriesDtypeEnum.StringIndexType.value:
        pnteh__aln, mya__rnts = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return pnteh__aln, StringIndexType(mya__rnts)
    elif typ_enum_list[0] == SeriesDtypeEnum.BinaryIndexType.value:
        pnteh__aln, mya__rnts = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return pnteh__aln, BinaryIndexType(mya__rnts)
    elif typ_enum_list[0] == SeriesDtypeEnum.TimedeltaIndexType.value:
        pnteh__aln, mya__rnts = _dtype_from_type_enum_list_recursor(
            typ_enum_list[1:])
        return pnteh__aln, TimedeltaIndexType(mya__rnts)
    else:
        raise_bodo_error(
            f'Unexpected Internal Error while converting typing metadata: unable to infer dtype for type enum {typ_enum_list[0]}. Please file the error here: https://github.com/Bodo-inc/Feedback'
            )


def _dtype_to_type_enum_list(typ):
    return guard(_dtype_to_type_enum_list_recursor, typ)


def _dtype_to_type_enum_list_recursor(typ, upcast_numeric_index=True):
    if typ.__hash__ and typ in _one_to_one_type_to_enum_map:
        return [_one_to_one_type_to_enum_map[typ]]
    if isinstance(typ, (dict, int, list, tuple, str, bool, bytes, float)):
        return [SeriesDtypeEnum.Literal.value, typ]
    elif typ is None:
        return [SeriesDtypeEnum.Literal.value, typ]
    elif is_overload_constant_int(typ):
        eeocq__wfn = get_overload_const_int(typ)
        if numba.types.maybe_literal(eeocq__wfn) == typ:
            return [SeriesDtypeEnum.LiteralType.value, eeocq__wfn]
    elif is_overload_constant_str(typ):
        eeocq__wfn = get_overload_const_str(typ)
        if numba.types.maybe_literal(eeocq__wfn) == typ:
            return [SeriesDtypeEnum.LiteralType.value, eeocq__wfn]
    elif is_overload_constant_bool(typ):
        eeocq__wfn = get_overload_const_bool(typ)
        if numba.types.maybe_literal(eeocq__wfn) == typ:
            return [SeriesDtypeEnum.LiteralType.value, eeocq__wfn]
    elif isinstance(typ, IntegerArrayType):
        return [SeriesDtypeEnum.IntegerArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, FloatingArrayType):
        return [SeriesDtypeEnum.FloatingArray.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif bodo.utils.utils.is_array_typ(typ, False):
        return [SeriesDtypeEnum.ARRAY.value
            ] + _dtype_to_type_enum_list_recursor(typ.dtype)
    elif isinstance(typ, StructType):
        bok__ypkct = [SeriesDtypeEnum.STRUCT.value, len(typ.names)]
        for dmtfv__xabnx in typ.names:
            bok__ypkct.append(dmtfv__xabnx)
        for hhlq__dtz in typ.data:
            bok__ypkct += _dtype_to_type_enum_list_recursor(hhlq__dtz)
        return bok__ypkct
    elif isinstance(typ, bodo.libs.decimal_arr_ext.Decimal128Type):
        return [SeriesDtypeEnum.Decimal.value, typ.precision, typ.scale]
    elif isinstance(typ, PDCategoricalDtype):
        dgzn__mrau = _dtype_to_type_enum_list_recursor(typ.categories)
        bdiw__brktx = _dtype_to_type_enum_list_recursor(typ.elem_type)
        cwm__vnat = _dtype_to_type_enum_list_recursor(typ.ordered)
        azhi__jcq = _dtype_to_type_enum_list_recursor(typ.data)
        xlykc__njq = _dtype_to_type_enum_list_recursor(typ.int_type)
        return [SeriesDtypeEnum.CategoricalType.value
            ] + dgzn__mrau + bdiw__brktx + cwm__vnat + azhi__jcq + xlykc__njq
    elif isinstance(typ, DatetimeIndexType):
        return [SeriesDtypeEnum.DatetimeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, NumericIndexType):
        if upcast_numeric_index:
            if isinstance(typ.dtype, types.Float):
                hexin__jpiib = types.float64
                if isinstance(typ.data, FloatingArrayType):
                    veug__zwjp = FloatingArrayType(hexin__jpiib)
                else:
                    veug__zwjp = types.Array(hexin__jpiib, 1, 'C')
            elif typ.dtype in {types.int8, types.int16, types.int32, types.
                int64}:
                hexin__jpiib = types.int64
                if isinstance(typ.data, IntegerArrayType):
                    veug__zwjp = IntegerArrayType(hexin__jpiib)
                else:
                    veug__zwjp = types.Array(hexin__jpiib, 1, 'C')
            elif typ.dtype in {types.uint8, types.uint16, types.uint32,
                types.uint64}:
                hexin__jpiib = types.uint64
                if isinstance(typ.data, IntegerArrayType):
                    veug__zwjp = IntegerArrayType(hexin__jpiib)
                else:
                    veug__zwjp = types.Array(hexin__jpiib, 1, 'C')
            elif typ.dtype == types.bool_:
                hexin__jpiib = typ.dtype
                veug__zwjp = typ.data
            else:
                raise GuardException('Unable to convert type')
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(hexin__jpiib
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(veug__zwjp)
        else:
            return [SeriesDtypeEnum.NumericIndexType.value
                ] + _dtype_to_type_enum_list_recursor(typ.dtype
                ) + _dtype_to_type_enum_list_recursor(typ.name_typ
                ) + _dtype_to_type_enum_list_recursor(typ.data)
    elif isinstance(typ, PeriodIndexType):
        return [SeriesDtypeEnum.PeriodIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.freq
            ) + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, CategoricalIndexType):
        return [SeriesDtypeEnum.CategoricalIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.data
            ) + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, RangeIndexType):
        return [SeriesDtypeEnum.RangeIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, StringIndexType):
        return [SeriesDtypeEnum.StringIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, BinaryIndexType):
        return [SeriesDtypeEnum.BinaryIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    elif isinstance(typ, TimedeltaIndexType):
        return [SeriesDtypeEnum.TimedeltaIndexType.value
            ] + _dtype_to_type_enum_list_recursor(typ.name_typ)
    else:
        raise GuardException('Unable to convert type')


def _is_wrapper_pd_arr(arr):
    if isinstance(arr, pd.arrays.StringArray):
        return False
    return isinstance(arr, (pd.arrays.PandasArray, pd.arrays.TimedeltaArray)
        ) or isinstance(arr, pd.arrays.DatetimeArray) and arr.tz is None


def unwrap_pd_arr(arr):
    if _is_wrapper_pd_arr(arr):
        return np.ascontiguousarray(arr._ndarray)
    return arr


def _fix_series_arr_type(pd_arr):
    if _is_wrapper_pd_arr(pd_arr):
        return pd_arr._ndarray
    return pd_arr


def _infer_series_arr_type(S, array_metadata=None):
    if S.dtype == np.dtype('O'):
        if len(S.array) == 0 or S.isna().sum() == len(S):
            if array_metadata is not None:
                return _dtype_from_type_enum_list(array_metadata)
            elif hasattr(S, '_bodo_meta'
                ) and S._bodo_meta is not None and 'type_metadata' in S._bodo_meta and S._bodo_meta[
                'type_metadata'][1] is not None:
                loq__mbnz = S._bodo_meta['type_metadata'][1]
                return dtype_to_array_type(_dtype_from_type_enum_list(
                    loq__mbnz))
        return bodo.typeof(_fix_series_arr_type(S.array))
    try:
        hlgbi__aszto = bodo.typeof(_fix_series_arr_type(S.array))
        if hlgbi__aszto == types.Array(types.bool_, 1, 'C'):
            hlgbi__aszto = bodo.boolean_array
        if isinstance(hlgbi__aszto, types.Array):
            assert hlgbi__aszto.ndim == 1, 'invalid numpy array type in Series'
            hlgbi__aszto = types.Array(hlgbi__aszto.dtype, 1, 'C')
        return hlgbi__aszto
    except:
        raise BodoError(
            f'data type {S.dtype} for column {S.name} not supported yet')


def _get_use_df_parent_obj_flag(builder, context, pyapi, parent_obj, n_cols):
    if n_cols is None:
        return context.get_constant(types.bool_, False)
    rcoyl__okwda = cgutils.is_not_null(builder, parent_obj)
    seemj__ssafl = cgutils.alloca_once_value(builder, context.get_constant(
        types.int64, 0))
    with builder.if_then(rcoyl__okwda):
        bnqzc__hqf = pyapi.object_getattr_string(parent_obj, 'columns')
        tzo__jyaz = pyapi.call_method(bnqzc__hqf, '__len__', ())
        builder.store(pyapi.long_as_longlong(tzo__jyaz), seemj__ssafl)
        pyapi.decref(tzo__jyaz)
        pyapi.decref(bnqzc__hqf)
    use_parent_obj = builder.and_(rcoyl__okwda, builder.icmp_unsigned('==',
        builder.load(seemj__ssafl), context.get_constant(types.int64, n_cols)))
    return use_parent_obj


def _get_df_columns_obj(c, builder, context, pyapi, df_typ, dataframe_payload):
    if df_typ.has_runtime_cols:
        zas__qynz = df_typ.runtime_colname_typ
        context.nrt.incref(builder, zas__qynz, dataframe_payload.columns)
        return pyapi.from_native_value(zas__qynz, dataframe_payload.columns,
            c.env_manager)
    if all(isinstance(c, str) for c in df_typ.columns):
        dywyu__tpru = pd.array(df_typ.columns, 'string')
    elif all(isinstance(c, int) for c in df_typ.columns):
        dywyu__tpru = np.array(df_typ.columns, 'int64')
    else:
        dywyu__tpru = df_typ.columns
    sqmti__hru = numba.typeof(dywyu__tpru)
    sxgog__dgt = context.get_constant_generic(builder, sqmti__hru, dywyu__tpru)
    vtf__jju = pyapi.from_native_value(sqmti__hru, sxgog__dgt, c.env_manager)
    if (sqmti__hru == bodo.string_array_type and bodo.libs.str_arr_ext.
        use_pd_pyarrow_string_array):
        jzw__qduo = vtf__jju
        vtf__jju = pyapi.call_method(vtf__jju, 'to_numpy', ())
        pyapi.decref(jzw__qduo)
    return vtf__jju


def _create_initial_df_object(builder, context, pyapi, c, df_typ, obj,
    dataframe_payload, res, use_parent_obj):
    with c.builder.if_else(use_parent_obj) as (uqus__myrpw, kteel__dswh):
        with uqus__myrpw:
            pyapi.incref(obj)
            kul__rfj = context.insert_const_string(c.builder.module, 'numpy')
            xam__ggh = pyapi.import_module_noblock(kul__rfj)
            if df_typ.has_runtime_cols:
                lvd__jli = 0
            else:
                lvd__jli = len(df_typ.columns)
            vkrjc__eyva = pyapi.long_from_longlong(lir.Constant(lir.IntType
                (64), lvd__jli))
            mac__gwqsl = pyapi.call_method(xam__ggh, 'arange', (vkrjc__eyva,))
            pyapi.object_setattr_string(obj, 'columns', mac__gwqsl)
            pyapi.decref(xam__ggh)
            pyapi.decref(mac__gwqsl)
            pyapi.decref(vkrjc__eyva)
        with kteel__dswh:
            context.nrt.incref(builder, df_typ.index, dataframe_payload.index)
            medgn__thbhq = c.pyapi.from_native_value(df_typ.index,
                dataframe_payload.index, c.env_manager)
            kul__rfj = context.insert_const_string(c.builder.module, 'pandas')
            xam__ggh = pyapi.import_module_noblock(kul__rfj)
            df_obj = pyapi.call_method(xam__ggh, 'DataFrame', (pyapi.
                borrow_none(), medgn__thbhq))
            pyapi.decref(xam__ggh)
            pyapi.decref(medgn__thbhq)
            builder.store(df_obj, res)


@box(DataFrameType)
def box_dataframe(typ, val, c):
    from bodo.hiframes.table import box_table
    context = c.context
    builder = c.builder
    pyapi = c.pyapi
    dataframe_payload = bodo.hiframes.pd_dataframe_ext.get_dataframe_payload(c
        .context, c.builder, typ, val)
    utqn__ohbyw = cgutils.create_struct_proxy(typ)(context, builder, value=val)
    n_cols = len(typ.columns) if not typ.has_runtime_cols else None
    obj = utqn__ohbyw.parent
    res = cgutils.alloca_once_value(builder, obj)
    use_parent_obj = _get_use_df_parent_obj_flag(builder, context, pyapi,
        obj, n_cols)
    _create_initial_df_object(builder, context, pyapi, c, typ, obj,
        dataframe_payload, res, use_parent_obj)
    if typ.is_table_format:
        uluft__jlfa = typ.table_type
        zhfxi__xky = builder.extract_value(dataframe_payload.data, 0)
        context.nrt.incref(builder, uluft__jlfa, zhfxi__xky)
        mqdop__fvxcr = box_table(uluft__jlfa, zhfxi__xky, c, builder.not_(
            use_parent_obj))
        with builder.if_else(use_parent_obj) as (mzzah__kmoao, par__ltz):
            with mzzah__kmoao:
                aefs__xtjth = pyapi.object_getattr_string(mqdop__fvxcr,
                    'arrays')
                wsqrx__igfjo = c.pyapi.make_none()
                if n_cols is None:
                    tzo__jyaz = pyapi.call_method(aefs__xtjth, '__len__', ())
                    kdrlw__tbl = pyapi.long_as_longlong(tzo__jyaz)
                    pyapi.decref(tzo__jyaz)
                else:
                    kdrlw__tbl = context.get_constant(types.int64, n_cols)
                with cgutils.for_range(builder, kdrlw__tbl) as caed__ipcfm:
                    i = caed__ipcfm.index
                    guxt__snhnu = pyapi.list_getitem(aefs__xtjth, i)
                    qord__ubmz = c.builder.icmp_unsigned('!=', guxt__snhnu,
                        wsqrx__igfjo)
                    with builder.if_then(qord__ubmz):
                        kzir__reppd = pyapi.long_from_longlong(i)
                        df_obj = builder.load(res)
                        pyapi.object_setitem(df_obj, kzir__reppd, guxt__snhnu)
                        pyapi.decref(kzir__reppd)
                pyapi.decref(aefs__xtjth)
                pyapi.decref(wsqrx__igfjo)
            with par__ltz:
                df_obj = builder.load(res)
                medgn__thbhq = pyapi.object_getattr_string(df_obj, 'index')
                kvxj__hdzwz = c.pyapi.call_method(mqdop__fvxcr, 'to_pandas',
                    (medgn__thbhq,))
                builder.store(kvxj__hdzwz, res)
                pyapi.decref(df_obj)
                pyapi.decref(medgn__thbhq)
        pyapi.decref(mqdop__fvxcr)
    else:
        wdhn__gvs = [builder.extract_value(dataframe_payload.data, i) for i in
            range(n_cols)]
        yfen__zturt = typ.data
        for i, arr, knnc__ncwww in zip(range(n_cols), wdhn__gvs, yfen__zturt):
            umec__urqqb = cgutils.alloca_once_value(builder, arr)
            ose__kga = cgutils.alloca_once_value(builder, context.
                get_constant_null(knnc__ncwww))
            qord__ubmz = builder.not_(is_ll_eq(builder, umec__urqqb, ose__kga))
            qvbz__bddyz = builder.or_(builder.not_(use_parent_obj), builder
                .and_(use_parent_obj, qord__ubmz))
            with builder.if_then(qvbz__bddyz):
                kzir__reppd = pyapi.long_from_longlong(context.get_constant
                    (types.int64, i))
                context.nrt.incref(builder, knnc__ncwww, arr)
                arr_obj = pyapi.from_native_value(knnc__ncwww, arr, c.
                    env_manager)
                df_obj = builder.load(res)
                pyapi.object_setitem(df_obj, kzir__reppd, arr_obj)
                pyapi.decref(arr_obj)
                pyapi.decref(kzir__reppd)
    df_obj = builder.load(res)
    vtf__jju = _get_df_columns_obj(c, builder, context, pyapi, typ,
        dataframe_payload)
    pyapi.object_setattr_string(df_obj, 'columns', vtf__jju)
    pyapi.decref(vtf__jju)
    _set_bodo_meta_dataframe(c, df_obj, typ)
    c.context.nrt.decref(c.builder, typ, val)
    return df_obj


def get_df_obj_column_codegen(context, builder, pyapi, df_obj, col_ind,
    data_typ):
    wsqrx__igfjo = pyapi.borrow_none()
    els__tgo = pyapi.unserialize(pyapi.serialize_object(slice))
    fyp__wci = pyapi.call_function_objargs(els__tgo, [wsqrx__igfjo])
    rax__bdo = pyapi.long_from_longlong(col_ind)
    xdbpb__gny = pyapi.tuple_pack([fyp__wci, rax__bdo])
    ratpp__yulff = pyapi.object_getattr_string(df_obj, 'iloc')
    xuzmx__vbjb = pyapi.object_getitem(ratpp__yulff, xdbpb__gny)
    joa__hlpu = pyapi.object_getattr_string(xuzmx__vbjb, 'array')
    pwdw__lag = pyapi.unserialize(pyapi.serialize_object(unwrap_pd_arr))
    arr_obj = pyapi.call_function_objargs(pwdw__lag, [joa__hlpu])
    pyapi.decref(joa__hlpu)
    pyapi.decref(pwdw__lag)
    pyapi.decref(els__tgo)
    pyapi.decref(fyp__wci)
    pyapi.decref(rax__bdo)
    pyapi.decref(xdbpb__gny)
    pyapi.decref(ratpp__yulff)
    pyapi.decref(xuzmx__vbjb)
    return arr_obj


@intrinsic
def unbox_dataframe_column(typingctx, df, i=None):
    assert isinstance(df, DataFrameType) and is_overload_constant_int(i)

    def codegen(context, builder, sig, args):
        pyapi = context.get_python_api(builder)
        c = numba.core.pythonapi._UnboxContext(context, builder, pyapi)
        df_typ = sig.args[0]
        col_ind = get_overload_const_int(sig.args[1])
        data_typ = df_typ.data[col_ind]
        utqn__ohbyw = cgutils.create_struct_proxy(sig.args[0])(context,
            builder, value=args[0])
        arr_obj = get_df_obj_column_codegen(context, builder, pyapi,
            utqn__ohbyw.parent, args[1], data_typ)
        cini__uusj = _unbox_series_data(data_typ.dtype, data_typ, arr_obj, c)
        c.pyapi.decref(arr_obj)
        dataframe_payload = (bodo.hiframes.pd_dataframe_ext.
            get_dataframe_payload(c.context, c.builder, df_typ, args[0]))
        if df_typ.is_table_format:
            zhfxi__xky = cgutils.create_struct_proxy(df_typ.table_type)(c.
                context, c.builder, builder.extract_value(dataframe_payload
                .data, 0))
            nipj__mtr = df_typ.table_type.type_to_blk[data_typ]
            druf__mxbk = getattr(zhfxi__xky, f'block_{nipj__mtr}')
            arcpy__vanp = ListInstance(c.context, c.builder, types.List(
                data_typ), druf__mxbk)
            rqgq__loo = context.get_constant(types.int64, df_typ.table_type
                .block_offsets[col_ind])
            arcpy__vanp.inititem(rqgq__loo, cini__uusj.value, incref=False)
        else:
            dataframe_payload.data = builder.insert_value(dataframe_payload
                .data, cini__uusj.value, col_ind)
        hkplo__ksxsm = DataFramePayloadType(df_typ)
        fcb__sot = context.nrt.meminfo_data(builder, utqn__ohbyw.meminfo)
        ozvtq__gkdmb = context.get_value_type(hkplo__ksxsm).as_pointer()
        fcb__sot = builder.bitcast(fcb__sot, ozvtq__gkdmb)
        builder.store(dataframe_payload._getvalue(), fcb__sot)
    return signature(types.none, df, i), codegen


@numba.njit
def unbox_col_if_needed(df, i):
    if bodo.hiframes.pd_dataframe_ext.has_parent(df
        ) and bodo.hiframes.pd_dataframe_ext._column_needs_unboxing(df, i):
        bodo.hiframes.boxing.unbox_dataframe_column(df, i)


@unbox(SeriesType)
def unbox_series(typ, val, c):
    joa__hlpu = c.pyapi.object_getattr_string(val, 'array')
    pwdw__lag = c.pyapi.unserialize(c.pyapi.serialize_object(unwrap_pd_arr))
    arr_obj = c.pyapi.call_function_objargs(pwdw__lag, [joa__hlpu])
    tycov__oii = _unbox_series_data(typ.dtype, typ.data, arr_obj, c).value
    medgn__thbhq = c.pyapi.object_getattr_string(val, 'index')
    jydgy__hvie = c.pyapi.to_native_value(typ.index, medgn__thbhq).value
    orm__dwai = c.pyapi.object_getattr_string(val, 'name')
    gkik__fpbcy = c.pyapi.to_native_value(typ.name_typ, orm__dwai).value
    yjkt__ncj = bodo.hiframes.pd_series_ext.construct_series(c.context, c.
        builder, typ, tycov__oii, jydgy__hvie, gkik__fpbcy)
    c.pyapi.decref(pwdw__lag)
    c.pyapi.decref(joa__hlpu)
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(medgn__thbhq)
    c.pyapi.decref(orm__dwai)
    return NativeValue(yjkt__ncj)


def _unbox_series_data(dtype, data_typ, arr_obj, c):
    if data_typ == string_array_split_view_type:
        xmc__jdsb = c.context.make_helper(c.builder,
            string_array_split_view_type)
        return NativeValue(xmc__jdsb._getvalue())
    return c.pyapi.to_native_value(data_typ, arr_obj)


@box(HeterogeneousSeriesType)
@box(SeriesType)
def box_series(typ, val, c):
    kul__rfj = c.context.insert_const_string(c.builder.module, 'pandas')
    var__kni = c.pyapi.import_module_noblock(kul__rfj)
    ssrb__qaj = bodo.hiframes.pd_series_ext.get_series_payload(c.context, c
        .builder, typ, val)
    c.context.nrt.incref(c.builder, typ.data, ssrb__qaj.data)
    c.context.nrt.incref(c.builder, typ.index, ssrb__qaj.index)
    c.context.nrt.incref(c.builder, typ.name_typ, ssrb__qaj.name)
    arr_obj = c.pyapi.from_native_value(typ.data, ssrb__qaj.data, c.env_manager
        )
    medgn__thbhq = c.pyapi.from_native_value(typ.index, ssrb__qaj.index, c.
        env_manager)
    orm__dwai = c.pyapi.from_native_value(typ.name_typ, ssrb__qaj.name, c.
        env_manager)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        dtype = c.pyapi.unserialize(c.pyapi.serialize_object(object))
    else:
        dtype = c.pyapi.make_none()
    res = c.pyapi.call_method(var__kni, 'Series', (arr_obj, medgn__thbhq,
        dtype, orm__dwai))
    c.pyapi.decref(arr_obj)
    c.pyapi.decref(medgn__thbhq)
    c.pyapi.decref(orm__dwai)
    if isinstance(typ, HeterogeneousSeriesType) and isinstance(typ.data,
        bodo.NullableTupleType):
        c.pyapi.decref(dtype)
    _set_bodo_meta_series(res, c, typ)
    c.pyapi.decref(var__kni)
    c.context.nrt.decref(c.builder, typ, val)
    return res


def type_enum_list_to_py_list_obj(pyapi, context, builder, env_manager,
    typ_list):
    ojey__dhcjw = []
    for dzn__cpqyf in typ_list:
        if isinstance(dzn__cpqyf, int) and not isinstance(dzn__cpqyf, bool):
            anjd__xoivy = pyapi.long_from_longlong(lir.Constant(lir.IntType
                (64), dzn__cpqyf))
        else:
            mof__vyt = numba.typeof(dzn__cpqyf)
            mmvex__wwqs = context.get_constant_generic(builder, mof__vyt,
                dzn__cpqyf)
            anjd__xoivy = pyapi.from_native_value(mof__vyt, mmvex__wwqs,
                env_manager)
        ojey__dhcjw.append(anjd__xoivy)
    lyky__ixkg = pyapi.list_pack(ojey__dhcjw)
    for val in ojey__dhcjw:
        pyapi.decref(val)
    return lyky__ixkg


def _set_bodo_meta_dataframe(c, obj, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    eslj__irmpy = not typ.has_runtime_cols
    pllqe__iotp = 2 if eslj__irmpy else 1
    ncddj__vzqj = pyapi.dict_new(pllqe__iotp)
    eix__cef = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    pyapi.dict_setitem_string(ncddj__vzqj, 'dist', eix__cef)
    pyapi.decref(eix__cef)
    if eslj__irmpy:
        roiwh__exoqn = _dtype_to_type_enum_list(typ.index)
        if roiwh__exoqn != None:
            kvp__cxho = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, roiwh__exoqn)
        else:
            kvp__cxho = pyapi.make_none()
        if typ.is_table_format:
            puoe__jng = typ.table_type
            lpkke__bbi = pyapi.list_new(lir.Constant(lir.IntType(64), len(
                typ.data)))
            for nipj__mtr, dtype in puoe__jng.blk_to_type.items():
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    typ_list = type_enum_list_to_py_list_obj(pyapi, context,
                        builder, c.env_manager, typ_list)
                else:
                    typ_list = pyapi.make_none()
                kdrlw__tbl = c.context.get_constant(types.int64, len(
                    puoe__jng.block_to_arr_ind[nipj__mtr]))
                tvwns__puzc = c.context.make_constant_array(c.builder,
                    types.Array(types.int64, 1, 'C'), np.array(puoe__jng.
                    block_to_arr_ind[nipj__mtr], dtype=np.int64))
                ityq__vdixy = c.context.make_array(types.Array(types.int64,
                    1, 'C'))(c.context, c.builder, tvwns__puzc)
                with cgutils.for_range(c.builder, kdrlw__tbl) as caed__ipcfm:
                    i = caed__ipcfm.index
                    hbsqn__qjdmh = _getitem_array_single_int(c.context, c.
                        builder, types.int64, types.Array(types.int64, 1,
                        'C'), ityq__vdixy, i)
                    c.context.nrt.incref(builder, types.pyobject, typ_list)
                    pyapi.list_setitem(lpkke__bbi, hbsqn__qjdmh, typ_list)
                c.context.nrt.decref(builder, types.pyobject, typ_list)
        else:
            apgcp__ltgqd = []
            for dtype in typ.data:
                typ_list = _dtype_to_type_enum_list(dtype)
                if typ_list != None:
                    lyky__ixkg = type_enum_list_to_py_list_obj(pyapi,
                        context, builder, c.env_manager, typ_list)
                else:
                    lyky__ixkg = pyapi.make_none()
                apgcp__ltgqd.append(lyky__ixkg)
            lpkke__bbi = pyapi.list_pack(apgcp__ltgqd)
            for val in apgcp__ltgqd:
                pyapi.decref(val)
        htdqi__tnmx = pyapi.list_pack([kvp__cxho, lpkke__bbi])
        pyapi.dict_setitem_string(ncddj__vzqj, 'type_metadata', htdqi__tnmx)
    pyapi.object_setattr_string(obj, '_bodo_meta', ncddj__vzqj)
    pyapi.decref(ncddj__vzqj)


def get_series_dtype_handle_null_int_and_hetrogenous(series_typ):
    if isinstance(series_typ, HeterogeneousSeriesType):
        return None
    if isinstance(series_typ.dtype, types.Number) and isinstance(series_typ
        .data, IntegerArrayType):
        return IntDtype(series_typ.dtype)
    if isinstance(series_typ.dtype, types.Float) and isinstance(series_typ.
        data, FloatingArrayType):
        return FloatDtype(series_typ.dtype)
    return series_typ.dtype


def _set_bodo_meta_series(obj, c, typ):
    pyapi = c.pyapi
    context = c.context
    builder = c.builder
    ncddj__vzqj = pyapi.dict_new(2)
    eix__cef = pyapi.long_from_longlong(lir.Constant(lir.IntType(64), typ.
        dist.value))
    roiwh__exoqn = _dtype_to_type_enum_list(typ.index)
    if roiwh__exoqn != None:
        kvp__cxho = type_enum_list_to_py_list_obj(pyapi, context, builder,
            c.env_manager, roiwh__exoqn)
    else:
        kvp__cxho = pyapi.make_none()
    dtype = get_series_dtype_handle_null_int_and_hetrogenous(typ)
    if dtype != None:
        typ_list = _dtype_to_type_enum_list(dtype)
        if typ_list != None:
            esd__jvkwq = type_enum_list_to_py_list_obj(pyapi, context,
                builder, c.env_manager, typ_list)
        else:
            esd__jvkwq = pyapi.make_none()
    else:
        esd__jvkwq = pyapi.make_none()
    rcz__mqxfv = pyapi.list_pack([kvp__cxho, esd__jvkwq])
    pyapi.dict_setitem_string(ncddj__vzqj, 'type_metadata', rcz__mqxfv)
    pyapi.decref(rcz__mqxfv)
    pyapi.dict_setitem_string(ncddj__vzqj, 'dist', eix__cef)
    pyapi.object_setattr_string(obj, '_bodo_meta', ncddj__vzqj)
    pyapi.decref(ncddj__vzqj)
    pyapi.decref(eix__cef)


@typeof_impl.register(np.ndarray)
def _typeof_ndarray(val, c):
    try:
        dtype = numba.np.numpy_support.from_dtype(val.dtype)
    except NotImplementedError as inch__whenv:
        dtype = types.pyobject
    if dtype == types.pyobject:
        return _infer_ndarray_obj_dtype(val)
    ioli__xmood = numba.np.numpy_support.map_layout(val)
    gavk__dkbhy = not val.flags.writeable
    return types.Array(dtype, val.ndim, ioli__xmood, readonly=gavk__dkbhy)


def _infer_ndarray_obj_dtype(val):
    if not val.dtype == np.dtype('O'):
        raise BodoError('Unsupported array dtype: {}'.format(val.dtype))
    i = 0
    while i < len(val) and (pd.api.types.is_scalar(val[i]) and pd.isna(val[
        i]) or not pd.api.types.is_scalar(val[i]) and len(val[i]) == 0):
        i += 1
    if i == len(val):
        warnings.warn(BodoWarning(
            'Empty object array passed to Bodo, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    soe__stb = val[i]
    wlw__mjumg = 100
    if isinstance(soe__stb, str):
        return (bodo.dict_str_arr_type if _use_dict_str_type else
            string_array_type)
    elif isinstance(soe__stb, (bytes, bytearray)):
        return binary_array_type
    elif isinstance(soe__stb, bool):
        return bodo.libs.bool_arr_ext.boolean_array
    elif isinstance(soe__stb, (int, np.int8, np.int16, np.int32, np.int64,
        np.uint8, np.uint16, np.uint32, np.uint64)):
        return bodo.libs.int_arr_ext.IntegerArrayType(numba.typeof(soe__stb))
    elif isinstance(soe__stb, (float, np.float32, np.float64)):
        return bodo.libs.float_arr_ext.FloatingArrayType(numba.typeof(soe__stb)
            )
    elif isinstance(soe__stb, (dict, Dict)) and len(soe__stb.keys()
        ) <= wlw__mjumg and all(isinstance(iah__kcgcj, str) for iah__kcgcj in
        soe__stb.keys()):
        ohx__ysrkz = tuple(soe__stb.keys())
        xweu__efsiu = tuple(_get_struct_value_arr_type(v) for v in soe__stb
            .values())
        return StructArrayType(xweu__efsiu, ohx__ysrkz)
    elif isinstance(soe__stb, (dict, Dict)):
        oys__ujuh = numba.typeof(_value_to_array(list(soe__stb.keys())))
        fure__hnvtq = numba.typeof(_value_to_array(list(soe__stb.values())))
        oys__ujuh = to_str_arr_if_dict_array(oys__ujuh)
        fure__hnvtq = to_str_arr_if_dict_array(fure__hnvtq)
        return MapArrayType(oys__ujuh, fure__hnvtq)
    elif isinstance(soe__stb, tuple):
        xweu__efsiu = tuple(_get_struct_value_arr_type(v) for v in soe__stb)
        return TupleArrayType(xweu__efsiu)
    if isinstance(soe__stb, (list, np.ndarray, pd.arrays.BooleanArray, pd.
        arrays.IntegerArray, pd.arrays.FloatingArray, pd.arrays.StringArray,
        pd.arrays.ArrowStringArray)):
        if isinstance(soe__stb, list):
            soe__stb = _value_to_array(soe__stb)
        cxklj__iavir = numba.typeof(soe__stb)
        cxklj__iavir = to_str_arr_if_dict_array(cxklj__iavir)
        return ArrayItemArrayType(cxklj__iavir)
    if isinstance(soe__stb, datetime.date):
        return datetime_date_array_type
    if isinstance(soe__stb, datetime.timedelta):
        return datetime_timedelta_array_type
    if isinstance(soe__stb, bodo.Time):
        return TimeArrayType(soe__stb.precision)
    if isinstance(soe__stb, decimal.Decimal):
        return DecimalArrayType(38, 18)
    if isinstance(soe__stb, pd._libs.interval.Interval):
        return bodo.libs.interval_arr_ext.IntervalArrayType
    raise BodoError(f'Unsupported object array with first value: {soe__stb}')


def _value_to_array(val):
    assert isinstance(val, (list, dict, Dict))
    if isinstance(val, (dict, Dict)):
        val = dict(val)
        return np.array([val], np.object_)
    mjtv__rhs = val.copy()
    mjtv__rhs.append(None)
    arr = np.array(mjtv__rhs, np.object_)
    if len(val) and isinstance(val[0], float):
        arr = np.array(val, np.float64)
    return arr


def _get_struct_value_arr_type(v):
    if isinstance(v, (dict, Dict)):
        return numba.typeof(_value_to_array(v))
    if isinstance(v, list):
        return dtype_to_array_type(numba.typeof(_value_to_array(v)))
    if pd.api.types.is_scalar(v) and pd.isna(v):
        warnings.warn(BodoWarning(
            'Field value in struct array is NA, which causes ambiguity in typing. This can cause errors in parallel execution.'
            ))
        return string_array_type
    knnc__ncwww = dtype_to_array_type(numba.typeof(v))
    if isinstance(v, (int, bool)):
        knnc__ncwww = to_nullable_type(knnc__ncwww)
    return knnc__ncwww
