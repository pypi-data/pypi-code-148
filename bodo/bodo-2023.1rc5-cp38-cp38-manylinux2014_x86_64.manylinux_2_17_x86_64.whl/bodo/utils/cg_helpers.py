"""helper functions for code generation with llvmlite
"""
import llvmlite.binding as ll
from llvmlite import ir as lir
from numba.core import cgutils, types
import bodo
from bodo.libs import array_ext, hdist
ll.add_symbol('array_getitem', array_ext.array_getitem)
ll.add_symbol('seq_getitem', array_ext.seq_getitem)
ll.add_symbol('list_check', array_ext.list_check)
ll.add_symbol('dict_keys', array_ext.dict_keys)
ll.add_symbol('dict_values', array_ext.dict_values)
ll.add_symbol('dict_merge_from_seq2', array_ext.dict_merge_from_seq2)
ll.add_symbol('is_na_value', array_ext.is_na_value)


def set_bitmap_bit(builder, null_bitmap_ptr, ind, val):
    php__pajs = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    yjqpw__rrw = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    qkx__vise = builder.gep(null_bitmap_ptr, [php__pajs], inbounds=True)
    ncbq__hpt = builder.load(qkx__vise)
    kovzb__esmld = lir.ArrayType(lir.IntType(8), 8)
    zce__sjup = cgutils.alloca_once_value(builder, lir.Constant(
        kovzb__esmld, (1, 2, 4, 8, 16, 32, 64, 128)))
    ybgny__jdj = builder.load(builder.gep(zce__sjup, [lir.Constant(lir.
        IntType(64), 0), yjqpw__rrw], inbounds=True))
    if val:
        builder.store(builder.or_(ncbq__hpt, ybgny__jdj), qkx__vise)
    else:
        ybgny__jdj = builder.xor(ybgny__jdj, lir.Constant(lir.IntType(8), -1))
        builder.store(builder.and_(ncbq__hpt, ybgny__jdj), qkx__vise)


def get_bitmap_bit(builder, null_bitmap_ptr, ind):
    php__pajs = builder.lshr(ind, lir.Constant(lir.IntType(64), 3))
    yjqpw__rrw = builder.urem(ind, lir.Constant(lir.IntType(64), 8))
    ncbq__hpt = builder.load(builder.gep(null_bitmap_ptr, [php__pajs],
        inbounds=True))
    kovzb__esmld = lir.ArrayType(lir.IntType(8), 8)
    zce__sjup = cgutils.alloca_once_value(builder, lir.Constant(
        kovzb__esmld, (1, 2, 4, 8, 16, 32, 64, 128)))
    ybgny__jdj = builder.load(builder.gep(zce__sjup, [lir.Constant(lir.
        IntType(64), 0), yjqpw__rrw], inbounds=True))
    return builder.and_(ncbq__hpt, ybgny__jdj)


def pyarray_check(builder, context, obj):
    jtmtr__tkrol = context.get_argument_type(types.pyobject)
    bye__hjba = lir.FunctionType(lir.IntType(32), [jtmtr__tkrol])
    odjuz__rchz = cgutils.get_or_insert_function(builder.module, bye__hjba,
        name='is_np_array')
    return builder.call(odjuz__rchz, [obj])


def pyarray_getitem(builder, context, arr_obj, ind):
    jtmtr__tkrol = context.get_argument_type(types.pyobject)
    rauw__qeeme = context.get_value_type(types.intp)
    tncgv__plyv = lir.FunctionType(lir.IntType(8).as_pointer(), [
        jtmtr__tkrol, rauw__qeeme])
    sqzwm__yibr = cgutils.get_or_insert_function(builder.module,
        tncgv__plyv, name='array_getptr1')
    zdmpe__keslr = lir.FunctionType(jtmtr__tkrol, [jtmtr__tkrol, lir.
        IntType(8).as_pointer()])
    ppis__vqx = cgutils.get_or_insert_function(builder.module, zdmpe__keslr,
        name='array_getitem')
    amvk__alosi = builder.call(sqzwm__yibr, [arr_obj, ind])
    return builder.call(ppis__vqx, [arr_obj, amvk__alosi])


def pyarray_setitem(builder, context, arr_obj, ind, val_obj):
    jtmtr__tkrol = context.get_argument_type(types.pyobject)
    rauw__qeeme = context.get_value_type(types.intp)
    tncgv__plyv = lir.FunctionType(lir.IntType(8).as_pointer(), [
        jtmtr__tkrol, rauw__qeeme])
    sqzwm__yibr = cgutils.get_or_insert_function(builder.module,
        tncgv__plyv, name='array_getptr1')
    hbj__ztyr = lir.FunctionType(lir.VoidType(), [jtmtr__tkrol, lir.IntType
        (8).as_pointer(), jtmtr__tkrol])
    gfc__sdw = cgutils.get_or_insert_function(builder.module, hbj__ztyr,
        name='array_setitem')
    amvk__alosi = builder.call(sqzwm__yibr, [arr_obj, ind])
    builder.call(gfc__sdw, [arr_obj, amvk__alosi, val_obj])


def seq_getitem(builder, context, obj, ind):
    jtmtr__tkrol = context.get_argument_type(types.pyobject)
    rauw__qeeme = context.get_value_type(types.intp)
    kcr__fhgb = lir.FunctionType(jtmtr__tkrol, [jtmtr__tkrol, rauw__qeeme])
    newbn__eyiwd = cgutils.get_or_insert_function(builder.module, kcr__fhgb,
        name='seq_getitem')
    return builder.call(newbn__eyiwd, [obj, ind])


def is_na_value(builder, context, val, C_NA):
    jtmtr__tkrol = context.get_argument_type(types.pyobject)
    xvt__crl = lir.FunctionType(lir.IntType(32), [jtmtr__tkrol, jtmtr__tkrol])
    ofe__prd = cgutils.get_or_insert_function(builder.module, xvt__crl,
        name='is_na_value')
    return builder.call(ofe__prd, [val, C_NA])


def list_check(builder, context, obj):
    jtmtr__tkrol = context.get_argument_type(types.pyobject)
    zeqt__iwoi = context.get_value_type(types.int32)
    szivr__iqkos = lir.FunctionType(zeqt__iwoi, [jtmtr__tkrol])
    skjdr__ypba = cgutils.get_or_insert_function(builder.module,
        szivr__iqkos, name='list_check')
    return builder.call(skjdr__ypba, [obj])


def dict_keys(builder, context, obj):
    jtmtr__tkrol = context.get_argument_type(types.pyobject)
    szivr__iqkos = lir.FunctionType(jtmtr__tkrol, [jtmtr__tkrol])
    skjdr__ypba = cgutils.get_or_insert_function(builder.module,
        szivr__iqkos, name='dict_keys')
    return builder.call(skjdr__ypba, [obj])


def dict_values(builder, context, obj):
    jtmtr__tkrol = context.get_argument_type(types.pyobject)
    szivr__iqkos = lir.FunctionType(jtmtr__tkrol, [jtmtr__tkrol])
    skjdr__ypba = cgutils.get_or_insert_function(builder.module,
        szivr__iqkos, name='dict_values')
    return builder.call(skjdr__ypba, [obj])


def dict_merge_from_seq2(builder, context, dict_obj, seq2_obj):
    jtmtr__tkrol = context.get_argument_type(types.pyobject)
    szivr__iqkos = lir.FunctionType(lir.VoidType(), [jtmtr__tkrol,
        jtmtr__tkrol])
    skjdr__ypba = cgutils.get_or_insert_function(builder.module,
        szivr__iqkos, name='dict_merge_from_seq2')
    builder.call(skjdr__ypba, [dict_obj, seq2_obj])


def to_arr_obj_if_list_obj(c, context, builder, val, typ):
    if not (isinstance(typ, types.List) or bodo.utils.utils.is_array_typ(
        typ, False)):
        return val
    zmqhl__tvimb = cgutils.alloca_once_value(builder, val)
    zfzp__qzlwz = list_check(builder, context, val)
    weid__mbn = builder.icmp_unsigned('!=', zfzp__qzlwz, lir.Constant(
        zfzp__qzlwz.type, 0))
    with builder.if_then(weid__mbn):
        wcewe__vlb = context.insert_const_string(builder.module, 'numpy')
        nbsw__shov = c.pyapi.import_module_noblock(wcewe__vlb)
        tbvk__omjc = 'object_'
        if isinstance(typ, types.Array) or isinstance(typ.dtype, types.Float):
            tbvk__omjc = str(typ.dtype)
        uzdiq__rfe = c.pyapi.object_getattr_string(nbsw__shov, tbvk__omjc)
        eeg__iqtbw = builder.load(zmqhl__tvimb)
        cbat__kvmpn = c.pyapi.call_method(nbsw__shov, 'asarray', (
            eeg__iqtbw, uzdiq__rfe))
        builder.store(cbat__kvmpn, zmqhl__tvimb)
        c.pyapi.decref(nbsw__shov)
        c.pyapi.decref(uzdiq__rfe)
    val = builder.load(zmqhl__tvimb)
    return val


def get_array_elem_counts(c, builder, context, arr_obj, typ):
    from bodo.libs.array_item_arr_ext import ArrayItemArrayType
    from bodo.libs.map_arr_ext import MapArrayType
    from bodo.libs.str_arr_ext import get_utf8_size, string_array_type
    from bodo.libs.struct_arr_ext import StructArrayType, StructType
    from bodo.libs.tuple_arr_ext import TupleArrayType
    if typ == bodo.string_type:
        gidh__mbylc = c.pyapi.to_native_value(bodo.string_type, arr_obj).value
        soj__gwhe, ert__psc = c.pyapi.call_jit_code(lambda a: get_utf8_size
            (a), types.int64(bodo.string_type), [gidh__mbylc])
        context.nrt.decref(builder, typ, gidh__mbylc)
        return cgutils.pack_array(builder, [ert__psc])
    if isinstance(typ, (StructType, types.BaseTuple)):
        wcewe__vlb = context.insert_const_string(builder.module, 'pandas')
        jmf__aluz = c.pyapi.import_module_noblock(wcewe__vlb)
        C_NA = c.pyapi.object_getattr_string(jmf__aluz, 'NA')
        esphk__ohhg = bodo.utils.transform.get_type_alloc_counts(typ)
        pogb__sfqv = context.make_tuple(builder, types.Tuple(esphk__ohhg *
            [types.int64]), esphk__ohhg * [context.get_constant(types.int64,
            0)])
        vfi__oqsuh = cgutils.alloca_once_value(builder, pogb__sfqv)
        cvy__qiome = 0
        wvv__gfpvr = typ.data if isinstance(typ, StructType) else typ.types
        for ojhqy__ixqlz, t in enumerate(wvv__gfpvr):
            qnid__tmhp = bodo.utils.transform.get_type_alloc_counts(t)
            if qnid__tmhp == 0:
                continue
            if isinstance(typ, StructType):
                val_obj = c.pyapi.dict_getitem_string(arr_obj, typ.names[
                    ojhqy__ixqlz])
            else:
                val_obj = c.pyapi.tuple_getitem(arr_obj, ojhqy__ixqlz)
            unztf__fqjo = is_na_value(builder, context, val_obj, C_NA)
            geh__dlrub = builder.icmp_unsigned('!=', unztf__fqjo, lir.
                Constant(unztf__fqjo.type, 1))
            with builder.if_then(geh__dlrub):
                pogb__sfqv = builder.load(vfi__oqsuh)
                yiv__dun = get_array_elem_counts(c, builder, context,
                    val_obj, t)
                for ojhqy__ixqlz in range(qnid__tmhp):
                    sur__qmsfm = builder.extract_value(pogb__sfqv, 
                        cvy__qiome + ojhqy__ixqlz)
                    mhs__hgaz = builder.extract_value(yiv__dun, ojhqy__ixqlz)
                    pogb__sfqv = builder.insert_value(pogb__sfqv, builder.
                        add(sur__qmsfm, mhs__hgaz), cvy__qiome + ojhqy__ixqlz)
                builder.store(pogb__sfqv, vfi__oqsuh)
            cvy__qiome += qnid__tmhp
        c.pyapi.decref(jmf__aluz)
        c.pyapi.decref(C_NA)
        return builder.load(vfi__oqsuh)
    if not bodo.utils.utils.is_array_typ(typ, False):
        return cgutils.pack_array(builder, [], lir.IntType(64))
    n = bodo.utils.utils.object_length(c, arr_obj)
    if not (isinstance(typ, (ArrayItemArrayType, StructArrayType,
        TupleArrayType, MapArrayType)) or typ == string_array_type):
        return cgutils.pack_array(builder, [n])
    wcewe__vlb = context.insert_const_string(builder.module, 'pandas')
    jmf__aluz = c.pyapi.import_module_noblock(wcewe__vlb)
    C_NA = c.pyapi.object_getattr_string(jmf__aluz, 'NA')
    esphk__ohhg = bodo.utils.transform.get_type_alloc_counts(typ)
    pogb__sfqv = context.make_tuple(builder, types.Tuple(esphk__ohhg * [
        types.int64]), [n] + (esphk__ohhg - 1) * [context.get_constant(
        types.int64, 0)])
    vfi__oqsuh = cgutils.alloca_once_value(builder, pogb__sfqv)
    with cgutils.for_range(builder, n) as rtvj__aalmd:
        cchht__kzz = rtvj__aalmd.index
        jqmws__eiu = seq_getitem(builder, context, arr_obj, cchht__kzz)
        unztf__fqjo = is_na_value(builder, context, jqmws__eiu, C_NA)
        geh__dlrub = builder.icmp_unsigned('!=', unztf__fqjo, lir.Constant(
            unztf__fqjo.type, 1))
        with builder.if_then(geh__dlrub):
            if isinstance(typ, ArrayItemArrayType) or typ == string_array_type:
                pogb__sfqv = builder.load(vfi__oqsuh)
                yiv__dun = get_array_elem_counts(c, builder, context,
                    jqmws__eiu, typ.dtype)
                for ojhqy__ixqlz in range(esphk__ohhg - 1):
                    sur__qmsfm = builder.extract_value(pogb__sfqv, 
                        ojhqy__ixqlz + 1)
                    mhs__hgaz = builder.extract_value(yiv__dun, ojhqy__ixqlz)
                    pogb__sfqv = builder.insert_value(pogb__sfqv, builder.
                        add(sur__qmsfm, mhs__hgaz), ojhqy__ixqlz + 1)
                builder.store(pogb__sfqv, vfi__oqsuh)
            elif isinstance(typ, (StructArrayType, TupleArrayType)):
                cvy__qiome = 1
                for ojhqy__ixqlz, t in enumerate(typ.data):
                    qnid__tmhp = bodo.utils.transform.get_type_alloc_counts(t
                        .dtype)
                    if qnid__tmhp == 0:
                        continue
                    if isinstance(typ, TupleArrayType):
                        val_obj = c.pyapi.tuple_getitem(jqmws__eiu,
                            ojhqy__ixqlz)
                    else:
                        val_obj = c.pyapi.dict_getitem_string(jqmws__eiu,
                            typ.names[ojhqy__ixqlz])
                    unztf__fqjo = is_na_value(builder, context, val_obj, C_NA)
                    geh__dlrub = builder.icmp_unsigned('!=', unztf__fqjo,
                        lir.Constant(unztf__fqjo.type, 1))
                    with builder.if_then(geh__dlrub):
                        pogb__sfqv = builder.load(vfi__oqsuh)
                        yiv__dun = get_array_elem_counts(c, builder,
                            context, val_obj, t.dtype)
                        for ojhqy__ixqlz in range(qnid__tmhp):
                            sur__qmsfm = builder.extract_value(pogb__sfqv, 
                                cvy__qiome + ojhqy__ixqlz)
                            mhs__hgaz = builder.extract_value(yiv__dun,
                                ojhqy__ixqlz)
                            pogb__sfqv = builder.insert_value(pogb__sfqv,
                                builder.add(sur__qmsfm, mhs__hgaz), 
                                cvy__qiome + ojhqy__ixqlz)
                        builder.store(pogb__sfqv, vfi__oqsuh)
                    cvy__qiome += qnid__tmhp
            else:
                assert isinstance(typ, MapArrayType), typ
                pogb__sfqv = builder.load(vfi__oqsuh)
                tigpp__fjn = dict_keys(builder, context, jqmws__eiu)
                mae__rfz = dict_values(builder, context, jqmws__eiu)
                mbci__kodd = get_array_elem_counts(c, builder, context,
                    tigpp__fjn, typ.key_arr_type)
                lvns__wzpo = bodo.utils.transform.get_type_alloc_counts(typ
                    .key_arr_type)
                for ojhqy__ixqlz in range(1, lvns__wzpo + 1):
                    sur__qmsfm = builder.extract_value(pogb__sfqv, ojhqy__ixqlz
                        )
                    mhs__hgaz = builder.extract_value(mbci__kodd, 
                        ojhqy__ixqlz - 1)
                    pogb__sfqv = builder.insert_value(pogb__sfqv, builder.
                        add(sur__qmsfm, mhs__hgaz), ojhqy__ixqlz)
                qef__cgnu = get_array_elem_counts(c, builder, context,
                    mae__rfz, typ.value_arr_type)
                for ojhqy__ixqlz in range(lvns__wzpo + 1, esphk__ohhg):
                    sur__qmsfm = builder.extract_value(pogb__sfqv, ojhqy__ixqlz
                        )
                    mhs__hgaz = builder.extract_value(qef__cgnu, 
                        ojhqy__ixqlz - lvns__wzpo)
                    pogb__sfqv = builder.insert_value(pogb__sfqv, builder.
                        add(sur__qmsfm, mhs__hgaz), ojhqy__ixqlz)
                builder.store(pogb__sfqv, vfi__oqsuh)
                c.pyapi.decref(tigpp__fjn)
                c.pyapi.decref(mae__rfz)
        c.pyapi.decref(jqmws__eiu)
    c.pyapi.decref(jmf__aluz)
    c.pyapi.decref(C_NA)
    return builder.load(vfi__oqsuh)


def gen_allocate_array(context, builder, arr_type, n_elems, c=None):
    itggh__ffx = n_elems.type.count
    assert itggh__ffx >= 1
    gcvo__aitjy = builder.extract_value(n_elems, 0)
    if itggh__ffx != 1:
        ffg__djtg = cgutils.pack_array(builder, [builder.extract_value(
            n_elems, ojhqy__ixqlz) for ojhqy__ixqlz in range(1, itggh__ffx)])
        iiure__wiiw = types.Tuple([types.int64] * (itggh__ffx - 1))
    else:
        ffg__djtg = context.get_dummy_value()
        iiure__wiiw = types.none
    soil__kcatd = types.TypeRef(arr_type)
    hie__kbgfa = arr_type(types.int64, soil__kcatd, iiure__wiiw)
    args = [gcvo__aitjy, context.get_dummy_value(), ffg__djtg]
    fzosm__ihwnz = lambda n, t, s: bodo.utils.utils.alloc_type(n, t, s)
    if c:
        soj__gwhe, pow__epie = c.pyapi.call_jit_code(fzosm__ihwnz,
            hie__kbgfa, args)
    else:
        pow__epie = context.compile_internal(builder, fzosm__ihwnz,
            hie__kbgfa, args)
    return pow__epie


def is_ll_eq(builder, val1, val2):
    hqvn__obcj = val1.type.pointee
    roj__shqd = val2.type.pointee
    assert hqvn__obcj == roj__shqd, 'invalid llvm value comparison'
    if isinstance(hqvn__obcj, (lir.BaseStructType, lir.ArrayType)):
        n_elems = len(hqvn__obcj.elements) if isinstance(hqvn__obcj, lir.
            BaseStructType) else hqvn__obcj.count
        fqy__hvm = lir.Constant(lir.IntType(1), 1)
        for ojhqy__ixqlz in range(n_elems):
            vqeh__utc = lir.IntType(32)(0)
            zzhfi__lsa = lir.IntType(32)(ojhqy__ixqlz)
            tpnv__gkqlq = builder.gep(val1, [vqeh__utc, zzhfi__lsa],
                inbounds=True)
            rjyku__uwky = builder.gep(val2, [vqeh__utc, zzhfi__lsa],
                inbounds=True)
            fqy__hvm = builder.and_(fqy__hvm, is_ll_eq(builder, tpnv__gkqlq,
                rjyku__uwky))
        return fqy__hvm
    chqrc__kly = builder.load(val1)
    dwvki__aau = builder.load(val2)
    if chqrc__kly.type in (lir.FloatType(), lir.DoubleType()):
        rvgr__txk = 32 if chqrc__kly.type == lir.FloatType() else 64
        chqrc__kly = builder.bitcast(chqrc__kly, lir.IntType(rvgr__txk))
        dwvki__aau = builder.bitcast(dwvki__aau, lir.IntType(rvgr__txk))
    return builder.icmp_unsigned('==', chqrc__kly, dwvki__aau)
