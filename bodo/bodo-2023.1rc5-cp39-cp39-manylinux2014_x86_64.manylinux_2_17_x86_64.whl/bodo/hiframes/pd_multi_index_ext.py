"""Support for MultiIndex type of Pandas
"""
import operator
import numba
import pandas as pd
from numba.core import cgutils, types
from numba.extending import NativeValue, box, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, register_model, typeof_impl, unbox
from bodo.utils.conversion import ensure_contig_if_np
from bodo.utils.typing import BodoError, check_unsupported_args, dtype_to_array_type, get_val_type_maybe_str_literal, is_overload_none


class MultiIndexType(types.ArrayCompatible):

    def __init__(self, array_types, names_typ=None, name_typ=None):
        names_typ = (types.none,) * len(array_types
            ) if names_typ is None else names_typ
        name_typ = types.none if name_typ is None else name_typ
        self.array_types = array_types
        self.names_typ = names_typ
        self.name_typ = name_typ
        super(MultiIndexType, self).__init__(name=
            'MultiIndexType({}, {}, {})'.format(array_types, names_typ,
            name_typ))
    ndim = 1

    @property
    def as_array(self):
        return types.Array(types.undefined, 1, 'C')

    def copy(self):
        return MultiIndexType(self.array_types, self.names_typ, self.name_typ)

    @property
    def nlevels(self):
        return len(self.array_types)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(MultiIndexType)
class MultiIndexModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ayp__ieym = [('data', types.Tuple(fe_type.array_types)), ('names',
            types.Tuple(fe_type.names_typ)), ('name', fe_type.name_typ)]
        super(MultiIndexModel, self).__init__(dmm, fe_type, ayp__ieym)


make_attribute_wrapper(MultiIndexType, 'data', '_data')
make_attribute_wrapper(MultiIndexType, 'names', '_names')
make_attribute_wrapper(MultiIndexType, 'name', '_name')


@typeof_impl.register(pd.MultiIndex)
def typeof_multi_index(val, c):
    array_types = tuple(numba.typeof(val.levels[fccjs__jbx].values) for
        fccjs__jbx in range(val.nlevels))
    return MultiIndexType(array_types, tuple(get_val_type_maybe_str_literal
        (ifnzb__jib) for ifnzb__jib in val.names), numba.typeof(val.name))


@box(MultiIndexType)
def box_multi_index(typ, val, c):
    akmdu__dpslm = c.context.insert_const_string(c.builder.module, 'pandas')
    vvft__knrag = c.pyapi.import_module_noblock(akmdu__dpslm)
    okbck__ppsd = c.pyapi.object_getattr_string(vvft__knrag, 'MultiIndex')
    grhpp__tzztb = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    c.context.nrt.incref(c.builder, types.Tuple(typ.array_types),
        grhpp__tzztb.data)
    mygpe__spa = c.pyapi.from_native_value(types.Tuple(typ.array_types),
        grhpp__tzztb.data, c.env_manager)
    c.context.nrt.incref(c.builder, types.Tuple(typ.names_typ),
        grhpp__tzztb.names)
    sgx__gthgp = c.pyapi.from_native_value(types.Tuple(typ.names_typ),
        grhpp__tzztb.names, c.env_manager)
    c.context.nrt.incref(c.builder, typ.name_typ, grhpp__tzztb.name)
    zpgpe__mtfve = c.pyapi.from_native_value(typ.name_typ, grhpp__tzztb.
        name, c.env_manager)
    pab__yrcfr = c.pyapi.borrow_none()
    cckxt__guin = c.pyapi.call_method(okbck__ppsd, 'from_arrays', (
        mygpe__spa, pab__yrcfr, sgx__gthgp))
    c.pyapi.object_setattr_string(cckxt__guin, 'name', zpgpe__mtfve)
    c.pyapi.decref(mygpe__spa)
    c.pyapi.decref(sgx__gthgp)
    c.pyapi.decref(zpgpe__mtfve)
    c.pyapi.decref(vvft__knrag)
    c.pyapi.decref(okbck__ppsd)
    c.context.nrt.decref(c.builder, typ, val)
    return cckxt__guin


@unbox(MultiIndexType)
def unbox_multi_index(typ, val, c):
    atju__jdcy = []
    axw__ajdu = []
    for fccjs__jbx in range(typ.nlevels):
        tgwci__mvm = c.pyapi.unserialize(c.pyapi.serialize_object(fccjs__jbx))
        tuygf__rtjpc = c.pyapi.call_method(val, 'get_level_values', (
            tgwci__mvm,))
        tnlbn__twu = c.pyapi.object_getattr_string(tuygf__rtjpc, 'values')
        c.pyapi.decref(tuygf__rtjpc)
        c.pyapi.decref(tgwci__mvm)
        ktdqv__ugw = c.pyapi.to_native_value(typ.array_types[fccjs__jbx],
            tnlbn__twu).value
        atju__jdcy.append(ktdqv__ugw)
        axw__ajdu.append(tnlbn__twu)
    if isinstance(types.Tuple(typ.array_types), types.UniTuple):
        data = cgutils.pack_array(c.builder, atju__jdcy)
    else:
        data = cgutils.pack_struct(c.builder, atju__jdcy)
    sgx__gthgp = c.pyapi.object_getattr_string(val, 'names')
    dsbz__dqc = c.pyapi.unserialize(c.pyapi.serialize_object(tuple))
    olwhr__ijwj = c.pyapi.call_function_objargs(dsbz__dqc, (sgx__gthgp,))
    names = c.pyapi.to_native_value(types.Tuple(typ.names_typ), olwhr__ijwj
        ).value
    zpgpe__mtfve = c.pyapi.object_getattr_string(val, 'name')
    name = c.pyapi.to_native_value(typ.name_typ, zpgpe__mtfve).value
    grhpp__tzztb = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    grhpp__tzztb.data = data
    grhpp__tzztb.names = names
    grhpp__tzztb.name = name
    for tnlbn__twu in axw__ajdu:
        c.pyapi.decref(tnlbn__twu)
    c.pyapi.decref(sgx__gthgp)
    c.pyapi.decref(dsbz__dqc)
    c.pyapi.decref(olwhr__ijwj)
    c.pyapi.decref(zpgpe__mtfve)
    return NativeValue(grhpp__tzztb._getvalue())


def from_product_error_checking(iterables, sortorder, names):
    guhit__nkq = 'pandas.MultiIndex.from_product'
    zksa__orb = dict(sortorder=sortorder)
    gxkf__lvtc = dict(sortorder=None)
    check_unsupported_args(guhit__nkq, zksa__orb, gxkf__lvtc, package_name=
        'pandas', module_name='Index')
    if not (is_overload_none(names) or isinstance(names, types.BaseTuple)):
        raise BodoError(f'{guhit__nkq}: names must be None or a tuple.')
    elif not isinstance(iterables, types.BaseTuple):
        raise BodoError(f'{guhit__nkq}: iterables must be a tuple.')
    elif not is_overload_none(names) and len(iterables) != len(names):
        raise BodoError(
            f'{guhit__nkq}: iterables and names must be of the same length.')


def from_product(iterable, sortorder=None, names=None):
    pass


@overload(from_product)
def from_product_overload(iterables, sortorder=None, names=None):
    from_product_error_checking(iterables, sortorder, names)
    array_types = tuple(dtype_to_array_type(iterable.dtype) for iterable in
        iterables)
    if is_overload_none(names):
        names_typ = tuple([types.none] * len(iterables))
    else:
        names_typ = names.types
    nvo__cqrfn = MultiIndexType(array_types, names_typ)
    kgydx__fwdr = f'from_product_multiindex{numba.core.ir_utils.next_label()}'
    setattr(types, kgydx__fwdr, nvo__cqrfn)
    toxf__mcs = f"""
def impl(iterables, sortorder=None, names=None):
    with numba.objmode(mi='{kgydx__fwdr}'):
        mi = pd.MultiIndex.from_product(iterables, names=names)
    return mi
"""
    unhw__mclrv = {}
    exec(toxf__mcs, globals(), unhw__mclrv)
    kjdtr__hjfcp = unhw__mclrv['impl']
    return kjdtr__hjfcp


@intrinsic
def init_multi_index(typingctx, data, names, name=None):
    name = types.none if name is None else name
    names = types.Tuple(names.types)

    def codegen(context, builder, signature, args):
        gukl__xcl, xsn__fzotu, bak__utr = args
        ekmqj__gze = cgutils.create_struct_proxy(signature.return_type)(context
            , builder)
        ekmqj__gze.data = gukl__xcl
        ekmqj__gze.names = xsn__fzotu
        ekmqj__gze.name = bak__utr
        context.nrt.incref(builder, signature.args[0], gukl__xcl)
        context.nrt.incref(builder, signature.args[1], xsn__fzotu)
        context.nrt.incref(builder, signature.args[2], bak__utr)
        return ekmqj__gze._getvalue()
    hvdc__yoff = MultiIndexType(data.types, names.types, name)
    return hvdc__yoff(data, names, name), codegen


@overload(len, no_unliteral=True)
def overload_len_pd_multiindex(A):
    if isinstance(A, MultiIndexType):
        return lambda A: len(A._data[0])


@overload(operator.getitem, no_unliteral=True)
def overload_multi_index_getitem(I, ind):
    if not isinstance(I, MultiIndexType):
        return
    if not isinstance(ind, types.Integer):
        ooaag__eczzo = len(I.array_types)
        toxf__mcs = 'def impl(I, ind):\n'
        toxf__mcs += '  data = I._data\n'
        toxf__mcs += ('  return init_multi_index(({},), I._names, I._name)\n'
            .format(', '.join(
            f'ensure_contig_if_np(data[{fccjs__jbx}][ind])' for fccjs__jbx in
            range(ooaag__eczzo))))
        unhw__mclrv = {}
        exec(toxf__mcs, {'init_multi_index': init_multi_index,
            'ensure_contig_if_np': ensure_contig_if_np}, unhw__mclrv)
        kjdtr__hjfcp = unhw__mclrv['impl']
        return kjdtr__hjfcp


@lower_builtin(operator.is_, MultiIndexType, MultiIndexType)
def multi_index_is(context, builder, sig, args):
    jyk__eexge, sst__jpu = sig.args
    if jyk__eexge != sst__jpu:
        return cgutils.false_bit

    def index_is_impl(a, b):
        return (a._data is b._data and a._names is b._names and a._name is
            b._name)
    return context.compile_internal(builder, index_is_impl, sig, args)
