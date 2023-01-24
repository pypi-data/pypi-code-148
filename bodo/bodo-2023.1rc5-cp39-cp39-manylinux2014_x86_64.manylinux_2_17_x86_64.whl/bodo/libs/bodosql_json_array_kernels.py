"""
Implements BodoSQL array kernels related to JSON utilities
"""
import numba
from numba.core import types
import bodo
from bodo.libs.bodosql_array_kernel_utils import *


@numba.generated_jit(nopython=True)
def parse_json(arg):
    if isinstance(arg, types.optional):
        return bodo.libs.bodosql_array_kernel_utils.unopt_argument(
            'bodo.libs.bodosql_array_kernels.parse_json', ['arg'], 0)

    def impl(arg):
        return parse_json_util(arg)
    return impl


@numba.generated_jit(nopython=True)
def parse_single_json_map(s):

    def impl(s):
        ycijv__xlwc = 1
        zgnor__gaicj = {}
        tsw__gine = ['{']
        prihb__esj = ''
        wfwgb__wcwoi = ''
        lsn__msx = False
        for iztjs__qgzom in s:
            if ycijv__xlwc == 1:
                if iztjs__qgzom.isspace():
                    continue
                elif iztjs__qgzom == '{':
                    ycijv__xlwc = 2
                else:
                    return None
            elif ycijv__xlwc == 2:
                if iztjs__qgzom.isspace():
                    continue
                elif iztjs__qgzom == '"':
                    ycijv__xlwc = 3
                elif iztjs__qgzom == '}':
                    ycijv__xlwc = 9
                else:
                    return None
            elif ycijv__xlwc == 3:
                if lsn__msx:
                    prihb__esj += iztjs__qgzom
                    lsn__msx = False
                elif iztjs__qgzom == '"':
                    ycijv__xlwc = 4
                elif iztjs__qgzom == '\\':
                    lsn__msx = True
                else:
                    prihb__esj += iztjs__qgzom
            elif ycijv__xlwc == 4:
                if iztjs__qgzom.isspace():
                    continue
                elif iztjs__qgzom == ':':
                    ycijv__xlwc = 5
                else:
                    return None
            elif ycijv__xlwc == 5:
                if iztjs__qgzom.isspace():
                    continue
                if iztjs__qgzom in '},]':
                    return None
                else:
                    ycijv__xlwc = 7 if iztjs__qgzom == '"' else 6
                    wfwgb__wcwoi += iztjs__qgzom
                    if iztjs__qgzom in '{[':
                        tsw__gine.append(iztjs__qgzom)
            elif ycijv__xlwc == 6:
                if iztjs__qgzom.isspace():
                    continue
                if iztjs__qgzom in '{[':
                    wfwgb__wcwoi += iztjs__qgzom
                    tsw__gine.append(iztjs__qgzom)
                elif iztjs__qgzom in '}]':
                    ztinh__nbldv = '{' if iztjs__qgzom == '}' else '['
                    if len(tsw__gine) == 0 or tsw__gine[-1] != ztinh__nbldv:
                        return None
                    elif len(tsw__gine) == 1:
                        zgnor__gaicj[prihb__esj] = wfwgb__wcwoi
                        prihb__esj = ''
                        wfwgb__wcwoi = ''
                        tsw__gine.pop()
                        ycijv__xlwc = 9
                    elif len(tsw__gine) == 2:
                        wfwgb__wcwoi += iztjs__qgzom
                        zgnor__gaicj[prihb__esj] = wfwgb__wcwoi
                        prihb__esj = ''
                        wfwgb__wcwoi = ''
                        tsw__gine.pop()
                        ycijv__xlwc = 8
                    else:
                        wfwgb__wcwoi += iztjs__qgzom
                        tsw__gine.pop()
                elif iztjs__qgzom == '"':
                    wfwgb__wcwoi += iztjs__qgzom
                    ycijv__xlwc = 7
                elif iztjs__qgzom == ',':
                    if len(tsw__gine) == 1:
                        zgnor__gaicj[prihb__esj] = wfwgb__wcwoi
                        prihb__esj = ''
                        wfwgb__wcwoi = ''
                        ycijv__xlwc = 2
                    else:
                        wfwgb__wcwoi += iztjs__qgzom
                else:
                    wfwgb__wcwoi += iztjs__qgzom
            elif ycijv__xlwc == 7:
                if lsn__msx:
                    wfwgb__wcwoi += iztjs__qgzom
                    lsn__msx = False
                elif iztjs__qgzom == '\\':
                    lsn__msx = True
                elif iztjs__qgzom == '"':
                    wfwgb__wcwoi += iztjs__qgzom
                    ycijv__xlwc = 6
                else:
                    wfwgb__wcwoi += iztjs__qgzom
            elif ycijv__xlwc == 8:
                if iztjs__qgzom.isspace():
                    continue
                elif iztjs__qgzom == ',':
                    ycijv__xlwc = 2
                elif iztjs__qgzom == '}':
                    ycijv__xlwc = 9
                else:
                    return None
            elif ycijv__xlwc == 9:
                if not iztjs__qgzom.isspace():
                    return None
        return zgnor__gaicj if ycijv__xlwc == 9 else None
    return impl


@numba.generated_jit(nopython=True)
def parse_json_util(arr):
    bodo.libs.bodosql_array_kernels.verify_string_arg(arr, 'PARSE_JSON', 's')
    ipkh__xmlhf = ['arr']
    rdv__gzrtm = [arr]
    xokdn__klr = [False]
    gaw__qpu = """jmap = bodo.libs.bodosql_json_array_kernels.parse_single_json_map(arg0) if arg0 is not None else None
"""
    if bodo.utils.utils.is_array_typ(arr, True):
        znj__meug = (
            'lengths = bodo.utils.utils.alloc_type(n, bodo.int32, (-1,))\n')
        gaw__qpu += 'res.append(jmap)\n'
        gaw__qpu += 'if jmap is None:\n'
        gaw__qpu += '   lengths[i] = 0\n'
        gaw__qpu += 'else:\n'
        gaw__qpu += '   lengths[i] = len(jmap)\n'
    else:
        znj__meug = None
        gaw__qpu += 'return jmap'
    elteb__mgb = (
        'res2 = bodo.libs.map_arr_ext.pre_alloc_map_array(n, lengths, out_dtype)\n'
        )
    elteb__mgb += 'numba.parfors.parfor.init_prange()\n'
    elteb__mgb += 'for i in numba.parfors.parfor.internal_prange(n):\n'
    elteb__mgb += '   if res[i] is None:\n'
    elteb__mgb += '     bodo.libs.array_kernels.setna(res2, i)\n'
    elteb__mgb += '   else:\n'
    elteb__mgb += '     res2[i] = res[i]\n'
    elteb__mgb += 'res = res2\n'
    uwfii__rfr = bodo.StructArrayType((bodo.string_array_type, bodo.
        string_array_type), ('key', 'value'))
    mcri__rwc = bodo.utils.typing.to_nullable_type(uwfii__rfr)
    return gen_vectorized(ipkh__xmlhf, rdv__gzrtm, xokdn__klr, gaw__qpu,
        mcri__rwc, prefix_code=znj__meug, suffix_code=elteb__mgb, res_list=
        True, support_dict_encoding=False)
