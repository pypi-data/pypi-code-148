"""
transforms the IR to handle bytecode issues in Python 3.10. This
should be removed once https://github.com/numba/numba/pull/7866
is included in Numba 0.56
"""
import operator
import numba
from numba.core import ir
from numba.core.compiler_machinery import FunctionPass, register_pass
from numba.core.errors import UnsupportedError
from numba.core.ir_utils import dprint_func_ir, get_definition, guard


@register_pass(mutates_CFG=False, analysis_only=False)
class Bodo310ByteCodePass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        dprint_func_ir(state.func_ir,
            'starting Bodo 3.10 Bytecode optimizations pass')
        peep_hole_call_function_ex_to_call_function_kw(state.func_ir)
        peep_hole_fuse_dict_add_updates(state.func_ir)
        peep_hole_fuse_tuple_adds(state.func_ir)
        return True


def peep_hole_fuse_tuple_adds(func_ir):
    for rnegs__icvn in func_ir.blocks.values():
        new_body = []
        mksyr__nfj = {}
        for kaci__jxz, nbg__wggtq in enumerate(rnegs__icvn.body):
            yphlg__bgjs = None
            if isinstance(nbg__wggtq, ir.Assign) and isinstance(nbg__wggtq.
                value, ir.Expr):
                jwaxg__ryye = nbg__wggtq.target.name
                if nbg__wggtq.value.op == 'build_tuple':
                    yphlg__bgjs = jwaxg__ryye
                    mksyr__nfj[jwaxg__ryye] = nbg__wggtq.value.items
                elif nbg__wggtq.value.op == 'binop' and nbg__wggtq.value.fn == operator.add and nbg__wggtq.value.lhs.name in mksyr__nfj and nbg__wggtq.value.rhs.name in mksyr__nfj:
                    yphlg__bgjs = jwaxg__ryye
                    new_items = mksyr__nfj[nbg__wggtq.value.lhs.name
                        ] + mksyr__nfj[nbg__wggtq.value.rhs.name]
                    jxkgx__ljcq = ir.Expr.build_tuple(new_items, nbg__wggtq
                        .value.loc)
                    mksyr__nfj[jwaxg__ryye] = new_items
                    del mksyr__nfj[nbg__wggtq.value.lhs.name]
                    del mksyr__nfj[nbg__wggtq.value.rhs.name]
                    if nbg__wggtq.value in func_ir._definitions[jwaxg__ryye]:
                        func_ir._definitions[jwaxg__ryye].remove(nbg__wggtq
                            .value)
                    func_ir._definitions[jwaxg__ryye].append(jxkgx__ljcq)
                    nbg__wggtq = ir.Assign(jxkgx__ljcq, nbg__wggtq.target,
                        nbg__wggtq.loc)
            for kbxdp__cioz in nbg__wggtq.list_vars():
                if (kbxdp__cioz.name in mksyr__nfj and kbxdp__cioz.name !=
                    yphlg__bgjs):
                    del mksyr__nfj[kbxdp__cioz.name]
            new_body.append(nbg__wggtq)
        rnegs__icvn.body = new_body
    return func_ir


def _call_function_ex_replace_kws_small(keyword_expr, new_body, buildmap_idx):
    pzk__aja = keyword_expr.items.copy()
    wanux__gpkw = keyword_expr.value_indexes
    for yofxk__kwfq, xumz__jnh in wanux__gpkw.items():
        pzk__aja[xumz__jnh] = yofxk__kwfq, pzk__aja[xumz__jnh][1]
    new_body[buildmap_idx] = None
    return pzk__aja


def _call_function_ex_replace_kws_large(body, buildmap_name, buildmap_idx,
    search_end, new_body):
    nnofe__qmb = 'CALL_FUNCTION_EX with **kwargs not supported'
    new_body[buildmap_idx] = None
    pzk__aja = []
    trisr__mgvx = buildmap_idx + 1
    while trisr__mgvx <= search_end:
        ghsz__qmzsp = body[trisr__mgvx]
        if not (isinstance(ghsz__qmzsp, ir.Assign) and isinstance(
            ghsz__qmzsp.value, ir.Const)):
            raise UnsupportedError(nnofe__qmb)
        dmud__qlzjy = ghsz__qmzsp.target.name
        jpyel__rag = ghsz__qmzsp.value.value
        trisr__mgvx += 1
        iwdx__zzs = True
        while trisr__mgvx <= search_end and iwdx__zzs:
            lioxm__ntan = body[trisr__mgvx]
            if (isinstance(lioxm__ntan, ir.Assign) and isinstance(
                lioxm__ntan.value, ir.Expr) and lioxm__ntan.value.op ==
                'getattr' and lioxm__ntan.value.value.name == buildmap_name and
                lioxm__ntan.value.attr == '__setitem__'):
                iwdx__zzs = False
            else:
                trisr__mgvx += 1
        if iwdx__zzs or trisr__mgvx == search_end:
            raise UnsupportedError(nnofe__qmb)
        zsghu__rlrtp = body[trisr__mgvx + 1]
        if not (isinstance(zsghu__rlrtp, ir.Assign) and isinstance(
            zsghu__rlrtp.value, ir.Expr) and zsghu__rlrtp.value.op ==
            'call' and zsghu__rlrtp.value.func.name == lioxm__ntan.target.
            name and len(zsghu__rlrtp.value.args) == 2 and zsghu__rlrtp.
            value.args[0].name == dmud__qlzjy):
            raise UnsupportedError(nnofe__qmb)
        uen__rnp = zsghu__rlrtp.value.args[1]
        pzk__aja.append((jpyel__rag, uen__rnp))
        new_body[trisr__mgvx] = None
        new_body[trisr__mgvx + 1] = None
        trisr__mgvx += 2
    return pzk__aja


def _call_function_ex_replace_args_small(tuple_expr, new_body, buildtuple_idx):
    new_body[buildtuple_idx] = None
    return tuple_expr.items


def _call_function_ex_replace_args_large(vararg_stmt, body, new_body,
    search_end):
    nnofe__qmb = 'CALL_FUNCTION_EX with **kwargs not supported'
    trisr__mgvx = 0
    ihnb__vjzm = []
    if isinstance(vararg_stmt, ir.Assign) and isinstance(vararg_stmt.value,
        ir.Var):
        ohun__vaiw = vararg_stmt.value.name
        new_body[search_end] = None
        search_end -= 1
    else:
        ohun__vaiw = vararg_stmt.target.name
    nqc__nlnl = True
    while search_end >= trisr__mgvx and nqc__nlnl:
        jxg__bbxo = body[search_end]
        if (isinstance(jxg__bbxo, ir.Assign) and jxg__bbxo.target.name ==
            ohun__vaiw and isinstance(jxg__bbxo.value, ir.Expr) and 
            jxg__bbxo.value.op == 'build_tuple' and not jxg__bbxo.value.items):
            nqc__nlnl = False
            new_body[search_end] = None
        else:
            if search_end == trisr__mgvx or not (isinstance(jxg__bbxo, ir.
                Assign) and jxg__bbxo.target.name == ohun__vaiw and
                isinstance(jxg__bbxo.value, ir.Expr) and jxg__bbxo.value.op ==
                'binop' and jxg__bbxo.value.fn == operator.add):
                raise UnsupportedError(nnofe__qmb)
            rasna__wdgt = jxg__bbxo.value.lhs.name
            wffkn__mfqpr = jxg__bbxo.value.rhs.name
            dmrgv__mnjm = body[search_end - 1]
            if not (isinstance(dmrgv__mnjm, ir.Assign) and isinstance(
                dmrgv__mnjm.value, ir.Expr) and dmrgv__mnjm.value.op ==
                'build_tuple' and len(dmrgv__mnjm.value.items) == 1):
                raise UnsupportedError(nnofe__qmb)
            if dmrgv__mnjm.target.name == rasna__wdgt:
                ohun__vaiw = wffkn__mfqpr
            elif dmrgv__mnjm.target.name == wffkn__mfqpr:
                ohun__vaiw = rasna__wdgt
            else:
                raise UnsupportedError(nnofe__qmb)
            ihnb__vjzm.append(dmrgv__mnjm.value.items[0])
            new_body[search_end] = None
            new_body[search_end - 1] = None
            search_end -= 2
            pqz__axz = True
            while search_end >= trisr__mgvx and pqz__axz:
                foe__sfzhm = body[search_end]
                if isinstance(foe__sfzhm, ir.Assign
                    ) and foe__sfzhm.target.name == ohun__vaiw:
                    pqz__axz = False
                else:
                    search_end -= 1
    if nqc__nlnl:
        raise UnsupportedError(nnofe__qmb)
    return ihnb__vjzm[::-1]


def peep_hole_call_function_ex_to_call_function_kw(func_ir):
    nnofe__qmb = 'CALL_FUNCTION_EX with **kwargs not supported'
    for rnegs__icvn in func_ir.blocks.values():
        fpzts__mplqc = False
        new_body = []
        for kaci__jxz, nbg__wggtq in enumerate(rnegs__icvn.body):
            if (isinstance(nbg__wggtq, ir.Assign) and isinstance(nbg__wggtq
                .value, ir.Expr) and nbg__wggtq.value.op == 'call' and 
                nbg__wggtq.value.varkwarg is not None):
                fpzts__mplqc = True
                tck__szhrq = nbg__wggtq.value
                args = tck__szhrq.args
                pzk__aja = tck__szhrq.kws
                vka__qca = tck__szhrq.vararg
                anzsx__yewiz = tck__szhrq.varkwarg
                uyhmi__pwbop = kaci__jxz - 1
                fdv__ivrnb = uyhmi__pwbop
                qele__mpkwp = None
                jwva__hom = True
                while fdv__ivrnb >= 0 and jwva__hom:
                    qele__mpkwp = rnegs__icvn.body[fdv__ivrnb]
                    if isinstance(qele__mpkwp, ir.Assign
                        ) and qele__mpkwp.target.name == anzsx__yewiz.name:
                        jwva__hom = False
                    else:
                        fdv__ivrnb -= 1
                if pzk__aja or jwva__hom or not (isinstance(qele__mpkwp.
                    value, ir.Expr) and qele__mpkwp.value.op == 'build_map'):
                    raise UnsupportedError(nnofe__qmb)
                if qele__mpkwp.value.items:
                    pzk__aja = _call_function_ex_replace_kws_small(qele__mpkwp
                        .value, new_body, fdv__ivrnb)
                else:
                    pzk__aja = _call_function_ex_replace_kws_large(rnegs__icvn
                        .body, anzsx__yewiz.name, fdv__ivrnb, kaci__jxz - 1,
                        new_body)
                uyhmi__pwbop = fdv__ivrnb
                if vka__qca is not None:
                    if args:
                        raise UnsupportedError(nnofe__qmb)
                    vghbj__ntqc = uyhmi__pwbop
                    assqy__xaml = None
                    jwva__hom = True
                    while vghbj__ntqc >= 0 and jwva__hom:
                        assqy__xaml = rnegs__icvn.body[vghbj__ntqc]
                        if isinstance(assqy__xaml, ir.Assign
                            ) and assqy__xaml.target.name == vka__qca.name:
                            jwva__hom = False
                        else:
                            vghbj__ntqc -= 1
                    if jwva__hom:
                        raise UnsupportedError(nnofe__qmb)
                    if isinstance(assqy__xaml.value, ir.Expr
                        ) and assqy__xaml.value.op == 'build_tuple':
                        args = _call_function_ex_replace_args_small(assqy__xaml
                            .value, new_body, vghbj__ntqc)
                    else:
                        args = _call_function_ex_replace_args_large(assqy__xaml
                            , rnegs__icvn.body, new_body, vghbj__ntqc)
                yairh__fnuf = ir.Expr.call(tck__szhrq.func, args, pzk__aja,
                    tck__szhrq.loc, target=tck__szhrq.target)
                if nbg__wggtq.target.name in func_ir._definitions and len(
                    func_ir._definitions[nbg__wggtq.target.name]) == 1:
                    func_ir._definitions[nbg__wggtq.target.name].clear()
                func_ir._definitions[nbg__wggtq.target.name].append(yairh__fnuf
                    )
                nbg__wggtq = ir.Assign(yairh__fnuf, nbg__wggtq.target,
                    nbg__wggtq.loc)
            new_body.append(nbg__wggtq)
        if fpzts__mplqc:
            rnegs__icvn.body = [iafp__sak for iafp__sak in new_body if 
                iafp__sak is not None]
    return func_ir


def peep_hole_fuse_dict_add_updates(func_ir):
    for rnegs__icvn in func_ir.blocks.values():
        new_body = []
        lit_old_idx = {}
        lit_new_idx = {}
        map_updates = {}
        fpzts__mplqc = False
        for kaci__jxz, nbg__wggtq in enumerate(rnegs__icvn.body):
            fbh__qvoos = True
            opny__uwq = None
            if isinstance(nbg__wggtq, ir.Assign) and isinstance(nbg__wggtq.
                value, ir.Expr):
                if nbg__wggtq.value.op == 'build_map':
                    opny__uwq = nbg__wggtq.target.name
                    lit_old_idx[nbg__wggtq.target.name] = kaci__jxz
                    lit_new_idx[nbg__wggtq.target.name] = kaci__jxz
                    map_updates[nbg__wggtq.target.name
                        ] = nbg__wggtq.value.items.copy()
                    fbh__qvoos = False
                elif nbg__wggtq.value.op == 'call' and kaci__jxz > 0:
                    tugd__hwg = nbg__wggtq.value.func.name
                    lioxm__ntan = rnegs__icvn.body[kaci__jxz - 1]
                    args = nbg__wggtq.value.args
                    if (isinstance(lioxm__ntan, ir.Assign) and lioxm__ntan.
                        target.name == tugd__hwg and isinstance(lioxm__ntan
                        .value, ir.Expr) and lioxm__ntan.value.op ==
                        'getattr' and lioxm__ntan.value.value.name in
                        lit_old_idx):
                        ccsbz__boke = lioxm__ntan.value.value.name
                        oifc__ujjt = lioxm__ntan.value.attr
                        if oifc__ujjt == '__setitem__':
                            fbh__qvoos = False
                            map_updates[ccsbz__boke].append(args)
                            new_body[-1] = None
                        elif oifc__ujjt == 'update' and args[0
                            ].name in lit_old_idx:
                            fbh__qvoos = False
                            map_updates[ccsbz__boke].extend(map_updates[
                                args[0].name])
                            new_body[-1] = None
                        if not fbh__qvoos:
                            lit_new_idx[ccsbz__boke] = kaci__jxz
                            func_ir._definitions[lioxm__ntan.target.name
                                ].remove(lioxm__ntan.value)
            if not (isinstance(nbg__wggtq, ir.Assign) and isinstance(
                nbg__wggtq.value, ir.Expr) and nbg__wggtq.value.op ==
                'getattr' and nbg__wggtq.value.value.name in lit_old_idx and
                nbg__wggtq.value.attr in ('__setitem__', 'update')):
                for kbxdp__cioz in nbg__wggtq.list_vars():
                    if (kbxdp__cioz.name in lit_old_idx and kbxdp__cioz.
                        name != opny__uwq):
                        _insert_build_map(func_ir, kbxdp__cioz.name,
                            rnegs__icvn.body, new_body, lit_old_idx,
                            lit_new_idx, map_updates)
            if fbh__qvoos:
                new_body.append(nbg__wggtq)
            else:
                func_ir._definitions[nbg__wggtq.target.name].remove(nbg__wggtq
                    .value)
                fpzts__mplqc = True
                new_body.append(None)
        hdl__aok = list(lit_old_idx.keys())
        for bmrt__jcbpj in hdl__aok:
            _insert_build_map(func_ir, bmrt__jcbpj, rnegs__icvn.body,
                new_body, lit_old_idx, lit_new_idx, map_updates)
        if fpzts__mplqc:
            rnegs__icvn.body = [iafp__sak for iafp__sak in new_body if 
                iafp__sak is not None]
    return func_ir


def _insert_build_map(func_ir, name, old_body, new_body, lit_old_idx,
    lit_new_idx, map_updates):
    oms__xdrdt = lit_old_idx[name]
    cedo__rutba = lit_new_idx[name]
    skyll__gzb = map_updates[name]
    new_body[cedo__rutba] = _build_new_build_map(func_ir, name, old_body,
        oms__xdrdt, skyll__gzb)
    del lit_old_idx[name]
    del lit_new_idx[name]
    del map_updates[name]


def _build_new_build_map(func_ir, name, old_body, old_lineno, new_items):
    bxze__pkst = old_body[old_lineno]
    sxlsz__uqbgr = bxze__pkst.target
    udqxv__eku = bxze__pkst.value
    bopwx__udts = []
    eng__xusr = []
    for zixjw__hkbnp in new_items:
        litgl__cfc, pslhj__dpcf = zixjw__hkbnp
        yprf__edi = guard(get_definition, func_ir, litgl__cfc)
        if isinstance(yprf__edi, (ir.Const, ir.Global, ir.FreeVar)):
            bopwx__udts.append(yprf__edi.value)
        kjwf__gwipn = guard(get_definition, func_ir, pslhj__dpcf)
        if isinstance(kjwf__gwipn, (ir.Const, ir.Global, ir.FreeVar)):
            eng__xusr.append(kjwf__gwipn.value)
        else:
            eng__xusr.append(numba.core.interpreter._UNKNOWN_VALUE(
                pslhj__dpcf.name))
    wanux__gpkw = {}
    if len(bopwx__udts) == len(new_items):
        vnb__xqhk = {iafp__sak: caf__vfnra for iafp__sak, caf__vfnra in zip
            (bopwx__udts, eng__xusr)}
        for kaci__jxz, litgl__cfc in enumerate(bopwx__udts):
            wanux__gpkw[litgl__cfc] = kaci__jxz
    else:
        vnb__xqhk = None
    pwhzh__bhbv = ir.Expr.build_map(items=new_items, size=len(new_items),
        literal_value=vnb__xqhk, value_indexes=wanux__gpkw, loc=udqxv__eku.loc)
    func_ir._definitions[name].append(pwhzh__bhbv)
    return ir.Assign(pwhzh__bhbv, ir.Var(sxlsz__uqbgr.scope, name,
        sxlsz__uqbgr.loc), pwhzh__bhbv.loc)
