import enum
import operator
import numba
import numpy as np
import pandas as pd
from llvmlite import ir as lir
from numba.core import cgutils, types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, box, intrinsic, lower_cast, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from numba.parfors.array_analysis import ArrayAnalysis
import bodo
from bodo.utils.typing import NOT_CONSTANT, BodoError, MetaType, check_unsupported_args, dtype_to_array_type, get_literal_value, get_overload_const, get_overload_const_bool, is_common_scalar_dtype, is_iterable_type, is_list_like_index_type, is_literal_type, is_overload_constant_bool, is_overload_none, is_overload_true, is_scalar_type, raise_bodo_error


class PDCategoricalDtype(types.Opaque):

    def __init__(self, categories, elem_type, ordered, data=None, int_type=None
        ):
        self.categories = categories
        self.elem_type = elem_type
        self.ordered = ordered
        self.data = _get_cat_index_type(elem_type) if data is None else data
        self.int_type = int_type
        ddnk__rpj = (
            f'PDCategoricalDtype({self.categories}, {self.elem_type}, {self.ordered}, {self.data}, {self.int_type})'
            )
        super(PDCategoricalDtype, self).__init__(name=ddnk__rpj)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.CategoricalDtype)
def _typeof_pd_cat_dtype(val, c):
    qltbr__cma = tuple(val.categories.values)
    elem_type = None if len(qltbr__cma) == 0 else bodo.typeof(val.
        categories.values).dtype
    int_type = getattr(val, '_int_type', None)
    return PDCategoricalDtype(qltbr__cma, elem_type, val.ordered, bodo.
        typeof(val.categories), int_type)


def _get_cat_index_type(elem_type):
    elem_type = bodo.string_type if elem_type is None else elem_type
    return bodo.utils.typing.get_index_type_from_dtype(elem_type)


@lower_constant(PDCategoricalDtype)
def lower_constant_categorical_type(context, builder, typ, pyval):
    categories = context.get_constant_generic(builder, bodo.typeof(pyval.
        categories), pyval.categories)
    ordered = context.get_constant(types.bool_, pyval.ordered)
    return lir.Constant.literal_struct([categories, ordered])


@register_model(PDCategoricalDtype)
class PDCategoricalDtypeModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ceksd__nccxo = [('categories', fe_type.data), ('ordered', types.bool_)]
        models.StructModel.__init__(self, dmm, fe_type, ceksd__nccxo)


make_attribute_wrapper(PDCategoricalDtype, 'categories', 'categories')
make_attribute_wrapper(PDCategoricalDtype, 'ordered', 'ordered')


@intrinsic
def init_cat_dtype(typingctx, categories_typ, ordered_typ, int_type,
    cat_vals_typ=None):
    assert bodo.hiframes.pd_index_ext.is_index_type(categories_typ
        ), 'init_cat_dtype requires index type for categories'
    assert is_overload_constant_bool(ordered_typ
        ), 'init_cat_dtype requires constant ordered flag'
    rjguc__lhuc = None if is_overload_none(int_type) else int_type.dtype
    assert is_overload_none(cat_vals_typ) or isinstance(cat_vals_typ, types
        .TypeRef), 'init_cat_dtype requires constant category values'
    gmduw__dzhc = None if is_overload_none(cat_vals_typ
        ) else cat_vals_typ.instance_type.meta

    def codegen(context, builder, sig, args):
        categories, ordered, bglxo__dxogk, bglxo__dxogk = args
        cat_dtype = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        cat_dtype.categories = categories
        context.nrt.incref(builder, sig.args[0], categories)
        context.nrt.incref(builder, sig.args[1], ordered)
        cat_dtype.ordered = ordered
        return cat_dtype._getvalue()
    olw__zwtic = PDCategoricalDtype(gmduw__dzhc, categories_typ.dtype,
        is_overload_true(ordered_typ), categories_typ, rjguc__lhuc)
    return olw__zwtic(categories_typ, ordered_typ, int_type, cat_vals_typ
        ), codegen


@unbox(PDCategoricalDtype)
def unbox_cat_dtype(typ, obj, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    jacsv__hkayp = c.pyapi.object_getattr_string(obj, 'ordered')
    cat_dtype.ordered = c.pyapi.to_native_value(types.bool_, jacsv__hkayp
        ).value
    c.pyapi.decref(jacsv__hkayp)
    gbqh__fnsa = c.pyapi.object_getattr_string(obj, 'categories')
    cat_dtype.categories = c.pyapi.to_native_value(typ.data, gbqh__fnsa).value
    c.pyapi.decref(gbqh__fnsa)
    pmi__hwdo = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(cat_dtype._getvalue(), is_error=pmi__hwdo)


@box(PDCategoricalDtype)
def box_cat_dtype(typ, val, c):
    cat_dtype = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    jacsv__hkayp = c.pyapi.from_native_value(types.bool_, cat_dtype.ordered,
        c.env_manager)
    c.context.nrt.incref(c.builder, typ.data, cat_dtype.categories)
    dqgi__wcnxo = c.pyapi.from_native_value(typ.data, cat_dtype.categories,
        c.env_manager)
    jua__kgaeb = c.context.insert_const_string(c.builder.module, 'pandas')
    dkihu__enwr = c.pyapi.import_module_noblock(jua__kgaeb)
    emb__plud = c.pyapi.call_method(dkihu__enwr, 'CategoricalDtype', (
        dqgi__wcnxo, jacsv__hkayp))
    c.pyapi.decref(jacsv__hkayp)
    c.pyapi.decref(dqgi__wcnxo)
    c.pyapi.decref(dkihu__enwr)
    c.context.nrt.decref(c.builder, typ, val)
    return emb__plud


@overload_attribute(PDCategoricalDtype, 'nbytes')
def pd_categorical_nbytes_overload(A):
    return lambda A: A.categories.nbytes + bodo.io.np_io.get_dtype_size(types
        .bool_)


class CategoricalArrayType(types.ArrayCompatible):

    def __init__(self, dtype):
        self.dtype = dtype
        super(CategoricalArrayType, self).__init__(name=
            f'CategoricalArrayType({dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return CategoricalArrayType(self.dtype)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@typeof_impl.register(pd.Categorical)
def _typeof_pd_cat(val, c):
    return CategoricalArrayType(bodo.typeof(val.dtype))


@register_model(CategoricalArrayType)
class CategoricalArrayModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ums__olyi = get_categories_int_type(fe_type.dtype)
        ceksd__nccxo = [('dtype', fe_type.dtype), ('codes', types.Array(
            ums__olyi, 1, 'C'))]
        super(CategoricalArrayModel, self).__init__(dmm, fe_type, ceksd__nccxo)


make_attribute_wrapper(CategoricalArrayType, 'codes', 'codes')
make_attribute_wrapper(CategoricalArrayType, 'dtype', 'dtype')


@unbox(CategoricalArrayType)
def unbox_categorical_array(typ, val, c):
    uuy__jvt = c.pyapi.object_getattr_string(val, 'codes')
    dtype = get_categories_int_type(typ.dtype)
    codes = c.pyapi.to_native_value(types.Array(dtype, 1, 'C'), uuy__jvt).value
    c.pyapi.decref(uuy__jvt)
    emb__plud = c.pyapi.object_getattr_string(val, 'dtype')
    dbqb__txsf = c.pyapi.to_native_value(typ.dtype, emb__plud).value
    c.pyapi.decref(emb__plud)
    jhzuu__gwms = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    jhzuu__gwms.codes = codes
    jhzuu__gwms.dtype = dbqb__txsf
    return NativeValue(jhzuu__gwms._getvalue())


@lower_constant(CategoricalArrayType)
def lower_constant_categorical_array(context, builder, typ, pyval):
    qacpr__dtzny = get_categories_int_type(typ.dtype)
    patp__kktx = context.get_constant_generic(builder, types.Array(
        qacpr__dtzny, 1, 'C'), pyval.codes)
    cat_dtype = context.get_constant_generic(builder, typ.dtype, pyval.dtype)
    return lir.Constant.literal_struct([cat_dtype, patp__kktx])


def get_categories_int_type(cat_dtype):
    dtype = types.int64
    if cat_dtype.int_type is not None:
        return cat_dtype.int_type
    if cat_dtype.categories is None:
        return types.int64
    tbfl__bpcdg = len(cat_dtype.categories)
    if tbfl__bpcdg < np.iinfo(np.int8).max:
        dtype = types.int8
    elif tbfl__bpcdg < np.iinfo(np.int16).max:
        dtype = types.int16
    elif tbfl__bpcdg < np.iinfo(np.int32).max:
        dtype = types.int32
    return dtype


@box(CategoricalArrayType)
def box_categorical_array(typ, val, c):
    dtype = typ.dtype
    jua__kgaeb = c.context.insert_const_string(c.builder.module, 'pandas')
    dkihu__enwr = c.pyapi.import_module_noblock(jua__kgaeb)
    ums__olyi = get_categories_int_type(dtype)
    tzkk__cjex = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    zekox__orf = types.Array(ums__olyi, 1, 'C')
    c.context.nrt.incref(c.builder, zekox__orf, tzkk__cjex.codes)
    uuy__jvt = c.pyapi.from_native_value(zekox__orf, tzkk__cjex.codes, c.
        env_manager)
    c.context.nrt.incref(c.builder, dtype, tzkk__cjex.dtype)
    emb__plud = c.pyapi.from_native_value(dtype, tzkk__cjex.dtype, c.
        env_manager)
    evw__eomca = c.pyapi.borrow_none()
    cks__pgqot = c.pyapi.object_getattr_string(dkihu__enwr, 'Categorical')
    fdrcf__qxdz = c.pyapi.call_method(cks__pgqot, 'from_codes', (uuy__jvt,
        evw__eomca, evw__eomca, emb__plud))
    c.pyapi.decref(cks__pgqot)
    c.pyapi.decref(uuy__jvt)
    c.pyapi.decref(emb__plud)
    c.pyapi.decref(dkihu__enwr)
    c.context.nrt.decref(c.builder, typ, val)
    return fdrcf__qxdz


def _to_readonly(t):
    from bodo.hiframes.pd_index_ext import DatetimeIndexType, NumericIndexType, TimedeltaIndexType
    if isinstance(t, CategoricalArrayType):
        return CategoricalArrayType(_to_readonly(t.dtype))
    if isinstance(t, PDCategoricalDtype):
        return PDCategoricalDtype(t.categories, t.elem_type, t.ordered,
            _to_readonly(t.data), t.int_type)
    if isinstance(t, types.Array):
        return types.Array(t.dtype, t.ndim, 'C', True)
    if isinstance(t, NumericIndexType):
        return NumericIndexType(t.dtype, t.name_typ, _to_readonly(t.data))
    if isinstance(t, (DatetimeIndexType, TimedeltaIndexType)):
        return t.__class__(t.name_typ, _to_readonly(t.data))
    return t


@lower_cast(CategoricalArrayType, CategoricalArrayType)
def cast_cat_arr(context, builder, fromty, toty, val):
    if _to_readonly(toty) == fromty:
        return val
    raise BodoError(f'Cannot cast from {fromty} to {toty}')


def create_cmp_op_overload(op):

    def overload_cat_arr_cmp(A, other):
        if not isinstance(A, CategoricalArrayType):
            return
        if A.dtype.categories and is_literal_type(other) and types.unliteral(
            other) == A.dtype.elem_type:
            val = get_literal_value(other)
            ojzi__olvl = list(A.dtype.categories).index(val
                ) if val in A.dtype.categories else -2

            def impl_lit(A, other):
                nqv__wxmf = op(bodo.hiframes.pd_categorical_ext.
                    get_categorical_arr_codes(A), ojzi__olvl)
                return nqv__wxmf
            return impl_lit

        def impl(A, other):
            ojzi__olvl = get_code_for_value(A.dtype, other)
            nqv__wxmf = op(bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A), ojzi__olvl)
            return nqv__wxmf
        return impl
    return overload_cat_arr_cmp


def _install_cmp_ops():
    for op in [operator.eq, operator.ne]:
        jvfai__dpps = create_cmp_op_overload(op)
        overload(op, inline='always', no_unliteral=True)(jvfai__dpps)


_install_cmp_ops()


@register_jitable
def get_code_for_value(cat_dtype, val):
    tzkk__cjex = cat_dtype.categories
    n = len(tzkk__cjex)
    for cnu__aia in range(n):
        if tzkk__cjex[cnu__aia] == val:
            return cnu__aia
    return -2


@overload_method(CategoricalArrayType, 'astype', inline='always',
    no_unliteral=True)
def overload_cat_arr_astype(A, dtype, copy=True, _bodo_nan_to_str=True):
    if dtype == types.unicode_type:
        raise_bodo_error(
            "CategoricalArray.astype(): 'dtype' when passed as string must be a constant value"
            )
    hfc__dngln = bodo.utils.typing.parse_dtype(dtype, 'CategoricalArray.astype'
        )
    if hfc__dngln != A.dtype.elem_type and hfc__dngln != types.unicode_type:
        raise BodoError(
            f'Converting categorical array {A} to dtype {dtype} not supported yet'
            )
    if hfc__dngln == types.unicode_type:

        def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
            codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(
                A)
            categories = A.dtype.categories
            n = len(codes)
            nqv__wxmf = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
            for cnu__aia in numba.parfors.parfor.internal_prange(n):
                rxz__vwrsj = codes[cnu__aia]
                if rxz__vwrsj == -1:
                    if _bodo_nan_to_str:
                        bodo.libs.str_arr_ext.str_arr_setitem_NA_str(nqv__wxmf,
                            cnu__aia)
                    else:
                        bodo.libs.array_kernels.setna(nqv__wxmf, cnu__aia)
                    continue
                nqv__wxmf[cnu__aia] = str(bodo.utils.conversion.
                    unbox_if_tz_naive_timestamp(categories[rxz__vwrsj]))
            return nqv__wxmf
        return impl
    zekox__orf = dtype_to_array_type(hfc__dngln)

    def impl(A, dtype, copy=True, _bodo_nan_to_str=True):
        codes = bodo.hiframes.pd_categorical_ext.get_categorical_arr_codes(A)
        categories = A.dtype.categories
        n = len(codes)
        nqv__wxmf = bodo.utils.utils.alloc_type(n, zekox__orf, (-1,))
        for cnu__aia in numba.parfors.parfor.internal_prange(n):
            rxz__vwrsj = codes[cnu__aia]
            if rxz__vwrsj == -1:
                bodo.libs.array_kernels.setna(nqv__wxmf, cnu__aia)
                continue
            nqv__wxmf[cnu__aia
                ] = bodo.utils.conversion.unbox_if_tz_naive_timestamp(
                categories[rxz__vwrsj])
        return nqv__wxmf
    return impl


@overload(pd.api.types.CategoricalDtype, no_unliteral=True)
def cat_overload_dummy(val_list):
    return lambda val_list: 1


@intrinsic
def init_categorical_array(typingctx, codes, cat_dtype=None):
    assert isinstance(codes, types.Array) and isinstance(codes.dtype, types
        .Integer)

    def codegen(context, builder, signature, args):
        fwo__iwrr, dbqb__txsf = args
        tzkk__cjex = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        tzkk__cjex.codes = fwo__iwrr
        tzkk__cjex.dtype = dbqb__txsf
        context.nrt.incref(builder, signature.args[0], fwo__iwrr)
        context.nrt.incref(builder, signature.args[1], dbqb__txsf)
        return tzkk__cjex._getvalue()
    swv__tkrca = CategoricalArrayType(cat_dtype)
    sig = swv__tkrca(codes, cat_dtype)
    return sig, codegen


def init_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    svfd__anfg = args[0]
    if equiv_set.has_shape(svfd__anfg):
        return ArrayAnalysis.AnalyzeResult(shape=svfd__anfg, pre=[])
    return None


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_init_categorical_array
    ) = init_categorical_array_equiv


def alloc_categorical_array(n, cat_dtype):
    pass


@overload(alloc_categorical_array, no_unliteral=True)
def _alloc_categorical_array(n, cat_dtype):
    ums__olyi = get_categories_int_type(cat_dtype)

    def impl(n, cat_dtype):
        codes = np.empty(n, ums__olyi)
        return init_categorical_array(codes, cat_dtype)
    return impl


def alloc_categorical_array_equiv(self, scope, equiv_set, loc, args, kws):
    assert len(args) == 2 and not kws
    return ArrayAnalysis.AnalyzeResult(shape=args[0], pre=[])


(ArrayAnalysis.
    _analyze_op_call_bodo_hiframes_pd_categorical_ext_alloc_categorical_array
    ) = alloc_categorical_array_equiv


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_categorical_arr_codes(A):
    return lambda A: A.codes


def alias_ext_dummy_func(lhs_name, args, alias_map, arg_aliases):
    assert len(args) >= 1
    numba.core.ir_utils._add_alias(lhs_name, args[0].name, alias_map,
        arg_aliases)


numba.core.ir_utils.alias_func_extensions['init_categorical_array',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func
numba.core.ir_utils.alias_func_extensions['get_categorical_arr_codes',
    'bodo.hiframes.pd_categorical_ext'] = alias_ext_dummy_func


@overload_method(CategoricalArrayType, 'copy', no_unliteral=True)
def cat_arr_copy_overload(arr):
    return lambda arr: init_categorical_array(arr.codes.copy(), arr.dtype)


def build_replace_dicts(to_replace, value, categories):
    return dict(), np.empty(len(categories) + 1), 0


@overload(build_replace_dicts, no_unliteral=True)
def _build_replace_dicts(to_replace, value, categories):
    if isinstance(to_replace, types.Number) or to_replace == bodo.string_type:

        def impl(to_replace, value, categories):
            return build_replace_dicts([to_replace], value, categories)
        return impl
    else:

        def impl(to_replace, value, categories):
            n = len(categories)
            hmxwu__nix = {}
            patp__kktx = np.empty(n + 1, np.int64)
            nive__sarcm = {}
            aim__dtq = []
            khbj__kokbs = {}
            for cnu__aia in range(n):
                khbj__kokbs[categories[cnu__aia]] = cnu__aia
            for nvku__uauj in to_replace:
                if nvku__uauj != value:
                    if nvku__uauj in khbj__kokbs:
                        if value in khbj__kokbs:
                            hmxwu__nix[nvku__uauj] = nvku__uauj
                            moj__uaw = khbj__kokbs[nvku__uauj]
                            nive__sarcm[moj__uaw] = khbj__kokbs[value]
                            aim__dtq.append(moj__uaw)
                        else:
                            hmxwu__nix[nvku__uauj] = value
                            khbj__kokbs[value] = khbj__kokbs[nvku__uauj]
            izosk__nth = np.sort(np.array(aim__dtq))
            gzzi__degf = 0
            vtkg__qjv = []
            for cnton__rtwi in range(-1, n):
                while gzzi__degf < len(izosk__nth
                    ) and cnton__rtwi > izosk__nth[gzzi__degf]:
                    gzzi__degf += 1
                vtkg__qjv.append(gzzi__degf)
            for mge__ormj in range(-1, n):
                xqlk__swi = mge__ormj
                if mge__ormj in nive__sarcm:
                    xqlk__swi = nive__sarcm[mge__ormj]
                patp__kktx[mge__ormj + 1] = xqlk__swi - vtkg__qjv[xqlk__swi + 1
                    ]
            return hmxwu__nix, patp__kktx, len(izosk__nth)
        return impl


@numba.njit
def python_build_replace_dicts(to_replace, value, categories):
    return build_replace_dicts(to_replace, value, categories)


@register_jitable
def reassign_codes(new_codes_arr, old_codes_arr, codes_map_arr):
    for cnu__aia in range(len(new_codes_arr)):
        new_codes_arr[cnu__aia] = codes_map_arr[old_codes_arr[cnu__aia] + 1]


@overload_method(CategoricalArrayType, 'replace', inline='always',
    no_unliteral=True)
def overload_replace(arr, to_replace, value):

    def impl(arr, to_replace, value):
        return bodo.hiframes.pd_categorical_ext.cat_replace(arr, to_replace,
            value)
    return impl


def cat_replace(arr, to_replace, value):
    return


@overload(cat_replace, no_unliteral=True)
def cat_replace_overload(arr, to_replace, value):
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(to_replace,
        'CategoricalArray.replace()')
    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(value,
        'CategoricalArray.replace()')
    awxjf__wzxl = arr.dtype.ordered
    eyjvj__xvw = arr.dtype.elem_type
    baswl__bppr = get_overload_const(to_replace)
    ndkd__qlwpv = get_overload_const(value)
    if (arr.dtype.categories is not None and baswl__bppr is not
        NOT_CONSTANT and ndkd__qlwpv is not NOT_CONSTANT):
        hydzh__amlgh, codes_map_arr, bglxo__dxogk = python_build_replace_dicts(
            baswl__bppr, ndkd__qlwpv, arr.dtype.categories)
        if len(hydzh__amlgh) == 0:
            return lambda arr, to_replace, value: arr.copy()
        psy__oip = []
        for urij__sqi in arr.dtype.categories:
            if urij__sqi in hydzh__amlgh:
                jcf__qvme = hydzh__amlgh[urij__sqi]
                if jcf__qvme != urij__sqi:
                    psy__oip.append(jcf__qvme)
            else:
                psy__oip.append(urij__sqi)
        ksfm__pey = bodo.utils.utils.create_categorical_type(psy__oip, arr.
            dtype.data.data, awxjf__wzxl)
        gfksy__acuuu = MetaType(tuple(ksfm__pey))

        def impl_dtype(arr, to_replace, value):
            uma__plipm = init_cat_dtype(bodo.utils.conversion.
                index_from_array(ksfm__pey), awxjf__wzxl, None, gfksy__acuuu)
            tzkk__cjex = alloc_categorical_array(len(arr.codes), uma__plipm)
            reassign_codes(tzkk__cjex.codes, arr.codes, codes_map_arr)
            return tzkk__cjex
        return impl_dtype
    eyjvj__xvw = arr.dtype.elem_type
    if eyjvj__xvw == types.unicode_type:

        def impl_str(arr, to_replace, value):
            categories = arr.dtype.categories
            hmxwu__nix, codes_map_arr, wuoth__gimpv = build_replace_dicts(
                to_replace, value, categories.values)
            if len(hmxwu__nix) == 0:
                return init_categorical_array(arr.codes.copy().astype(np.
                    int64), init_cat_dtype(categories.copy(), awxjf__wzxl,
                    None, None))
            n = len(categories)
            ksfm__pey = bodo.libs.str_arr_ext.pre_alloc_string_array(n -
                wuoth__gimpv, -1)
            ward__jkfb = 0
            for cnton__rtwi in range(n):
                uvqvu__ork = categories[cnton__rtwi]
                if uvqvu__ork in hmxwu__nix:
                    mdagm__dbna = hmxwu__nix[uvqvu__ork]
                    if mdagm__dbna != uvqvu__ork:
                        ksfm__pey[ward__jkfb] = mdagm__dbna
                        ward__jkfb += 1
                else:
                    ksfm__pey[ward__jkfb] = uvqvu__ork
                    ward__jkfb += 1
            tzkk__cjex = alloc_categorical_array(len(arr.codes),
                init_cat_dtype(bodo.utils.conversion.index_from_array(
                ksfm__pey), awxjf__wzxl, None, None))
            reassign_codes(tzkk__cjex.codes, arr.codes, codes_map_arr)
            return tzkk__cjex
        return impl_str
    aofp__lzaj = dtype_to_array_type(eyjvj__xvw)

    def impl(arr, to_replace, value):
        categories = arr.dtype.categories
        hmxwu__nix, codes_map_arr, wuoth__gimpv = build_replace_dicts(
            to_replace, value, categories.values)
        if len(hmxwu__nix) == 0:
            return init_categorical_array(arr.codes.copy().astype(np.int64),
                init_cat_dtype(categories.copy(), awxjf__wzxl, None, None))
        n = len(categories)
        ksfm__pey = bodo.utils.utils.alloc_type(n - wuoth__gimpv,
            aofp__lzaj, None)
        ward__jkfb = 0
        for cnu__aia in range(n):
            uvqvu__ork = categories[cnu__aia]
            if uvqvu__ork in hmxwu__nix:
                mdagm__dbna = hmxwu__nix[uvqvu__ork]
                if mdagm__dbna != uvqvu__ork:
                    ksfm__pey[ward__jkfb] = mdagm__dbna
                    ward__jkfb += 1
            else:
                ksfm__pey[ward__jkfb] = uvqvu__ork
                ward__jkfb += 1
        tzkk__cjex = alloc_categorical_array(len(arr.codes), init_cat_dtype
            (bodo.utils.conversion.index_from_array(ksfm__pey), awxjf__wzxl,
            None, None))
        reassign_codes(tzkk__cjex.codes, arr.codes, codes_map_arr)
        return tzkk__cjex
    return impl


@overload(len, no_unliteral=True)
def overload_cat_arr_len(A):
    if isinstance(A, CategoricalArrayType):
        return lambda A: len(A.codes)


@overload_attribute(CategoricalArrayType, 'shape')
def overload_cat_arr_shape(A):
    return lambda A: (len(A.codes),)


@overload_attribute(CategoricalArrayType, 'ndim')
def overload_cat_arr_ndim(A):
    return lambda A: 1


@overload_attribute(CategoricalArrayType, 'nbytes')
def cat_arr_nbytes_overload(A):
    return lambda A: A.codes.nbytes + A.dtype.nbytes


@register_jitable
def get_label_dict_from_categories(vals):
    cpdz__fsoel = dict()
    qgmh__ssq = 0
    for cnu__aia in range(len(vals)):
        val = vals[cnu__aia]
        if val in cpdz__fsoel:
            continue
        cpdz__fsoel[val] = qgmh__ssq
        qgmh__ssq += 1
    return cpdz__fsoel


@register_jitable
def get_label_dict_from_categories_no_duplicates(vals):
    cpdz__fsoel = dict()
    for cnu__aia in range(len(vals)):
        val = vals[cnu__aia]
        cpdz__fsoel[val] = cnu__aia
    return cpdz__fsoel


@overload(pd.Categorical, no_unliteral=True)
def pd_categorical_overload(values, categories=None, ordered=None, dtype=
    None, fastpath=False):
    dnxxd__obaqh = dict(fastpath=fastpath)
    bcml__tsmh = dict(fastpath=False)
    check_unsupported_args('pd.Categorical', dnxxd__obaqh, bcml__tsmh)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):

        def impl_dtype(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, dtype)
        return impl_dtype
    if not is_overload_none(categories):
        afo__fdrv = get_overload_const(categories)
        if afo__fdrv is not NOT_CONSTANT and get_overload_const(ordered
            ) is not NOT_CONSTANT:
            if is_overload_none(ordered):
                mew__ynwvr = False
            else:
                mew__ynwvr = get_overload_const_bool(ordered)
            uzt__utvnc = pd.CategoricalDtype(pd.array(afo__fdrv), mew__ynwvr
                ).categories.array
            aptgn__rdwnx = MetaType(tuple(uzt__utvnc))

            def impl_cats_const(values, categories=None, ordered=None,
                dtype=None, fastpath=False):
                data = bodo.utils.conversion.coerce_to_array(values)
                uma__plipm = init_cat_dtype(bodo.utils.conversion.
                    index_from_array(uzt__utvnc), mew__ynwvr, None,
                    aptgn__rdwnx)
                return bodo.utils.conversion.fix_arr_dtype(data, uma__plipm)
            return impl_cats_const

        def impl_cats(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            ordered = bodo.utils.conversion.false_if_none(ordered)
            data = bodo.utils.conversion.coerce_to_array(values)
            qltbr__cma = bodo.utils.conversion.convert_to_index(categories)
            cat_dtype = bodo.hiframes.pd_categorical_ext.init_cat_dtype(
                qltbr__cma, ordered, None, None)
            return bodo.utils.conversion.fix_arr_dtype(data, cat_dtype)
        return impl_cats
    elif is_overload_none(ordered):

        def impl_auto(values, categories=None, ordered=None, dtype=None,
            fastpath=False):
            data = bodo.utils.conversion.coerce_to_array(values)
            return bodo.utils.conversion.fix_arr_dtype(data, 'category')
        return impl_auto
    raise BodoError(
        f'pd.Categorical(): argument combination not supported yet: {values}, {categories}, {ordered}, {dtype}'
        )


@overload(operator.getitem, no_unliteral=True)
def categorical_array_getitem(arr, ind):
    if not isinstance(arr, CategoricalArrayType):
        return
    if isinstance(ind, types.Integer):

        def categorical_getitem_impl(arr, ind):
            yvp__djb = arr.codes[ind]
            return arr.dtype.categories[max(yvp__djb, 0)]
        return categorical_getitem_impl
    if ind != bodo.boolean_array and is_list_like_index_type(ind
        ) or isinstance(ind, types.SliceType):

        def impl_bool(arr, ind):
            return init_categorical_array(arr.codes[ind], arr.dtype)
        return impl_bool
    if ind != bodo.boolean_array:
        raise BodoError(
            f'getitem for CategoricalArrayType with indexing type {ind} not supported.'
            )


class CategoricalMatchingValues(enum.Enum):
    DIFFERENT_TYPES = -1
    DONT_MATCH = 0
    MAY_MATCH = 1
    DO_MATCH = 2


def categorical_arrs_match(arr1, arr2):
    if not (isinstance(arr1, CategoricalArrayType) and isinstance(arr2,
        CategoricalArrayType)):
        return CategoricalMatchingValues.DIFFERENT_TYPES
    if arr1.dtype.categories is None or arr2.dtype.categories is None:
        return CategoricalMatchingValues.MAY_MATCH
    return (CategoricalMatchingValues.DO_MATCH if arr1.dtype.categories ==
        arr2.dtype.categories and arr1.dtype.ordered == arr2.dtype.ordered else
        CategoricalMatchingValues.DONT_MATCH)


@register_jitable
def cat_dtype_equal(dtype1, dtype2):
    if dtype1.ordered != dtype2.ordered or len(dtype1.categories) != len(dtype2
        .categories):
        return False
    arr1 = dtype1.categories.values
    arr2 = dtype2.categories.values
    for cnu__aia in range(len(arr1)):
        if arr1[cnu__aia] != arr2[cnu__aia]:
            return False
    return True


@overload(operator.setitem, no_unliteral=True)
def categorical_array_setitem(arr, ind, val):
    if not isinstance(arr, CategoricalArrayType):
        return
    if val == types.none or isinstance(val, types.optional):
        return
    yqpwt__syeui = is_scalar_type(val) and is_common_scalar_dtype([types.
        unliteral(val), arr.dtype.elem_type]) and not (isinstance(arr.dtype
        .elem_type, types.Integer) and isinstance(val, types.Float))
    infgo__cbw = not isinstance(val, CategoricalArrayType
        ) and is_iterable_type(val) and is_common_scalar_dtype([val.dtype,
        arr.dtype.elem_type]) and not (isinstance(arr.dtype.elem_type,
        types.Integer) and isinstance(val.dtype, types.Float))
    wblc__sukk = categorical_arrs_match(arr, val)
    sshuf__qdsue = (
        f"setitem for CategoricalArrayType of dtype {arr.dtype} with indexing type {ind} received an incorrect 'value' type {val}."
        )
    pfwmi__ajqwp = (
        'Cannot set a Categorical with another, without identical categories')
    if isinstance(ind, types.Integer):
        if not yqpwt__syeui:
            raise BodoError(sshuf__qdsue)

        def impl_scalar(arr, ind, val):
            if val not in arr.dtype.categories:
                raise ValueError(
                    'Cannot setitem on a Categorical with a new category, set the categories first'
                    )
            yvp__djb = arr.dtype.categories.get_loc(val)
            arr.codes[ind] = yvp__djb
        return impl_scalar
    if is_list_like_index_type(ind) and isinstance(ind.dtype, types.Integer):
        if not (yqpwt__syeui or infgo__cbw or wblc__sukk !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(sshuf__qdsue)
        if wblc__sukk == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(pfwmi__ajqwp)
        if yqpwt__syeui:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                qaxkh__lmli = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for cnton__rtwi in range(n):
                    arr.codes[ind[cnton__rtwi]] = qaxkh__lmli
            return impl_scalar
        if wblc__sukk == CategoricalMatchingValues.DO_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                n = len(val.codes)
                for cnu__aia in range(n):
                    arr.codes[ind[cnu__aia]] = val.codes[cnu__aia]
            return impl_arr_ind_mask
        if wblc__sukk == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(pfwmi__ajqwp)
                n = len(val.codes)
                for cnu__aia in range(n):
                    arr.codes[ind[cnu__aia]] = val.codes[cnu__aia]
            return impl_arr_ind_mask
        if infgo__cbw:

            def impl_arr_ind_mask_cat_values(arr, ind, val):
                n = len(val)
                categories = arr.dtype.categories
                for cnton__rtwi in range(n):
                    mxj__lruxc = (bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(val[cnton__rtwi]))
                    if mxj__lruxc not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    yvp__djb = categories.get_loc(mxj__lruxc)
                    arr.codes[ind[cnton__rtwi]] = yvp__djb
            return impl_arr_ind_mask_cat_values
    if is_list_like_index_type(ind) and ind.dtype == types.bool_:
        if not (yqpwt__syeui or infgo__cbw or wblc__sukk !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(sshuf__qdsue)
        if wblc__sukk == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(pfwmi__ajqwp)
        if yqpwt__syeui:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                qaxkh__lmli = arr.dtype.categories.get_loc(val)
                n = len(ind)
                for cnton__rtwi in range(n):
                    if ind[cnton__rtwi]:
                        arr.codes[cnton__rtwi] = qaxkh__lmli
            return impl_scalar
        if wblc__sukk == CategoricalMatchingValues.DO_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                n = len(ind)
                arq__rgu = 0
                for cnu__aia in range(n):
                    if ind[cnu__aia]:
                        arr.codes[cnu__aia] = val.codes[arq__rgu]
                        arq__rgu += 1
            return impl_bool_ind_mask
        if wblc__sukk == CategoricalMatchingValues.MAY_MATCH:

            def impl_bool_ind_mask(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(pfwmi__ajqwp)
                n = len(ind)
                arq__rgu = 0
                for cnu__aia in range(n):
                    if ind[cnu__aia]:
                        arr.codes[cnu__aia] = val.codes[arq__rgu]
                        arq__rgu += 1
            return impl_bool_ind_mask
        if infgo__cbw:

            def impl_bool_ind_mask_cat_values(arr, ind, val):
                n = len(ind)
                arq__rgu = 0
                categories = arr.dtype.categories
                for cnton__rtwi in range(n):
                    if ind[cnton__rtwi]:
                        mxj__lruxc = (bodo.utils.conversion.
                            unbox_if_tz_naive_timestamp(val[arq__rgu]))
                        if mxj__lruxc not in categories:
                            raise ValueError(
                                'Cannot setitem on a Categorical with a new category, set the categories first'
                                )
                        yvp__djb = categories.get_loc(mxj__lruxc)
                        arr.codes[cnton__rtwi] = yvp__djb
                        arq__rgu += 1
            return impl_bool_ind_mask_cat_values
    if isinstance(ind, types.SliceType):
        if not (yqpwt__syeui or infgo__cbw or wblc__sukk !=
            CategoricalMatchingValues.DIFFERENT_TYPES):
            raise BodoError(sshuf__qdsue)
        if wblc__sukk == CategoricalMatchingValues.DONT_MATCH:
            raise BodoError(pfwmi__ajqwp)
        if yqpwt__syeui:

            def impl_scalar(arr, ind, val):
                if val not in arr.dtype.categories:
                    raise ValueError(
                        'Cannot setitem on a Categorical with a new category, set the categories first'
                        )
                qaxkh__lmli = arr.dtype.categories.get_loc(val)
                egi__uoi = numba.cpython.unicode._normalize_slice(ind, len(arr)
                    )
                for cnton__rtwi in range(egi__uoi.start, egi__uoi.stop,
                    egi__uoi.step):
                    arr.codes[cnton__rtwi] = qaxkh__lmli
            return impl_scalar
        if wblc__sukk == CategoricalMatchingValues.DO_MATCH:

            def impl_arr(arr, ind, val):
                arr.codes[ind] = val.codes
            return impl_arr
        if wblc__sukk == CategoricalMatchingValues.MAY_MATCH:

            def impl_arr(arr, ind, val):
                if not cat_dtype_equal(arr.dtype, val.dtype):
                    raise ValueError(pfwmi__ajqwp)
                arr.codes[ind] = val.codes
            return impl_arr
        if infgo__cbw:

            def impl_slice_cat_values(arr, ind, val):
                categories = arr.dtype.categories
                egi__uoi = numba.cpython.unicode._normalize_slice(ind, len(arr)
                    )
                arq__rgu = 0
                for cnton__rtwi in range(egi__uoi.start, egi__uoi.stop,
                    egi__uoi.step):
                    mxj__lruxc = (bodo.utils.conversion.
                        unbox_if_tz_naive_timestamp(val[arq__rgu]))
                    if mxj__lruxc not in categories:
                        raise ValueError(
                            'Cannot setitem on a Categorical with a new category, set the categories first'
                            )
                    yvp__djb = categories.get_loc(mxj__lruxc)
                    arr.codes[cnton__rtwi] = yvp__djb
                    arq__rgu += 1
            return impl_slice_cat_values
    raise BodoError(
        f'setitem for CategoricalArrayType with indexing type {ind} not supported.'
        )
