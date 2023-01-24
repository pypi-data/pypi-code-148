"""typing for rolling window functions
"""
from numba.core import cgutils, types
from numba.core.imputils import impl_ret_borrowed
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, signature
from numba.extending import infer, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_method, register_model
import bodo
from bodo.hiframes.datetime_timedelta_ext import datetime_timedelta_type, pd_timedelta_type
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.hiframes.pd_groupby_ext import DataFrameGroupByType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.rolling import supported_rolling_funcs, unsupported_rolling_methods
from bodo.utils.typing import BodoError, check_unsupported_args, create_unsupported_overload, get_literal_value, is_const_func_type, is_literal_type, is_overload_bool, is_overload_constant_str, is_overload_int, is_overload_none, raise_bodo_error


class RollingType(types.Type):

    def __init__(self, obj_type, window_type, on, selection,
        explicit_select=False, series_select=False):
        if isinstance(obj_type, bodo.SeriesType):
            jbuia__qzjr = 'Series'
        else:
            jbuia__qzjr = 'DataFrame'
        bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(obj_type,
            f'{jbuia__qzjr}.rolling()')
        self.obj_type = obj_type
        self.window_type = window_type
        self.on = on
        self.selection = selection
        self.explicit_select = explicit_select
        self.series_select = series_select
        super(RollingType, self).__init__(name=
            f'RollingType({obj_type}, {window_type}, {on}, {selection}, {explicit_select}, {series_select})'
            )

    def copy(self):
        return RollingType(self.obj_type, self.window_type, self.on, self.
            selection, self.explicit_select, self.series_select)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(RollingType)
class RollingModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ntaqt__cnc = [('obj', fe_type.obj_type), ('window', fe_type.
            window_type), ('min_periods', types.int64), ('center', types.bool_)
            ]
        super(RollingModel, self).__init__(dmm, fe_type, ntaqt__cnc)


make_attribute_wrapper(RollingType, 'obj', 'obj')
make_attribute_wrapper(RollingType, 'window', 'window')
make_attribute_wrapper(RollingType, 'center', 'center')
make_attribute_wrapper(RollingType, 'min_periods', 'min_periods')


@overload_method(DataFrameType, 'rolling', inline='always', no_unliteral=True)
def df_rolling_overload(df, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    check_runtime_cols_unsupported(df, 'DataFrame.rolling()')
    cqgg__hcm = dict(win_type=win_type, axis=axis, closed=closed)
    aje__egwq = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('DataFrame.rolling', cqgg__hcm, aje__egwq,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(df, window, min_periods, center, on)

    def impl(df, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(df, window,
            min_periods, center, on)
    return impl


@overload_method(SeriesType, 'rolling', inline='always', no_unliteral=True)
def overload_series_rolling(S, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None):
    cqgg__hcm = dict(win_type=win_type, axis=axis, closed=closed)
    aje__egwq = dict(win_type=None, axis=0, closed=None)
    check_unsupported_args('Series.rolling', cqgg__hcm, aje__egwq,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(S, window, min_periods, center, on)

    def impl(S, window, min_periods=None, center=False, win_type=None, on=
        None, axis=0, closed=None):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(S, window,
            min_periods, center, on)
    return impl


@intrinsic
def init_rolling(typingctx, obj_type, window_type, min_periods_type,
    center_type, on_type=None):

    def codegen(context, builder, signature, args):
        knl__ybjyo, ehp__kcr, thfwr__wisyk, osv__mfrw, czdp__inehg = args
        ekgq__psju = signature.return_type
        kzbth__stm = cgutils.create_struct_proxy(ekgq__psju)(context, builder)
        kzbth__stm.obj = knl__ybjyo
        kzbth__stm.window = ehp__kcr
        kzbth__stm.min_periods = thfwr__wisyk
        kzbth__stm.center = osv__mfrw
        context.nrt.incref(builder, signature.args[0], knl__ybjyo)
        context.nrt.incref(builder, signature.args[1], ehp__kcr)
        context.nrt.incref(builder, signature.args[2], thfwr__wisyk)
        context.nrt.incref(builder, signature.args[3], osv__mfrw)
        return kzbth__stm._getvalue()
    on = get_literal_value(on_type)
    if isinstance(obj_type, SeriesType):
        selection = None
    elif isinstance(obj_type, DataFrameType):
        selection = obj_type.columns
    else:
        assert isinstance(obj_type, DataFrameGroupByType
            ), f'invalid obj type for rolling: {obj_type}'
        selection = obj_type.selection
    ekgq__psju = RollingType(obj_type, window_type, on, selection, False)
    return ekgq__psju(obj_type, window_type, min_periods_type, center_type,
        on_type), codegen


def _handle_default_min_periods(min_periods, window):
    return min_periods


@overload(_handle_default_min_periods)
def overload_handle_default_min_periods(min_periods, window):
    if is_overload_none(min_periods):
        if isinstance(window, types.Integer):
            return lambda min_periods, window: window
        else:
            return lambda min_periods, window: 1
    else:
        return lambda min_periods, window: min_periods


def _gen_df_rolling_out_data(rolling):
    gmnm__cwjx = not isinstance(rolling.window_type, types.Integer)
    wpnuk__ipffw = 'variable' if gmnm__cwjx else 'fixed'
    exz__dzypc = 'None'
    if gmnm__cwjx:
        exz__dzypc = ('bodo.utils.conversion.index_to_array(index)' if 
            rolling.on is None else
            f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {rolling.obj_type.columns.index(rolling.on)})'
            )
    gmpt__ptnis = []
    lebv__vbxbc = 'on_arr, ' if gmnm__cwjx else ''
    if isinstance(rolling.obj_type, SeriesType):
        return (
            f'bodo.hiframes.rolling.rolling_{wpnuk__ipffw}(bodo.hiframes.pd_series_ext.get_series_data(df), {lebv__vbxbc}index_arr, window, minp, center, func, raw)'
            , exz__dzypc, rolling.selection)
    assert isinstance(rolling.obj_type, DataFrameType
        ), 'expected df in rolling obj'
    bpuui__yezk = rolling.obj_type.data
    out_cols = []
    for vza__gxqsm in rolling.selection:
        soxjw__teasz = rolling.obj_type.columns.index(vza__gxqsm)
        if vza__gxqsm == rolling.on:
            if len(rolling.selection) == 2 and rolling.series_select:
                continue
            pkv__wuze = (
                f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {soxjw__teasz})'
                )
            out_cols.append(vza__gxqsm)
        else:
            if not isinstance(bpuui__yezk[soxjw__teasz].dtype, (types.
                Boolean, types.Number)):
                continue
            pkv__wuze = (
                f'bodo.hiframes.rolling.rolling_{wpnuk__ipffw}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {soxjw__teasz}), {lebv__vbxbc}index_arr, window, minp, center, func, raw)'
                )
            out_cols.append(vza__gxqsm)
        gmpt__ptnis.append(pkv__wuze)
    return ', '.join(gmpt__ptnis), exz__dzypc, tuple(out_cols)


@overload_method(RollingType, 'apply', inline='always', no_unliteral=True)
def overload_rolling_apply(rolling, func, raw=False, engine=None,
    engine_kwargs=None, args=None, kwargs=None):
    cqgg__hcm = dict(engine=engine, engine_kwargs=engine_kwargs, args=args,
        kwargs=kwargs)
    aje__egwq = dict(engine=None, engine_kwargs=None, args=None, kwargs=None)
    check_unsupported_args('Rolling.apply', cqgg__hcm, aje__egwq,
        package_name='pandas', module_name='Window')
    if not is_const_func_type(func):
        raise BodoError(
            f"Rolling.apply(): 'func' parameter must be a function, not {func} (builtin functions not supported yet)."
            )
    if not is_overload_bool(raw):
        raise BodoError(
            f"Rolling.apply(): 'raw' parameter must be bool, not {raw}.")
    return _gen_rolling_impl(rolling, 'apply')


@overload_method(DataFrameGroupByType, 'rolling', inline='always',
    no_unliteral=True)
def groupby_rolling_overload(grp, window, min_periods=None, center=False,
    win_type=None, on=None, axis=0, closed=None, method='single'):
    cqgg__hcm = dict(win_type=win_type, axis=axis, closed=closed, method=method
        )
    aje__egwq = dict(win_type=None, axis=0, closed=None, method='single')
    check_unsupported_args('GroupBy.rolling', cqgg__hcm, aje__egwq,
        package_name='pandas', module_name='Window')
    _validate_rolling_args(grp, window, min_periods, center, on)

    def _impl(grp, window, min_periods=None, center=False, win_type=None,
        on=None, axis=0, closed=None, method='single'):
        min_periods = _handle_default_min_periods(min_periods, window)
        return bodo.hiframes.pd_rolling_ext.init_rolling(grp, window,
            min_periods, center, on)
    return _impl


def _gen_rolling_impl(rolling, fname, other=None):
    if isinstance(rolling.obj_type, DataFrameGroupByType):
        qypu__avsd = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
        tpw__fji = f"'{rolling.on}'" if isinstance(rolling.on, str
            ) else f'{rolling.on}'
        selection = ''
        if rolling.explicit_select:
            selection = '[{}]'.format(', '.join(f"'{ryv__qnndp}'" if
                isinstance(ryv__qnndp, str) else f'{ryv__qnndp}' for
                ryv__qnndp in rolling.selection if ryv__qnndp != rolling.on))
        zau__vvs = bpcyg__pieja = ''
        if fname == 'apply':
            zau__vvs = 'func, raw, args, kwargs'
            bpcyg__pieja = 'func, raw, None, None, args, kwargs'
        if fname == 'corr':
            zau__vvs = bpcyg__pieja = 'other, pairwise'
        if fname == 'cov':
            zau__vvs = bpcyg__pieja = 'other, pairwise, ddof'
        lys__czdg = (
            f'lambda df, window, minp, center, {zau__vvs}: bodo.hiframes.pd_rolling_ext.init_rolling(df, window, minp, center, {tpw__fji}){selection}.{fname}({bpcyg__pieja})'
            )
        qypu__avsd += f"""  return rolling.obj.apply({lys__czdg}, rolling.window, rolling.min_periods, rolling.center, {zau__vvs})
"""
        iua__xka = {}
        exec(qypu__avsd, {'bodo': bodo}, iua__xka)
        impl = iua__xka['impl']
        return impl
    wkhg__egqu = isinstance(rolling.obj_type, SeriesType)
    if fname in ('corr', 'cov'):
        out_cols = None if wkhg__egqu else _get_corr_cov_out_cols(rolling,
            other, fname)
        df_cols = None if wkhg__egqu else rolling.obj_type.columns
        other_cols = None if wkhg__egqu else other.columns
        gmpt__ptnis, exz__dzypc = _gen_corr_cov_out_data(out_cols, df_cols,
            other_cols, rolling.window_type, fname)
    else:
        gmpt__ptnis, exz__dzypc, out_cols = _gen_df_rolling_out_data(rolling)
    wehar__cxh = wkhg__egqu or len(rolling.selection) == (1 if rolling.on is
        None else 2) and rolling.series_select
    joyi__abnpw = f'def impl(rolling, {_get_rolling_func_args(fname)}):\n'
    joyi__abnpw += '  df = rolling.obj\n'
    joyi__abnpw += '  index = {}\n'.format(
        'bodo.hiframes.pd_series_ext.get_series_index(df)' if wkhg__egqu else
        'bodo.hiframes.pd_dataframe_ext.get_dataframe_index(df)')
    jbuia__qzjr = 'None'
    if wkhg__egqu:
        jbuia__qzjr = 'bodo.hiframes.pd_series_ext.get_series_name(df)'
    elif wehar__cxh:
        vza__gxqsm = (set(out_cols) - set([rolling.on])).pop()
        jbuia__qzjr = f"'{vza__gxqsm}'" if isinstance(vza__gxqsm, str
            ) else str(vza__gxqsm)
    joyi__abnpw += f'  name = {jbuia__qzjr}\n'
    joyi__abnpw += '  window = rolling.window\n'
    joyi__abnpw += '  center = rolling.center\n'
    joyi__abnpw += '  minp = rolling.min_periods\n'
    joyi__abnpw += f'  on_arr = {exz__dzypc}\n'
    if fname == 'apply':
        joyi__abnpw += (
            f'  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    else:
        joyi__abnpw += f"  func = '{fname}'\n"
        joyi__abnpw += f'  index_arr = None\n'
        joyi__abnpw += f'  raw = False\n'
    if wehar__cxh:
        joyi__abnpw += (
            f'  return bodo.hiframes.pd_series_ext.init_series({gmpt__ptnis}, index, name)'
            )
        iua__xka = {}
        qni__umbxh = {'bodo': bodo}
        exec(joyi__abnpw, qni__umbxh, iua__xka)
        impl = iua__xka['impl']
        return impl
    return bodo.hiframes.dataframe_impl._gen_init_df(joyi__abnpw, out_cols,
        gmpt__ptnis)


def _get_rolling_func_args(fname):
    if fname == 'apply':
        return (
            'func, raw=False, engine=None, engine_kwargs=None, args=None, kwargs=None\n'
            )
    elif fname == 'corr':
        return 'other=None, pairwise=None, ddof=1\n'
    elif fname == 'cov':
        return 'other=None, pairwise=None, ddof=1\n'
    return ''


def create_rolling_overload(fname):

    def overload_rolling_func(rolling):
        return _gen_rolling_impl(rolling, fname)
    return overload_rolling_func


def _install_rolling_methods():
    for fname in supported_rolling_funcs:
        if fname in ('apply', 'corr', 'cov'):
            continue
        fxu__txlss = create_rolling_overload(fname)
        overload_method(RollingType, fname, inline='always', no_unliteral=True
            )(fxu__txlss)


def _install_rolling_unsupported_methods():
    for fname in unsupported_rolling_methods:
        overload_method(RollingType, fname, no_unliteral=True)(
            create_unsupported_overload(
            f'pandas.core.window.rolling.Rolling.{fname}()'))


_install_rolling_methods()
_install_rolling_unsupported_methods()


def _get_corr_cov_out_cols(rolling, other, func_name):
    if not isinstance(other, DataFrameType):
        raise_bodo_error(
            f"DataFrame.rolling.{func_name}(): requires providing a DataFrame for 'other'"
            )
    xegd__ejgu = rolling.selection
    if rolling.on is not None:
        raise BodoError(
            f'variable window rolling {func_name} not supported yet.')
    out_cols = tuple(sorted(set(xegd__ejgu) | set(other.columns), key=lambda
        k: str(k)))
    return out_cols


def _gen_corr_cov_out_data(out_cols, df_cols, other_cols, window_type,
    func_name):
    gmnm__cwjx = not isinstance(window_type, types.Integer)
    exz__dzypc = 'None'
    if gmnm__cwjx:
        exz__dzypc = 'bodo.utils.conversion.index_to_array(index)'
    lebv__vbxbc = 'on_arr, ' if gmnm__cwjx else ''
    gmpt__ptnis = []
    if out_cols is None:
        return (
            f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_series_ext.get_series_data(df), bodo.hiframes.pd_series_ext.get_series_data(other), {lebv__vbxbc}window, minp, center)'
            , exz__dzypc)
    for vza__gxqsm in out_cols:
        if vza__gxqsm in df_cols and vza__gxqsm in other_cols:
            pghy__rvq = df_cols.index(vza__gxqsm)
            pmht__sbzhy = other_cols.index(vza__gxqsm)
            pkv__wuze = (
                f'bodo.hiframes.rolling.rolling_{func_name}(bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {pghy__rvq}), bodo.hiframes.pd_dataframe_ext.get_dataframe_data(other, {pmht__sbzhy}), {lebv__vbxbc}window, minp, center)'
                )
        else:
            pkv__wuze = 'np.full(len(df), np.nan)'
        gmpt__ptnis.append(pkv__wuze)
    return ', '.join(gmpt__ptnis), exz__dzypc


@overload_method(RollingType, 'corr', inline='always', no_unliteral=True)
def overload_rolling_corr(rolling, other=None, pairwise=None, ddof=1):
    ckdh__dktz = {'pairwise': pairwise, 'ddof': ddof}
    kugk__ejs = {'pairwise': None, 'ddof': 1}
    check_unsupported_args('pandas.core.window.rolling.Rolling.corr',
        ckdh__dktz, kugk__ejs, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'corr', other)


@overload_method(RollingType, 'cov', inline='always', no_unliteral=True)
def overload_rolling_cov(rolling, other=None, pairwise=None, ddof=1):
    ckdh__dktz = {'ddof': ddof, 'pairwise': pairwise}
    kugk__ejs = {'ddof': 1, 'pairwise': None}
    check_unsupported_args('pandas.core.window.rolling.Rolling.cov',
        ckdh__dktz, kugk__ejs, package_name='pandas', module_name='Window')
    return _gen_rolling_impl(rolling, 'cov', other)


@infer
class GetItemDataFrameRolling2(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        rolling, shzf__iito = args
        if isinstance(rolling, RollingType):
            xegd__ejgu = rolling.obj_type.selection if isinstance(rolling.
                obj_type, DataFrameGroupByType) else rolling.obj_type.columns
            series_select = False
            if isinstance(shzf__iito, (tuple, list)):
                if len(set(shzf__iito).difference(set(xegd__ejgu))) > 0:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(set(shzf__iito).difference(set(xegd__ejgu))))
                selection = list(shzf__iito)
            else:
                if shzf__iito not in xegd__ejgu:
                    raise_bodo_error(
                        'rolling: selected column {} not found in dataframe'
                        .format(shzf__iito))
                selection = [shzf__iito]
                series_select = True
            if rolling.on is not None:
                selection.append(rolling.on)
            vnpd__jnor = RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, tuple(selection), True, series_select)
            return signature(vnpd__jnor, *args)


@lower_builtin('static_getitem', RollingType, types.Any)
def static_getitem_df_groupby(context, builder, sig, args):
    return impl_ret_borrowed(context, builder, sig.return_type, args[0])


@infer_getattr
class RollingAttribute(AttributeTemplate):
    key = RollingType

    def generic_resolve(self, rolling, attr):
        xegd__ejgu = ()
        if isinstance(rolling.obj_type, DataFrameGroupByType):
            xegd__ejgu = rolling.obj_type.selection
        if isinstance(rolling.obj_type, DataFrameType):
            xegd__ejgu = rolling.obj_type.columns
        if attr in xegd__ejgu:
            return RollingType(rolling.obj_type, rolling.window_type,
                rolling.on, (attr,) if rolling.on is None else (attr,
                rolling.on), True, True)


def _validate_rolling_args(obj, window, min_periods, center, on):
    assert isinstance(obj, (SeriesType, DataFrameType, DataFrameGroupByType)
        ), 'invalid rolling obj'
    func_name = 'Series' if isinstance(obj, SeriesType
        ) else 'DataFrame' if isinstance(obj, DataFrameType
        ) else 'DataFrameGroupBy'
    if not (is_overload_int(window) or is_overload_constant_str(window) or 
        window == bodo.string_type or window in (pd_timedelta_type,
        datetime_timedelta_type)):
        raise BodoError(
            f"{func_name}.rolling(): 'window' should be int or time offset (str, pd.Timedelta, datetime.timedelta), not {window}"
            )
    if not is_overload_bool(center):
        raise BodoError(
            f'{func_name}.rolling(): center must be a boolean, not {center}')
    if not (is_overload_none(min_periods) or isinstance(min_periods, types.
        Integer)):
        raise BodoError(
            f'{func_name}.rolling(): min_periods must be an integer, not {min_periods}'
            )
    if isinstance(obj, SeriesType) and not is_overload_none(on):
        raise BodoError(
            f"{func_name}.rolling(): 'on' not supported for Series yet (can use a DataFrame instead)."
            )
    yxa__nsrpr = obj.columns if isinstance(obj, DataFrameType
        ) else obj.df_type.columns if isinstance(obj, DataFrameGroupByType
        ) else []
    bpuui__yezk = [obj.data] if isinstance(obj, SeriesType
        ) else obj.data if isinstance(obj, DataFrameType) else obj.df_type.data
    if not is_overload_none(on) and (not is_literal_type(on) or 
        get_literal_value(on) not in yxa__nsrpr):
        raise BodoError(
            f"{func_name}.rolling(): 'on' should be a constant column name.")
    if not is_overload_none(on):
        gxsz__mtivp = bpuui__yezk[yxa__nsrpr.index(get_literal_value(on))]
        if not isinstance(gxsz__mtivp, types.Array
            ) or gxsz__mtivp.dtype != bodo.datetime64ns:
            raise BodoError(
                f"{func_name}.rolling(): 'on' column should have datetime64 data."
                )
    if not any(isinstance(qfo__ghsp.dtype, (types.Boolean, types.Number)) for
        qfo__ghsp in bpuui__yezk):
        raise BodoError(f'{func_name}.rolling(): No numeric types to aggregate'
            )
