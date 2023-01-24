"""Tools for handling bodo arrays, e.g. passing to C/C++ code
"""
from collections import defaultdict
import llvmlite.binding as ll
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_cast
from numba.core.typing.templates import signature
from numba.cpython.listobj import ListInstance
from numba.extending import intrinsic, models, register_model
from numba.np.arrayobj import _getitem_array_single_int
import bodo
from bodo.hiframes.datetime_date_ext import datetime_date_array_type
from bodo.hiframes.pd_categorical_ext import CategoricalArrayType, get_categories_int_type
from bodo.hiframes.time_ext import TimeArrayType, TimeType
from bodo.libs import array_ext
from bodo.libs.array_item_arr_ext import ArrayItemArrayPayloadType, ArrayItemArrayType, _get_array_item_arr_payload, define_array_item_dtor, offset_type
from bodo.libs.binary_arr_ext import binary_array_type
from bodo.libs.bool_arr_ext import boolean_array
from bodo.libs.decimal_arr_ext import DecimalArrayType, int128_type
from bodo.libs.float_arr_ext import FloatingArrayType
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.interval_arr_ext import IntervalArrayType
from bodo.libs.map_arr_ext import MapArrayType, _get_map_arr_data_type, init_map_arr_codegen
from bodo.libs.str_arr_ext import _get_str_binary_arr_payload, char_arr_type, null_bitmap_arr_type, offset_arr_type, string_array_type
from bodo.libs.struct_arr_ext import StructArrayPayloadType, StructArrayType, StructType, _get_struct_arr_payload, define_struct_arr_dtor
from bodo.libs.tuple_arr_ext import TupleArrayType
from bodo.utils.typing import BodoError, MetaType, decode_if_dict_array, get_overload_const_int, is_overload_none, is_str_arr_type, raise_bodo_error, type_has_unknown_cats, unwrap_typeref
from bodo.utils.utils import CTypeEnum, check_and_propagate_cpp_exception, numba_to_c_type
ll.add_symbol('list_string_array_to_info', array_ext.list_string_array_to_info)
ll.add_symbol('nested_array_to_info', array_ext.nested_array_to_info)
ll.add_symbol('string_array_to_info', array_ext.string_array_to_info)
ll.add_symbol('dict_str_array_to_info', array_ext.dict_str_array_to_info)
ll.add_symbol('get_nested_info', array_ext.get_nested_info)
ll.add_symbol('get_has_global_dictionary', array_ext.get_has_global_dictionary)
ll.add_symbol('get_has_deduped_local_dictionary', array_ext.
    get_has_deduped_local_dictionary)
ll.add_symbol('numpy_array_to_info', array_ext.numpy_array_to_info)
ll.add_symbol('categorical_array_to_info', array_ext.categorical_array_to_info)
ll.add_symbol('nullable_array_to_info', array_ext.nullable_array_to_info)
ll.add_symbol('interval_array_to_info', array_ext.interval_array_to_info)
ll.add_symbol('decimal_array_to_info', array_ext.decimal_array_to_info)
ll.add_symbol('time_array_to_info', array_ext.time_array_to_info)
ll.add_symbol('info_to_nested_array', array_ext.info_to_nested_array)
ll.add_symbol('info_to_list_string_array', array_ext.info_to_list_string_array)
ll.add_symbol('info_to_string_array', array_ext.info_to_string_array)
ll.add_symbol('info_to_numpy_array', array_ext.info_to_numpy_array)
ll.add_symbol('info_to_nullable_array', array_ext.info_to_nullable_array)
ll.add_symbol('info_to_interval_array', array_ext.info_to_interval_array)
ll.add_symbol('alloc_numpy', array_ext.alloc_numpy)
ll.add_symbol('alloc_string_array', array_ext.alloc_string_array)
ll.add_symbol('arr_info_list_to_table', array_ext.arr_info_list_to_table)
ll.add_symbol('info_from_table', array_ext.info_from_table)
ll.add_symbol('delete_info_decref_array', array_ext.delete_info_decref_array)
ll.add_symbol('delete_table_decref_arrays', array_ext.
    delete_table_decref_arrays)
ll.add_symbol('decref_table_array', array_ext.decref_table_array)
ll.add_symbol('delete_table', array_ext.delete_table)
ll.add_symbol('shuffle_table', array_ext.shuffle_table)
ll.add_symbol('get_shuffle_info', array_ext.get_shuffle_info)
ll.add_symbol('delete_shuffle_info', array_ext.delete_shuffle_info)
ll.add_symbol('reverse_shuffle_table', array_ext.reverse_shuffle_table)
ll.add_symbol('hash_join_table', array_ext.hash_join_table)
ll.add_symbol('cross_join_table', array_ext.cross_join_table)
ll.add_symbol('drop_duplicates_table', array_ext.drop_duplicates_table)
ll.add_symbol('sort_values_table', array_ext.sort_values_table)
ll.add_symbol('sample_table', array_ext.sample_table)
ll.add_symbol('shuffle_renormalization', array_ext.shuffle_renormalization)
ll.add_symbol('shuffle_renormalization_group', array_ext.
    shuffle_renormalization_group)
ll.add_symbol('groupby_and_aggregate', array_ext.groupby_and_aggregate)
ll.add_symbol('convert_local_dictionary_to_global', array_ext.
    convert_local_dictionary_to_global)
ll.add_symbol('drop_duplicates_local_dictionary', array_ext.
    drop_duplicates_local_dictionary)
ll.add_symbol('get_groupby_labels', array_ext.get_groupby_labels)
ll.add_symbol('array_isin', array_ext.array_isin)
ll.add_symbol('get_search_regex', array_ext.get_search_regex)
ll.add_symbol('array_info_getitem', array_ext.array_info_getitem)
ll.add_symbol('array_info_getdata1', array_ext.array_info_getdata1)


class ArrayInfoType(types.Type):

    def __init__(self):
        super(ArrayInfoType, self).__init__(name='ArrayInfoType()')


array_info_type = ArrayInfoType()
register_model(ArrayInfoType)(models.OpaqueModel)


class TableTypeCPP(types.Type):

    def __init__(self):
        super(TableTypeCPP, self).__init__(name='TableTypeCPP()')


table_type = TableTypeCPP()
register_model(TableTypeCPP)(models.OpaqueModel)


@lower_cast(table_type, types.voidptr)
def lower_table_type(context, builder, fromty, toty, val):
    return val


@intrinsic
def array_to_info(typingctx, arr_type_t=None):
    return array_info_type(arr_type_t), array_to_info_codegen


def array_to_info_codegen(context, builder, sig, args, incref=True):
    in_arr, = args
    arr_type = sig.args[0]
    if incref:
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, TupleArrayType):
        hlfmj__csv = context.make_helper(builder, arr_type, in_arr)
        in_arr = hlfmj__csv.data
        arr_type = StructArrayType(arr_type.data, ('dummy',) * len(arr_type
            .data))
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        zqfgc__voem = context.make_helper(builder, arr_type, in_arr)
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer()])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='list_string_array_to_info')
        return builder.call(mlt__mwj, [zqfgc__voem.meminfo])
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType, StructArrayType)
        ):

        def get_types(arr_typ):
            if isinstance(arr_typ, MapArrayType):
                return get_types(_get_map_arr_data_type(arr_typ))
            elif isinstance(arr_typ, ArrayItemArrayType):
                return [CTypeEnum.LIST.value] + get_types(arr_typ.dtype)
            elif isinstance(arr_typ, (StructType, StructArrayType)):
                dtzy__olh = [CTypeEnum.STRUCT.value, len(arr_typ.names)]
                for yeyxq__hmu in arr_typ.data:
                    dtzy__olh += get_types(yeyxq__hmu)
                return dtzy__olh
            elif isinstance(arr_typ, (types.Array, IntegerArrayType,
                FloatingArrayType)) or arr_typ == boolean_array:
                return get_types(arr_typ.dtype)
            elif arr_typ == string_array_type:
                return [CTypeEnum.STRING.value]
            elif arr_typ == binary_array_type:
                return [CTypeEnum.BINARY.value]
            elif isinstance(arr_typ, DecimalArrayType):
                return [CTypeEnum.Decimal.value, arr_typ.precision, arr_typ
                    .scale]
            else:
                return [numba_to_c_type(arr_typ)]

        def get_lengths(arr_typ, arr):
            length = context.compile_internal(builder, lambda a: len(a),
                types.intp(arr_typ), [arr])
            if isinstance(arr_typ, MapArrayType):
                wra__zprkk = context.make_helper(builder, arr_typ, value=arr)
                ucmlv__fmd = get_lengths(_get_map_arr_data_type(arr_typ),
                    wra__zprkk.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                hkh__frivj = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                ucmlv__fmd = get_lengths(arr_typ.dtype, hkh__frivj.data)
                ucmlv__fmd = cgutils.pack_array(builder, [hkh__frivj.
                    n_arrays] + [builder.extract_value(ucmlv__fmd,
                    kkve__lrrv) for kkve__lrrv in range(ucmlv__fmd.type.count)]
                    )
            elif isinstance(arr_typ, StructArrayType):
                hkh__frivj = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                ucmlv__fmd = []
                for kkve__lrrv, yeyxq__hmu in enumerate(arr_typ.data):
                    qijyz__spy = get_lengths(yeyxq__hmu, builder.
                        extract_value(hkh__frivj.data, kkve__lrrv))
                    ucmlv__fmd += [builder.extract_value(qijyz__spy,
                        eski__xvws) for eski__xvws in range(qijyz__spy.type
                        .count)]
                ucmlv__fmd = cgutils.pack_array(builder, [length, context.
                    get_constant(types.int64, -1)] + ucmlv__fmd)
            elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
                DecimalArrayType, types.Array)) or arr_typ in (boolean_array,
                datetime_date_array_type, string_array_type, binary_array_type
                ):
                ucmlv__fmd = cgutils.pack_array(builder, [length])
            else:
                raise BodoError(
                    f'array_to_info: unsupported type for subarray {arr_typ}')
            return ucmlv__fmd

        def get_buffers(arr_typ, arr):
            if isinstance(arr_typ, MapArrayType):
                wra__zprkk = context.make_helper(builder, arr_typ, value=arr)
                ewtyh__tvhe = get_buffers(_get_map_arr_data_type(arr_typ),
                    wra__zprkk.data)
            elif isinstance(arr_typ, ArrayItemArrayType):
                hkh__frivj = _get_array_item_arr_payload(context, builder,
                    arr_typ, arr)
                xqs__paks = get_buffers(arr_typ.dtype, hkh__frivj.data)
                evp__aro = context.make_array(types.Array(offset_type, 1, 'C')
                    )(context, builder, hkh__frivj.offsets)
                pkcm__ecq = builder.bitcast(evp__aro.data, lir.IntType(8).
                    as_pointer())
                qiity__nzbo = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, hkh__frivj.null_bitmap)
                ywp__url = builder.bitcast(qiity__nzbo.data, lir.IntType(8)
                    .as_pointer())
                ewtyh__tvhe = cgutils.pack_array(builder, [pkcm__ecq,
                    ywp__url] + [builder.extract_value(xqs__paks,
                    kkve__lrrv) for kkve__lrrv in range(xqs__paks.type.count)])
            elif isinstance(arr_typ, StructArrayType):
                hkh__frivj = _get_struct_arr_payload(context, builder,
                    arr_typ, arr)
                xqs__paks = []
                for kkve__lrrv, yeyxq__hmu in enumerate(arr_typ.data):
                    arc__rkq = get_buffers(yeyxq__hmu, builder.
                        extract_value(hkh__frivj.data, kkve__lrrv))
                    xqs__paks += [builder.extract_value(arc__rkq,
                        eski__xvws) for eski__xvws in range(arc__rkq.type.
                        count)]
                qiity__nzbo = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, hkh__frivj.null_bitmap)
                ywp__url = builder.bitcast(qiity__nzbo.data, lir.IntType(8)
                    .as_pointer())
                ewtyh__tvhe = cgutils.pack_array(builder, [ywp__url] +
                    xqs__paks)
            elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
                DecimalArrayType)) or arr_typ in (boolean_array,
                datetime_date_array_type):
                fgfz__dkds = arr_typ.dtype
                if isinstance(arr_typ, DecimalArrayType):
                    fgfz__dkds = int128_type
                elif arr_typ == datetime_date_array_type:
                    fgfz__dkds = types.int64
                arr = cgutils.create_struct_proxy(arr_typ)(context, builder,
                    arr)
                exwsq__esix = context.make_array(types.Array(fgfz__dkds, 1,
                    'C'))(context, builder, arr.data)
                qiity__nzbo = context.make_array(types.Array(types.uint8, 1,
                    'C'))(context, builder, arr.null_bitmap)
                zkt__gxu = builder.bitcast(exwsq__esix.data, lir.IntType(8)
                    .as_pointer())
                ywp__url = builder.bitcast(qiity__nzbo.data, lir.IntType(8)
                    .as_pointer())
                ewtyh__tvhe = cgutils.pack_array(builder, [ywp__url, zkt__gxu])
            elif arr_typ in (string_array_type, binary_array_type):
                hkh__frivj = _get_str_binary_arr_payload(context, builder,
                    arr, arr_typ)
                ccz__cmw = context.make_helper(builder, offset_arr_type,
                    hkh__frivj.offsets).data
                data = context.make_helper(builder, char_arr_type,
                    hkh__frivj.data).data
                ixpl__bfw = context.make_helper(builder,
                    null_bitmap_arr_type, hkh__frivj.null_bitmap).data
                ewtyh__tvhe = cgutils.pack_array(builder, [builder.bitcast(
                    ccz__cmw, lir.IntType(8).as_pointer()), builder.bitcast
                    (ixpl__bfw, lir.IntType(8).as_pointer()), builder.
                    bitcast(data, lir.IntType(8).as_pointer())])
            elif isinstance(arr_typ, types.Array):
                arr = context.make_array(arr_typ)(context, builder, arr)
                zkt__gxu = builder.bitcast(arr.data, lir.IntType(8).
                    as_pointer())
                laiu__hzx = lir.Constant(lir.IntType(8).as_pointer(), None)
                ewtyh__tvhe = cgutils.pack_array(builder, [laiu__hzx, zkt__gxu]
                    )
            else:
                raise RuntimeError(
                    'array_to_info: unsupported type for subarray ' + str(
                    arr_typ))
            return ewtyh__tvhe

        def get_field_names(arr_typ):
            fkb__bbjp = []
            if isinstance(arr_typ, StructArrayType):
                for tas__gqvvk, qpklf__apf in zip(arr_typ.dtype.names,
                    arr_typ.data):
                    fkb__bbjp.append(tas__gqvvk)
                    fkb__bbjp += get_field_names(qpklf__apf)
            elif isinstance(arr_typ, ArrayItemArrayType):
                fkb__bbjp += get_field_names(arr_typ.dtype)
            elif isinstance(arr_typ, MapArrayType):
                fkb__bbjp += get_field_names(_get_map_arr_data_type(arr_typ))
            return fkb__bbjp
        dtzy__olh = get_types(arr_type)
        geq__elji = cgutils.pack_array(builder, [context.get_constant(types
            .int32, t) for t in dtzy__olh])
        qhs__xfypy = cgutils.alloca_once_value(builder, geq__elji)
        ucmlv__fmd = get_lengths(arr_type, in_arr)
        lengths_ptr = cgutils.alloca_once_value(builder, ucmlv__fmd)
        ewtyh__tvhe = get_buffers(arr_type, in_arr)
        zolg__zvoyx = cgutils.alloca_once_value(builder, ewtyh__tvhe)
        fkb__bbjp = get_field_names(arr_type)
        if len(fkb__bbjp) == 0:
            fkb__bbjp = ['irrelevant']
        nkl__iyti = cgutils.pack_array(builder, [context.
            insert_const_string(builder.module, a) for a in fkb__bbjp])
        rdvgl__lcloi = cgutils.alloca_once_value(builder, nkl__iyti)
        if isinstance(arr_type, MapArrayType):
            elaq__ajyhc = _get_map_arr_data_type(arr_type)
            llo__yaxlq = context.make_helper(builder, arr_type, value=in_arr)
            cmbw__dpfyc = llo__yaxlq.data
        else:
            elaq__ajyhc = arr_type
            cmbw__dpfyc = in_arr
        psbb__cpr = context.make_helper(builder, elaq__ajyhc, cmbw__dpfyc)
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(32).as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer()])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='nested_array_to_info')
        eok__devig = builder.call(mlt__mwj, [builder.bitcast(qhs__xfypy,
            lir.IntType(32).as_pointer()), builder.bitcast(zolg__zvoyx, lir
            .IntType(8).as_pointer().as_pointer()), builder.bitcast(
            lengths_ptr, lir.IntType(64).as_pointer()), builder.bitcast(
            rdvgl__lcloi, lir.IntType(8).as_pointer()), psbb__cpr.meminfo])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eok__devig
    if arr_type in (string_array_type, binary_array_type):
        krpeh__qjc = context.make_helper(builder, arr_type, in_arr)
        wcszu__xqy = ArrayItemArrayType(char_arr_type)
        zqfgc__voem = context.make_helper(builder, wcszu__xqy, krpeh__qjc.data)
        hkh__frivj = _get_str_binary_arr_payload(context, builder, in_arr,
            arr_type)
        ccz__cmw = context.make_helper(builder, offset_arr_type, hkh__frivj
            .offsets).data
        data = context.make_helper(builder, char_arr_type, hkh__frivj.data
            ).data
        ixpl__bfw = context.make_helper(builder, null_bitmap_arr_type,
            hkh__frivj.null_bitmap).data
        ztmw__lsgk = builder.zext(builder.load(builder.gep(ccz__cmw, [
            hkh__frivj.n_arrays])), lir.IntType(64))
        tktpc__cnhj = context.get_constant(types.int32, int(arr_type ==
            binary_array_type))
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64), lir.IntType(8).as_pointer(), lir.
            IntType(offset_type.bitwidth).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(32)])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='string_array_to_info')
        return builder.call(mlt__mwj, [hkh__frivj.n_arrays, ztmw__lsgk,
            data, ccz__cmw, ixpl__bfw, zqfgc__voem.meminfo, tktpc__cnhj])
    if arr_type == bodo.dict_str_arr_type:
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        fmh__gtd = arr.data
        igx__mzez = arr.indices
        sig = array_info_type(arr_type.data)
        gpn__ddl = array_to_info_codegen(context, builder, sig, (fmh__gtd,),
            False)
        sig = array_info_type(bodo.libs.dict_arr_ext.dict_indices_arr_type)
        gxqbr__ithj = array_to_info_codegen(context, builder, sig, (
            igx__mzez,), False)
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(32), lir.IntType(32)])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='dict_str_array_to_info')
        gcj__qpa = builder.zext(arr.has_global_dictionary, lir.IntType(32))
        tqq__ezz = builder.zext(arr.has_deduped_local_dictionary, lir.
            IntType(32))
        return builder.call(mlt__mwj, [gpn__ddl, gxqbr__ithj, gcj__qpa,
            tqq__ezz])
    ldrr__obz = False
    if isinstance(arr_type, CategoricalArrayType):
        context.nrt.decref(builder, arr_type, in_arr)
        yml__snba = context.compile_internal(builder, lambda a: len(a.dtype
            .categories), types.intp(arr_type), [in_arr])
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).codes
        tyf__flke = get_categories_int_type(arr_type.dtype)
        arr_type = types.Array(tyf__flke, 1, 'C')
        ldrr__obz = True
        context.nrt.incref(builder, arr_type, in_arr)
    if isinstance(arr_type, bodo.DatetimeArrayType):
        if ldrr__obz:
            raise BodoError(
                'array_to_info(): Categorical PandasDatetimeArrayType not supported'
                )
        in_arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr
            ).data
        arr_type = arr_type.data_array_type
    if isinstance(arr_type, types.Array):
        arr = context.make_array(arr_type)(context, builder, in_arr)
        assert arr_type.ndim == 1, 'only 1D array shuffle supported'
        length = builder.extract_value(arr.shape, 0)
        nph__ddkk = arr_type.dtype
        teyvu__phkw = numba_to_c_type(nph__ddkk)
        hvcu__kvh = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), teyvu__phkw))
        if ldrr__obz:
            lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(64), lir.IntType(8).as_pointer()])
            mlt__mwj = cgutils.get_or_insert_function(builder.module,
                lbxq__bmhdb, name='categorical_array_to_info')
            return builder.call(mlt__mwj, [length, builder.bitcast(arr.data,
                lir.IntType(8).as_pointer()), builder.load(hvcu__kvh),
                yml__snba, arr.meminfo])
        else:
            lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer()])
            mlt__mwj = cgutils.get_or_insert_function(builder.module,
                lbxq__bmhdb, name='numpy_array_to_info')
            return builder.call(mlt__mwj, [length, builder.bitcast(arr.data,
                lir.IntType(8).as_pointer()), builder.load(hvcu__kvh), arr.
                meminfo])
    if isinstance(arr_type, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, TimeArrayType)) or arr_type in (boolean_array,
        datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        nph__ddkk = arr_type.dtype
        fgfz__dkds = nph__ddkk
        if isinstance(arr_type, DecimalArrayType):
            fgfz__dkds = int128_type
        if arr_type == datetime_date_array_type:
            fgfz__dkds = types.int64
        exwsq__esix = context.make_array(types.Array(fgfz__dkds, 1, 'C'))(
            context, builder, arr.data)
        length = builder.extract_value(exwsq__esix.shape, 0)
        vxuid__qxet = context.make_array(types.Array(types.uint8, 1, 'C'))(
            context, builder, arr.null_bitmap)
        teyvu__phkw = numba_to_c_type(nph__ddkk)
        hvcu__kvh = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), teyvu__phkw))
        if isinstance(arr_type, DecimalArrayType):
            lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer(), lir.IntType(32), lir.
                IntType(32)])
            mlt__mwj = cgutils.get_or_insert_function(builder.module,
                lbxq__bmhdb, name='decimal_array_to_info')
            return builder.call(mlt__mwj, [length, builder.bitcast(
                exwsq__esix.data, lir.IntType(8).as_pointer()), builder.
                load(hvcu__kvh), builder.bitcast(vxuid__qxet.data, lir.
                IntType(8).as_pointer()), exwsq__esix.meminfo, vxuid__qxet.
                meminfo, context.get_constant(types.int32, arr_type.
                precision), context.get_constant(types.int32, arr_type.scale)])
        elif isinstance(arr_type, TimeArrayType):
            lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer(), lir.IntType(32)])
            mlt__mwj = cgutils.get_or_insert_function(builder.module,
                lbxq__bmhdb, name='time_array_to_info')
            return builder.call(mlt__mwj, [length, builder.bitcast(
                exwsq__esix.data, lir.IntType(8).as_pointer()), builder.
                load(hvcu__kvh), builder.bitcast(vxuid__qxet.data, lir.
                IntType(8).as_pointer()), exwsq__esix.meminfo, vxuid__qxet.
                meminfo, lir.Constant(lir.IntType(32), arr_type.precision)])
        else:
            lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [
                lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(
                32), lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer
                (), lir.IntType(8).as_pointer()])
            mlt__mwj = cgutils.get_or_insert_function(builder.module,
                lbxq__bmhdb, name='nullable_array_to_info')
            return builder.call(mlt__mwj, [length, builder.bitcast(
                exwsq__esix.data, lir.IntType(8).as_pointer()), builder.
                load(hvcu__kvh), builder.bitcast(vxuid__qxet.data, lir.
                IntType(8).as_pointer()), exwsq__esix.meminfo, vxuid__qxet.
                meminfo])
    if isinstance(arr_type, IntervalArrayType):
        assert isinstance(arr_type.arr_type, types.Array
            ), 'array_to_info(): only IntervalArrayType with Numpy arrays supported'
        arr = cgutils.create_struct_proxy(arr_type)(context, builder, in_arr)
        gsnjk__ciy = context.make_array(arr_type.arr_type)(context, builder,
            arr.left)
        jheyb__ndmih = context.make_array(arr_type.arr_type)(context,
            builder, arr.right)
        length = builder.extract_value(gsnjk__ciy.shape, 0)
        teyvu__phkw = numba_to_c_type(arr_type.arr_type.dtype)
        hvcu__kvh = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), teyvu__phkw))
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(32), lir.IntType(8).as_pointer(), lir
            .IntType(8).as_pointer()])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='interval_array_to_info')
        return builder.call(mlt__mwj, [length, builder.bitcast(gsnjk__ciy.
            data, lir.IntType(8).as_pointer()), builder.bitcast(
            jheyb__ndmih.data, lir.IntType(8).as_pointer()), builder.load(
            hvcu__kvh), gsnjk__ciy.meminfo, jheyb__ndmih.meminfo])
    raise_bodo_error(f'array_to_info(): array type {arr_type} is not supported'
        )


def _lower_info_to_array_numpy(arr_type, context, builder, in_info):
    assert arr_type.ndim == 1, 'only 1D array supported'
    arr = context.make_array(arr_type)(context, builder)
    pbrd__ospjp = cgutils.alloca_once(builder, lir.IntType(64))
    zkt__gxu = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    ufnt__tulm = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
    lbxq__bmhdb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
        as_pointer().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    mlt__mwj = cgutils.get_or_insert_function(builder.module, lbxq__bmhdb,
        name='info_to_numpy_array')
    builder.call(mlt__mwj, [in_info, pbrd__ospjp, zkt__gxu, ufnt__tulm])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    zul__vnoel = context.get_value_type(types.intp)
    exsxw__dpx = cgutils.pack_array(builder, [builder.load(pbrd__ospjp)],
        ty=zul__vnoel)
    jvegh__fmcf = context.get_constant(types.intp, context.get_abi_sizeof(
        context.get_data_type(arr_type.dtype)))
    ddi__qmxh = cgutils.pack_array(builder, [jvegh__fmcf], ty=zul__vnoel)
    data = builder.bitcast(builder.load(zkt__gxu), context.get_data_type(
        arr_type.dtype).as_pointer())
    numba.np.arrayobj.populate_array(arr, data=data, shape=exsxw__dpx,
        strides=ddi__qmxh, itemsize=jvegh__fmcf, meminfo=builder.load(
        ufnt__tulm))
    return arr._getvalue()


def _lower_info_to_array_list_string_array(arr_type, context, builder, in_info
    ):
    rvg__fnbdj = context.make_helper(builder, arr_type)
    lbxq__bmhdb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
        as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
    mlt__mwj = cgutils.get_or_insert_function(builder.module, lbxq__bmhdb,
        name='info_to_list_string_array')
    builder.call(mlt__mwj, [in_info, rvg__fnbdj._get_ptr_by_name('meminfo')])
    context.compile_internal(builder, lambda :
        check_and_propagate_cpp_exception(), types.none(), [])
    return rvg__fnbdj._getvalue()


def nested_to_array(context, builder, arr_typ, lengths_ptr, array_infos_ptr,
    lengths_pos, infos_pos):
    lvxkm__sjyl = context.get_data_type(array_info_type)
    if isinstance(arr_typ, ArrayItemArrayType):
        htpu__ynrj = lengths_pos
        xeo__eurkc = infos_pos
        fdq__pgl, lengths_pos, infos_pos = nested_to_array(context, builder,
            arr_typ.dtype, lengths_ptr, array_infos_ptr, lengths_pos + 1, 
            infos_pos + 2)
        oupxi__mjpq = ArrayItemArrayPayloadType(arr_typ)
        gvls__haaa = context.get_data_type(oupxi__mjpq)
        tprie__awxfh = context.get_abi_sizeof(gvls__haaa)
        pcadx__lzkat = define_array_item_dtor(context, builder, arr_typ,
            oupxi__mjpq)
        iah__njkvo = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, tprie__awxfh), pcadx__lzkat)
        deh__nnkdi = context.nrt.meminfo_data(builder, iah__njkvo)
        umida__xrxs = builder.bitcast(deh__nnkdi, gvls__haaa.as_pointer())
        hkh__frivj = cgutils.create_struct_proxy(oupxi__mjpq)(context, builder)
        hkh__frivj.n_arrays = builder.extract_value(builder.load(
            lengths_ptr), htpu__ynrj)
        hkh__frivj.data = fdq__pgl
        fulci__jqjp = builder.load(array_infos_ptr)
        zje__uowm = builder.bitcast(builder.extract_value(fulci__jqjp,
            xeo__eurkc), lvxkm__sjyl)
        hkh__frivj.offsets = _lower_info_to_array_numpy(types.Array(
            offset_type, 1, 'C'), context, builder, zje__uowm)
        ztmc__yty = builder.bitcast(builder.extract_value(fulci__jqjp, 
            xeo__eurkc + 1), lvxkm__sjyl)
        hkh__frivj.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, ztmc__yty)
        builder.store(hkh__frivj._getvalue(), umida__xrxs)
        zqfgc__voem = context.make_helper(builder, arr_typ)
        zqfgc__voem.meminfo = iah__njkvo
        return zqfgc__voem._getvalue(), lengths_pos, infos_pos
    elif isinstance(arr_typ, StructArrayType):
        cnhpx__yhoq = []
        xeo__eurkc = infos_pos
        lengths_pos += 1
        infos_pos += 1
        for vyco__kjt in arr_typ.data:
            fdq__pgl, lengths_pos, infos_pos = nested_to_array(context,
                builder, vyco__kjt, lengths_ptr, array_infos_ptr,
                lengths_pos, infos_pos)
            cnhpx__yhoq.append(fdq__pgl)
        oupxi__mjpq = StructArrayPayloadType(arr_typ.data)
        gvls__haaa = context.get_value_type(oupxi__mjpq)
        tprie__awxfh = context.get_abi_sizeof(gvls__haaa)
        pcadx__lzkat = define_struct_arr_dtor(context, builder, arr_typ,
            oupxi__mjpq)
        iah__njkvo = context.nrt.meminfo_alloc_dtor(builder, context.
            get_constant(types.uintp, tprie__awxfh), pcadx__lzkat)
        deh__nnkdi = context.nrt.meminfo_data(builder, iah__njkvo)
        umida__xrxs = builder.bitcast(deh__nnkdi, gvls__haaa.as_pointer())
        hkh__frivj = cgutils.create_struct_proxy(oupxi__mjpq)(context, builder)
        hkh__frivj.data = cgutils.pack_array(builder, cnhpx__yhoq
            ) if types.is_homogeneous(*arr_typ.data) else cgutils.pack_struct(
            builder, cnhpx__yhoq)
        fulci__jqjp = builder.load(array_infos_ptr)
        ztmc__yty = builder.bitcast(builder.extract_value(fulci__jqjp,
            xeo__eurkc), lvxkm__sjyl)
        hkh__frivj.null_bitmap = _lower_info_to_array_numpy(types.Array(
            types.uint8, 1, 'C'), context, builder, ztmc__yty)
        builder.store(hkh__frivj._getvalue(), umida__xrxs)
        odi__kof = context.make_helper(builder, arr_typ)
        odi__kof.meminfo = iah__njkvo
        return odi__kof._getvalue(), lengths_pos, infos_pos
    elif arr_typ in (string_array_type, binary_array_type):
        fulci__jqjp = builder.load(array_infos_ptr)
        xttvz__dxovf = builder.bitcast(builder.extract_value(fulci__jqjp,
            infos_pos), lvxkm__sjyl)
        krpeh__qjc = context.make_helper(builder, arr_typ)
        wcszu__xqy = ArrayItemArrayType(char_arr_type)
        zqfgc__voem = context.make_helper(builder, wcszu__xqy)
        lbxq__bmhdb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='info_to_string_array')
        builder.call(mlt__mwj, [xttvz__dxovf, zqfgc__voem._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        krpeh__qjc.data = zqfgc__voem._getvalue()
        return krpeh__qjc._getvalue(), lengths_pos + 1, infos_pos + 1
    elif isinstance(arr_typ, types.Array):
        fulci__jqjp = builder.load(array_infos_ptr)
        yjx__gyiyv = builder.bitcast(builder.extract_value(fulci__jqjp, 
            infos_pos + 1), lvxkm__sjyl)
        return _lower_info_to_array_numpy(arr_typ, context, builder, yjx__gyiyv
            ), lengths_pos + 1, infos_pos + 2
    elif isinstance(arr_typ, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType)) or arr_typ in (boolean_array,
        datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_typ)(context, builder)
        fgfz__dkds = arr_typ.dtype
        if isinstance(arr_typ, DecimalArrayType):
            fgfz__dkds = int128_type
        elif arr_typ == datetime_date_array_type:
            fgfz__dkds = types.int64
        fulci__jqjp = builder.load(array_infos_ptr)
        ztmc__yty = builder.bitcast(builder.extract_value(fulci__jqjp,
            infos_pos), lvxkm__sjyl)
        arr.null_bitmap = _lower_info_to_array_numpy(types.Array(types.
            uint8, 1, 'C'), context, builder, ztmc__yty)
        yjx__gyiyv = builder.bitcast(builder.extract_value(fulci__jqjp, 
            infos_pos + 1), lvxkm__sjyl)
        arr.data = _lower_info_to_array_numpy(types.Array(fgfz__dkds, 1,
            'C'), context, builder, yjx__gyiyv)
        return arr._getvalue(), lengths_pos + 1, infos_pos + 2


def info_to_array_codegen(context, builder, sig, args):
    array_type = sig.args[1]
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    in_info, eburd__cmus = args
    if isinstance(arr_type, ArrayItemArrayType
        ) and arr_type.dtype == string_array_type:
        return _lower_info_to_array_list_string_array(arr_type, context,
            builder, in_info)
    if isinstance(arr_type, (MapArrayType, ArrayItemArrayType,
        StructArrayType, TupleArrayType)):

        def get_num_arrays(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 1 + get_num_arrays(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_arrays(vyco__kjt) for vyco__kjt in
                    arr_typ.data])
            else:
                return 1

        def get_num_infos(arr_typ):
            if isinstance(arr_typ, ArrayItemArrayType):
                return 2 + get_num_infos(arr_typ.dtype)
            elif isinstance(arr_typ, StructArrayType):
                return 1 + sum([get_num_infos(vyco__kjt) for vyco__kjt in
                    arr_typ.data])
            elif arr_typ in (string_array_type, binary_array_type):
                return 1
            else:
                return 2
        if isinstance(arr_type, TupleArrayType):
            hbxg__vwsi = StructArrayType(arr_type.data, ('dummy',) * len(
                arr_type.data))
        elif isinstance(arr_type, MapArrayType):
            hbxg__vwsi = _get_map_arr_data_type(arr_type)
        else:
            hbxg__vwsi = arr_type
        paxwq__wzkmi = get_num_arrays(hbxg__vwsi)
        ucmlv__fmd = cgutils.pack_array(builder, [lir.Constant(lir.IntType(
            64), 0) for eburd__cmus in range(paxwq__wzkmi)])
        lengths_ptr = cgutils.alloca_once_value(builder, ucmlv__fmd)
        laiu__hzx = lir.Constant(lir.IntType(8).as_pointer(), None)
        ifixb__qrvim = cgutils.pack_array(builder, [laiu__hzx for
            eburd__cmus in range(get_num_infos(hbxg__vwsi))])
        array_infos_ptr = cgutils.alloca_once_value(builder, ifixb__qrvim)
        lbxq__bmhdb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer()])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='info_to_nested_array')
        builder.call(mlt__mwj, [in_info, builder.bitcast(lengths_ptr, lir.
            IntType(64).as_pointer()), builder.bitcast(array_infos_ptr, lir
            .IntType(8).as_pointer().as_pointer())])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        arr, eburd__cmus, eburd__cmus = nested_to_array(context, builder,
            hbxg__vwsi, lengths_ptr, array_infos_ptr, 0, 0)
        if isinstance(arr_type, TupleArrayType):
            hlfmj__csv = context.make_helper(builder, arr_type)
            hlfmj__csv.data = arr
            context.nrt.incref(builder, hbxg__vwsi, arr)
            arr = hlfmj__csv._getvalue()
        elif isinstance(arr_type, MapArrayType):
            sig = signature(arr_type, hbxg__vwsi)
            arr = init_map_arr_codegen(context, builder, sig, (arr,))
        return arr
    if arr_type in (string_array_type, binary_array_type):
        krpeh__qjc = context.make_helper(builder, arr_type)
        wcszu__xqy = ArrayItemArrayType(char_arr_type)
        zqfgc__voem = context.make_helper(builder, wcszu__xqy)
        lbxq__bmhdb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='info_to_string_array')
        builder.call(mlt__mwj, [in_info, zqfgc__voem._get_ptr_by_name(
            'meminfo')])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        krpeh__qjc.data = zqfgc__voem._getvalue()
        return krpeh__qjc._getvalue()
    if arr_type == bodo.dict_str_arr_type:
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32)])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='get_nested_info')
        gpn__ddl = builder.call(mlt__mwj, [in_info, lir.Constant(lir.
            IntType(32), 1)])
        gxqbr__ithj = builder.call(mlt__mwj, [in_info, lir.Constant(lir.
            IntType(32), 2)])
        oqcx__jaup = context.make_helper(builder, arr_type)
        sig = arr_type.data(array_info_type, arr_type.data)
        oqcx__jaup.data = info_to_array_codegen(context, builder, sig, (
            gpn__ddl, context.get_constant_null(arr_type.data)))
        dphe__kabsh = bodo.libs.dict_arr_ext.dict_indices_arr_type
        sig = dphe__kabsh(array_info_type, dphe__kabsh)
        oqcx__jaup.indices = info_to_array_codegen(context, builder, sig, (
            gxqbr__ithj, context.get_constant_null(dphe__kabsh)))
        lbxq__bmhdb = lir.FunctionType(lir.IntType(32), [lir.IntType(8).
            as_pointer()])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='get_has_global_dictionary')
        gcj__qpa = builder.call(mlt__mwj, [in_info])
        oqcx__jaup.has_global_dictionary = builder.trunc(gcj__qpa, cgutils.
            bool_t)
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='get_has_deduped_local_dictionary')
        tqq__ezz = builder.call(mlt__mwj, [in_info])
        oqcx__jaup.has_deduped_local_dictionary = builder.trunc(tqq__ezz,
            cgutils.bool_t)
        return oqcx__jaup._getvalue()
    if isinstance(arr_type, CategoricalArrayType):
        out_arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        tyf__flke = get_categories_int_type(arr_type.dtype)
        sbkbl__cmu = types.Array(tyf__flke, 1, 'C')
        out_arr.codes = _lower_info_to_array_numpy(sbkbl__cmu, context,
            builder, in_info)
        if isinstance(array_type, types.TypeRef):
            assert arr_type.dtype.categories is not None, 'info_to_array: unknown categories'
            is_ordered = arr_type.dtype.ordered
            engea__yyjok = bodo.utils.utils.create_categorical_type(arr_type
                .dtype.categories, arr_type.dtype.data.data, is_ordered)
            new_cats_tup = MetaType(tuple(engea__yyjok))
            int_type = arr_type.dtype.int_type
            ihdyw__xibed = arr_type.dtype.data.data
            rlrid__iicai = context.get_constant_generic(builder,
                ihdyw__xibed, engea__yyjok)
            nph__ddkk = context.compile_internal(builder, lambda c_arr:
                bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo.utils.
                conversion.index_from_array(c_arr), is_ordered, int_type,
                new_cats_tup), arr_type.dtype(ihdyw__xibed), [rlrid__iicai])
        else:
            nph__ddkk = cgutils.create_struct_proxy(arr_type)(context,
                builder, args[1]).dtype
            context.nrt.incref(builder, arr_type.dtype, nph__ddkk)
        out_arr.dtype = nph__ddkk
        return out_arr._getvalue()
    if isinstance(arr_type, bodo.DatetimeArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        data = _lower_info_to_array_numpy(arr_type.data_array_type, context,
            builder, in_info)
        arr.data = data
        return arr._getvalue()
    if isinstance(arr_type, types.Array):
        return _lower_info_to_array_numpy(arr_type, context, builder, in_info)
    if isinstance(arr_type, (IntegerArrayType, FloatingArrayType,
        DecimalArrayType, TimeArrayType)) or arr_type in (boolean_array,
        datetime_date_array_type):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        fgfz__dkds = arr_type.dtype
        if isinstance(arr_type, DecimalArrayType):
            fgfz__dkds = int128_type
        elif arr_type == datetime_date_array_type:
            fgfz__dkds = types.int64
        cxjdg__qon = types.Array(fgfz__dkds, 1, 'C')
        exwsq__esix = context.make_array(cxjdg__qon)(context, builder)
        xwptg__pwhi = types.Array(types.uint8, 1, 'C')
        xjg__zyfh = context.make_array(xwptg__pwhi)(context, builder)
        pbrd__ospjp = cgutils.alloca_once(builder, lir.IntType(64))
        xqec__mklva = cgutils.alloca_once(builder, lir.IntType(64))
        zkt__gxu = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        jnqxh__ouv = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        ufnt__tulm = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        fynh__xgarq = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        lbxq__bmhdb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(64).
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer(), lir.IntType(8).as_pointer
            ().as_pointer(), lir.IntType(8).as_pointer().as_pointer()])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='info_to_nullable_array')
        builder.call(mlt__mwj, [in_info, pbrd__ospjp, xqec__mklva, zkt__gxu,
            jnqxh__ouv, ufnt__tulm, fynh__xgarq])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        zul__vnoel = context.get_value_type(types.intp)
        exsxw__dpx = cgutils.pack_array(builder, [builder.load(pbrd__ospjp)
            ], ty=zul__vnoel)
        jvegh__fmcf = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(fgfz__dkds)))
        ddi__qmxh = cgutils.pack_array(builder, [jvegh__fmcf], ty=zul__vnoel)
        data = builder.bitcast(builder.load(zkt__gxu), context.
            get_data_type(fgfz__dkds).as_pointer())
        numba.np.arrayobj.populate_array(exwsq__esix, data=data, shape=
            exsxw__dpx, strides=ddi__qmxh, itemsize=jvegh__fmcf, meminfo=
            builder.load(ufnt__tulm))
        arr.data = exwsq__esix._getvalue()
        exsxw__dpx = cgutils.pack_array(builder, [builder.load(xqec__mklva)
            ], ty=zul__vnoel)
        jvegh__fmcf = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(types.uint8)))
        ddi__qmxh = cgutils.pack_array(builder, [jvegh__fmcf], ty=zul__vnoel)
        data = builder.bitcast(builder.load(jnqxh__ouv), context.
            get_data_type(types.uint8).as_pointer())
        numba.np.arrayobj.populate_array(xjg__zyfh, data=data, shape=
            exsxw__dpx, strides=ddi__qmxh, itemsize=jvegh__fmcf, meminfo=
            builder.load(fynh__xgarq))
        arr.null_bitmap = xjg__zyfh._getvalue()
        return arr._getvalue()
    if isinstance(arr_type, IntervalArrayType):
        arr = cgutils.create_struct_proxy(arr_type)(context, builder)
        gsnjk__ciy = context.make_array(arr_type.arr_type)(context, builder)
        jheyb__ndmih = context.make_array(arr_type.arr_type)(context, builder)
        pbrd__ospjp = cgutils.alloca_once(builder, lir.IntType(64))
        dntg__rneph = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        uqrsm__ntvmn = cgutils.alloca_once(builder, lir.IntType(8).as_pointer()
            )
        utpj__fjhgj = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        bfs__qqcs = cgutils.alloca_once(builder, lir.IntType(8).as_pointer())
        lbxq__bmhdb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer(), lir.IntType(64).as_pointer(), lir.IntType(8).
            as_pointer().as_pointer(), lir.IntType(8).as_pointer().
            as_pointer(), lir.IntType(8).as_pointer().as_pointer(), lir.
            IntType(8).as_pointer().as_pointer()])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='info_to_interval_array')
        builder.call(mlt__mwj, [in_info, pbrd__ospjp, dntg__rneph,
            uqrsm__ntvmn, utpj__fjhgj, bfs__qqcs])
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        zul__vnoel = context.get_value_type(types.intp)
        exsxw__dpx = cgutils.pack_array(builder, [builder.load(pbrd__ospjp)
            ], ty=zul__vnoel)
        jvegh__fmcf = context.get_constant(types.intp, context.
            get_abi_sizeof(context.get_data_type(arr_type.arr_type.dtype)))
        ddi__qmxh = cgutils.pack_array(builder, [jvegh__fmcf], ty=zul__vnoel)
        skd__lojf = builder.bitcast(builder.load(dntg__rneph), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(gsnjk__ciy, data=skd__lojf, shape=
            exsxw__dpx, strides=ddi__qmxh, itemsize=jvegh__fmcf, meminfo=
            builder.load(utpj__fjhgj))
        arr.left = gsnjk__ciy._getvalue()
        sbl__nyfh = builder.bitcast(builder.load(uqrsm__ntvmn), context.
            get_data_type(arr_type.arr_type.dtype).as_pointer())
        numba.np.arrayobj.populate_array(jheyb__ndmih, data=sbl__nyfh,
            shape=exsxw__dpx, strides=ddi__qmxh, itemsize=jvegh__fmcf,
            meminfo=builder.load(bfs__qqcs))
        arr.right = jheyb__ndmih._getvalue()
        return arr._getvalue()
    raise_bodo_error(f'info_to_array(): array type {arr_type} is not supported'
        )


@intrinsic
def info_to_array(typingctx, info_type, array_type):
    arr_type = array_type.instance_type if isinstance(array_type, types.TypeRef
        ) else array_type
    assert info_type == array_info_type, 'info_to_array: expected info type'
    return arr_type(info_type, array_type), info_to_array_codegen


@intrinsic
def test_alloc_np(typingctx, len_typ, arr_type):
    array_type = arr_type.instance_type if isinstance(arr_type, types.TypeRef
        ) else arr_type

    def codegen(context, builder, sig, args):
        length, eburd__cmus = args
        teyvu__phkw = numba_to_c_type(array_type.dtype)
        hvcu__kvh = cgutils.alloca_once_value(builder, lir.Constant(lir.
            IntType(32), teyvu__phkw))
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(32)])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='alloc_numpy')
        return builder.call(mlt__mwj, [length, builder.load(hvcu__kvh)])
    return array_info_type(len_typ, arr_type), codegen


@intrinsic
def test_alloc_string(typingctx, len_typ, n_chars_typ):

    def codegen(context, builder, sig, args):
        length, cirr__kqpj = args
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(64), lir.IntType(64)])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='alloc_string_array')
        return builder.call(mlt__mwj, [length, cirr__kqpj])
    return array_info_type(len_typ, n_chars_typ), codegen


@intrinsic
def arr_info_list_to_table(typingctx, list_arr_info_typ=None):
    assert list_arr_info_typ == types.List(array_info_type)
    return table_type(list_arr_info_typ), arr_info_list_to_table_codegen


def arr_info_list_to_table_codegen(context, builder, sig, args):
    xbih__rhpi, = args
    fvlbm__djw = numba.cpython.listobj.ListInstance(context, builder, sig.
        args[0], xbih__rhpi)
    lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
        IntType(8).as_pointer().as_pointer(), lir.IntType(64)])
    mlt__mwj = cgutils.get_or_insert_function(builder.module, lbxq__bmhdb,
        name='arr_info_list_to_table')
    return builder.call(mlt__mwj, [fvlbm__djw.data, fvlbm__djw.size])


@intrinsic
def info_from_table(typingctx, table_t, ind_t):

    def codegen(context, builder, sig, args):
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='info_from_table')
        return builder.call(mlt__mwj, args)
    return array_info_type(table_t, ind_t), codegen


@intrinsic
def cpp_table_to_py_table(typingctx, cpp_table_t, table_idx_arr_t,
    py_table_type_t):
    assert cpp_table_t == table_type, 'invalid cpp table type'
    assert isinstance(table_idx_arr_t, types.Array
        ) and table_idx_arr_t.dtype == types.int64, 'invalid table index array'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    tydq__ibaqa = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        cpp_table, fbqnt__iyzv, eburd__cmus = args
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='info_from_table')
        mqf__pfx = cgutils.create_struct_proxy(tydq__ibaqa)(context, builder)
        mqf__pfx.parent = cgutils.get_null_value(mqf__pfx.parent.type)
        zqtz__vfi = context.make_array(table_idx_arr_t)(context, builder,
            fbqnt__iyzv)
        ujt__wvuo = context.get_constant(types.int64, -1)
        ywd__ssk = context.get_constant(types.int64, 0)
        hjrq__aof = cgutils.alloca_once_value(builder, ywd__ssk)
        for t, ymyxn__yhcu in tydq__ibaqa.type_to_blk.items():
            ysr__qypw = context.get_constant(types.int64, len(tydq__ibaqa.
                block_to_arr_ind[ymyxn__yhcu]))
            eburd__cmus, lrlkr__bar = ListInstance.allocate_ex(context,
                builder, types.List(t), ysr__qypw)
            lrlkr__bar.size = ysr__qypw
            jjxb__gsstp = context.make_constant_array(builder, types.Array(
                types.int64, 1, 'C'), np.array(tydq__ibaqa.block_to_arr_ind
                [ymyxn__yhcu], dtype=np.int64))
            erug__akwpw = context.make_array(types.Array(types.int64, 1, 'C'))(
                context, builder, jjxb__gsstp)
            with cgutils.for_range(builder, ysr__qypw) as svy__gfv:
                kkve__lrrv = svy__gfv.index
                bkk__ocp = _getitem_array_single_int(context, builder,
                    types.int64, types.Array(types.int64, 1, 'C'),
                    erug__akwpw, kkve__lrrv)
                hcwf__jmc = _getitem_array_single_int(context, builder,
                    types.int64, table_idx_arr_t, zqtz__vfi, bkk__ocp)
                zmxz__erqan = builder.icmp_unsigned('!=', hcwf__jmc, ujt__wvuo)
                with builder.if_else(zmxz__erqan) as (gbxr__gnsj, zcah__qqpvk):
                    with gbxr__gnsj:
                        opz__ijd = builder.call(mlt__mwj, [cpp_table,
                            hcwf__jmc])
                        arr = context.compile_internal(builder, lambda info:
                            info_to_array(info, t), t(array_info_type), [
                            opz__ijd])
                        lrlkr__bar.inititem(kkve__lrrv, arr, incref=False)
                        length = context.compile_internal(builder, lambda
                            arr: len(arr), types.int64(t), [arr])
                        builder.store(length, hjrq__aof)
                    with zcah__qqpvk:
                        vcd__aisry = context.get_constant_null(t)
                        lrlkr__bar.inititem(kkve__lrrv, vcd__aisry, incref=
                            False)
            setattr(mqf__pfx, f'block_{ymyxn__yhcu}', lrlkr__bar.value)
        mqf__pfx.len = builder.load(hjrq__aof)
        return mqf__pfx._getvalue()
    return tydq__ibaqa(cpp_table_t, table_idx_arr_t, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def cpp_table_to_py_data(cpp_table, out_col_inds_t, out_types_t, n_rows_t,
    n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
    rscq__vofx = out_col_inds_t.instance_type.meta
    tydq__ibaqa = unwrap_typeref(out_types_t.types[0])
    sriic__riyo = [unwrap_typeref(out_types_t.types[kkve__lrrv]) for
        kkve__lrrv in range(1, len(out_types_t.types))]
    ovm__jfqn = {}
    goswd__yriz = get_overload_const_int(n_table_cols_t)
    eaaf__wpk = {nwmuh__skmzz: kkve__lrrv for kkve__lrrv, nwmuh__skmzz in
        enumerate(rscq__vofx)}
    if not is_overload_none(unknown_cat_arrs_t):
        kgg__aelvz = {ejhy__jea: kkve__lrrv for kkve__lrrv, ejhy__jea in
            enumerate(cat_inds_t.instance_type.meta)}
    dify__fiq = []
    sviu__qwuzf = """def impl(cpp_table, out_col_inds_t, out_types_t, n_rows_t, n_table_cols_t, unknown_cat_arrs_t=None, cat_inds_t=None):
"""
    if isinstance(tydq__ibaqa, bodo.TableType):
        sviu__qwuzf += f'  py_table = init_table(py_table_type, False)\n'
        sviu__qwuzf += f'  py_table = set_table_len(py_table, n_rows_t)\n'
        for pcp__ooc, ymyxn__yhcu in tydq__ibaqa.type_to_blk.items():
            mcm__pnu = [eaaf__wpk.get(kkve__lrrv, -1) for kkve__lrrv in
                tydq__ibaqa.block_to_arr_ind[ymyxn__yhcu]]
            ovm__jfqn[f'out_inds_{ymyxn__yhcu}'] = np.array(mcm__pnu, np.int64)
            ovm__jfqn[f'out_type_{ymyxn__yhcu}'] = pcp__ooc
            ovm__jfqn[f'typ_list_{ymyxn__yhcu}'] = types.List(pcp__ooc)
            ptexh__soft = f'out_type_{ymyxn__yhcu}'
            if type_has_unknown_cats(pcp__ooc):
                if is_overload_none(unknown_cat_arrs_t):
                    sviu__qwuzf += f"""  in_arr_list_{ymyxn__yhcu} = get_table_block(out_types_t[0], {ymyxn__yhcu})
"""
                    ptexh__soft = f'in_arr_list_{ymyxn__yhcu}[i]'
                else:
                    ovm__jfqn[f'cat_arr_inds_{ymyxn__yhcu}'] = np.array([
                        kgg__aelvz.get(kkve__lrrv, -1) for kkve__lrrv in
                        tydq__ibaqa.block_to_arr_ind[ymyxn__yhcu]], np.int64)
                    ptexh__soft = (
                        f'unknown_cat_arrs_t[cat_arr_inds_{ymyxn__yhcu}[i]]')
            ysr__qypw = len(tydq__ibaqa.block_to_arr_ind[ymyxn__yhcu])
            sviu__qwuzf += f"""  arr_list_{ymyxn__yhcu} = alloc_list_like(typ_list_{ymyxn__yhcu}, {ysr__qypw}, False)
"""
            sviu__qwuzf += f'  for i in range(len(arr_list_{ymyxn__yhcu})):\n'
            sviu__qwuzf += (
                f'    cpp_ind_{ymyxn__yhcu} = out_inds_{ymyxn__yhcu}[i]\n')
            sviu__qwuzf += f'    if cpp_ind_{ymyxn__yhcu} == -1:\n'
            sviu__qwuzf += f'      continue\n'
            sviu__qwuzf += f"""    arr_{ymyxn__yhcu} = info_to_array(info_from_table(cpp_table, cpp_ind_{ymyxn__yhcu}), {ptexh__soft})
"""
            sviu__qwuzf += (
                f'    arr_list_{ymyxn__yhcu}[i] = arr_{ymyxn__yhcu}\n')
            sviu__qwuzf += f"""  py_table = set_table_block(py_table, arr_list_{ymyxn__yhcu}, {ymyxn__yhcu})
"""
        dify__fiq.append('py_table')
    elif tydq__ibaqa != types.none:
        pxsmg__evj = eaaf__wpk.get(0, -1)
        if pxsmg__evj != -1:
            ovm__jfqn[f'arr_typ_arg0'] = tydq__ibaqa
            ptexh__soft = f'arr_typ_arg0'
            if type_has_unknown_cats(tydq__ibaqa):
                if is_overload_none(unknown_cat_arrs_t):
                    ptexh__soft = f'out_types_t[0]'
                else:
                    ptexh__soft = f'unknown_cat_arrs_t[{kgg__aelvz[0]}]'
            sviu__qwuzf += f"""  out_arg0 = info_to_array(info_from_table(cpp_table, {pxsmg__evj}), {ptexh__soft})
"""
            dify__fiq.append('out_arg0')
    for kkve__lrrv, t in enumerate(sriic__riyo):
        pxsmg__evj = eaaf__wpk.get(goswd__yriz + kkve__lrrv, -1)
        if pxsmg__evj != -1:
            ovm__jfqn[f'extra_arr_type_{kkve__lrrv}'] = t
            ptexh__soft = f'extra_arr_type_{kkve__lrrv}'
            if type_has_unknown_cats(t):
                if is_overload_none(unknown_cat_arrs_t):
                    ptexh__soft = f'out_types_t[{kkve__lrrv + 1}]'
                else:
                    ptexh__soft = (
                        f'unknown_cat_arrs_t[{kgg__aelvz[goswd__yriz + kkve__lrrv]}]'
                        )
            sviu__qwuzf += f"""  out_{kkve__lrrv} = info_to_array(info_from_table(cpp_table, {pxsmg__evj}), {ptexh__soft})
"""
            dify__fiq.append(f'out_{kkve__lrrv}')
    wzt__ncm = ',' if len(dify__fiq) == 1 else ''
    sviu__qwuzf += f"  return ({', '.join(dify__fiq)}{wzt__ncm})\n"
    ovm__jfqn.update({'init_table': bodo.hiframes.table.init_table,
        'alloc_list_like': bodo.hiframes.table.alloc_list_like,
        'set_table_block': bodo.hiframes.table.set_table_block,
        'set_table_len': bodo.hiframes.table.set_table_len,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'info_to_array': info_to_array, 'info_from_table': info_from_table,
        'out_col_inds': list(rscq__vofx), 'py_table_type': tydq__ibaqa})
    vsf__oqpsl = {}
    exec(sviu__qwuzf, ovm__jfqn, vsf__oqpsl)
    return vsf__oqpsl['impl']


@intrinsic
def py_table_to_cpp_table(typingctx, py_table_t, py_table_type_t):
    assert isinstance(py_table_t, bodo.hiframes.table.TableType
        ), 'invalid py table type'
    assert isinstance(py_table_type_t, types.TypeRef), 'invalid py table ref'
    tydq__ibaqa = py_table_type_t.instance_type

    def codegen(context, builder, sig, args):
        py_table, eburd__cmus = args
        ngdi__hqq = cgutils.create_struct_proxy(tydq__ibaqa)(context,
            builder, py_table)
        if tydq__ibaqa.has_runtime_cols:
            ayr__wie = lir.Constant(lir.IntType(64), 0)
            for ymyxn__yhcu, t in enumerate(tydq__ibaqa.arr_types):
                saan__vxvbv = getattr(ngdi__hqq, f'block_{ymyxn__yhcu}')
                uwgf__dzq = ListInstance(context, builder, types.List(t),
                    saan__vxvbv)
                ayr__wie = builder.add(ayr__wie, uwgf__dzq.size)
        else:
            ayr__wie = lir.Constant(lir.IntType(64), len(tydq__ibaqa.arr_types)
                )
        eburd__cmus, zpo__yapd = ListInstance.allocate_ex(context, builder,
            types.List(array_info_type), ayr__wie)
        zpo__yapd.size = ayr__wie
        if tydq__ibaqa.has_runtime_cols:
            vpzab__smoa = lir.Constant(lir.IntType(64), 0)
            for ymyxn__yhcu, t in enumerate(tydq__ibaqa.arr_types):
                saan__vxvbv = getattr(ngdi__hqq, f'block_{ymyxn__yhcu}')
                uwgf__dzq = ListInstance(context, builder, types.List(t),
                    saan__vxvbv)
                ysr__qypw = uwgf__dzq.size
                with cgutils.for_range(builder, ysr__qypw) as svy__gfv:
                    kkve__lrrv = svy__gfv.index
                    arr = uwgf__dzq.getitem(kkve__lrrv)
                    nufnh__iatq = signature(array_info_type, t)
                    xstd__cxtaq = arr,
                    ptgt__bqx = array_to_info_codegen(context, builder,
                        nufnh__iatq, xstd__cxtaq)
                    zpo__yapd.inititem(builder.add(vpzab__smoa, kkve__lrrv),
                        ptgt__bqx, incref=False)
                vpzab__smoa = builder.add(vpzab__smoa, ysr__qypw)
        else:
            for t, ymyxn__yhcu in tydq__ibaqa.type_to_blk.items():
                ysr__qypw = context.get_constant(types.int64, len(
                    tydq__ibaqa.block_to_arr_ind[ymyxn__yhcu]))
                saan__vxvbv = getattr(ngdi__hqq, f'block_{ymyxn__yhcu}')
                uwgf__dzq = ListInstance(context, builder, types.List(t),
                    saan__vxvbv)
                jjxb__gsstp = context.make_constant_array(builder, types.
                    Array(types.int64, 1, 'C'), np.array(tydq__ibaqa.
                    block_to_arr_ind[ymyxn__yhcu], dtype=np.int64))
                erug__akwpw = context.make_array(types.Array(types.int64, 1,
                    'C'))(context, builder, jjxb__gsstp)
                with cgutils.for_range(builder, ysr__qypw) as svy__gfv:
                    kkve__lrrv = svy__gfv.index
                    bkk__ocp = _getitem_array_single_int(context, builder,
                        types.int64, types.Array(types.int64, 1, 'C'),
                        erug__akwpw, kkve__lrrv)
                    gjt__ybl = signature(types.none, tydq__ibaqa, types.
                        List(t), types.int64, types.int64)
                    pqsf__madm = py_table, saan__vxvbv, kkve__lrrv, bkk__ocp
                    bodo.hiframes.table.ensure_column_unboxed_codegen(context,
                        builder, gjt__ybl, pqsf__madm)
                    arr = uwgf__dzq.getitem(kkve__lrrv)
                    nufnh__iatq = signature(array_info_type, t)
                    xstd__cxtaq = arr,
                    ptgt__bqx = array_to_info_codegen(context, builder,
                        nufnh__iatq, xstd__cxtaq)
                    zpo__yapd.inititem(bkk__ocp, ptgt__bqx, incref=False)
        fzg__qsfho = zpo__yapd.value
        bkw__uue = signature(table_type, types.List(array_info_type))
        bhqix__ruqa = fzg__qsfho,
        cpp_table = arr_info_list_to_table_codegen(context, builder,
            bkw__uue, bhqix__ruqa)
        context.nrt.decref(builder, types.List(array_info_type), fzg__qsfho)
        return cpp_table
    return table_type(tydq__ibaqa, py_table_type_t), codegen


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def py_data_to_cpp_table(py_table, extra_arrs_tup, in_col_inds_t,
    n_table_cols_t):
    vkod__qopf = in_col_inds_t.instance_type.meta
    ovm__jfqn = {}
    goswd__yriz = get_overload_const_int(n_table_cols_t)
    eury__wzpct = defaultdict(list)
    eaaf__wpk = {}
    for kkve__lrrv, nwmuh__skmzz in enumerate(vkod__qopf):
        if nwmuh__skmzz in eaaf__wpk:
            eury__wzpct[nwmuh__skmzz].append(kkve__lrrv)
        else:
            eaaf__wpk[nwmuh__skmzz] = kkve__lrrv
    sviu__qwuzf = (
        'def impl(py_table, extra_arrs_tup, in_col_inds_t, n_table_cols_t):\n')
    sviu__qwuzf += (
        f'  cpp_arr_list = alloc_empty_list_type({len(vkod__qopf)}, array_info_type)\n'
        )
    if py_table != types.none:
        for ymyxn__yhcu in py_table.type_to_blk.values():
            mcm__pnu = [eaaf__wpk.get(kkve__lrrv, -1) for kkve__lrrv in
                py_table.block_to_arr_ind[ymyxn__yhcu]]
            ovm__jfqn[f'out_inds_{ymyxn__yhcu}'] = np.array(mcm__pnu, np.int64)
            ovm__jfqn[f'arr_inds_{ymyxn__yhcu}'] = np.array(py_table.
                block_to_arr_ind[ymyxn__yhcu], np.int64)
            sviu__qwuzf += (
                f'  arr_list_{ymyxn__yhcu} = get_table_block(py_table, {ymyxn__yhcu})\n'
                )
            sviu__qwuzf += f'  for i in range(len(arr_list_{ymyxn__yhcu})):\n'
            sviu__qwuzf += (
                f'    out_arr_ind_{ymyxn__yhcu} = out_inds_{ymyxn__yhcu}[i]\n')
            sviu__qwuzf += f'    if out_arr_ind_{ymyxn__yhcu} == -1:\n'
            sviu__qwuzf += f'      continue\n'
            sviu__qwuzf += (
                f'    arr_ind_{ymyxn__yhcu} = arr_inds_{ymyxn__yhcu}[i]\n')
            sviu__qwuzf += f"""    ensure_column_unboxed(py_table, arr_list_{ymyxn__yhcu}, i, arr_ind_{ymyxn__yhcu})
"""
            sviu__qwuzf += f"""    cpp_arr_list[out_arr_ind_{ymyxn__yhcu}] = array_to_info(arr_list_{ymyxn__yhcu}[i])
"""
        for dnzx__qpial, ybgua__ebk in eury__wzpct.items():
            if dnzx__qpial < goswd__yriz:
                ymyxn__yhcu = py_table.block_nums[dnzx__qpial]
                qgz__jhnbx = py_table.block_offsets[dnzx__qpial]
                for pxsmg__evj in ybgua__ebk:
                    sviu__qwuzf += f"""  cpp_arr_list[{pxsmg__evj}] = array_to_info(arr_list_{ymyxn__yhcu}[{qgz__jhnbx}])
"""
    for kkve__lrrv in range(len(extra_arrs_tup)):
        bqxyo__hbr = eaaf__wpk.get(goswd__yriz + kkve__lrrv, -1)
        if bqxyo__hbr != -1:
            rgje__lhrq = [bqxyo__hbr] + eury__wzpct.get(goswd__yriz +
                kkve__lrrv, [])
            for pxsmg__evj in rgje__lhrq:
                sviu__qwuzf += f"""  cpp_arr_list[{pxsmg__evj}] = array_to_info(extra_arrs_tup[{kkve__lrrv}])
"""
    sviu__qwuzf += f'  return arr_info_list_to_table(cpp_arr_list)\n'
    ovm__jfqn.update({'array_info_type': array_info_type,
        'alloc_empty_list_type': bodo.hiframes.table.alloc_empty_list_type,
        'get_table_block': bodo.hiframes.table.get_table_block,
        'ensure_column_unboxed': bodo.hiframes.table.ensure_column_unboxed,
        'array_to_info': array_to_info, 'arr_info_list_to_table':
        arr_info_list_to_table})
    vsf__oqpsl = {}
    exec(sviu__qwuzf, ovm__jfqn, vsf__oqpsl)
    return vsf__oqpsl['impl']


delete_info_decref_array = types.ExternalFunction('delete_info_decref_array',
    types.void(array_info_type))
delete_table_decref_arrays = types.ExternalFunction(
    'delete_table_decref_arrays', types.void(table_type))
decref_table_array = types.ExternalFunction('decref_table_array', types.
    void(table_type, types.int32))


@intrinsic
def delete_table(typingctx, table_t=None):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        lbxq__bmhdb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='delete_table')
        builder.call(mlt__mwj, args)
    return types.void(table_t), codegen


@intrinsic
def shuffle_table(typingctx, table_t, n_keys_t, _is_parallel, keep_comm_info_t
    ):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(32)])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='shuffle_table')
        eok__devig = builder.call(mlt__mwj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eok__devig
    return table_type(table_t, types.int64, types.boolean, types.int32
        ), codegen


class ShuffleInfoType(types.Type):

    def __init__(self):
        super(ShuffleInfoType, self).__init__(name='ShuffleInfoType()')


shuffle_info_type = ShuffleInfoType()
register_model(ShuffleInfoType)(models.OpaqueModel)
get_shuffle_info = types.ExternalFunction('get_shuffle_info',
    shuffle_info_type(table_type))


@intrinsic
def delete_shuffle_info(typingctx, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[0] == types.none:
            return
        lbxq__bmhdb = lir.FunctionType(lir.VoidType(), [lir.IntType(8).
            as_pointer()])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='delete_shuffle_info')
        return builder.call(mlt__mwj, args)
    return types.void(shuffle_info_t), codegen


@intrinsic
def reverse_shuffle_table(typingctx, table_t, shuffle_info_t=None):

    def codegen(context, builder, sig, args):
        if sig.args[-1] == types.none:
            return context.get_constant_null(table_type)
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer()])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='reverse_shuffle_table')
        return builder.call(mlt__mwj, args)
    return table_type(table_type, shuffle_info_t), codegen


@intrinsic
def get_null_shuffle_info(typingctx):

    def codegen(context, builder, sig, args):
        return context.get_constant_null(sig.return_type)
    return shuffle_info_type(), codegen


@intrinsic
def hash_join_table(typingctx, left_table_t, right_table_t, left_parallel_t,
    right_parallel_t, n_keys_t, n_data_left_t, n_data_right_t, same_vect_t,
    key_in_out_t, same_need_typechange_t, is_left_t, is_right_t, is_join_t,
    extra_data_col_t, indicator, _bodo_na_equal, cond_func, left_col_nums,
    left_col_nums_len, right_col_nums, right_col_nums_len, num_rows_ptr_t):
    assert left_table_t == table_type
    assert right_table_t == table_type

    def codegen(context, builder, sig, args):
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(64), lir.IntType(64),
            lir.IntType(64), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(1), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(1), lir
            .IntType(1), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(64), lir.IntType(8).as_pointer(), lir
            .IntType(64), lir.IntType(8).as_pointer()])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='hash_join_table')
        eok__devig = builder.call(mlt__mwj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eok__devig
    return table_type(left_table_t, right_table_t, types.boolean, types.
        boolean, types.int64, types.int64, types.int64, types.voidptr,
        types.voidptr, types.voidptr, types.boolean, types.boolean, types.
        boolean, types.boolean, types.boolean, types.boolean, types.voidptr,
        types.voidptr, types.int64, types.voidptr, types.int64, types.voidptr
        ), codegen


@intrinsic
def cross_join_table(typingctx, left_table_t, right_table_t,
    left_parallel_t, right_parallel_t, is_left_t, is_right_t,
    key_in_output_t, need_typechange_t, cond_func, left_col_nums,
    left_col_nums_len, right_col_nums, right_col_nums_len, num_rows_ptr_t):
    assert left_table_t == table_type, 'cross_join_table: cpp table type expected'
    assert right_table_t == table_type, 'cross_join_table: cpp table type expected'

    def codegen(context, builder, sig, args):
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(1), lir.IntType(1), lir.IntType(1), lir.IntType(1), lir
            .IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(64), lir.IntType(8).as_pointer(), lir.IntType(64), lir.
            IntType(8).as_pointer()])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='cross_join_table')
        eok__devig = builder.call(mlt__mwj, args)
        bodo.utils.utils.inlined_check_and_propagate_cpp_exception(context,
            builder)
        return eok__devig
    return table_type(left_table_t, right_table_t, types.boolean, types.
        boolean, types.boolean, types.boolean, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.int64, types.voidptr, types.
        int64, types.voidptr), codegen


@intrinsic
def sort_values_table(typingctx, table_t, n_keys_t, vect_ascending_t,
    na_position_b_t, dead_keys_t, n_rows_t, bounds_t, parallel_t):
    assert table_t == table_type, 'C++ table type expected'

    def codegen(context, builder, sig, args):
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(8).as_pointer(), lir.IntType(8).
            as_pointer(), lir.IntType(1)])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='sort_values_table')
        eok__devig = builder.call(mlt__mwj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eok__devig
    return table_type(table_t, types.int64, types.voidptr, types.voidptr,
        types.voidptr, types.voidptr, types.voidptr, types.boolean), codegen


@intrinsic
def sample_table(typingctx, table_t, n_keys_t, frac_t, replace_t, parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.DoubleType(), lir
            .IntType(1), lir.IntType(1)])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='sample_table')
        eok__devig = builder.call(mlt__mwj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eok__devig
    return table_type(table_t, types.int64, types.float64, types.boolean,
        types.boolean), codegen


@intrinsic
def shuffle_renormalization(typingctx, table_t, random_t, random_seed_t,
    is_parallel_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1)])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='shuffle_renormalization')
        eok__devig = builder.call(mlt__mwj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eok__devig
    return table_type(table_t, types.int32, types.int64, types.boolean
        ), codegen


@intrinsic
def shuffle_renormalization_group(typingctx, table_t, random_t,
    random_seed_t, is_parallel_t, num_ranks_t, ranks_t):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(32), lir.IntType(64), lir.
            IntType(1), lir.IntType(64), lir.IntType(8).as_pointer()])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='shuffle_renormalization_group')
        eok__devig = builder.call(mlt__mwj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eok__devig
    return table_type(table_t, types.int32, types.int64, types.boolean,
        types.int64, types.voidptr), codegen


@intrinsic
def drop_duplicates_table(typingctx, table_t, parallel_t, nkey_t, keep_t,
    dropna, drop_local_first):
    assert table_t == table_type

    def codegen(context, builder, sig, args):
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(64), lir.
            IntType(64), lir.IntType(1), lir.IntType(1)])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='drop_duplicates_table')
        eok__devig = builder.call(mlt__mwj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eok__devig
    return table_type(table_t, types.boolean, types.int64, types.int64,
        types.boolean, types.boolean), codegen


@intrinsic
def groupby_and_aggregate(typingctx, table_t, n_keys_t, input_has_index,
    ftypes, func_offsets, udf_n_redvars, is_parallel, skipdropna_t,
    shift_periods_t, transform_func, head_n, return_keys, return_index,
    dropna, update_cb, combine_cb, eval_cb, general_udfs_cb,
    udf_table_dummy_t, n_out_rows_t, n_shuffle_keys_t):
    assert table_t == table_type
    assert udf_table_dummy_t == table_type

    def codegen(context, builder, sig, args):
        lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(), [lir.
            IntType(8).as_pointer(), lir.IntType(64), lir.IntType(1), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(1), lir.IntType(1), lir.
            IntType(64), lir.IntType(64), lir.IntType(64), lir.IntType(1),
            lir.IntType(1), lir.IntType(1), lir.IntType(8).as_pointer(),
            lir.IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(8).as_pointer(), lir.
            IntType(8).as_pointer(), lir.IntType(64)])
        mlt__mwj = cgutils.get_or_insert_function(builder.module,
            lbxq__bmhdb, name='groupby_and_aggregate')
        eok__devig = builder.call(mlt__mwj, args)
        context.compile_internal(builder, lambda :
            check_and_propagate_cpp_exception(), types.none(), [])
        return eok__devig
    return table_type(table_t, types.int64, types.boolean, types.voidptr,
        types.voidptr, types.voidptr, types.boolean, types.boolean, types.
        int64, types.int64, types.int64, types.boolean, types.boolean,
        types.boolean, types.voidptr, types.voidptr, types.voidptr, types.
        voidptr, table_t, types.voidptr, types.int64), codegen


_drop_duplicates_local_dictionary = types.ExternalFunction(
    'drop_duplicates_local_dictionary', types.void(array_info_type, types.
    bool_))


@numba.njit(no_cpython_wrapper=True)
def drop_duplicates_local_dictionary(dict_arr, sort_dictionary):
    nbm__dgpfr = array_to_info(dict_arr)
    _drop_duplicates_local_dictionary(nbm__dgpfr, sort_dictionary)
    check_and_propagate_cpp_exception()
    out_arr = info_to_array(nbm__dgpfr, bodo.dict_str_arr_type)
    return out_arr


_convert_local_dictionary_to_global = types.ExternalFunction(
    'convert_local_dictionary_to_global', types.void(array_info_type, types
    .bool_, types.bool_))


@numba.njit(no_cpython_wrapper=True)
def convert_local_dictionary_to_global(dict_arr, sort_dictionary,
    is_parallel=False):
    nbm__dgpfr = array_to_info(dict_arr)
    _convert_local_dictionary_to_global(nbm__dgpfr, is_parallel,
        sort_dictionary)
    check_and_propagate_cpp_exception()
    out_arr = info_to_array(nbm__dgpfr, bodo.dict_str_arr_type)
    return out_arr


get_groupby_labels = types.ExternalFunction('get_groupby_labels', types.
    int64(table_type, types.voidptr, types.voidptr, types.boolean, types.bool_)
    )
_array_isin = types.ExternalFunction('array_isin', types.void(
    array_info_type, array_info_type, array_info_type, types.bool_))


@numba.njit(no_cpython_wrapper=True)
def array_isin(out_arr, in_arr, in_values, is_parallel):
    in_arr = decode_if_dict_array(in_arr)
    in_values = decode_if_dict_array(in_values)
    sccc__cygf = array_to_info(in_arr)
    lhe__pmzvc = array_to_info(in_values)
    kgbm__tgu = array_to_info(out_arr)
    wuyd__wwhja = arr_info_list_to_table([sccc__cygf, lhe__pmzvc, kgbm__tgu])
    _array_isin(kgbm__tgu, sccc__cygf, lhe__pmzvc, is_parallel)
    check_and_propagate_cpp_exception()
    delete_table(wuyd__wwhja)


_get_search_regex = types.ExternalFunction('get_search_regex', types.void(
    array_info_type, types.bool_, types.bool_, types.voidptr, array_info_type))


@numba.njit(no_cpython_wrapper=True)
def get_search_regex(in_arr, case, match, pat, out_arr):
    sccc__cygf = array_to_info(in_arr)
    kgbm__tgu = array_to_info(out_arr)
    _get_search_regex(sccc__cygf, case, match, pat, kgbm__tgu)
    check_and_propagate_cpp_exception()


def _gen_row_access_intrinsic(col_array_typ, c_ind):
    from llvmlite import ir as lir
    biq__ezevd = col_array_typ.dtype
    if isinstance(biq__ezevd, (types.Number, TimeType, bodo.libs.
        pd_datetime_arr_ext.PandasDatetimeTZDtype)) or biq__ezevd in [bodo.
        datetime_date_type, bodo.datetime64ns, bodo.timedelta64ns, types.bool_
        ]:
        if isinstance(biq__ezevd, bodo.libs.pd_datetime_arr_ext.
            PandasDatetimeTZDtype):
            biq__ezevd = bodo.datetime64ns

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                mqf__pfx, xtb__dpn = args
                mqf__pfx = builder.bitcast(mqf__pfx, lir.IntType(8).
                    as_pointer().as_pointer())
                viiqp__morln = lir.Constant(lir.IntType(64), c_ind)
                tidt__yjn = builder.load(builder.gep(mqf__pfx, [viiqp__morln]))
                tidt__yjn = builder.bitcast(tidt__yjn, context.
                    get_data_type(biq__ezevd).as_pointer())
                return context.unpack_value(builder, biq__ezevd, builder.
                    gep(tidt__yjn, [xtb__dpn]))
            return biq__ezevd(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ in (bodo.string_array_type, bodo.binary_array_type):

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                mqf__pfx, xtb__dpn = args
                mqf__pfx = builder.bitcast(mqf__pfx, lir.IntType(8).
                    as_pointer().as_pointer())
                viiqp__morln = lir.Constant(lir.IntType(64), c_ind)
                tidt__yjn = builder.load(builder.gep(mqf__pfx, [viiqp__morln]))
                lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                paaw__dmyhv = cgutils.get_or_insert_function(builder.module,
                    lbxq__bmhdb, name='array_info_getitem')
                guf__fbxs = cgutils.alloca_once(builder, lir.IntType(64))
                args = tidt__yjn, xtb__dpn, guf__fbxs
                zkt__gxu = builder.call(paaw__dmyhv, args)
                ifd__zqysl = bodo.string_type(types.voidptr, types.int64)
                return context.compile_internal(builder, lambda data,
                    length: bodo.libs.str_arr_ext.decode_utf8(data, length),
                    ifd__zqysl, [zkt__gxu, builder.load(guf__fbxs)])
            return bodo.string_type(types.voidptr, types.int64), codegen
        return getitem_func
    if col_array_typ == bodo.libs.dict_arr_ext.dict_str_arr_type:

        @intrinsic
        def getitem_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                hlj__wekaq = lir.Constant(lir.IntType(64), 1)
                ygp__nhdwc = lir.Constant(lir.IntType(64), 2)
                mqf__pfx, xtb__dpn = args
                mqf__pfx = builder.bitcast(mqf__pfx, lir.IntType(8).
                    as_pointer().as_pointer())
                viiqp__morln = lir.Constant(lir.IntType(64), c_ind)
                tidt__yjn = builder.load(builder.gep(mqf__pfx, [viiqp__morln]))
                lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64)])
                qcgtb__kiy = cgutils.get_or_insert_function(builder.module,
                    lbxq__bmhdb, name='get_nested_info')
                args = tidt__yjn, ygp__nhdwc
                pqz__jydgt = builder.call(qcgtb__kiy, args)
                lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer()])
                bfppv__hdbhv = cgutils.get_or_insert_function(builder.
                    module, lbxq__bmhdb, name='array_info_getdata1')
                args = pqz__jydgt,
                jwa__wmhj = builder.call(bfppv__hdbhv, args)
                jwa__wmhj = builder.bitcast(jwa__wmhj, context.
                    get_data_type(col_array_typ.indices_dtype).as_pointer())
                fcrs__svf = builder.sext(builder.load(builder.gep(jwa__wmhj,
                    [xtb__dpn])), lir.IntType(64))
                args = tidt__yjn, hlj__wekaq
                axmpq__pbsv = builder.call(qcgtb__kiy, args)
                lbxq__bmhdb = lir.FunctionType(lir.IntType(8).as_pointer(),
                    [lir.IntType(8).as_pointer(), lir.IntType(64), lir.
                    IntType(64).as_pointer()])
                paaw__dmyhv = cgutils.get_or_insert_function(builder.module,
                    lbxq__bmhdb, name='array_info_getitem')
                guf__fbxs = cgutils.alloca_once(builder, lir.IntType(64))
                args = axmpq__pbsv, fcrs__svf, guf__fbxs
                zkt__gxu = builder.call(paaw__dmyhv, args)
                ifd__zqysl = bodo.string_type(types.voidptr, types.int64)
                return context.compile_internal(builder, lambda data,
                    length: bodo.libs.str_arr_ext.decode_utf8(data, length),
                    ifd__zqysl, [zkt__gxu, builder.load(guf__fbxs)])
            return bodo.string_type(types.voidptr, types.int64), codegen
        return getitem_func
    raise BodoError(
        f"General Join Conditions with '{biq__ezevd}' column data type not supported"
        )


def _gen_row_na_check_intrinsic(col_array_dtype, c_ind):
    if isinstance(col_array_dtype, (IntegerArrayType, FloatingArrayType,
        bodo.TimeArrayType)) or col_array_dtype in (bodo.libs.bool_arr_ext.
        boolean_array, bodo.binary_array_type, bodo.datetime_date_array_type
        ) or is_str_arr_type(col_array_dtype):

        @intrinsic
        def checkna_func(typingctx, table_t, ind_t):

            def codegen(context, builder, sig, args):
                oeg__jyv, xtb__dpn = args
                oeg__jyv = builder.bitcast(oeg__jyv, lir.IntType(8).
                    as_pointer().as_pointer())
                viiqp__morln = lir.Constant(lir.IntType(64), c_ind)
                tidt__yjn = builder.load(builder.gep(oeg__jyv, [viiqp__morln]))
                ixpl__bfw = builder.bitcast(tidt__yjn, context.
                    get_data_type(types.bool_).as_pointer())
                srj__deyls = bodo.utils.cg_helpers.get_bitmap_bit(builder,
                    ixpl__bfw, xtb__dpn)
                mkz__udy = builder.icmp_unsigned('!=', srj__deyls, lir.
                    Constant(lir.IntType(8), 0))
                return builder.sext(mkz__udy, lir.IntType(8))
            return types.int8(types.voidptr, types.int64), codegen
        return checkna_func
    elif isinstance(col_array_dtype, (types.Array, bodo.DatetimeArrayType)):
        biq__ezevd = col_array_dtype.dtype
        if biq__ezevd in [bodo.datetime64ns, bodo.timedelta64ns] or isinstance(
            biq__ezevd, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype):
            if isinstance(biq__ezevd, bodo.libs.pd_datetime_arr_ext.
                PandasDatetimeTZDtype):
                biq__ezevd = bodo.datetime64ns

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    mqf__pfx, xtb__dpn = args
                    mqf__pfx = builder.bitcast(mqf__pfx, lir.IntType(8).
                        as_pointer().as_pointer())
                    viiqp__morln = lir.Constant(lir.IntType(64), c_ind)
                    tidt__yjn = builder.load(builder.gep(mqf__pfx, [
                        viiqp__morln]))
                    tidt__yjn = builder.bitcast(tidt__yjn, context.
                        get_data_type(biq__ezevd).as_pointer())
                    ohje__kprt = builder.load(builder.gep(tidt__yjn, [
                        xtb__dpn]))
                    mkz__udy = builder.icmp_unsigned('!=', ohje__kprt, lir.
                        Constant(lir.IntType(64), pd._libs.iNaT))
                    return builder.sext(mkz__udy, lir.IntType(8))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
        elif isinstance(biq__ezevd, types.Float):

            @intrinsic
            def checkna_func(typingctx, table_t, ind_t):

                def codegen(context, builder, sig, args):
                    mqf__pfx, xtb__dpn = args
                    mqf__pfx = builder.bitcast(mqf__pfx, lir.IntType(8).
                        as_pointer().as_pointer())
                    viiqp__morln = lir.Constant(lir.IntType(64), c_ind)
                    tidt__yjn = builder.load(builder.gep(mqf__pfx, [
                        viiqp__morln]))
                    tidt__yjn = builder.bitcast(tidt__yjn, context.
                        get_data_type(biq__ezevd).as_pointer())
                    ohje__kprt = builder.load(builder.gep(tidt__yjn, [
                        xtb__dpn]))
                    sjrr__krmym = signature(types.bool_, biq__ezevd)
                    srj__deyls = numba.np.npyfuncs.np_real_isnan_impl(context,
                        builder, sjrr__krmym, (ohje__kprt,))
                    return builder.not_(builder.sext(srj__deyls, lir.
                        IntType(8)))
                return types.int8(types.voidptr, types.int64), codegen
            return checkna_func
    raise BodoError(
        f"General Join Conditions with '{col_array_dtype}' column type not supported"
        )
