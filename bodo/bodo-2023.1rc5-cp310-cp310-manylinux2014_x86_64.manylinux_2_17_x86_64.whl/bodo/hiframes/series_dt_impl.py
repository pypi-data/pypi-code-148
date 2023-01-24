"""
Support for Series.dt attributes and methods
"""
import datetime
import operator
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_series_ext import SeriesType, get_series_data, get_series_index, get_series_name, init_series
from bodo.libs.pd_datetime_arr_ext import PandasDatetimeTZDtype
from bodo.utils.typing import BodoError, ColNamesMetaType, check_unsupported_args, create_unsupported_overload, raise_bodo_error
dt64_dtype = np.dtype('datetime64[ns]')
timedelta64_dtype = np.dtype('timedelta64[ns]')


class SeriesDatetimePropertiesType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        otmrw__zoi = 'SeriesDatetimePropertiesType({})'.format(stype)
        super(SeriesDatetimePropertiesType, self).__init__(otmrw__zoi)


@register_model(SeriesDatetimePropertiesType)
class SeriesDtModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        ago__lhjv = [('obj', fe_type.stype)]
        super(SeriesDtModel, self).__init__(dmm, fe_type, ago__lhjv)


make_attribute_wrapper(SeriesDatetimePropertiesType, 'obj', '_obj')


@intrinsic
def init_series_dt_properties(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        eqvmu__ieqx, = args
        fcg__fstxc = signature.return_type
        wvo__tmugh = cgutils.create_struct_proxy(fcg__fstxc)(context, builder)
        wvo__tmugh.obj = eqvmu__ieqx
        context.nrt.incref(builder, signature.args[0], eqvmu__ieqx)
        return wvo__tmugh._getvalue()
    return SeriesDatetimePropertiesType(obj)(obj), codegen


@overload_attribute(SeriesType, 'dt')
def overload_series_dt(s):
    if not (bodo.hiframes.pd_series_ext.is_dt64_series_typ(s) or bodo.
        hiframes.pd_series_ext.is_timedelta64_series_typ(s)):
        raise_bodo_error('Can only use .dt accessor with datetimelike values.')
    return lambda s: bodo.hiframes.series_dt_impl.init_series_dt_properties(s)


def create_date_field_overload(field):

    def overload_field(S_dt):
        if S_dt.stype.dtype != types.NPDatetime('ns') and not isinstance(S_dt
            .stype.dtype, PandasDatetimeTZDtype):
            return
        oxle__eqzfh = isinstance(S_dt.stype.dtype, PandasDatetimeTZDtype)
        fjii__tat = ['year', 'quarter', 'month', 'week', 'day', 'hour',
            'minute', 'second', 'microsecond']
        if field not in fjii__tat:
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
                f'Series.dt.{field}')
        ezv__kaqzk = 'def impl(S_dt):\n'
        ezv__kaqzk += '    S = S_dt._obj\n'
        ezv__kaqzk += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ezv__kaqzk += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ezv__kaqzk += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        ezv__kaqzk += '    numba.parfors.parfor.init_prange()\n'
        ezv__kaqzk += '    n = len(arr)\n'
        if field in ('is_leap_year', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end', 'is_year_start',
            'is_year_end'):
            ezv__kaqzk += '    out_arr = np.empty(n, np.bool_)\n'
        else:
            ezv__kaqzk += (
                '    out_arr = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n'
                )
        ezv__kaqzk += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        ezv__kaqzk += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        ezv__kaqzk += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        ezv__kaqzk += '            continue\n'
        if not oxle__eqzfh:
            ezv__kaqzk += (
                '        dt64 = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(arr[i])\n'
                )
            ezv__kaqzk += """        ts = bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp(dt64)
"""
            if field == 'weekday':
                ezv__kaqzk += '        out_arr[i] = ts.weekday()\n'
            else:
                ezv__kaqzk += '        out_arr[i] = ts.' + field + '\n'
        else:
            ezv__kaqzk += '        out_arr[i] = arr[i].{}\n'.format(field)
        ezv__kaqzk += (
            '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
            )
        plyax__skj = {}
        exec(ezv__kaqzk, {'bodo': bodo, 'numba': numba, 'np': np}, plyax__skj)
        impl = plyax__skj['impl']
        return impl
    return overload_field


def _install_date_fields():
    for field in bodo.hiframes.pd_timestamp_ext.date_fields:
        ofiv__qhq = create_date_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(ofiv__qhq)


_install_date_fields()


def create_date_method_overload(method):
    eaof__latrs = method in ['day_name', 'month_name']
    if eaof__latrs:
        ezv__kaqzk = 'def overload_method(S_dt, locale=None):\n'
        ezv__kaqzk += '    unsupported_args = dict(locale=locale)\n'
        ezv__kaqzk += '    arg_defaults = dict(locale=None)\n'
        ezv__kaqzk += '    bodo.utils.typing.check_unsupported_args(\n'
        ezv__kaqzk += f"        'Series.dt.{method}',\n"
        ezv__kaqzk += '        unsupported_args,\n'
        ezv__kaqzk += '        arg_defaults,\n'
        ezv__kaqzk += "        package_name='pandas',\n"
        ezv__kaqzk += "        module_name='Series',\n"
        ezv__kaqzk += '    )\n'
    else:
        ezv__kaqzk = 'def overload_method(S_dt):\n'
        ezv__kaqzk += f"""    bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt, 'Series.dt.{method}()')
"""
    ezv__kaqzk += """    if not (S_dt.stype.dtype == bodo.datetime64ns or isinstance(S_dt.stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
"""
    ezv__kaqzk += '        return\n'
    if eaof__latrs:
        ezv__kaqzk += '    def impl(S_dt, locale=None):\n'
    else:
        ezv__kaqzk += '    def impl(S_dt):\n'
    ezv__kaqzk += '        S = S_dt._obj\n'
    ezv__kaqzk += (
        '        arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    ezv__kaqzk += (
        '        index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    ezv__kaqzk += (
        '        name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    ezv__kaqzk += '        numba.parfors.parfor.init_prange()\n'
    ezv__kaqzk += '        n = len(arr)\n'
    if eaof__latrs:
        ezv__kaqzk += """        out_arr = bodo.utils.utils.alloc_type(n, bodo.string_array_type, (-1,))
"""
    else:
        ezv__kaqzk += (
            "        out_arr = np.empty(n, np.dtype('datetime64[ns]'))\n")
    ezv__kaqzk += '        for i in numba.parfors.parfor.internal_prange(n):\n'
    ezv__kaqzk += '            if bodo.libs.array_kernels.isna(arr, i):\n'
    ezv__kaqzk += '                bodo.libs.array_kernels.setna(out_arr, i)\n'
    ezv__kaqzk += '                continue\n'
    ezv__kaqzk += (
        '            ts = bodo.utils.conversion.box_if_dt64(arr[i])\n')
    ezv__kaqzk += f'            method_val = ts.{method}()\n'
    if eaof__latrs:
        ezv__kaqzk += '            out_arr[i] = method_val\n'
    else:
        ezv__kaqzk += """            out_arr[i] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(method_val.value)
"""
    ezv__kaqzk += (
        '        return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    ezv__kaqzk += '    return impl\n'
    plyax__skj = {}
    exec(ezv__kaqzk, {'bodo': bodo, 'numba': numba, 'np': np}, plyax__skj)
    overload_method = plyax__skj['overload_method']
    return overload_method


def _install_date_methods():
    for method in bodo.hiframes.pd_timestamp_ext.date_methods:
        ofiv__qhq = create_date_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            ofiv__qhq)


_install_date_methods()


@overload_attribute(SeriesDatetimePropertiesType, 'date')
def series_dt_date_overload(S_dt):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return

    def impl(S_dt):
        clod__lhj = S_dt._obj
        xeglq__wiwi = bodo.hiframes.pd_series_ext.get_series_data(clod__lhj)
        lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(clod__lhj)
        otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(clod__lhj)
        numba.parfors.parfor.init_prange()
        juwh__epp = len(xeglq__wiwi)
        xra__fcp = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
            juwh__epp)
        for vmglf__hylkl in numba.parfors.parfor.internal_prange(juwh__epp):
            jqg__omkd = xeglq__wiwi[vmglf__hylkl]
            yiyt__tqwxd = bodo.utils.conversion.box_if_dt64(jqg__omkd)
            xra__fcp[vmglf__hylkl] = datetime.date(yiyt__tqwxd.year,
                yiyt__tqwxd.month, yiyt__tqwxd.day)
        return bodo.hiframes.pd_series_ext.init_series(xra__fcp, lqgv__fqhg,
            otmrw__zoi)
    return impl


def create_series_dt_df_output_overload(attr):

    def series_dt_df_output_overload(S_dt):
        if not (attr == 'components' and S_dt.stype.dtype == types.
            NPTimedelta('ns') or attr == 'isocalendar' and (S_dt.stype.
            dtype == types.NPDatetime('ns') or isinstance(S_dt.stype.dtype,
            PandasDatetimeTZDtype))):
            return
        oxle__eqzfh = isinstance(S_dt.stype.dtype, PandasDatetimeTZDtype)
        if attr != 'isocalendar':
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(S_dt,
                f'Series.dt.{attr}')
        if attr == 'components':
            ipm__wspdk = ['days', 'hours', 'minutes', 'seconds',
                'milliseconds', 'microseconds', 'nanoseconds']
            yuegk__ixtvw = 'convert_numpy_timedelta64_to_pd_timedelta'
            oeg__vehe = 'np.empty(n, np.int64)'
            pkm__acarf = attr
        elif attr == 'isocalendar':
            ipm__wspdk = ['year', 'week', 'day']
            if oxle__eqzfh:
                yuegk__ixtvw = None
            else:
                yuegk__ixtvw = 'convert_datetime64_to_timestamp'
            oeg__vehe = 'bodo.libs.int_arr_ext.alloc_int_array(n, np.uint32)'
            pkm__acarf = attr + '()'
        ezv__kaqzk = 'def impl(S_dt):\n'
        ezv__kaqzk += '    S = S_dt._obj\n'
        ezv__kaqzk += (
            '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ezv__kaqzk += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ezv__kaqzk += '    numba.parfors.parfor.init_prange()\n'
        ezv__kaqzk += '    n = len(arr)\n'
        for field in ipm__wspdk:
            ezv__kaqzk += '    {} = {}\n'.format(field, oeg__vehe)
        ezv__kaqzk += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        ezv__kaqzk += '        if bodo.libs.array_kernels.isna(arr, i):\n'
        for field in ipm__wspdk:
            ezv__kaqzk += ('            bodo.libs.array_kernels.setna({}, i)\n'
                .format(field))
        ezv__kaqzk += '            continue\n'
        qqat__empxa = '(' + '[i], '.join(ipm__wspdk) + '[i])'
        if yuegk__ixtvw:
            gds__hgy = f'bodo.hiframes.pd_timestamp_ext.{yuegk__ixtvw}(arr[i])'
        else:
            gds__hgy = 'arr[i]'
        ezv__kaqzk += f'        {qqat__empxa} = {gds__hgy}.{pkm__acarf}\n'
        odf__oqkb = '(' + ', '.join(ipm__wspdk) + ')'
        ezv__kaqzk += (
            """    return bodo.hiframes.pd_dataframe_ext.init_dataframe({}, index, __col_name_meta_value_series_dt_df_output)
"""
            .format(odf__oqkb))
        plyax__skj = {}
        exec(ezv__kaqzk, {'bodo': bodo, 'numba': numba, 'np': np,
            '__col_name_meta_value_series_dt_df_output': ColNamesMetaType(
            tuple(ipm__wspdk))}, plyax__skj)
        impl = plyax__skj['impl']
        return impl
    return series_dt_df_output_overload


def _install_df_output_overload():
    vmx__dbds = [('components', overload_attribute), ('isocalendar',
        overload_method)]
    for attr, szxvm__bopkm in vmx__dbds:
        ofiv__qhq = create_series_dt_df_output_overload(attr)
        szxvm__bopkm(SeriesDatetimePropertiesType, attr, inline='always')(
            ofiv__qhq)


_install_df_output_overload()


def create_timedelta_field_overload(field):

    def overload_field(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        ezv__kaqzk = 'def impl(S_dt):\n'
        ezv__kaqzk += '    S = S_dt._obj\n'
        ezv__kaqzk += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ezv__kaqzk += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ezv__kaqzk += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        ezv__kaqzk += '    numba.parfors.parfor.init_prange()\n'
        ezv__kaqzk += '    n = len(A)\n'
        ezv__kaqzk += (
            '    B = bodo.libs.int_arr_ext.alloc_int_array(n, np.int64)\n')
        ezv__kaqzk += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        ezv__kaqzk += '        if bodo.libs.array_kernels.isna(A, i):\n'
        ezv__kaqzk += '            bodo.libs.array_kernels.setna(B, i)\n'
        ezv__kaqzk += '            continue\n'
        ezv__kaqzk += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if field == 'nanoseconds':
            ezv__kaqzk += '        B[i] = td64 % 1000\n'
        elif field == 'microseconds':
            ezv__kaqzk += '        B[i] = td64 // 1000 % 1000000\n'
        elif field == 'seconds':
            ezv__kaqzk += (
                '        B[i] = td64 // (1000 * 1000000) % (60 * 60 * 24)\n')
        elif field == 'days':
            ezv__kaqzk += (
                '        B[i] = td64 // (1000 * 1000000 * 60 * 60 * 24)\n')
        else:
            assert False, 'invalid timedelta field'
        ezv__kaqzk += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        plyax__skj = {}
        exec(ezv__kaqzk, {'numba': numba, 'np': np, 'bodo': bodo}, plyax__skj)
        impl = plyax__skj['impl']
        return impl
    return overload_field


def create_timedelta_method_overload(method):

    def overload_method(S_dt):
        if not S_dt.stype.dtype == types.NPTimedelta('ns'):
            return
        ezv__kaqzk = 'def impl(S_dt):\n'
        ezv__kaqzk += '    S = S_dt._obj\n'
        ezv__kaqzk += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ezv__kaqzk += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ezv__kaqzk += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        ezv__kaqzk += '    numba.parfors.parfor.init_prange()\n'
        ezv__kaqzk += '    n = len(A)\n'
        if method == 'total_seconds':
            ezv__kaqzk += '    B = np.empty(n, np.float64)\n'
        else:
            ezv__kaqzk += """    B = bodo.hiframes.datetime_timedelta_ext.alloc_datetime_timedelta_array(n)
"""
        ezv__kaqzk += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        ezv__kaqzk += '        if bodo.libs.array_kernels.isna(A, i):\n'
        ezv__kaqzk += '            bodo.libs.array_kernels.setna(B, i)\n'
        ezv__kaqzk += '            continue\n'
        ezv__kaqzk += """        td64 = bodo.hiframes.pd_timestamp_ext.timedelta64_to_integer(A[i])
"""
        if method == 'total_seconds':
            ezv__kaqzk += '        B[i] = td64 / (1000.0 * 1000000.0)\n'
        elif method == 'to_pytimedelta':
            ezv__kaqzk += (
                '        B[i] = datetime.timedelta(microseconds=td64 // 1000)\n'
                )
        else:
            assert False, 'invalid timedelta method'
        if method == 'total_seconds':
            ezv__kaqzk += (
                '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
                )
        else:
            ezv__kaqzk += '    return B\n'
        plyax__skj = {}
        exec(ezv__kaqzk, {'numba': numba, 'np': np, 'bodo': bodo,
            'datetime': datetime}, plyax__skj)
        impl = plyax__skj['impl']
        return impl
    return overload_method


def _install_S_dt_timedelta_fields():
    for field in bodo.hiframes.pd_timestamp_ext.timedelta_fields:
        ofiv__qhq = create_timedelta_field_overload(field)
        overload_attribute(SeriesDatetimePropertiesType, field)(ofiv__qhq)


_install_S_dt_timedelta_fields()


def _install_S_dt_timedelta_methods():
    for method in bodo.hiframes.pd_timestamp_ext.timedelta_methods:
        ofiv__qhq = create_timedelta_method_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            ofiv__qhq)


_install_S_dt_timedelta_methods()


@overload_method(SeriesDatetimePropertiesType, 'strftime', inline='always',
    no_unliteral=True)
def dt_strftime(S_dt, date_format):
    if not (S_dt.stype.dtype == types.NPDatetime('ns') or isinstance(S_dt.
        stype.dtype, bodo.libs.pd_datetime_arr_ext.PandasDatetimeTZDtype)):
        return
    if types.unliteral(date_format) != types.unicode_type:
        raise BodoError(
            "Series.str.strftime(): 'date_format' argument must be a string")

    def impl(S_dt, date_format):
        clod__lhj = S_dt._obj
        qkot__qvw = bodo.hiframes.pd_series_ext.get_series_data(clod__lhj)
        lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(clod__lhj)
        otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(clod__lhj)
        numba.parfors.parfor.init_prange()
        juwh__epp = len(qkot__qvw)
        ppynq__yya = bodo.libs.str_arr_ext.pre_alloc_string_array(juwh__epp, -1
            )
        for nvapz__pelrz in numba.parfors.parfor.internal_prange(juwh__epp):
            if bodo.libs.array_kernels.isna(qkot__qvw, nvapz__pelrz):
                bodo.libs.array_kernels.setna(ppynq__yya, nvapz__pelrz)
                continue
            ppynq__yya[nvapz__pelrz] = bodo.utils.conversion.box_if_dt64(
                qkot__qvw[nvapz__pelrz]).strftime(date_format)
        return bodo.hiframes.pd_series_ext.init_series(ppynq__yya,
            lqgv__fqhg, otmrw__zoi)
    return impl


@overload_method(SeriesDatetimePropertiesType, 'tz_convert', inline=
    'always', no_unliteral=True)
def overload_dt_tz_convert(S_dt, tz):

    def impl(S_dt, tz):
        clod__lhj = S_dt._obj
        sxl__evcpi = get_series_data(clod__lhj).tz_convert(tz)
        lqgv__fqhg = get_series_index(clod__lhj)
        otmrw__zoi = get_series_name(clod__lhj)
        return init_series(sxl__evcpi, lqgv__fqhg, otmrw__zoi)
    return impl


def create_timedelta_freq_overload(method):

    def freq_overload(S_dt, freq, ambiguous='raise', nonexistent='raise'):
        if S_dt.stype.dtype != types.NPTimedelta('ns'
            ) and S_dt.stype.dtype != types.NPDatetime('ns'
            ) and not isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype):
            return
        cgm__wbnpc = isinstance(S_dt.stype.dtype, bodo.libs.
            pd_datetime_arr_ext.PandasDatetimeTZDtype)
        lfqqn__dzz = dict(ambiguous=ambiguous, nonexistent=nonexistent)
        agv__fox = dict(ambiguous='raise', nonexistent='raise')
        check_unsupported_args(f'Series.dt.{method}', lfqqn__dzz, agv__fox,
            package_name='pandas', module_name='Series')
        ezv__kaqzk = (
            "def impl(S_dt, freq, ambiguous='raise', nonexistent='raise'):\n")
        ezv__kaqzk += '    S = S_dt._obj\n'
        ezv__kaqzk += (
            '    A = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ezv__kaqzk += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ezv__kaqzk += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        ezv__kaqzk += '    numba.parfors.parfor.init_prange()\n'
        ezv__kaqzk += '    n = len(A)\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            ezv__kaqzk += "    B = np.empty(n, np.dtype('timedelta64[ns]'))\n"
        elif cgm__wbnpc:
            ezv__kaqzk += """    B = bodo.libs.pd_datetime_arr_ext.alloc_pd_datetime_array(n, tz_literal)
"""
        else:
            ezv__kaqzk += "    B = np.empty(n, np.dtype('datetime64[ns]'))\n"
        ezv__kaqzk += '    for i in numba.parfors.parfor.internal_prange(n):\n'
        ezv__kaqzk += '        if bodo.libs.array_kernels.isna(A, i):\n'
        ezv__kaqzk += '            bodo.libs.array_kernels.setna(B, i)\n'
        ezv__kaqzk += '            continue\n'
        if S_dt.stype.dtype == types.NPTimedelta('ns'):
            xzn__pnhj = (
                'bodo.hiframes.pd_timestamp_ext.convert_numpy_timedelta64_to_pd_timedelta'
                )
            frcpo__pxp = (
                'bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64')
        else:
            xzn__pnhj = (
                'bodo.hiframes.pd_timestamp_ext.convert_datetime64_to_timestamp'
                )
            frcpo__pxp = 'bodo.hiframes.pd_timestamp_ext.integer_to_dt64'
        if cgm__wbnpc:
            ezv__kaqzk += f'        B[i] = A[i].{method}(freq)\n'
        else:
            ezv__kaqzk += ('        B[i] = {}({}(A[i]).{}(freq).value)\n'.
                format(frcpo__pxp, xzn__pnhj, method))
        ezv__kaqzk += (
            '    return bodo.hiframes.pd_series_ext.init_series(B, index, name)\n'
            )
        plyax__skj = {}
        gevz__xsrn = None
        if cgm__wbnpc:
            gevz__xsrn = S_dt.stype.dtype.tz
        exec(ezv__kaqzk, {'numba': numba, 'np': np, 'bodo': bodo,
            'tz_literal': gevz__xsrn}, plyax__skj)
        impl = plyax__skj['impl']
        return impl
    return freq_overload


def _install_S_dt_timedelta_freq_methods():
    wxdb__ylup = ['ceil', 'floor', 'round']
    for method in wxdb__ylup:
        ofiv__qhq = create_timedelta_freq_overload(method)
        overload_method(SeriesDatetimePropertiesType, method, inline='always')(
            ofiv__qhq)


_install_S_dt_timedelta_freq_methods()


def create_bin_op_overload(op):

    def overload_series_dt_binop(lhs, rhs):
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs):
            bxd__rqhoy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                ddwab__tyot = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                qpa__yji = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    ddwab__tyot)
                lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                uwz__gnz = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                lpbcm__uwqsb = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    uwz__gnz)
                juwh__epp = len(qpa__yji)
                clod__lhj = np.empty(juwh__epp, timedelta64_dtype)
                kzix__rmeky = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bxd__rqhoy)
                for vmglf__hylkl in numba.parfors.parfor.internal_prange(
                    juwh__epp):
                    oelo__fvnyt = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(qpa__yji[vmglf__hylkl]))
                    umvk__hvkk = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(lpbcm__uwqsb[vmglf__hylkl]))
                    if oelo__fvnyt == kzix__rmeky or umvk__hvkk == kzix__rmeky:
                        gptfn__wkvct = kzix__rmeky
                    else:
                        gptfn__wkvct = op(oelo__fvnyt, umvk__hvkk)
                    clod__lhj[vmglf__hylkl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        gptfn__wkvct)
                return bodo.hiframes.pd_series_ext.init_series(clod__lhj,
                    lqgv__fqhg, otmrw__zoi)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs):
            bxd__rqhoy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tyrar__vsb = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                xeglq__wiwi = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tyrar__vsb)
                lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                lpbcm__uwqsb = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                juwh__epp = len(xeglq__wiwi)
                clod__lhj = np.empty(juwh__epp, dt64_dtype)
                kzix__rmeky = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bxd__rqhoy)
                for vmglf__hylkl in numba.parfors.parfor.internal_prange(
                    juwh__epp):
                    pcam__xjx = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        xeglq__wiwi[vmglf__hylkl])
                    tsx__aooz = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(lpbcm__uwqsb[vmglf__hylkl]))
                    if pcam__xjx == kzix__rmeky or tsx__aooz == kzix__rmeky:
                        gptfn__wkvct = kzix__rmeky
                    else:
                        gptfn__wkvct = op(pcam__xjx, tsx__aooz)
                    clod__lhj[vmglf__hylkl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        gptfn__wkvct)
                return bodo.hiframes.pd_series_ext.init_series(clod__lhj,
                    lqgv__fqhg, otmrw__zoi)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs):
            bxd__rqhoy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tyrar__vsb = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                xeglq__wiwi = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tyrar__vsb)
                lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                lpbcm__uwqsb = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                juwh__epp = len(xeglq__wiwi)
                clod__lhj = np.empty(juwh__epp, dt64_dtype)
                kzix__rmeky = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bxd__rqhoy)
                for vmglf__hylkl in numba.parfors.parfor.internal_prange(
                    juwh__epp):
                    pcam__xjx = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        xeglq__wiwi[vmglf__hylkl])
                    tsx__aooz = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(lpbcm__uwqsb[vmglf__hylkl]))
                    if pcam__xjx == kzix__rmeky or tsx__aooz == kzix__rmeky:
                        gptfn__wkvct = kzix__rmeky
                    else:
                        gptfn__wkvct = op(pcam__xjx, tsx__aooz)
                    clod__lhj[vmglf__hylkl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        gptfn__wkvct)
                return bodo.hiframes.pd_series_ext.init_series(clod__lhj,
                    lqgv__fqhg, otmrw__zoi)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            bxd__rqhoy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tyrar__vsb = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                xeglq__wiwi = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tyrar__vsb)
                lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                juwh__epp = len(xeglq__wiwi)
                clod__lhj = np.empty(juwh__epp, timedelta64_dtype)
                kzix__rmeky = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bxd__rqhoy)
                siaog__flwvo = rhs.value
                for vmglf__hylkl in numba.parfors.parfor.internal_prange(
                    juwh__epp):
                    pcam__xjx = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        xeglq__wiwi[vmglf__hylkl])
                    if pcam__xjx == kzix__rmeky or siaog__flwvo == kzix__rmeky:
                        gptfn__wkvct = kzix__rmeky
                    else:
                        gptfn__wkvct = op(pcam__xjx, siaog__flwvo)
                    clod__lhj[vmglf__hylkl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        gptfn__wkvct)
                return bodo.hiframes.pd_series_ext.init_series(clod__lhj,
                    lqgv__fqhg, otmrw__zoi)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs
            ) and lhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            bxd__rqhoy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tyrar__vsb = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                xeglq__wiwi = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tyrar__vsb)
                lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                juwh__epp = len(xeglq__wiwi)
                clod__lhj = np.empty(juwh__epp, timedelta64_dtype)
                kzix__rmeky = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bxd__rqhoy)
                siaog__flwvo = lhs.value
                for vmglf__hylkl in numba.parfors.parfor.internal_prange(
                    juwh__epp):
                    pcam__xjx = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        xeglq__wiwi[vmglf__hylkl])
                    if siaog__flwvo == kzix__rmeky or pcam__xjx == kzix__rmeky:
                        gptfn__wkvct = kzix__rmeky
                    else:
                        gptfn__wkvct = op(siaog__flwvo, pcam__xjx)
                    clod__lhj[vmglf__hylkl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        gptfn__wkvct)
                return bodo.hiframes.pd_series_ext.init_series(clod__lhj,
                    lqgv__fqhg, otmrw__zoi)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            bxd__rqhoy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tyrar__vsb = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                xeglq__wiwi = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tyrar__vsb)
                lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                juwh__epp = len(xeglq__wiwi)
                clod__lhj = np.empty(juwh__epp, dt64_dtype)
                kzix__rmeky = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bxd__rqhoy)
                zpuo__kejz = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                tsx__aooz = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(zpuo__kejz))
                for vmglf__hylkl in numba.parfors.parfor.internal_prange(
                    juwh__epp):
                    pcam__xjx = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        xeglq__wiwi[vmglf__hylkl])
                    if pcam__xjx == kzix__rmeky or tsx__aooz == kzix__rmeky:
                        gptfn__wkvct = kzix__rmeky
                    else:
                        gptfn__wkvct = op(pcam__xjx, tsx__aooz)
                    clod__lhj[vmglf__hylkl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        gptfn__wkvct)
                return bodo.hiframes.pd_series_ext.init_series(clod__lhj,
                    lqgv__fqhg, otmrw__zoi)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type):
            bxd__rqhoy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tyrar__vsb = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                xeglq__wiwi = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tyrar__vsb)
                lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                juwh__epp = len(xeglq__wiwi)
                clod__lhj = np.empty(juwh__epp, dt64_dtype)
                kzix__rmeky = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bxd__rqhoy)
                zpuo__kejz = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                tsx__aooz = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(zpuo__kejz))
                for vmglf__hylkl in numba.parfors.parfor.internal_prange(
                    juwh__epp):
                    pcam__xjx = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                        xeglq__wiwi[vmglf__hylkl])
                    if pcam__xjx == kzix__rmeky or tsx__aooz == kzix__rmeky:
                        gptfn__wkvct = kzix__rmeky
                    else:
                        gptfn__wkvct = op(pcam__xjx, tsx__aooz)
                    clod__lhj[vmglf__hylkl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                        gptfn__wkvct)
                return bodo.hiframes.pd_series_ext.init_series(clod__lhj,
                    lqgv__fqhg, otmrw__zoi)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and rhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            bxd__rqhoy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tyrar__vsb = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                xeglq__wiwi = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tyrar__vsb)
                lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                juwh__epp = len(xeglq__wiwi)
                clod__lhj = np.empty(juwh__epp, timedelta64_dtype)
                kzix__rmeky = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bxd__rqhoy)
                hldfl__eiits = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(rhs))
                pcam__xjx = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hldfl__eiits)
                for vmglf__hylkl in numba.parfors.parfor.internal_prange(
                    juwh__epp):
                    elkd__vrve = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(xeglq__wiwi[vmglf__hylkl]))
                    if elkd__vrve == kzix__rmeky or pcam__xjx == kzix__rmeky:
                        gptfn__wkvct = kzix__rmeky
                    else:
                        gptfn__wkvct = op(elkd__vrve, pcam__xjx)
                    clod__lhj[vmglf__hylkl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        gptfn__wkvct)
                return bodo.hiframes.pd_series_ext.init_series(clod__lhj,
                    lqgv__fqhg, otmrw__zoi)
            return impl
        if (bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and lhs ==
            bodo.hiframes.datetime_datetime_ext.datetime_datetime_type):
            bxd__rqhoy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tyrar__vsb = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                xeglq__wiwi = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tyrar__vsb)
                lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                juwh__epp = len(xeglq__wiwi)
                clod__lhj = np.empty(juwh__epp, timedelta64_dtype)
                kzix__rmeky = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bxd__rqhoy)
                hldfl__eiits = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(lhs))
                pcam__xjx = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    hldfl__eiits)
                for vmglf__hylkl in numba.parfors.parfor.internal_prange(
                    juwh__epp):
                    elkd__vrve = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(xeglq__wiwi[vmglf__hylkl]))
                    if pcam__xjx == kzix__rmeky or elkd__vrve == kzix__rmeky:
                        gptfn__wkvct = kzix__rmeky
                    else:
                        gptfn__wkvct = op(pcam__xjx, elkd__vrve)
                    clod__lhj[vmglf__hylkl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        gptfn__wkvct)
                return bodo.hiframes.pd_series_ext.init_series(clod__lhj,
                    lqgv__fqhg, otmrw__zoi)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            bxd__rqhoy = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                xeglq__wiwi = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                juwh__epp = len(xeglq__wiwi)
                clod__lhj = np.empty(juwh__epp, timedelta64_dtype)
                kzix__rmeky = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(bxd__rqhoy))
                zpuo__kejz = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                tsx__aooz = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(zpuo__kejz))
                for vmglf__hylkl in numba.parfors.parfor.internal_prange(
                    juwh__epp):
                    ibsw__kji = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(xeglq__wiwi[vmglf__hylkl]))
                    if tsx__aooz == kzix__rmeky or ibsw__kji == kzix__rmeky:
                        gptfn__wkvct = kzix__rmeky
                    else:
                        gptfn__wkvct = op(ibsw__kji, tsx__aooz)
                    clod__lhj[vmglf__hylkl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        gptfn__wkvct)
                return bodo.hiframes.pd_series_ext.init_series(clod__lhj,
                    lqgv__fqhg, otmrw__zoi)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            bxd__rqhoy = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                xeglq__wiwi = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                juwh__epp = len(xeglq__wiwi)
                clod__lhj = np.empty(juwh__epp, timedelta64_dtype)
                kzix__rmeky = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(bxd__rqhoy))
                zpuo__kejz = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                tsx__aooz = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(zpuo__kejz))
                for vmglf__hylkl in numba.parfors.parfor.internal_prange(
                    juwh__epp):
                    ibsw__kji = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(xeglq__wiwi[vmglf__hylkl]))
                    if tsx__aooz == kzix__rmeky or ibsw__kji == kzix__rmeky:
                        gptfn__wkvct = kzix__rmeky
                    else:
                        gptfn__wkvct = op(tsx__aooz, ibsw__kji)
                    clod__lhj[vmglf__hylkl
                        ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                        gptfn__wkvct)
                return bodo.hiframes.pd_series_ext.init_series(clod__lhj,
                    lqgv__fqhg, otmrw__zoi)
            return impl
        raise BodoError(f'{op} not supported for data types {lhs} and {rhs}.')
    return overload_series_dt_binop


def create_cmp_op_overload(op):

    def overload_series_dt64_cmp(lhs, rhs):
        if op == operator.ne:
            jlbjk__fvlpl = True
        else:
            jlbjk__fvlpl = False
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(lhs) and 
            rhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            bxd__rqhoy = lhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                xeglq__wiwi = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                juwh__epp = len(xeglq__wiwi)
                xra__fcp = bodo.libs.bool_arr_ext.alloc_bool_array(juwh__epp)
                kzix__rmeky = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(bxd__rqhoy))
                ynkrp__xgeaz = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(rhs))
                jwrax__oeeoc = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(ynkrp__xgeaz))
                for vmglf__hylkl in numba.parfors.parfor.internal_prange(
                    juwh__epp):
                    oewi__vlywu = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(xeglq__wiwi[vmglf__hylkl]))
                    if (oewi__vlywu == kzix__rmeky or jwrax__oeeoc ==
                        kzix__rmeky):
                        gptfn__wkvct = jlbjk__fvlpl
                    else:
                        gptfn__wkvct = op(oewi__vlywu, jwrax__oeeoc)
                    xra__fcp[vmglf__hylkl] = gptfn__wkvct
                return bodo.hiframes.pd_series_ext.init_series(xra__fcp,
                    lqgv__fqhg, otmrw__zoi)
            return impl
        if (bodo.hiframes.pd_series_ext.is_timedelta64_series_typ(rhs) and 
            lhs == bodo.hiframes.datetime_timedelta_ext.datetime_timedelta_type
            ):
            bxd__rqhoy = rhs.dtype('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                xeglq__wiwi = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                juwh__epp = len(xeglq__wiwi)
                xra__fcp = bodo.libs.bool_arr_ext.alloc_bool_array(juwh__epp)
                kzix__rmeky = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(bxd__rqhoy))
                uerho__tdlzc = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(lhs))
                oewi__vlywu = (bodo.hiframes.pd_timestamp_ext.
                    timedelta64_to_integer(uerho__tdlzc))
                for vmglf__hylkl in numba.parfors.parfor.internal_prange(
                    juwh__epp):
                    jwrax__oeeoc = (bodo.hiframes.pd_timestamp_ext.
                        timedelta64_to_integer(xeglq__wiwi[vmglf__hylkl]))
                    if (oewi__vlywu == kzix__rmeky or jwrax__oeeoc ==
                        kzix__rmeky):
                        gptfn__wkvct = jlbjk__fvlpl
                    else:
                        gptfn__wkvct = op(oewi__vlywu, jwrax__oeeoc)
                    xra__fcp[vmglf__hylkl] = gptfn__wkvct
                return bodo.hiframes.pd_series_ext.init_series(xra__fcp,
                    lqgv__fqhg, otmrw__zoi)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs
            ) and rhs == bodo.hiframes.pd_timestamp_ext.pd_timestamp_tz_naive_type:
            bxd__rqhoy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tyrar__vsb = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                xeglq__wiwi = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tyrar__vsb)
                lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                juwh__epp = len(xeglq__wiwi)
                xra__fcp = bodo.libs.bool_arr_ext.alloc_bool_array(juwh__epp)
                kzix__rmeky = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bxd__rqhoy)
                for vmglf__hylkl in numba.parfors.parfor.internal_prange(
                    juwh__epp):
                    oewi__vlywu = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(xeglq__wiwi[vmglf__hylkl]))
                    if oewi__vlywu == kzix__rmeky or rhs.value == kzix__rmeky:
                        gptfn__wkvct = jlbjk__fvlpl
                    else:
                        gptfn__wkvct = op(oewi__vlywu, rhs.value)
                    xra__fcp[vmglf__hylkl] = gptfn__wkvct
                return bodo.hiframes.pd_series_ext.init_series(xra__fcp,
                    lqgv__fqhg, otmrw__zoi)
            return impl
        if (lhs == bodo.hiframes.pd_timestamp_ext.
            pd_timestamp_tz_naive_type and bodo.hiframes.pd_series_ext.
            is_dt64_series_typ(rhs)):
            bxd__rqhoy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                numba.parfors.parfor.init_prange()
                tyrar__vsb = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                xeglq__wiwi = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tyrar__vsb)
                lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                juwh__epp = len(xeglq__wiwi)
                xra__fcp = bodo.libs.bool_arr_ext.alloc_bool_array(juwh__epp)
                kzix__rmeky = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bxd__rqhoy)
                for vmglf__hylkl in numba.parfors.parfor.internal_prange(
                    juwh__epp):
                    jwrax__oeeoc = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(xeglq__wiwi[vmglf__hylkl]))
                    if jwrax__oeeoc == kzix__rmeky or lhs.value == kzix__rmeky:
                        gptfn__wkvct = jlbjk__fvlpl
                    else:
                        gptfn__wkvct = op(lhs.value, jwrax__oeeoc)
                    xra__fcp[vmglf__hylkl] = gptfn__wkvct
                return bodo.hiframes.pd_series_ext.init_series(xra__fcp,
                    lqgv__fqhg, otmrw__zoi)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(lhs) and (rhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(rhs)):
            bxd__rqhoy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                tyrar__vsb = bodo.hiframes.pd_series_ext.get_series_data(lhs)
                xeglq__wiwi = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tyrar__vsb)
                lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(lhs)
                otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(lhs)
                numba.parfors.parfor.init_prange()
                juwh__epp = len(xeglq__wiwi)
                xra__fcp = bodo.libs.bool_arr_ext.alloc_bool_array(juwh__epp)
                kzix__rmeky = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bxd__rqhoy)
                bbg__luntw = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    rhs)
                fghx__qxpjz = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bbg__luntw)
                for vmglf__hylkl in numba.parfors.parfor.internal_prange(
                    juwh__epp):
                    oewi__vlywu = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(xeglq__wiwi[vmglf__hylkl]))
                    if (oewi__vlywu == kzix__rmeky or fghx__qxpjz ==
                        kzix__rmeky):
                        gptfn__wkvct = jlbjk__fvlpl
                    else:
                        gptfn__wkvct = op(oewi__vlywu, fghx__qxpjz)
                    xra__fcp[vmglf__hylkl] = gptfn__wkvct
                return bodo.hiframes.pd_series_ext.init_series(xra__fcp,
                    lqgv__fqhg, otmrw__zoi)
            return impl
        if bodo.hiframes.pd_series_ext.is_dt64_series_typ(rhs) and (lhs ==
            bodo.libs.str_ext.string_type or bodo.utils.typing.
            is_overload_constant_str(lhs)):
            bxd__rqhoy = bodo.datetime64ns('NaT')

            def impl(lhs, rhs):
                tyrar__vsb = bodo.hiframes.pd_series_ext.get_series_data(rhs)
                xeglq__wiwi = bodo.libs.pd_datetime_arr_ext.unwrap_tz_array(
                    tyrar__vsb)
                lqgv__fqhg = bodo.hiframes.pd_series_ext.get_series_index(rhs)
                otmrw__zoi = bodo.hiframes.pd_series_ext.get_series_name(rhs)
                numba.parfors.parfor.init_prange()
                juwh__epp = len(xeglq__wiwi)
                xra__fcp = bodo.libs.bool_arr_ext.alloc_bool_array(juwh__epp)
                kzix__rmeky = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bxd__rqhoy)
                bbg__luntw = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(
                    lhs)
                fghx__qxpjz = bodo.hiframes.pd_timestamp_ext.dt64_to_integer(
                    bbg__luntw)
                for vmglf__hylkl in numba.parfors.parfor.internal_prange(
                    juwh__epp):
                    hldfl__eiits = (bodo.hiframes.pd_timestamp_ext.
                        dt64_to_integer(xeglq__wiwi[vmglf__hylkl]))
                    if (hldfl__eiits == kzix__rmeky or fghx__qxpjz ==
                        kzix__rmeky):
                        gptfn__wkvct = jlbjk__fvlpl
                    else:
                        gptfn__wkvct = op(fghx__qxpjz, hldfl__eiits)
                    xra__fcp[vmglf__hylkl] = gptfn__wkvct
                return bodo.hiframes.pd_series_ext.init_series(xra__fcp,
                    lqgv__fqhg, otmrw__zoi)
            return impl
        raise BodoError(
            f'{op} operator not supported for data types {lhs} and {rhs}.')
    return overload_series_dt64_cmp


series_dt_unsupported_methods = {'to_period', 'to_pydatetime',
    'tz_localize', 'asfreq', 'to_timestamp'}
series_dt_unsupported_attrs = {'time', 'timetz', 'tz', 'freq', 'qyear',
    'start_time', 'end_time'}


def _install_series_dt_unsupported():
    for aaa__txnp in series_dt_unsupported_attrs:
        epdiw__ell = 'Series.dt.' + aaa__txnp
        overload_attribute(SeriesDatetimePropertiesType, aaa__txnp)(
            create_unsupported_overload(epdiw__ell))
    for jfl__vkjq in series_dt_unsupported_methods:
        epdiw__ell = 'Series.dt.' + jfl__vkjq
        overload_method(SeriesDatetimePropertiesType, jfl__vkjq,
            no_unliteral=True)(create_unsupported_overload(epdiw__ell))


_install_series_dt_unsupported()
