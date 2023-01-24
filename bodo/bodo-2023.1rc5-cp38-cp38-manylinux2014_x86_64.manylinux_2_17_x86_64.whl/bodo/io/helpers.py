"""
File that contains some IO related helpers.
"""
import os
import threading
import uuid
import numba
import pyarrow as pa
from mpi4py import MPI
from numba.core import types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, models, register_model, typeof_impl, unbox
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type, datetime_date_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, PDCategoricalDtype
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.time_ext import TimeArrayType, TimeType
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType
from bodo.libs.dict_arr_ext import dict_str_arr_type
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.struct_arr_ext import StructArrayType
from bodo.utils import tracing
from bodo.utils.typing import BodoError, raise_bodo_error


class PyArrowTableSchemaType(types.Opaque):

    def __init__(self):
        super(PyArrowTableSchemaType, self).__init__(name=
            'PyArrowTableSchemaType')


pyarrow_table_schema_type = PyArrowTableSchemaType()
types.pyarrow_table_schema_type = pyarrow_table_schema_type
register_model(PyArrowTableSchemaType)(models.OpaqueModel)


@unbox(PyArrowTableSchemaType)
def unbox_pyarrow_table_schema_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(PyArrowTableSchemaType)
def box_pyarrow_table_schema_type(typ, val, c):
    c.pyapi.incref(val)
    return val


@typeof_impl.register(pa.lib.Schema)
def typeof_pyarrow_table_schema(val, c):
    return pyarrow_table_schema_type


@lower_constant(PyArrowTableSchemaType)
def lower_pyarrow_table_schema(context, builder, ty, pyval):
    vkle__npylu = context.get_python_api(builder)
    return vkle__npylu.unserialize(vkle__npylu.serialize_object(pyval))


def is_nullable(typ):
    return bodo.utils.utils.is_array_typ(typ, False) and (not isinstance(
        typ, types.Array) and not isinstance(typ, bodo.DatetimeArrayType))


def pa_schema_unify_reduction(schema_a, schema_b, unused):
    return pa.unify_schemas([schema_a, schema_b])


pa_schema_unify_mpi_op = MPI.Op.Create(pa_schema_unify_reduction, commute=True)
use_nullable_pd_arr = True
_pyarrow_numba_type_map = {pa.bool_(): types.bool_, pa.int8(): types.int8,
    pa.int16(): types.int16, pa.int32(): types.int32, pa.int64(): types.
    int64, pa.uint8(): types.uint8, pa.uint16(): types.uint16, pa.uint32():
    types.uint32, pa.uint64(): types.uint64, pa.float32(): types.float32,
    pa.float64(): types.float64, pa.string(): string_type, pa.large_string(
    ): string_type, pa.binary(): bytes_type, pa.date32():
    datetime_date_type, pa.date64(): types.NPDatetime('ns'), pa.time32('s'):
    TimeType(0), pa.time32('ms'): TimeType(3), pa.time64('us'): TimeType(6),
    pa.time64('ns'): TimeType(9), pa.null(): string_type}


def get_arrow_timestamp_type(pa_ts_typ):
    sgz__nqruw = ['ns', 'us', 'ms', 's']
    if pa_ts_typ.unit not in sgz__nqruw:
        return types.Array(bodo.datetime64ns, 1, 'C'), False
    elif pa_ts_typ.tz is not None:
        gph__ihbxw = pa_ts_typ.to_pandas_dtype().tz
        zfe__lvhto = bodo.libs.pd_datetime_arr_ext.get_pytz_type_info(
            gph__ihbxw)
        return bodo.DatetimeArrayType(zfe__lvhto), True
    else:
        return types.Array(bodo.datetime64ns, 1, 'C'), True


def _get_numba_typ_from_pa_typ(pa_typ: pa.Field, is_index,
    nullable_from_metadata, category_info, str_as_dict=False):
    if isinstance(pa_typ.type, pa.ListType):
        jpb__ebi, jcso__vsi = _get_numba_typ_from_pa_typ(pa_typ.type.
            value_field, is_index, nullable_from_metadata, category_info)
        return ArrayItemArrayType(jpb__ebi), jcso__vsi
    if isinstance(pa_typ.type, pa.StructType):
        fetz__iwb = []
        bou__nkuim = []
        jcso__vsi = True
        for dyclp__tnuq in pa_typ.flatten():
            bou__nkuim.append(dyclp__tnuq.name.split('.')[-1])
            psnu__rjsot, lkou__rhbk = _get_numba_typ_from_pa_typ(dyclp__tnuq,
                is_index, nullable_from_metadata, category_info)
            fetz__iwb.append(psnu__rjsot)
            jcso__vsi = jcso__vsi and lkou__rhbk
        return StructArrayType(tuple(fetz__iwb), tuple(bou__nkuim)), jcso__vsi
    if isinstance(pa_typ.type, pa.Decimal128Type):
        return DecimalArrayType(pa_typ.type.precision, pa_typ.type.scale), True
    if str_as_dict:
        if pa_typ.type != pa.string():
            raise BodoError(
                f'Read as dictionary used for non-string column {pa_typ}')
        return dict_str_arr_type, True
    if isinstance(pa_typ.type, pa.DictionaryType):
        if pa_typ.type.value_type != pa.string():
            raise BodoError(
                f'Parquet Categorical data type should be string, not {pa_typ.type.value_type}'
                )
        cbg__uca = _pyarrow_numba_type_map[pa_typ.type.index_type]
        hsfk__zmnb = PDCategoricalDtype(category_info[pa_typ.name], bodo.
            string_type, pa_typ.type.ordered, int_type=cbg__uca)
        return CategoricalArrayType(hsfk__zmnb), True
    if isinstance(pa_typ.type, pa.lib.TimestampType):
        return get_arrow_timestamp_type(pa_typ.type)
    elif pa_typ.type in _pyarrow_numba_type_map:
        obb__wrfji = _pyarrow_numba_type_map[pa_typ.type]
        jcso__vsi = True
    else:
        raise BodoError('Arrow data type {} not supported yet'.format(
            pa_typ.type))
    if obb__wrfji == datetime_date_type:
        return datetime_date_array_type, jcso__vsi
    if isinstance(obb__wrfji, TimeType):
        return TimeArrayType(obb__wrfji.precision), jcso__vsi
    if obb__wrfji == bytes_type:
        return binary_array_type, jcso__vsi
    jpb__ebi = string_array_type if obb__wrfji == string_type else types.Array(
        obb__wrfji, 1, 'C')
    if obb__wrfji == types.bool_:
        jpb__ebi = boolean_array
    iaaxv__hrei = (use_nullable_pd_arr if nullable_from_metadata is None else
        nullable_from_metadata)
    if iaaxv__hrei and not is_index and isinstance(obb__wrfji, types.Integer
        ) and pa_typ.nullable:
        jpb__ebi = IntegerArrayType(obb__wrfji)
    if (iaaxv__hrei and bodo.libs.float_arr_ext._use_nullable_float and not
        is_index and isinstance(obb__wrfji, types.Float) and pa_typ.nullable):
        jpb__ebi = FloatingArrayType(obb__wrfji)
    return jpb__ebi, jcso__vsi


_numba_pyarrow_type_map = {types.bool_: pa.bool_(), types.int8: pa.int8(),
    types.int16: pa.int16(), types.int32: pa.int32(), types.int64: pa.int64
    (), types.uint8: pa.uint8(), types.uint16: pa.uint16(), types.uint32:
    pa.uint32(), types.uint64: pa.uint64(), types.float32: pa.float32(),
    types.float64: pa.float64(), types.NPDatetime('ns'): pa.date64()}


def is_nullable_arrow_out(numba_type: types.ArrayCompatible) ->bool:
    return is_nullable(numba_type) or isinstance(numba_type, bodo.
        DatetimeArrayType) or isinstance(numba_type, types.Array
        ) and numba_type.dtype == bodo.datetime64ns


def _numba_to_pyarrow_type(numba_type: types.ArrayCompatible, is_iceberg:
    bool=False):
    if isinstance(numba_type, ArrayItemArrayType):
        axvde__zkhc = pa.field('element', _numba_to_pyarrow_type(numba_type
            .dtype, is_iceberg)[0])
        obb__wrfji = pa.list_(axvde__zkhc)
    elif isinstance(numba_type, StructArrayType):
        loefb__xmh = []
        for onoqp__twwi, lyn__obl in zip(numba_type.names, numba_type.data):
            uxixg__aysr, lobbx__qqatn = _numba_to_pyarrow_type(lyn__obl,
                is_iceberg)
            loefb__xmh.append(pa.field(onoqp__twwi, uxixg__aysr, True))
        obb__wrfji = pa.struct(loefb__xmh)
    elif isinstance(numba_type, DecimalArrayType):
        obb__wrfji = pa.decimal128(numba_type.precision, numba_type.scale)
    elif isinstance(numba_type, CategoricalArrayType):
        hsfk__zmnb: PDCategoricalDtype = numba_type.dtype
        obb__wrfji = pa.dictionary(_numba_to_pyarrow_type(hsfk__zmnb.
            int_type, is_iceberg)[0], _numba_to_pyarrow_type(hsfk__zmnb.
            elem_type, is_iceberg)[0], ordered=False if hsfk__zmnb.ordered is
            None else hsfk__zmnb.ordered)
    elif numba_type == boolean_array:
        obb__wrfji = pa.bool_()
    elif numba_type in (string_array_type, bodo.dict_str_arr_type):
        obb__wrfji = pa.string()
    elif numba_type == binary_array_type:
        obb__wrfji = pa.binary()
    elif numba_type == datetime_date_array_type:
        obb__wrfji = pa.date32()
    elif isinstance(numba_type, bodo.DatetimeArrayType) or isinstance(
        numba_type, types.Array) and numba_type.dtype == bodo.datetime64ns:
        obb__wrfji = pa.timestamp('us', 'UTC') if is_iceberg else pa.timestamp(
            'ns', 'UTC')
    elif isinstance(numba_type, types.Array
        ) and numba_type.dtype == bodo.timedelta64ns:
        obb__wrfji = pa.duration('ns')
    elif isinstance(numba_type, (types.Array, IntegerArrayType,
        FloatingArrayType)) and numba_type.dtype in _numba_pyarrow_type_map:
        obb__wrfji = _numba_pyarrow_type_map[numba_type.dtype]
    elif isinstance(numba_type, bodo.TimeArrayType):
        if numba_type.precision == 0:
            obb__wrfji = pa.time32('s')
        elif numba_type.precision == 3:
            obb__wrfji = pa.time32('ms')
        elif numba_type.precision == 6:
            obb__wrfji = pa.time64('us')
        elif numba_type.precision == 9:
            obb__wrfji = pa.time64('ns')
    else:
        raise BodoError(
            f'Conversion from Bodo array type {numba_type} to PyArrow type not supported yet'
            )
    return obb__wrfji, is_nullable_arrow_out(numba_type)


def numba_to_pyarrow_schema(df: DataFrameType, is_iceberg: bool=False
    ) ->pa.Schema:
    loefb__xmh = []
    for onoqp__twwi, wlwb__vkt in zip(df.columns, df.data):
        try:
            xrm__mjwdr, itr__vux = _numba_to_pyarrow_type(wlwb__vkt, is_iceberg
                )
        except BodoError as ajl__jhwko:
            raise_bodo_error(ajl__jhwko.msg, ajl__jhwko.loc)
        loefb__xmh.append(pa.field(onoqp__twwi, xrm__mjwdr, itr__vux))
    return pa.schema(loefb__xmh)


def update_env_vars(env_vars):
    cyv__cmatd = {}
    for apqd__ljgu, cunc__afy in env_vars.items():
        if apqd__ljgu in os.environ:
            cyv__cmatd[apqd__ljgu] = os.environ[apqd__ljgu]
        else:
            cyv__cmatd[apqd__ljgu] = '__none__'
        if cunc__afy == '__none__':
            del os.environ[apqd__ljgu]
        else:
            os.environ[apqd__ljgu] = cunc__afy
    return cyv__cmatd


def update_file_contents(fname: str, contents: str, is_parallel=True) ->str:
    bxvvz__fopxq = MPI.COMM_WORLD
    ykqs__jdlq = None
    if not is_parallel or bxvvz__fopxq.Get_rank() == 0:
        if os.path.exists(fname):
            with open(fname, 'r') as vqc__pqjk:
                ykqs__jdlq = vqc__pqjk.read()
    if is_parallel:
        ykqs__jdlq = bxvvz__fopxq.bcast(ykqs__jdlq)
    if ykqs__jdlq is None:
        ykqs__jdlq = '__none__'
    uae__uxbn = bodo.get_rank() in bodo.get_nodes_first_ranks(
        ) if is_parallel else True
    if contents == '__none__':
        if uae__uxbn and os.path.exists(fname):
            os.remove(fname)
    elif uae__uxbn:
        with open(fname, 'w') as vqc__pqjk:
            vqc__pqjk.write(contents)
    if is_parallel:
        bxvvz__fopxq.Barrier()
    return ykqs__jdlq


@numba.njit
def uuid4_helper():
    with numba.objmode(out='unicode_type'):
        out = str(uuid.uuid4())
    return out


class ExceptionPropagatingThread(threading.Thread):

    def run(self):
        self.exc = None
        try:
            self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as ajl__jhwko:
            self.exc = ajl__jhwko

    def join(self, timeout=None):
        super().join(timeout)
        if self.exc:
            raise self.exc
        return self.ret


class ExceptionPropagatingThreadType(types.Opaque):

    def __init__(self):
        super(ExceptionPropagatingThreadType, self).__init__(name=
            'ExceptionPropagatingThreadType')


exception_propagating_thread_type = ExceptionPropagatingThreadType()
types.exception_propagating_thread_type = exception_propagating_thread_type
register_model(ExceptionPropagatingThreadType)(models.OpaqueModel)


@unbox(ExceptionPropagatingThreadType)
def unbox_exception_propagating_thread_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@box(ExceptionPropagatingThreadType)
def box_exception_propagating_thread_type(typ, val, c):
    c.pyapi.incref(val)
    return val


@typeof_impl.register(ExceptionPropagatingThread)
def typeof_exception_propagating_thread(val, c):
    return exception_propagating_thread_type


def join_all_threads(thread_list):
    bqvye__pex = tracing.Event('join_all_threads', is_parallel=True)
    bxvvz__fopxq = MPI.COMM_WORLD
    qsy__indwk = None
    try:
        for nbgu__hptw in thread_list:
            if isinstance(nbgu__hptw, threading.Thread):
                nbgu__hptw.join()
    except Exception as ajl__jhwko:
        qsy__indwk = ajl__jhwko
    rre__cee = int(qsy__indwk is not None)
    scea__lrbid, kuaa__xvlgt = bxvvz__fopxq.allreduce((rre__cee,
        bxvvz__fopxq.Get_rank()), op=MPI.MAXLOC)
    if scea__lrbid:
        if bxvvz__fopxq.Get_rank() == kuaa__xvlgt:
            fjlgk__yqq = qsy__indwk
        else:
            fjlgk__yqq = None
        fjlgk__yqq = bxvvz__fopxq.bcast(fjlgk__yqq, root=kuaa__xvlgt)
        if rre__cee:
            raise qsy__indwk
        else:
            raise fjlgk__yqq
    bqvye__pex.finalize()
