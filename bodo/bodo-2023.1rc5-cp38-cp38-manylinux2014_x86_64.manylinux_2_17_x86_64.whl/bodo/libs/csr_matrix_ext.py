"""CSR Matrix data type implementation for scipy.sparse.csr_matrix
"""
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
import bodo
from bodo.utils.typing import BodoError


class CSRMatrixType(types.ArrayCompatible):
    ndim = 2

    def __init__(self, dtype, idx_dtype):
        self.dtype = dtype
        self.idx_dtype = idx_dtype
        super(CSRMatrixType, self).__init__(name=
            f'CSRMatrixType({dtype}, {idx_dtype})')

    @property
    def as_array(self):
        return types.Array(types.undefined, 2, 'C')

    def copy(self):
        return CSRMatrixType(self.dtype, self.idx_dtype)


@register_model(CSRMatrixType)
class CSRMatrixModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        pyzme__cbaz = [('data', types.Array(fe_type.dtype, 1, 'C')), (
            'indices', types.Array(fe_type.idx_dtype, 1, 'C')), ('indptr',
            types.Array(fe_type.idx_dtype, 1, 'C')), ('shape', types.
            UniTuple(types.int64, 2))]
        models.StructModel.__init__(self, dmm, fe_type, pyzme__cbaz)


make_attribute_wrapper(CSRMatrixType, 'data', 'data')
make_attribute_wrapper(CSRMatrixType, 'indices', 'indices')
make_attribute_wrapper(CSRMatrixType, 'indptr', 'indptr')
make_attribute_wrapper(CSRMatrixType, 'shape', 'shape')


@intrinsic
def init_csr_matrix(typingctx, data_t, indices_t, indptr_t, shape_t=None):
    assert isinstance(data_t, types.Array)
    assert isinstance(indices_t, types.Array) and isinstance(indices_t.
        dtype, types.Integer)
    assert indices_t == indptr_t

    def codegen(context, builder, signature, args):
        vzyqe__mbpne, pyr__nazr, txp__amwc, ixew__wmujv = args
        odk__fucjg = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        odk__fucjg.data = vzyqe__mbpne
        odk__fucjg.indices = pyr__nazr
        odk__fucjg.indptr = txp__amwc
        odk__fucjg.shape = ixew__wmujv
        context.nrt.incref(builder, signature.args[0], vzyqe__mbpne)
        context.nrt.incref(builder, signature.args[1], pyr__nazr)
        context.nrt.incref(builder, signature.args[2], txp__amwc)
        return odk__fucjg._getvalue()
    dpf__gqa = CSRMatrixType(data_t.dtype, indices_t.dtype)
    qziwt__usg = dpf__gqa(data_t, indices_t, indptr_t, types.UniTuple(types
        .int64, 2))
    return qziwt__usg, codegen


if bodo.utils.utils.has_scipy():
    import scipy.sparse

    @typeof_impl.register(scipy.sparse.csr_matrix)
    def _typeof_csr_matrix(val, c):
        dtype = numba.from_dtype(val.dtype)
        idx_dtype = numba.from_dtype(val.indices.dtype)
        return CSRMatrixType(dtype, idx_dtype)


@unbox(CSRMatrixType)
def unbox_csr_matrix(typ, val, c):
    odk__fucjg = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    scdd__kgth = c.pyapi.object_getattr_string(val, 'data')
    vle__fyg = c.pyapi.object_getattr_string(val, 'indices')
    okzi__xfph = c.pyapi.object_getattr_string(val, 'indptr')
    ctta__zehw = c.pyapi.object_getattr_string(val, 'shape')
    odk__fucjg.data = c.pyapi.to_native_value(types.Array(typ.dtype, 1, 'C'
        ), scdd__kgth).value
    odk__fucjg.indices = c.pyapi.to_native_value(types.Array(typ.idx_dtype,
        1, 'C'), vle__fyg).value
    odk__fucjg.indptr = c.pyapi.to_native_value(types.Array(typ.idx_dtype, 
        1, 'C'), okzi__xfph).value
    odk__fucjg.shape = c.pyapi.to_native_value(types.UniTuple(types.int64, 
        2), ctta__zehw).value
    c.pyapi.decref(scdd__kgth)
    c.pyapi.decref(vle__fyg)
    c.pyapi.decref(okzi__xfph)
    c.pyapi.decref(ctta__zehw)
    bwda__nevtr = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(odk__fucjg._getvalue(), is_error=bwda__nevtr)


@box(CSRMatrixType)
def box_csr_matrix(typ, val, c):
    xoei__rwf = c.context.insert_const_string(c.builder.module, 'scipy.sparse')
    epgq__qwk = c.pyapi.import_module_noblock(xoei__rwf)
    odk__fucjg = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Array(typ.dtype, 1, 'C'),
        odk__fucjg.data)
    scdd__kgth = c.pyapi.from_native_value(types.Array(typ.dtype, 1, 'C'),
        odk__fucjg.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        odk__fucjg.indices)
    vle__fyg = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1, 'C'),
        odk__fucjg.indices, c.env_manager)
    c.context.nrt.incref(c.builder, types.Array(typ.idx_dtype, 1, 'C'),
        odk__fucjg.indptr)
    okzi__xfph = c.pyapi.from_native_value(types.Array(typ.idx_dtype, 1,
        'C'), odk__fucjg.indptr, c.env_manager)
    ctta__zehw = c.pyapi.from_native_value(types.UniTuple(types.int64, 2),
        odk__fucjg.shape, c.env_manager)
    sho__utiob = c.pyapi.tuple_pack([scdd__kgth, vle__fyg, okzi__xfph])
    ijbw__bsfab = c.pyapi.call_method(epgq__qwk, 'csr_matrix', (sho__utiob,
        ctta__zehw))
    c.pyapi.decref(sho__utiob)
    c.pyapi.decref(scdd__kgth)
    c.pyapi.decref(vle__fyg)
    c.pyapi.decref(okzi__xfph)
    c.pyapi.decref(ctta__zehw)
    c.pyapi.decref(epgq__qwk)
    c.context.nrt.decref(c.builder, typ, val)
    return ijbw__bsfab


@overload(len, no_unliteral=True)
def overload_csr_matrix_len(A):
    if isinstance(A, CSRMatrixType):
        return lambda A: A.shape[0]


@overload_attribute(CSRMatrixType, 'ndim')
def overload_csr_matrix_ndim(A):
    return lambda A: 2


@overload_method(CSRMatrixType, 'copy', no_unliteral=True)
def overload_csr_matrix_copy(A):

    def copy_impl(A):
        return init_csr_matrix(A.data.copy(), A.indices.copy(), A.indptr.
            copy(), A.shape)
    return copy_impl


@overload(operator.getitem, no_unliteral=True)
def csr_matrix_getitem(A, idx):
    if not isinstance(A, CSRMatrixType):
        return
    gicrb__rajh = A.dtype
    prne__rie = A.idx_dtype
    if isinstance(idx, types.BaseTuple) and len(idx) == 2 and isinstance(idx
        [0], types.SliceType) and isinstance(idx[1], types.SliceType):

        def impl(A, idx):
            squte__ahj, qwmik__xytm = A.shape
            ujejl__uerqj = numba.cpython.unicode._normalize_slice(idx[0],
                squte__ahj)
            fdefv__tgr = numba.cpython.unicode._normalize_slice(idx[1],
                qwmik__xytm)
            if ujejl__uerqj.step != 1 or fdefv__tgr.step != 1:
                raise ValueError(
                    'CSR matrix slice getitem only supports step=1 currently')
            oihrf__pjy = ujejl__uerqj.start
            qjsrg__owgek = ujejl__uerqj.stop
            zhal__vooal = fdefv__tgr.start
            qqx__aopxc = fdefv__tgr.stop
            apytc__lwbuy = A.indptr
            tcgx__ixlj = A.indices
            zhrfx__frt = A.data
            xnik__pwuf = qjsrg__owgek - oihrf__pjy
            bmllg__rjtc = qqx__aopxc - zhal__vooal
            mscg__olyqm = 0
            uzj__ksaai = 0
            for bhs__aoom in range(xnik__pwuf):
                lfvp__lvljg = apytc__lwbuy[oihrf__pjy + bhs__aoom]
                ugfs__khjq = apytc__lwbuy[oihrf__pjy + bhs__aoom + 1]
                for liaw__fiffx in range(lfvp__lvljg, ugfs__khjq):
                    if tcgx__ixlj[liaw__fiffx] >= zhal__vooal and tcgx__ixlj[
                        liaw__fiffx] < qqx__aopxc:
                        mscg__olyqm += 1
            nsmo__enwvm = np.empty(xnik__pwuf + 1, prne__rie)
            tns__wtm = np.empty(mscg__olyqm, prne__rie)
            pui__cyr = np.empty(mscg__olyqm, gicrb__rajh)
            nsmo__enwvm[0] = 0
            for bhs__aoom in range(xnik__pwuf):
                lfvp__lvljg = apytc__lwbuy[oihrf__pjy + bhs__aoom]
                ugfs__khjq = apytc__lwbuy[oihrf__pjy + bhs__aoom + 1]
                for liaw__fiffx in range(lfvp__lvljg, ugfs__khjq):
                    if tcgx__ixlj[liaw__fiffx] >= zhal__vooal and tcgx__ixlj[
                        liaw__fiffx] < qqx__aopxc:
                        tns__wtm[uzj__ksaai] = tcgx__ixlj[liaw__fiffx
                            ] - zhal__vooal
                        pui__cyr[uzj__ksaai] = zhrfx__frt[liaw__fiffx]
                        uzj__ksaai += 1
                nsmo__enwvm[bhs__aoom + 1] = uzj__ksaai
            return init_csr_matrix(pui__cyr, tns__wtm, nsmo__enwvm, (
                xnik__pwuf, bmllg__rjtc))
        return impl
    elif isinstance(idx, types.Array
        ) and idx.ndim == 1 and idx.dtype == prne__rie:

        def impl(A, idx):
            squte__ahj, qwmik__xytm = A.shape
            apytc__lwbuy = A.indptr
            tcgx__ixlj = A.indices
            zhrfx__frt = A.data
            xnik__pwuf = len(idx)
            mscg__olyqm = 0
            uzj__ksaai = 0
            for bhs__aoom in range(xnik__pwuf):
                xuvy__pxf = idx[bhs__aoom]
                lfvp__lvljg = apytc__lwbuy[xuvy__pxf]
                ugfs__khjq = apytc__lwbuy[xuvy__pxf + 1]
                mscg__olyqm += ugfs__khjq - lfvp__lvljg
            nsmo__enwvm = np.empty(xnik__pwuf + 1, prne__rie)
            tns__wtm = np.empty(mscg__olyqm, prne__rie)
            pui__cyr = np.empty(mscg__olyqm, gicrb__rajh)
            nsmo__enwvm[0] = 0
            for bhs__aoom in range(xnik__pwuf):
                xuvy__pxf = idx[bhs__aoom]
                lfvp__lvljg = apytc__lwbuy[xuvy__pxf]
                ugfs__khjq = apytc__lwbuy[xuvy__pxf + 1]
                tns__wtm[uzj__ksaai:uzj__ksaai + ugfs__khjq - lfvp__lvljg
                    ] = tcgx__ixlj[lfvp__lvljg:ugfs__khjq]
                pui__cyr[uzj__ksaai:uzj__ksaai + ugfs__khjq - lfvp__lvljg
                    ] = zhrfx__frt[lfvp__lvljg:ugfs__khjq]
                uzj__ksaai += ugfs__khjq - lfvp__lvljg
                nsmo__enwvm[bhs__aoom + 1] = uzj__ksaai
            jyuz__eqyc = init_csr_matrix(pui__cyr, tns__wtm, nsmo__enwvm, (
                xnik__pwuf, qwmik__xytm))
            return jyuz__eqyc
        return impl
    raise BodoError(
        f'getitem for CSR matrix with index type {idx} not supported yet.')
