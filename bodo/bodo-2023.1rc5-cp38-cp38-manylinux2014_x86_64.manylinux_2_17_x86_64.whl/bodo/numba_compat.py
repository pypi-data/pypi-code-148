"""
Numba monkey patches to fix issues related to Bodo. Should be imported before any
other module in bodo package.
"""
import copy
import functools
import hashlib
import inspect
import itertools
import operator
import os
import re
import sys
import textwrap
import traceback
import types as pytypes
import warnings
from collections import OrderedDict
from collections.abc import Sequence
from contextlib import ExitStack
import numba
import numba.core.boxing
import numba.core.inline_closurecall
import numba.core.typing.listdecl
import numba.np.linalg
from numba.core import analysis, cgutils, errors, ir, ir_utils, types
from numba.core.compiler import Compiler
from numba.core.errors import ForceLiteralArg, LiteralTypingError, TypingError
from numba.core.ir_utils import GuardException, _create_function_from_code_obj, analysis, build_definitions, find_callname, get_definition, guard, has_no_side_effect, mk_unique_var, remove_dead_extensions, replace_vars_inner, require, visit_vars_extensions, visit_vars_inner
from numba.core.types import literal
from numba.core.types.functions import _bt_as_lines, _ResolutionFailures, _termcolor, _unlit_non_poison
from numba.core.typing.templates import AbstractTemplate, Signature, _EmptyImplementationEntry, _inline_info, _OverloadAttributeTemplate, infer_global, signature
from numba.core.typing.typeof import Purpose, typeof
from numba.experimental.jitclass import base as jitclass_base
from numba.experimental.jitclass import decorators as jitclass_decorators
from numba.extending import NativeValue, lower_builtin, typeof_impl
from numba.parfors.parfor import get_expr_args
from bodo.utils.python_310_bytecode_pass import Bodo310ByteCodePass, peep_hole_call_function_ex_to_call_function_kw, peep_hole_fuse_dict_add_updates, peep_hole_fuse_tuple_adds
from bodo.utils.typing import BodoError, get_overload_const_str, is_overload_constant_str, raise_bodo_error
_check_numba_change = False
numba.core.typing.templates._IntrinsicTemplate.prefer_literal = True


def run_frontend(func, inline_closures=False, emit_dels=False):
    from numba.core.utils import PYVERSION
    lidva__yleq = numba.core.bytecode.FunctionIdentity.from_function(func)
    qmta__kpxut = numba.core.interpreter.Interpreter(lidva__yleq)
    dofu__laaj = numba.core.bytecode.ByteCode(func_id=lidva__yleq)
    func_ir = qmta__kpxut.interpret(dofu__laaj)
    if PYVERSION == (3, 10):
        func_ir = peep_hole_call_function_ex_to_call_function_kw(func_ir)
        func_ir = peep_hole_fuse_dict_add_updates(func_ir)
        func_ir = peep_hole_fuse_tuple_adds(func_ir)
    if inline_closures:
        from numba.core.inline_closurecall import InlineClosureCallPass


        class DummyPipeline:

            def __init__(self, f_ir):
                self.state = numba.core.compiler.StateDict()
                self.state.typingctx = None
                self.state.targetctx = None
                self.state.args = None
                self.state.func_ir = f_ir
                self.state.typemap = None
                self.state.return_type = None
                self.state.calltypes = None
        numba.core.rewrites.rewrite_registry.apply('before-inference',
            DummyPipeline(func_ir).state)
        ypcjr__msf = InlineClosureCallPass(func_ir, numba.core.cpu.
            ParallelOptions(False), {}, False)
        ypcjr__msf.run()
    nob__qhih = numba.core.postproc.PostProcessor(func_ir)
    nob__qhih.run(emit_dels)
    return func_ir


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.run_frontend)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8c2477a793b2c08d56430997880974ac12c5570e69c9e54d37d694b322ea18b6':
        warnings.warn('numba.core.compiler.run_frontend has changed')
numba.core.compiler.run_frontend = run_frontend


def visit_vars_stmt(stmt, callback, cbdata):
    for t, sltmu__pph in visit_vars_extensions.items():
        if isinstance(stmt, t):
            sltmu__pph(stmt, callback, cbdata)
            return
    if isinstance(stmt, ir.Assign):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Arg):
        stmt.name = visit_vars_inner(stmt.name, callback, cbdata)
    elif isinstance(stmt, ir.Return):
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Raise):
        stmt.exception = visit_vars_inner(stmt.exception, callback, cbdata)
    elif isinstance(stmt, ir.Branch):
        stmt.cond = visit_vars_inner(stmt.cond, callback, cbdata)
    elif isinstance(stmt, ir.Jump):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
    elif isinstance(stmt, ir.Del):
        var = ir.Var(None, stmt.value, stmt.loc)
        var = visit_vars_inner(var, callback, cbdata)
        stmt.value = var.name
    elif isinstance(stmt, ir.DelAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
    elif isinstance(stmt, ir.SetAttr):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.attr = visit_vars_inner(stmt.attr, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.DelItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
    elif isinstance(stmt, ir.StaticSetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index_var = visit_vars_inner(stmt.index_var, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.SetItem):
        stmt.target = visit_vars_inner(stmt.target, callback, cbdata)
        stmt.index = visit_vars_inner(stmt.index, callback, cbdata)
        stmt.value = visit_vars_inner(stmt.value, callback, cbdata)
    elif isinstance(stmt, ir.Print):
        stmt.args = [visit_vars_inner(x, callback, cbdata) for x in stmt.args]
        stmt.vararg = visit_vars_inner(stmt.vararg, callback, cbdata)
    else:
        pass
    return


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.visit_vars_stmt)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '52b7b645ba65c35f3cf564f936e113261db16a2dff1e80fbee2459af58844117':
        warnings.warn('numba.core.ir_utils.visit_vars_stmt has changed')
numba.core.ir_utils.visit_vars_stmt = visit_vars_stmt
old_run_pass = numba.core.typed_passes.InlineOverloads.run_pass


def InlineOverloads_run_pass(self, state):
    import bodo
    bodo.compiler.bodo_overload_inline_pass(state.func_ir, state.typingctx,
        state.targetctx, state.typemap, state.calltypes)
    return old_run_pass(self, state)


numba.core.typed_passes.InlineOverloads.run_pass = InlineOverloads_run_pass
from numba.core.ir_utils import _add_alias, alias_analysis_extensions, alias_func_extensions
_immutable_type_class = (types.Number, types.scalars._NPDatetimeBase, types
    .iterators.RangeType, types.UnicodeType)


def is_immutable_type(var, typemap):
    if typemap is None or var not in typemap:
        return False
    typ = typemap[var]
    if isinstance(typ, _immutable_type_class):
        return True
    if isinstance(typ, types.BaseTuple) and all(isinstance(t,
        _immutable_type_class) for t in typ.types):
        return True
    return False


def find_potential_aliases(blocks, args, typemap, func_ir, alias_map=None,
    arg_aliases=None):
    if alias_map is None:
        alias_map = {}
    if arg_aliases is None:
        arg_aliases = set(a for a in args if not is_immutable_type(a, typemap))
    func_ir._definitions = build_definitions(func_ir.blocks)
    qev__cduus = ['ravel', 'transpose', 'reshape']
    for fykv__fliwh in blocks.values():
        for utotr__zitb in fykv__fliwh.body:
            if type(utotr__zitb) in alias_analysis_extensions:
                sltmu__pph = alias_analysis_extensions[type(utotr__zitb)]
                sltmu__pph(utotr__zitb, args, typemap, func_ir, alias_map,
                    arg_aliases)
            if isinstance(utotr__zitb, ir.Assign):
                ddt__egw = utotr__zitb.value
                dizzz__kevk = utotr__zitb.target.name
                if is_immutable_type(dizzz__kevk, typemap):
                    continue
                if isinstance(ddt__egw, ir.Var
                    ) and dizzz__kevk != ddt__egw.name:
                    _add_alias(dizzz__kevk, ddt__egw.name, alias_map,
                        arg_aliases)
                if isinstance(ddt__egw, ir.Expr) and (ddt__egw.op == 'cast' or
                    ddt__egw.op in ['getitem', 'static_getitem']):
                    _add_alias(dizzz__kevk, ddt__egw.value.name, alias_map,
                        arg_aliases)
                if isinstance(ddt__egw, ir.Expr
                    ) and ddt__egw.op == 'inplace_binop':
                    _add_alias(dizzz__kevk, ddt__egw.lhs.name, alias_map,
                        arg_aliases)
                if isinstance(ddt__egw, ir.Expr
                    ) and ddt__egw.op == 'getattr' and ddt__egw.attr in ['T',
                    'ctypes', 'flat']:
                    _add_alias(dizzz__kevk, ddt__egw.value.name, alias_map,
                        arg_aliases)
                if isinstance(ddt__egw, ir.Expr
                    ) and ddt__egw.op == 'getattr' and ddt__egw.attr not in [
                    'shape'] and ddt__egw.value.name in arg_aliases:
                    _add_alias(dizzz__kevk, ddt__egw.value.name, alias_map,
                        arg_aliases)
                if isinstance(ddt__egw, ir.Expr
                    ) and ddt__egw.op == 'getattr' and ddt__egw.attr in ('loc',
                    'iloc', 'iat', '_obj', 'obj', 'codes', '_df'):
                    _add_alias(dizzz__kevk, ddt__egw.value.name, alias_map,
                        arg_aliases)
                if isinstance(ddt__egw, ir.Expr) and ddt__egw.op in (
                    'build_tuple', 'build_list', 'build_set'
                    ) and not is_immutable_type(dizzz__kevk, typemap):
                    for gprl__aoel in ddt__egw.items:
                        _add_alias(dizzz__kevk, gprl__aoel.name, alias_map,
                            arg_aliases)
                if isinstance(ddt__egw, ir.Expr) and ddt__egw.op == 'call':
                    iofg__jtp = guard(find_callname, func_ir, ddt__egw, typemap
                        )
                    if iofg__jtp is None:
                        continue
                    xlr__uum, xaxc__vweck = iofg__jtp
                    if iofg__jtp in alias_func_extensions:
                        irqb__zikhz = alias_func_extensions[iofg__jtp]
                        irqb__zikhz(dizzz__kevk, ddt__egw.args, alias_map,
                            arg_aliases)
                    if xaxc__vweck == 'numpy' and xlr__uum in qev__cduus:
                        _add_alias(dizzz__kevk, ddt__egw.args[0].name,
                            alias_map, arg_aliases)
                    if isinstance(xaxc__vweck, ir.Var
                        ) and xlr__uum in qev__cduus:
                        _add_alias(dizzz__kevk, xaxc__vweck.name, alias_map,
                            arg_aliases)
    jpx__phvec = copy.deepcopy(alias_map)
    for gprl__aoel in jpx__phvec:
        for ubxl__fkts in jpx__phvec[gprl__aoel]:
            alias_map[gprl__aoel] |= alias_map[ubxl__fkts]
        for ubxl__fkts in jpx__phvec[gprl__aoel]:
            alias_map[ubxl__fkts] = alias_map[gprl__aoel]
    return alias_map, arg_aliases


if _check_numba_change:
    lines = inspect.getsource(ir_utils.find_potential_aliases)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'e6cf3e0f502f903453eb98346fc6854f87dc4ea1ac62f65c2d6aef3bf690b6c5':
        warnings.warn('ir_utils.find_potential_aliases has changed')
ir_utils.find_potential_aliases = find_potential_aliases
numba.parfors.array_analysis.find_potential_aliases = find_potential_aliases
if _check_numba_change:
    lines = inspect.getsource(ir_utils.dead_code_elimination)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '40a8626300a1a17523944ec7842b093c91258bbc60844bbd72191a35a4c366bf':
        warnings.warn('ir_utils.dead_code_elimination has changed')


def mini_dce(func_ir, typemap=None, alias_map=None, arg_aliases=None):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    pxp__htka = compute_cfg_from_blocks(func_ir.blocks)
    sqv__isw = compute_use_defs(func_ir.blocks)
    fqzfn__szywl = compute_live_map(pxp__htka, func_ir.blocks, sqv__isw.
        usemap, sqv__isw.defmap)
    grmya__twmm = True
    while grmya__twmm:
        grmya__twmm = False
        for label, block in func_ir.blocks.items():
            lives = {gprl__aoel.name for gprl__aoel in block.terminator.
                list_vars()}
            for tymrx__jrju, rwbdh__dqqw in pxp__htka.successors(label):
                lives |= fqzfn__szywl[tymrx__jrju]
            qwaym__qlfk = [block.terminator]
            for stmt in reversed(block.body[:-1]):
                if isinstance(stmt, ir.Assign):
                    dizzz__kevk = stmt.target
                    uqxkt__czrf = stmt.value
                    if dizzz__kevk.name not in lives:
                        if isinstance(uqxkt__czrf, ir.Expr
                            ) and uqxkt__czrf.op == 'make_function':
                            continue
                        if isinstance(uqxkt__czrf, ir.Expr
                            ) and uqxkt__czrf.op == 'getattr':
                            continue
                        if isinstance(uqxkt__czrf, ir.Const):
                            continue
                        if typemap and isinstance(typemap.get(dizzz__kevk,
                            None), types.Function):
                            continue
                        if isinstance(uqxkt__czrf, ir.Expr
                            ) and uqxkt__czrf.op == 'build_map':
                            continue
                        if isinstance(uqxkt__czrf, ir.Expr
                            ) and uqxkt__czrf.op == 'build_tuple':
                            continue
                        if isinstance(uqxkt__czrf, ir.Expr
                            ) and uqxkt__czrf.op == 'binop':
                            continue
                        if isinstance(uqxkt__czrf, ir.Expr
                            ) and uqxkt__czrf.op == 'unary':
                            continue
                        if isinstance(uqxkt__czrf, ir.Expr
                            ) and uqxkt__czrf.op in ('static_getitem',
                            'getitem'):
                            continue
                    if isinstance(uqxkt__czrf, ir.Var
                        ) and dizzz__kevk.name == uqxkt__czrf.name:
                        continue
                if isinstance(stmt, ir.Del):
                    if stmt.value not in lives:
                        continue
                if type(stmt) in analysis.ir_extension_usedefs:
                    yjo__flwiw = analysis.ir_extension_usedefs[type(stmt)]
                    oorwg__ntzmd, uxs__pwot = yjo__flwiw(stmt)
                    lives -= uxs__pwot
                    lives |= oorwg__ntzmd
                else:
                    lives |= {gprl__aoel.name for gprl__aoel in stmt.
                        list_vars()}
                    if isinstance(stmt, ir.Assign):
                        tgheg__wlh = set()
                        if isinstance(uqxkt__czrf, ir.Expr):
                            tgheg__wlh = {gprl__aoel.name for gprl__aoel in
                                uqxkt__czrf.list_vars()}
                        if dizzz__kevk.name not in tgheg__wlh:
                            lives.remove(dizzz__kevk.name)
                qwaym__qlfk.append(stmt)
            qwaym__qlfk.reverse()
            if len(block.body) != len(qwaym__qlfk):
                grmya__twmm = True
            block.body = qwaym__qlfk


ir_utils.dead_code_elimination = mini_dce
numba.core.typed_passes.dead_code_elimination = mini_dce
numba.core.inline_closurecall.dead_code_elimination = mini_dce
from numba.core.cpu_options import InlineOptions


def make_overload_template(func, overload_func, jit_options, strict, inline,
    prefer_literal=False, **kwargs):
    nja__thi = getattr(func, '__name__', str(func))
    name = 'OverloadTemplate_%s' % (nja__thi,)
    no_unliteral = kwargs.pop('no_unliteral', False)
    base = numba.core.typing.templates._OverloadFunctionTemplate
    kdord__bphcj = dict(key=func, _overload_func=staticmethod(overload_func
        ), _impl_cache={}, _compiled_overloads={}, _jit_options=jit_options,
        _strict=strict, _inline=staticmethod(InlineOptions(inline)),
        _inline_overloads={}, prefer_literal=prefer_literal, _no_unliteral=
        no_unliteral, metadata=kwargs)
    return type(base)(name, (base,), kdord__bphcj)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '7f6974584cb10e49995b652827540cc6732e497c0b9f8231b44fd83fcc1c0a83':
        warnings.warn(
            'numba.core.typing.templates.make_overload_template has changed')
numba.core.typing.templates.make_overload_template = make_overload_template


def _resolve(self, typ, attr):
    if self._attr != attr:
        return None
    if isinstance(typ, types.TypeRef):
        assert typ == self.key
    else:
        assert isinstance(typ, self.key)


    class MethodTemplate(AbstractTemplate):
        key = self.key, attr
        _inline = self._inline
        _no_unliteral = getattr(self, '_no_unliteral', False)
        _overload_func = staticmethod(self._overload_func)
        _inline_overloads = self._inline_overloads
        prefer_literal = self.prefer_literal

        def generic(_, args, kws):
            args = (typ,) + tuple(args)
            fnty = self._get_function_type(self.context, typ)
            sig = self._get_signature(self.context, fnty, args, kws)
            sig = sig.replace(pysig=numba.core.utils.pysignature(self.
                _overload_func))
            for xpsta__wju in fnty.templates:
                self._inline_overloads.update(xpsta__wju._inline_overloads)
            if sig is not None:
                return sig.as_method()
    return types.BoundFunction(MethodTemplate, typ)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadMethodTemplate._resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ce8e0935dc939d0867ef969e1ed2975adb3533a58a4133fcc90ae13c4418e4d6':
        warnings.warn(
            'numba.core.typing.templates._OverloadMethodTemplate._resolve has changed'
            )
numba.core.typing.templates._OverloadMethodTemplate._resolve = _resolve


def make_overload_attribute_template(typ, attr, overload_func, inline,
    prefer_literal=False, base=_OverloadAttributeTemplate, **kwargs):
    assert isinstance(typ, types.Type) or issubclass(typ, types.Type)
    name = 'OverloadAttributeTemplate_%s_%s' % (typ, attr)
    no_unliteral = kwargs.pop('no_unliteral', False)
    kdord__bphcj = dict(key=typ, _attr=attr, _impl_cache={}, _inline=
        staticmethod(InlineOptions(inline)), _inline_overloads={},
        _no_unliteral=no_unliteral, _overload_func=staticmethod(
        overload_func), prefer_literal=prefer_literal, metadata=kwargs)
    obj = type(base)(name, (base,), kdord__bphcj)
    return obj


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        make_overload_attribute_template)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f066c38c482d6cf8bf5735a529c3264118ba9b52264b24e58aad12a6b1960f5d':
        warnings.warn(
            'numba.core.typing.templates.make_overload_attribute_template has changed'
            )
numba.core.typing.templates.make_overload_attribute_template = (
    make_overload_attribute_template)


def generic(self, args, kws):
    from numba.core.typed_passes import PreLowerStripPhis
    zynof__ydlcs, plqwq__gax = self._get_impl(args, kws)
    if zynof__ydlcs is None:
        return
    goic__cjj = types.Dispatcher(zynof__ydlcs)
    if not self._inline.is_never_inline:
        from numba.core import compiler, typed_passes
        from numba.core.inline_closurecall import InlineWorker
        bvscc__gcjg = zynof__ydlcs._compiler
        flags = compiler.Flags()
        igit__ypqv = bvscc__gcjg.targetdescr.typing_context
        fqccp__ies = bvscc__gcjg.targetdescr.target_context
        naih__swo = bvscc__gcjg.pipeline_class(igit__ypqv, fqccp__ies, None,
            None, None, flags, None)
        miqz__dduj = InlineWorker(igit__ypqv, fqccp__ies, bvscc__gcjg.
            locals, naih__swo, flags, None)
        ycapd__ckzao = goic__cjj.dispatcher.get_call_template
        xpsta__wju, zknfj__mgbtw, xyr__awwwl, kws = ycapd__ckzao(plqwq__gax,
            kws)
        if xyr__awwwl in self._inline_overloads:
            return self._inline_overloads[xyr__awwwl]['iinfo'].signature
        ir = miqz__dduj.run_untyped_passes(goic__cjj.dispatcher.py_func,
            enable_ssa=True)
        typemap, return_type, calltypes, _ = typed_passes.type_inference_stage(
            self.context, fqccp__ies, ir, xyr__awwwl, None)
        ir = PreLowerStripPhis()._strip_phi_nodes(ir)
        ir._definitions = numba.core.ir_utils.build_definitions(ir.blocks)
        sig = Signature(return_type, xyr__awwwl, None)
        self._inline_overloads[sig.args] = {'folded_args': xyr__awwwl}
        keax__aoy = _EmptyImplementationEntry('always inlined')
        self._compiled_overloads[sig.args] = keax__aoy
        if not self._inline.is_always_inline:
            sig = goic__cjj.get_call_type(self.context, plqwq__gax, kws)
            self._compiled_overloads[sig.args] = goic__cjj.get_overload(sig)
        sssn__gqd = _inline_info(ir, typemap, calltypes, sig)
        self._inline_overloads[sig.args] = {'folded_args': xyr__awwwl,
            'iinfo': sssn__gqd}
    else:
        sig = goic__cjj.get_call_type(self.context, plqwq__gax, kws)
        if sig is None:
            return None
        self._compiled_overloads[sig.args] = goic__cjj.get_overload(sig)
    return sig


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5d453a6d0215ebf0bab1279ff59eb0040b34938623be99142ce20acc09cdeb64':
        warnings.warn(
            'numba.core.typing.templates._OverloadFunctionTemplate.generic has changed'
            )
numba.core.typing.templates._OverloadFunctionTemplate.generic = generic


def bound_function(template_key, no_unliteral=False):

    def wrapper(method_resolver):

        @functools.wraps(method_resolver)
        def attribute_resolver(self, ty):


            class MethodTemplate(AbstractTemplate):
                key = template_key

                def generic(_, args, kws):
                    sig = method_resolver(self, ty, args, kws)
                    if sig is not None and sig.recvr is None:
                        sig = sig.replace(recvr=ty)
                    return sig
            MethodTemplate._no_unliteral = no_unliteral
            return types.BoundFunction(MethodTemplate, ty)
        return attribute_resolver
    return wrapper


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.bound_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a2feefe64eae6a15c56affc47bf0c1d04461f9566913442d539452b397103322':
        warnings.warn('numba.core.typing.templates.bound_function has changed')
numba.core.typing.templates.bound_function = bound_function


def get_call_type(self, context, args, kws):
    from numba.core import utils
    ybgm__geiki = [True, False]
    xkerx__ner = [False, True]
    jcby__gwha = _ResolutionFailures(context, self, args, kws, depth=self.
        _depth)
    from numba.core.target_extension import get_local_target
    mag__ppzcx = get_local_target(context)
    hmut__ris = utils.order_by_target_specificity(mag__ppzcx, self.
        templates, fnkey=self.key[0])
    self._depth += 1
    for kkgea__xpvu in hmut__ris:
        mtv__etjrq = kkgea__xpvu(context)
        ktw__mrmk = ybgm__geiki if mtv__etjrq.prefer_literal else xkerx__ner
        ktw__mrmk = [True] if getattr(mtv__etjrq, '_no_unliteral', False
            ) else ktw__mrmk
        for dmre__svvxp in ktw__mrmk:
            try:
                if dmre__svvxp:
                    sig = mtv__etjrq.apply(args, kws)
                else:
                    bshf__ifx = tuple([_unlit_non_poison(a) for a in args])
                    ebil__yjgdi = {nvtk__ucegf: _unlit_non_poison(
                        gprl__aoel) for nvtk__ucegf, gprl__aoel in kws.items()}
                    sig = mtv__etjrq.apply(bshf__ifx, ebil__yjgdi)
            except Exception as e:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                else:
                    sig = None
                    jcby__gwha.add_error(mtv__etjrq, False, e, dmre__svvxp)
            else:
                if sig is not None:
                    self._impl_keys[sig.args] = mtv__etjrq.get_impl_key(sig)
                    self._depth -= 1
                    return sig
                else:
                    wsub__khjux = getattr(mtv__etjrq, 'cases', None)
                    if wsub__khjux is not None:
                        msg = 'No match for registered cases:\n%s'
                        msg = msg % '\n'.join(' * {}'.format(x) for x in
                            wsub__khjux)
                    else:
                        msg = 'No match.'
                    jcby__gwha.add_error(mtv__etjrq, True, msg, dmre__svvxp)
    jcby__gwha.raise_error()


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BaseFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '25f038a7216f8e6f40068ea81e11fd9af8ad25d19888f7304a549941b01b7015':
        warnings.warn(
            'numba.core.types.functions.BaseFunction.get_call_type has changed'
            )
numba.core.types.functions.BaseFunction.get_call_type = get_call_type
bodo_typing_error_info = """
This is often caused by the use of unsupported features or typing issues.
See https://docs.bodo.ai/
"""


def get_call_type2(self, context, args, kws):
    xpsta__wju = self.template(context)
    hlodm__kuarp = None
    dqupd__jsklb = None
    qkr__iewf = None
    ktw__mrmk = [True, False] if xpsta__wju.prefer_literal else [False, True]
    ktw__mrmk = [True] if getattr(xpsta__wju, '_no_unliteral', False
        ) else ktw__mrmk
    for dmre__svvxp in ktw__mrmk:
        if dmre__svvxp:
            try:
                qkr__iewf = xpsta__wju.apply(args, kws)
            except Exception as dum__clv:
                if isinstance(dum__clv, errors.ForceLiteralArg):
                    raise dum__clv
                hlodm__kuarp = dum__clv
                qkr__iewf = None
            else:
                break
        else:
            tgr__utwl = tuple([_unlit_non_poison(a) for a in args])
            cidto__mjwkf = {nvtk__ucegf: _unlit_non_poison(gprl__aoel) for 
                nvtk__ucegf, gprl__aoel in kws.items()}
            zaigk__sdsym = tgr__utwl == args and kws == cidto__mjwkf
            if not zaigk__sdsym and qkr__iewf is None:
                try:
                    qkr__iewf = xpsta__wju.apply(tgr__utwl, cidto__mjwkf)
                except Exception as dum__clv:
                    from numba.core import utils
                    if utils.use_new_style_errors() and not isinstance(dum__clv
                        , errors.NumbaError):
                        raise dum__clv
                    if isinstance(dum__clv, errors.ForceLiteralArg):
                        if xpsta__wju.prefer_literal:
                            raise dum__clv
                    dqupd__jsklb = dum__clv
                else:
                    break
    if qkr__iewf is None and (dqupd__jsklb is not None or hlodm__kuarp is not
        None):
        lagn__vfb = '- Resolution failure for {} arguments:\n{}\n'
        hmg__lrkub = _termcolor.highlight(lagn__vfb)
        if numba.core.config.DEVELOPER_MODE:
            rqnh__amr = ' ' * 4

            def add_bt(error):
                if isinstance(error, BaseException):
                    ady__haam = traceback.format_exception(type(error),
                        error, error.__traceback__)
                else:
                    ady__haam = ['']
                azjtz__pswm = '\n{}'.format(2 * rqnh__amr)
                agc__ivy = _termcolor.reset(azjtz__pswm + azjtz__pswm.join(
                    _bt_as_lines(ady__haam)))
                return _termcolor.reset(agc__ivy)
        else:
            add_bt = lambda X: ''

        def nested_msg(literalness, e):
            kmdv__iozhx = str(e)
            kmdv__iozhx = kmdv__iozhx if kmdv__iozhx else str(repr(e)
                ) + add_bt(e)
            mnbtp__qjjf = errors.TypingError(textwrap.dedent(kmdv__iozhx))
            return hmg__lrkub.format(literalness, str(mnbtp__qjjf))
        import bodo
        if isinstance(hlodm__kuarp, bodo.utils.typing.BodoError):
            raise hlodm__kuarp
        if numba.core.config.DEVELOPER_MODE:
            raise errors.TypingError(nested_msg('literal', hlodm__kuarp) +
                nested_msg('non-literal', dqupd__jsklb))
        else:
            if 'missing a required argument' in hlodm__kuarp.msg:
                msg = 'missing a required argument'
            else:
                msg = 'Compilation error for '
                if isinstance(self.this, bodo.hiframes.pd_dataframe_ext.
                    DataFrameType):
                    msg += 'DataFrame.'
                elif isinstance(self.this, bodo.hiframes.pd_series_ext.
                    SeriesType):
                    msg += 'Series.'
                msg += f'{self.typing_key[1]}().{bodo_typing_error_info}'
            raise errors.TypingError(msg, loc=hlodm__kuarp.loc)
    return qkr__iewf


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.BoundFunction.
        get_call_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '502cd77c0084452e903a45a0f1f8107550bfbde7179363b57dabd617ce135f4a':
        warnings.warn(
            'numba.core.types.functions.BoundFunction.get_call_type has changed'
            )
numba.core.types.functions.BoundFunction.get_call_type = get_call_type2


def string_from_string_and_size(self, string, size):
    from llvmlite import ir as lir
    fnty = lir.FunctionType(self.pyobj, [self.cstring, self.py_ssize_t])
    xlr__uum = 'PyUnicode_FromStringAndSize'
    fn = self._get_function(fnty, name=xlr__uum)
    return self.builder.call(fn, [string, size])


numba.core.pythonapi.PythonAPI.string_from_string_and_size = (
    string_from_string_and_size)


def _compile_for_args(self, *args, **kws):
    assert not kws
    self._compilation_chain_init_hook()
    import bodo

    def error_rewrite(e, issue_type):
        if numba.core.config.SHOW_HELP:
            raoc__llhj = errors.error_extras[issue_type]
            e.patch_message('\n'.join((str(e).rstrip(), raoc__llhj)))
        if numba.core.config.FULL_TRACEBACKS:
            raise e
        else:
            raise e.with_traceback(None)
    uodjk__tsbt = []
    for a in args:
        if isinstance(a, numba.core.dispatcher.OmittedArg):
            uodjk__tsbt.append(types.Omitted(a.value))
        else:
            uodjk__tsbt.append(self.typeof_pyval(a))
    xrg__ykmwh = None
    try:
        error = None
        xrg__ykmwh = self.compile(tuple(uodjk__tsbt))
    except errors.ForceLiteralArg as e:
        rfet__sxyw = [i for i in e.requested_args if isinstance(args[i],
            types.Literal) and not isinstance(args[i], types.LiteralStrKeyDict)
            ]
        if rfet__sxyw:
            hesq__zye = """Repeated literal typing request.
{}.
This is likely caused by an error in typing. Please see nested and suppressed exceptions."""
            zjqdc__cbx = ', '.join('Arg #{} is {}'.format(i, args[i]) for i in
                sorted(rfet__sxyw))
            raise errors.CompilerError(hesq__zye.format(zjqdc__cbx))
        plqwq__gax = []
        try:
            for i, gprl__aoel in enumerate(args):
                if i in e.requested_args:
                    if i in e.file_infos:
                        plqwq__gax.append(types.FilenameType(args[i], e.
                            file_infos[i]))
                    else:
                        plqwq__gax.append(types.literal(args[i]))
                else:
                    plqwq__gax.append(args[i])
            args = plqwq__gax
        except (OSError, FileNotFoundError) as dazn__swcs:
            error = FileNotFoundError(str(dazn__swcs) + '\n' + e.loc.
                strformat() + '\n')
        except bodo.utils.typing.BodoError as e:
            error = bodo.utils.typing.BodoError(str(e))
        if error is None:
            try:
                xrg__ykmwh = self._compile_for_args(*args)
            except TypingError as e:
                error = errors.TypingError(str(e))
            except bodo.utils.typing.BodoError as e:
                error = bodo.utils.typing.BodoError(str(e))
    except errors.TypingError as e:
        vhuc__xxyss = []
        for i, qvj__lxysa in enumerate(args):
            val = qvj__lxysa.value if isinstance(qvj__lxysa, numba.core.
                dispatcher.OmittedArg) else qvj__lxysa
            try:
                vdppk__ujs = typeof(val, Purpose.argument)
            except ValueError as rja__bmhx:
                vhuc__xxyss.append((i, str(rja__bmhx)))
            else:
                if vdppk__ujs is None:
                    vhuc__xxyss.append((i,
                        f'cannot determine Numba type of value {val}'))
        if vhuc__xxyss:
            mmibz__mel = '\n'.join(f'- argument {i}: {fcau__hods}' for i,
                fcau__hods in vhuc__xxyss)
            msg = f"""{str(e).rstrip()} 

This error may have been caused by the following argument(s):
{mmibz__mel}
"""
            e.patch_message(msg)
        if "Cannot determine Numba type of <class 'numpy.ufunc'>" in e.msg:
            msg = 'Unsupported Numpy ufunc encountered in JIT code'
            error = bodo.utils.typing.BodoError(msg, loc=e.loc)
        elif not numba.core.config.DEVELOPER_MODE:
            if bodo_typing_error_info not in e.msg:
                ufeol__nmenw = ['Failed in nopython mode pipeline',
                    'Failed in bodo mode pipeline', 'Failed at nopython',
                    'Overload', 'lowering']
                bfbo__gtsg = False
                for jwrte__rpvp in ufeol__nmenw:
                    if jwrte__rpvp in e.msg:
                        msg = 'Compilation error. '
                        msg += f'{bodo_typing_error_info}'
                        bfbo__gtsg = True
                        break
                if not bfbo__gtsg:
                    msg = f'{str(e)}'
                msg += '\n' + e.loc.strformat() + '\n'
                e.patch_message(msg)
        error_rewrite(e, 'typing')
    except errors.UnsupportedError as e:
        error_rewrite(e, 'unsupported_error')
    except (errors.NotDefinedError, errors.RedefinedError, errors.
        VerificationError) as e:
        error_rewrite(e, 'interpreter')
    except errors.ConstantInferenceError as e:
        error_rewrite(e, 'constant_inference')
    except bodo.utils.typing.BodoError as e:
        error = bodo.utils.typing.BodoError(str(e))
    except Exception as e:
        if numba.core.config.SHOW_HELP:
            if hasattr(e, 'patch_message'):
                raoc__llhj = errors.error_extras['reportable']
                e.patch_message('\n'.join((str(e).rstrip(), raoc__llhj)))
        raise e
    finally:
        self._types_active_call = []
        del args
        if error:
            raise error
    return xrg__ykmwh


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher._DispatcherBase.
        _compile_for_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5cdfbf0b13a528abf9f0408e70f67207a03e81d610c26b1acab5b2dc1f79bf06':
        warnings.warn(
            'numba.core.dispatcher._DispatcherBase._compile_for_args has changed'
            )
numba.core.dispatcher._DispatcherBase._compile_for_args = _compile_for_args


def resolve_gb_agg_funcs(cres):
    from bodo.ir.aggregate import gb_agg_cfunc_addr
    for ruaj__lmqu in cres.library._codegen._engine._defined_symbols:
        if ruaj__lmqu.startswith('cfunc'
            ) and 'get_agg_udf_addr' not in ruaj__lmqu and (
            'bodo_gb_udf_update_local' in ruaj__lmqu or 
            'bodo_gb_udf_combine' in ruaj__lmqu or 'bodo_gb_udf_eval' in
            ruaj__lmqu or 'bodo_gb_apply_general_udfs' in ruaj__lmqu):
            gb_agg_cfunc_addr[ruaj__lmqu
                ] = cres.library.get_pointer_to_function(ruaj__lmqu)


def resolve_join_general_cond_funcs(cres):
    from bodo.ir.join import join_gen_cond_cfunc_addr
    for ruaj__lmqu in cres.library._codegen._engine._defined_symbols:
        if ruaj__lmqu.startswith('cfunc') and ('get_join_cond_addr' not in
            ruaj__lmqu or 'bodo_join_gen_cond' in ruaj__lmqu):
            join_gen_cond_cfunc_addr[ruaj__lmqu
                ] = cres.library.get_pointer_to_function(ruaj__lmqu)


def compile(self, sig):
    import numba.core.event as ev
    from numba.core import sigutils
    from numba.core.compiler_lock import global_compiler_lock
    import bodo
    zynof__ydlcs = self._get_dispatcher_for_current_target()
    if zynof__ydlcs is not self:
        return zynof__ydlcs.compile(sig)
    with ExitStack() as scope:
        cres = None

        def cb_compiler(dur):
            if cres is not None:
                self._callback_add_compiler_timer(dur, cres)

        def cb_llvm(dur):
            if cres is not None:
                self._callback_add_llvm_timer(dur, cres)
        scope.enter_context(ev.install_timer('numba:compiler_lock',
            cb_compiler))
        scope.enter_context(ev.install_timer('numba:llvm_lock', cb_llvm))
        scope.enter_context(global_compiler_lock)
        if not self._can_compile:
            raise RuntimeError('compilation disabled')
        with self._compiling_counter:
            args, return_type = sigutils.normalize_signature(sig)
            fdy__vqfz = self.overloads.get(tuple(args))
            if fdy__vqfz is not None:
                return fdy__vqfz.entry_point
            cres = self._cache.load_overload(sig, self.targetctx)
            if cres is not None:
                resolve_gb_agg_funcs(cres)
                resolve_join_general_cond_funcs(cres)
                self._cache_hits[sig] += 1
                if not cres.objectmode:
                    self.targetctx.insert_user_function(cres.entry_point,
                        cres.fndesc, [cres.library])
                self.add_overload(cres)
                return cres.entry_point
            self._cache_misses[sig] += 1
            cxhzq__nngeq = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=cxhzq__nngeq):
                try:
                    cres = self._compiler.compile(args, return_type)
                except errors.ForceLiteralArg as e:

                    def folded(args, kws):
                        return self._compiler.fold_argument_types(args, kws)[1]
                    raise e.bind_fold_arguments(folded)
                self.add_overload(cres)
            if os.environ.get('BODO_PLATFORM_CACHE_LOCATION') is not None:
                if bodo.get_rank() == 0:
                    self._cache.save_overload(sig, cres)
            else:
                mjrbj__zye = bodo.get_nodes_first_ranks()
                if bodo.get_rank() in mjrbj__zye:
                    self._cache.save_overload(sig, cres)
            return cres.entry_point


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.Dispatcher.compile)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '934ec993577ea3b1c7dd2181ac02728abf8559fd42c17062cc821541b092ff8f':
        warnings.warn('numba.core.dispatcher.Dispatcher.compile has changed')
numba.core.dispatcher.Dispatcher.compile = compile


def _get_module_for_linking(self):
    import llvmlite.binding as ll
    self._ensure_finalized()
    if self._shared_module is not None:
        return self._shared_module
    zcgt__ynb = self._final_module
    trsh__bjp = []
    jrot__nulk = 0
    for fn in zcgt__ynb.functions:
        jrot__nulk += 1
        if not fn.is_declaration and fn.linkage == ll.Linkage.external:
            if 'get_agg_udf_addr' not in fn.name:
                if 'bodo_gb_udf_update_local' in fn.name:
                    continue
                if 'bodo_gb_udf_combine' in fn.name:
                    continue
                if 'bodo_gb_udf_eval' in fn.name:
                    continue
                if 'bodo_gb_apply_general_udfs' in fn.name:
                    continue
            if 'get_join_cond_addr' not in fn.name:
                if 'bodo_join_gen_cond' in fn.name:
                    continue
            trsh__bjp.append(fn.name)
    if jrot__nulk == 0:
        raise RuntimeError(
            'library unfit for linking: no available functions in %s' % (self,)
            )
    if trsh__bjp:
        zcgt__ynb = zcgt__ynb.clone()
        for name in trsh__bjp:
            zcgt__ynb.get_function(name).linkage = 'linkonce_odr'
    self._shared_module = zcgt__ynb
    return zcgt__ynb


if _check_numba_change:
    lines = inspect.getsource(numba.core.codegen.CPUCodeLibrary.
        _get_module_for_linking)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '56dde0e0555b5ec85b93b97c81821bce60784515a1fbf99e4542e92d02ff0a73':
        warnings.warn(
            'numba.core.codegen.CPUCodeLibrary._get_module_for_linking has changed'
            )
numba.core.codegen.CPUCodeLibrary._get_module_for_linking = (
    _get_module_for_linking)


def propagate(self, typeinfer):
    import bodo
    errors = []
    for exm__ouzn in self.constraints:
        loc = exm__ouzn.loc
        with typeinfer.warnings.catch_warnings(filename=loc.filename,
            lineno=loc.line):
            try:
                exm__ouzn(typeinfer)
            except numba.core.errors.ForceLiteralArg as e:
                errors.append(e)
            except numba.core.errors.TypingError as e:
                numba.core.typeinfer._logger.debug('captured error', exc_info=e
                    )
                tkxjr__wxi = numba.core.errors.TypingError(str(e), loc=
                    exm__ouzn.loc, highlighting=False)
                errors.append(numba.core.utils.chain_exception(tkxjr__wxi, e))
            except bodo.utils.typing.BodoError as e:
                if loc not in e.locs_in_msg:
                    errors.append(bodo.utils.typing.BodoError(str(e.msg) +
                        '\n' + loc.strformat() + '\n', locs_in_msg=e.
                        locs_in_msg + [loc]))
                else:
                    errors.append(bodo.utils.typing.BodoError(e.msg,
                        locs_in_msg=e.locs_in_msg))
            except Exception as e:
                from numba.core import utils
                if utils.use_old_style_errors():
                    numba.core.typeinfer._logger.debug('captured error',
                        exc_info=e)
                    msg = """Internal error at {con}.
{err}
Enable logging at debug level for details."""
                    tkxjr__wxi = numba.core.errors.TypingError(msg.format(
                        con=exm__ouzn, err=str(e)), loc=exm__ouzn.loc,
                        highlighting=False)
                    errors.append(utils.chain_exception(tkxjr__wxi, e))
                elif utils.use_new_style_errors():
                    raise e
                else:
                    msg = (
                        f"Unknown CAPTURED_ERRORS style: '{numba.core.config.CAPTURED_ERRORS}'."
                        )
                    assert 0, msg
    return errors


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.ConstraintNetwork.propagate)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1e73635eeba9ba43cb3372f395b747ae214ce73b729fb0adba0a55237a1cb063':
        warnings.warn(
            'numba.core.typeinfer.ConstraintNetwork.propagate has changed')
numba.core.typeinfer.ConstraintNetwork.propagate = propagate


def raise_error(self):
    import bodo
    for zzs__rhi in self._failures.values():
        for dmkfc__pdrj in zzs__rhi:
            if isinstance(dmkfc__pdrj.error, ForceLiteralArg):
                raise dmkfc__pdrj.error
            if isinstance(dmkfc__pdrj.error, bodo.utils.typing.BodoError):
                raise dmkfc__pdrj.error
    raise TypingError(self.format())


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.functions.
        _ResolutionFailures.raise_error)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '84b89430f5c8b46cfc684804e6037f00a0f170005cd128ad245551787b2568ea':
        warnings.warn(
            'numba.core.types.functions._ResolutionFailures.raise_error has changed'
            )
numba.core.types.functions._ResolutionFailures.raise_error = raise_error


def bodo_remove_dead_block(block, lives, call_table, arg_aliases, alias_map,
    alias_set, func_ir, typemap):
    from bodo.transforms.distributed_pass import saved_array_analysis
    from bodo.utils.utils import is_array_typ, is_expr
    olw__fselu = False
    qwaym__qlfk = [block.terminator]
    for stmt in reversed(block.body[:-1]):
        psocf__bfv = set()
        xsngr__wsunt = lives & alias_set
        for gprl__aoel in xsngr__wsunt:
            psocf__bfv |= alias_map[gprl__aoel]
        lives_n_aliases = lives | psocf__bfv | arg_aliases
        if type(stmt) in remove_dead_extensions:
            sltmu__pph = remove_dead_extensions[type(stmt)]
            stmt = sltmu__pph(stmt, lives, lives_n_aliases, arg_aliases,
                alias_map, func_ir, typemap)
            if stmt is None:
                olw__fselu = True
                continue
        if isinstance(stmt, ir.Assign):
            dizzz__kevk = stmt.target
            uqxkt__czrf = stmt.value
            if dizzz__kevk.name not in lives:
                if has_no_side_effect(uqxkt__czrf, lives_n_aliases, call_table
                    ):
                    olw__fselu = True
                    continue
                if isinstance(uqxkt__czrf, ir.Expr
                    ) and uqxkt__czrf.op == 'call' and call_table[uqxkt__czrf
                    .func.name] == ['astype']:
                    rjl__kpxyp = guard(get_definition, func_ir, uqxkt__czrf
                        .func)
                    if (rjl__kpxyp is not None and rjl__kpxyp.op ==
                        'getattr' and isinstance(typemap[rjl__kpxyp.value.
                        name], types.Array) and rjl__kpxyp.attr == 'astype'):
                        olw__fselu = True
                        continue
            if saved_array_analysis and dizzz__kevk.name in lives and is_expr(
                uqxkt__czrf, 'getattr'
                ) and uqxkt__czrf.attr == 'shape' and is_array_typ(typemap[
                uqxkt__czrf.value.name]
                ) and uqxkt__czrf.value.name not in lives:
                kcvt__atoe = {gprl__aoel: nvtk__ucegf for nvtk__ucegf,
                    gprl__aoel in func_ir.blocks.items()}
                if block in kcvt__atoe:
                    label = kcvt__atoe[block]
                    ptbl__wlrj = saved_array_analysis.get_equiv_set(label)
                    mtmej__thws = ptbl__wlrj.get_equiv_set(uqxkt__czrf.value)
                    if mtmej__thws is not None:
                        for gprl__aoel in mtmej__thws:
                            if gprl__aoel.endswith('#0'):
                                gprl__aoel = gprl__aoel[:-2]
                            if gprl__aoel in typemap and is_array_typ(typemap
                                [gprl__aoel]) and gprl__aoel in lives:
                                uqxkt__czrf.value = ir.Var(uqxkt__czrf.
                                    value.scope, gprl__aoel, uqxkt__czrf.
                                    value.loc)
                                olw__fselu = True
                                break
            if isinstance(uqxkt__czrf, ir.Var
                ) and dizzz__kevk.name == uqxkt__czrf.name:
                olw__fselu = True
                continue
        if isinstance(stmt, ir.Del):
            if stmt.value not in lives:
                olw__fselu = True
                continue
        if isinstance(stmt, ir.SetItem):
            name = stmt.target.name
            if name not in lives_n_aliases:
                continue
        if type(stmt) in analysis.ir_extension_usedefs:
            yjo__flwiw = analysis.ir_extension_usedefs[type(stmt)]
            oorwg__ntzmd, uxs__pwot = yjo__flwiw(stmt)
            lives -= uxs__pwot
            lives |= oorwg__ntzmd
        else:
            lives |= {gprl__aoel.name for gprl__aoel in stmt.list_vars()}
            if isinstance(stmt, ir.Assign):
                tgheg__wlh = set()
                if isinstance(uqxkt__czrf, ir.Expr):
                    tgheg__wlh = {gprl__aoel.name for gprl__aoel in
                        uqxkt__czrf.list_vars()}
                if dizzz__kevk.name not in tgheg__wlh:
                    lives.remove(dizzz__kevk.name)
        qwaym__qlfk.append(stmt)
    qwaym__qlfk.reverse()
    block.body = qwaym__qlfk
    return olw__fselu


ir_utils.remove_dead_block = bodo_remove_dead_block


@infer_global(set)
class SetBuiltin(AbstractTemplate):

    def generic(self, args, kws):
        assert not kws
        if args:
            ihcs__nufos, = args
            if isinstance(ihcs__nufos, types.IterableType):
                dtype = ihcs__nufos.iterator_type.yield_type
                if isinstance(dtype, types.Hashable
                    ) or dtype == numba.core.types.unicode_type:
                    return signature(types.Set(dtype), ihcs__nufos)
        else:
            return signature(types.Set(types.undefined))


def Set__init__(self, dtype, reflected=False):
    assert isinstance(dtype, (types.Hashable, types.Undefined)
        ) or dtype == numba.core.types.unicode_type
    self.dtype = dtype
    self.reflected = reflected
    lez__ybp = 'reflected set' if reflected else 'set'
    name = '%s(%s)' % (lez__ybp, self.dtype)
    super(types.Set, self).__init__(name=name)


types.Set.__init__ = Set__init__


@lower_builtin(operator.eq, types.UnicodeType, types.UnicodeType)
def eq_str(context, builder, sig, args):
    func = numba.cpython.unicode.unicode_eq(*sig.args)
    return context.compile_internal(builder, func, sig, args)


numba.parfors.parfor.push_call_vars = (lambda blocks, saved_globals,
    saved_getattrs, typemap, nested=False: None)


def maybe_literal(value):
    if isinstance(value, (list, dict, pytypes.FunctionType)):
        return
    if isinstance(value, tuple):
        try:
            return types.Tuple([literal(x) for x in value])
        except LiteralTypingError as tnpc__ypis:
            return
    try:
        return literal(value)
    except LiteralTypingError as tnpc__ypis:
        return


if _check_numba_change:
    lines = inspect.getsource(types.maybe_literal)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8fb2fd93acf214b28e33e37d19dc2f7290a42792ec59b650553ac278854b5081':
        warnings.warn('types.maybe_literal has changed')
types.maybe_literal = maybe_literal
types.misc.maybe_literal = maybe_literal


def CacheImpl__init__(self, py_func):
    self._lineno = py_func.__code__.co_firstlineno
    try:
        geech__mjsue = py_func.__qualname__
    except AttributeError as tnpc__ypis:
        geech__mjsue = py_func.__name__
    vyb__dit = inspect.getfile(py_func)
    for cls in self._locator_classes:
        ivgr__zcmxz = cls.from_function(py_func, vyb__dit)
        if ivgr__zcmxz is not None:
            break
    else:
        raise RuntimeError(
            'cannot cache function %r: no locator available for file %r' %
            (geech__mjsue, vyb__dit))
    self._locator = ivgr__zcmxz
    xcy__jrkp = inspect.getfile(py_func)
    mmer__muybu = os.path.splitext(os.path.basename(xcy__jrkp))[0]
    if vyb__dit.startswith('<ipython-'):
        zjlr__rwmv = re.sub('(ipython-input)(-\\d+)(-[0-9a-fA-F]+)',
            '\\1\\3', mmer__muybu, count=1)
        if zjlr__rwmv == mmer__muybu:
            warnings.warn(
                'Did not recognize ipython module name syntax. Caching might not work'
                )
        mmer__muybu = zjlr__rwmv
    ghk__gnlor = '%s.%s' % (mmer__muybu, geech__mjsue)
    jgki__wpng = getattr(sys, 'abiflags', '')
    from bodo import __version__ as bodo_version
    self._filename_base = self.get_filename_base(ghk__gnlor, jgki__wpng
        ) + 'bodo' + bodo_version


if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheImpl.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b46d298146e3844e9eaeef29d36f5165ba4796c270ca50d2b35f9fcdc0fa032a':
        warnings.warn('numba.core.caching._CacheImpl.__init__ has changed')
numba.core.caching._CacheImpl.__init__ = CacheImpl__init__


def _analyze_broadcast(self, scope, equiv_set, loc, args, fn):
    from numba.parfors.array_analysis import ArrayAnalysis
    ktcyp__qdix = list(filter(lambda a: self._istuple(a.name), args))
    if len(ktcyp__qdix) == 2 and fn.__name__ == 'add':
        dhtdt__houly = self.typemap[ktcyp__qdix[0].name]
        smbev__xhd = self.typemap[ktcyp__qdix[1].name]
        if dhtdt__houly.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                ktcyp__qdix[1]))
        if smbev__xhd.count == 0:
            return ArrayAnalysis.AnalyzeResult(shape=equiv_set.get_shape(
                ktcyp__qdix[0]))
        try:
            gnqe__eeg = [equiv_set.get_shape(x) for x in ktcyp__qdix]
            if None in gnqe__eeg:
                return None
            gmnlq__jazb = sum(gnqe__eeg, ())
            return ArrayAnalysis.AnalyzeResult(shape=gmnlq__jazb)
        except GuardException as tnpc__ypis:
            return None
    qkk__wte = list(filter(lambda a: self._isarray(a.name), args))
    require(len(qkk__wte) > 0)
    okc__irac = [x.name for x in qkk__wte]
    aapq__zegau = [self.typemap[x.name].ndim for x in qkk__wte]
    gjbq__dzgzp = max(aapq__zegau)
    require(gjbq__dzgzp > 0)
    gnqe__eeg = [equiv_set.get_shape(x) for x in qkk__wte]
    if any(a is None for a in gnqe__eeg):
        return ArrayAnalysis.AnalyzeResult(shape=qkk__wte[0], pre=self.
            _call_assert_equiv(scope, loc, equiv_set, qkk__wte))
    return self._broadcast_assert_shapes(scope, equiv_set, loc, gnqe__eeg,
        okc__irac)


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.array_analysis.ArrayAnalysis.
        _analyze_broadcast)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6c91fec038f56111338ea2b08f5f0e7f61ebdab1c81fb811fe26658cc354e40f':
        warnings.warn(
            'numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast has changed'
            )
numba.parfors.array_analysis.ArrayAnalysis._analyze_broadcast = (
    _analyze_broadcast)


def slice_size(self, index, dsize, equiv_set, scope, stmts):
    return None, None


numba.parfors.array_analysis.ArrayAnalysis.slice_size = slice_size


def convert_code_obj_to_function(code_obj, caller_ir):
    import bodo
    axa__tmrhq = code_obj.code
    bddj__szzhd = len(axa__tmrhq.co_freevars)
    jns__qop = axa__tmrhq.co_freevars
    if code_obj.closure is not None:
        assert isinstance(code_obj.closure, ir.Var)
        svjlh__atcit, op = ir_utils.find_build_sequence(caller_ir, code_obj
            .closure)
        assert op == 'build_tuple'
        jns__qop = [gprl__aoel.name for gprl__aoel in svjlh__atcit]
    aqgw__ldko = caller_ir.func_id.func.__globals__
    try:
        aqgw__ldko = getattr(code_obj, 'globals', aqgw__ldko)
    except KeyError as tnpc__ypis:
        pass
    msg = (
        "Inner function is using non-constant variable '{}' from outer function. Please pass as argument if possible. See https://docs.bodo.ai/latest/api_docs/udfs/."
        )
    rnrnp__ezc = []
    for x in jns__qop:
        try:
            vwyd__fnf = caller_ir.get_definition(x)
        except KeyError as tnpc__ypis:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
        from numba.core.registry import CPUDispatcher
        if isinstance(vwyd__fnf, (ir.Const, ir.Global, ir.FreeVar)):
            val = vwyd__fnf.value
            if isinstance(val, str):
                val = "'{}'".format(val)
            if isinstance(val, pytypes.FunctionType):
                nja__thi = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                aqgw__ldko[nja__thi] = bodo.jit(distributed=False)(val)
                aqgw__ldko[nja__thi].is_nested_func = True
                val = nja__thi
            if isinstance(val, CPUDispatcher):
                nja__thi = ir_utils.mk_unique_var('nested_func').replace('.',
                    '_')
                aqgw__ldko[nja__thi] = val
                val = nja__thi
            rnrnp__ezc.append(val)
        elif isinstance(vwyd__fnf, ir.Expr
            ) and vwyd__fnf.op == 'make_function':
            uweq__scccy = convert_code_obj_to_function(vwyd__fnf, caller_ir)
            nja__thi = ir_utils.mk_unique_var('nested_func').replace('.', '_')
            aqgw__ldko[nja__thi] = bodo.jit(distributed=False)(uweq__scccy)
            aqgw__ldko[nja__thi].is_nested_func = True
            rnrnp__ezc.append(nja__thi)
        else:
            raise bodo.utils.typing.BodoError(msg.format(x), loc=code_obj.loc)
    lkzuh__xwt = '\n'.join([('\tc_%d = %s' % (i, x)) for i, x in enumerate(
        rnrnp__ezc)])
    zfkh__bwen = ','.join([('c_%d' % i) for i in range(bddj__szzhd)])
    fra__vuu = list(axa__tmrhq.co_varnames)
    ybmm__odon = 0
    chzb__qjr = axa__tmrhq.co_argcount
    iowj__ynqyk = caller_ir.get_definition(code_obj.defaults)
    if iowj__ynqyk is not None:
        if isinstance(iowj__ynqyk, tuple):
            d = [caller_ir.get_definition(x).value for x in iowj__ynqyk]
            fqgjy__rkyg = tuple(d)
        else:
            d = [caller_ir.get_definition(x).value for x in iowj__ynqyk.items]
            fqgjy__rkyg = tuple(d)
        ybmm__odon = len(fqgjy__rkyg)
    fdl__vjc = chzb__qjr - ybmm__odon
    nowvl__puep = ','.join([('%s' % fra__vuu[i]) for i in range(fdl__vjc)])
    if ybmm__odon:
        kvy__fiml = [('%s = %s' % (fra__vuu[i + fdl__vjc], fqgjy__rkyg[i])) for
            i in range(ybmm__odon)]
        nowvl__puep += ', '
        nowvl__puep += ', '.join(kvy__fiml)
    return _create_function_from_code_obj(axa__tmrhq, lkzuh__xwt,
        nowvl__puep, zfkh__bwen, aqgw__ldko)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.convert_code_obj_to_function)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b840769812418d589460e924a15477e83e7919aac8a3dcb0188ff447344aa8ac':
        warnings.warn(
            'numba.core.ir_utils.convert_code_obj_to_function has changed')
numba.core.ir_utils.convert_code_obj_to_function = convert_code_obj_to_function
numba.core.untyped_passes.convert_code_obj_to_function = (
    convert_code_obj_to_function)


def passmanager_run(self, state):
    from numba.core.compiler import _EarlyPipelineCompletion
    if not self.finalized:
        raise RuntimeError('Cannot run non-finalised pipeline')
    from numba.core.compiler_machinery import CompilerPass, _pass_registry
    import bodo
    for rvf__yahzd, (ilo__xbnrs, sdm__abd) in enumerate(self.passes):
        try:
            numba.core.tracing.event('-- %s' % sdm__abd)
            jbar__xdl = _pass_registry.get(ilo__xbnrs).pass_inst
            if isinstance(jbar__xdl, CompilerPass):
                self._runPass(rvf__yahzd, jbar__xdl, state)
            else:
                raise BaseException('Legacy pass in use')
        except _EarlyPipelineCompletion as e:
            raise e
        except bodo.utils.typing.BodoError as e:
            raise
        except Exception as e:
            if numba.core.config.DEVELOPER_MODE:
                from numba.core import utils
                if utils.use_new_style_errors() and not isinstance(e,
                    errors.NumbaError):
                    raise e
                msg = 'Failed in %s mode pipeline (step: %s)' % (self.
                    pipeline_name, sdm__abd)
                cmb__zhd = self._patch_error(msg, e)
                raise cmb__zhd
            else:
                raise e


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler_machinery.PassManager.run)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '43505782e15e690fd2d7e53ea716543bec37aa0633502956864edf649e790cdb':
        warnings.warn(
            'numba.core.compiler_machinery.PassManager.run has changed')
numba.core.compiler_machinery.PassManager.run = passmanager_run
if _check_numba_change:
    lines = inspect.getsource(numba.np.ufunc.parallel._launch_threads)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a57ef28c4168fdd436a5513bba4351ebc6d9fba76c5819f44046431a79b9030f':
        warnings.warn('numba.np.ufunc.parallel._launch_threads has changed')
numba.np.ufunc.parallel._launch_threads = lambda : None


def get_reduce_nodes(reduction_node, nodes, func_ir):
    hhsnb__lcj = None
    uxs__pwot = {}

    def lookup(var, already_seen, varonly=True):
        val = uxs__pwot.get(var.name, None)
        if isinstance(val, ir.Var):
            if val.name in already_seen:
                return var
            already_seen.add(val.name)
            return lookup(val, already_seen, varonly)
        else:
            return var if varonly or val is None else val
    name = reduction_node.name
    kqmy__xrk = reduction_node.unversioned_name
    for i, stmt in enumerate(nodes):
        dizzz__kevk = stmt.target
        uqxkt__czrf = stmt.value
        uxs__pwot[dizzz__kevk.name] = uqxkt__czrf
        if isinstance(uqxkt__czrf, ir.Var) and uqxkt__czrf.name in uxs__pwot:
            uqxkt__czrf = lookup(uqxkt__czrf, set())
        if isinstance(uqxkt__czrf, ir.Expr):
            viv__vhp = set(lookup(gprl__aoel, set(), True).name for
                gprl__aoel in uqxkt__czrf.list_vars())
            if name in viv__vhp:
                args = [(x.name, lookup(x, set(), True)) for x in
                    get_expr_args(uqxkt__czrf)]
                vhvs__cmjj = [x for x, vql__wvonz in args if vql__wvonz.
                    name != name]
                args = [(x, vql__wvonz) for x, vql__wvonz in args if x !=
                    vql__wvonz.name]
                ihkxj__ybsif = dict(args)
                if len(vhvs__cmjj) == 1:
                    ihkxj__ybsif[vhvs__cmjj[0]] = ir.Var(dizzz__kevk.scope,
                        name + '#init', dizzz__kevk.loc)
                replace_vars_inner(uqxkt__czrf, ihkxj__ybsif)
                hhsnb__lcj = nodes[i:]
                break
    return hhsnb__lcj


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_reduce_nodes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a05b52aff9cb02e595a510cd34e973857303a71097fc5530567cb70ca183ef3b':
        warnings.warn('numba.parfors.parfor.get_reduce_nodes has changed')
numba.parfors.parfor.get_reduce_nodes = get_reduce_nodes


def _can_reorder_stmts(stmt, next_stmt, func_ir, call_table, alias_map,
    arg_aliases):
    from numba.parfors.parfor import Parfor, expand_aliases, is_assert_equiv
    if isinstance(stmt, Parfor) and not isinstance(next_stmt, Parfor
        ) and not isinstance(next_stmt, ir.Print) and (not isinstance(
        next_stmt, ir.Assign) or has_no_side_effect(next_stmt.value, set(),
        call_table) or guard(is_assert_equiv, func_ir, next_stmt.value)):
        aoho__ruhie = expand_aliases({gprl__aoel.name for gprl__aoel in
            stmt.list_vars()}, alias_map, arg_aliases)
        vke__psuti = expand_aliases(get_parfor_writes(stmt, func_ir),
            alias_map, arg_aliases)
        kathj__gstr = expand_aliases({gprl__aoel.name for gprl__aoel in
            next_stmt.list_vars()}, alias_map, arg_aliases)
        xjf__deojm = expand_aliases(get_stmt_writes(next_stmt, func_ir),
            alias_map, arg_aliases)
        if len(vke__psuti & kathj__gstr | xjf__deojm & aoho__ruhie) == 0:
            return True
    return False


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor._can_reorder_stmts)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '18caa9a01b21ab92b4f79f164cfdbc8574f15ea29deedf7bafdf9b0e755d777c':
        warnings.warn('numba.parfors.parfor._can_reorder_stmts has changed')
numba.parfors.parfor._can_reorder_stmts = _can_reorder_stmts


def get_parfor_writes(parfor, func_ir):
    from numba.parfors.parfor import Parfor
    assert isinstance(parfor, Parfor)
    ookcc__vudy = set()
    blocks = parfor.loop_body.copy()
    blocks[-1] = parfor.init_block
    for block in blocks.values():
        for stmt in block.body:
            ookcc__vudy.update(get_stmt_writes(stmt, func_ir))
            if isinstance(stmt, Parfor):
                ookcc__vudy.update(get_parfor_writes(stmt, func_ir))
    return ookcc__vudy


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.get_parfor_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a7b29cd76832b6f6f1f2d2397ec0678c1409b57a6eab588bffd344b775b1546f':
        warnings.warn('numba.parfors.parfor.get_parfor_writes has changed')


def get_stmt_writes(stmt, func_ir):
    import bodo
    from bodo.utils.utils import is_call_assign
    ookcc__vudy = set()
    if isinstance(stmt, (ir.Assign, ir.SetItem, ir.StaticSetItem)):
        ookcc__vudy.add(stmt.target.name)
    if isinstance(stmt, (bodo.ir.csv_ext.CsvReader, bodo.ir.parquet_ext.
        ParquetReader)):
        ookcc__vudy = {gprl__aoel.name for gprl__aoel in stmt.out_vars}
    if isinstance(stmt, (bodo.ir.join.Join, bodo.ir.aggregate.Aggregate)):
        ookcc__vudy = {gprl__aoel.name for gprl__aoel in stmt.
            get_live_out_vars()}
    if isinstance(stmt, bodo.ir.sort.Sort):
        if not stmt.inplace:
            ookcc__vudy.update({gprl__aoel.name for gprl__aoel in stmt.
                get_live_out_vars()})
    if is_call_assign(stmt):
        iofg__jtp = guard(find_callname, func_ir, stmt.value)
        if iofg__jtp in (('setitem_str_arr_ptr', 'bodo.libs.str_arr_ext'),
            ('setna', 'bodo.libs.array_kernels'), (
            'str_arr_item_to_numeric', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_int_to_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_setitem_NA_str', 'bodo.libs.str_arr_ext'), (
            'str_arr_set_not_na', 'bodo.libs.str_arr_ext'), (
            'get_str_arr_item_copy', 'bodo.libs.str_arr_ext'), (
            'copy_array_element', 'bodo.libs.array_kernels'), (
            'set_bit_to_arr', 'bodo.libs.int_arr_ext'), (
            'tuple_list_to_array', 'bodo.utils.utils')):
            ookcc__vudy.add(stmt.value.args[0].name)
        if iofg__jtp == ('generate_table_nbytes', 'bodo.utils.table_utils'):
            ookcc__vudy.add(stmt.value.args[1].name)
    return ookcc__vudy


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.get_stmt_writes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1a7a80b64c9a0eb27e99dc8eaae187bde379d4da0b74c84fbf87296d87939974':
        warnings.warn('numba.core.ir_utils.get_stmt_writes has changed')


def patch_message(self, new_message):
    self.msg = new_message
    self.args = (new_message,) + self.args[1:]


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.patch_message)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'ed189a428a7305837e76573596d767b6e840e99f75c05af6941192e0214fa899':
        warnings.warn('numba.core.errors.NumbaError.patch_message has changed')
numba.core.errors.NumbaError.patch_message = patch_message


def add_context(self, msg):
    if numba.core.config.DEVELOPER_MODE:
        self.contexts.append(msg)
        sltmu__pph = _termcolor.errmsg('{0}') + _termcolor.filename(
            'During: {1}')
        rbso__wmh = sltmu__pph.format(self, msg)
        self.args = rbso__wmh,
    else:
        sltmu__pph = _termcolor.errmsg('{0}')
        rbso__wmh = sltmu__pph.format(self)
        self.args = rbso__wmh,
    return self


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.NumbaError.add_context)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '6a388d87788f8432c2152ac55ca9acaa94dbc3b55be973b2cf22dd4ee7179ab8':
        warnings.warn('numba.core.errors.NumbaError.add_context has changed')
numba.core.errors.NumbaError.add_context = add_context


def _get_dist_spec_from_options(spec, **options):
    from bodo.transforms.distributed_analysis import Distribution
    dist_spec = {}
    if 'distributed' in options:
        for awq__mrqix in options['distributed']:
            dist_spec[awq__mrqix] = Distribution.OneD_Var
    if 'distributed_block' in options:
        for awq__mrqix in options['distributed_block']:
            dist_spec[awq__mrqix] = Distribution.OneD
    return dist_spec


def register_class_type(cls, spec, class_ctor, builder, **options):
    import typing as pt
    from numba.core.typing.asnumbatype import as_numba_type
    import bodo
    dist_spec = _get_dist_spec_from_options(spec, **options)
    edjep__qglzu = options.get('returns_maybe_distributed', True)
    if spec is None:
        spec = OrderedDict()
    elif isinstance(spec, Sequence):
        spec = OrderedDict(spec)
    for attr, wvu__rue in pt.get_type_hints(cls).items():
        if attr not in spec:
            spec[attr] = as_numba_type(wvu__rue)
    jitclass_base._validate_spec(spec)
    spec = jitclass_base._fix_up_private_attr(cls.__name__, spec)
    wwy__axooc = {}
    for xwb__ioswb in reversed(inspect.getmro(cls)):
        wwy__axooc.update(xwb__ioswb.__dict__)
    xkw__gaytb, dmrv__yjwyh, utpb__tqbb, dwy__mvkgw = {}, {}, {}, {}
    for nvtk__ucegf, gprl__aoel in wwy__axooc.items():
        if isinstance(gprl__aoel, pytypes.FunctionType):
            xkw__gaytb[nvtk__ucegf] = gprl__aoel
        elif isinstance(gprl__aoel, property):
            dmrv__yjwyh[nvtk__ucegf] = gprl__aoel
        elif isinstance(gprl__aoel, staticmethod):
            utpb__tqbb[nvtk__ucegf] = gprl__aoel
        else:
            dwy__mvkgw[nvtk__ucegf] = gprl__aoel
    urq__koa = (set(xkw__gaytb) | set(dmrv__yjwyh) | set(utpb__tqbb)) & set(
        spec)
    if urq__koa:
        raise NameError('name shadowing: {0}'.format(', '.join(urq__koa)))
    hmi__wkdo = dwy__mvkgw.pop('__doc__', '')
    jitclass_base._drop_ignored_attrs(dwy__mvkgw)
    if dwy__mvkgw:
        msg = 'class members are not yet supported: {0}'
        sej__bun = ', '.join(dwy__mvkgw.keys())
        raise TypeError(msg.format(sej__bun))
    for nvtk__ucegf, gprl__aoel in dmrv__yjwyh.items():
        if gprl__aoel.fdel is not None:
            raise TypeError('deleter is not supported: {0}'.format(nvtk__ucegf)
                )
    jit_methods = {nvtk__ucegf: bodo.jit(returns_maybe_distributed=
        edjep__qglzu)(gprl__aoel) for nvtk__ucegf, gprl__aoel in xkw__gaytb
        .items()}
    jit_props = {}
    for nvtk__ucegf, gprl__aoel in dmrv__yjwyh.items():
        kdord__bphcj = {}
        if gprl__aoel.fget:
            kdord__bphcj['get'] = bodo.jit(gprl__aoel.fget)
        if gprl__aoel.fset:
            kdord__bphcj['set'] = bodo.jit(gprl__aoel.fset)
        jit_props[nvtk__ucegf] = kdord__bphcj
    jit_static_methods = {nvtk__ucegf: bodo.jit(gprl__aoel.__func__) for 
        nvtk__ucegf, gprl__aoel in utpb__tqbb.items()}
    qhzws__kzecj = class_ctor(cls, jitclass_base.ConstructorTemplate, spec,
        jit_methods, jit_props, jit_static_methods, dist_spec)
    uidz__rnf = dict(class_type=qhzws__kzecj, __doc__=hmi__wkdo)
    uidz__rnf.update(jit_static_methods)
    cls = jitclass_base.JitClassType(cls.__name__, (cls,), uidz__rnf)
    typingctx = numba.core.registry.cpu_target.typing_context
    typingctx.insert_global(cls, qhzws__kzecj)
    targetctx = numba.core.registry.cpu_target.target_context
    builder(qhzws__kzecj, typingctx, targetctx).register()
    as_numba_type.register(cls, qhzws__kzecj.instance_type)
    return cls


if _check_numba_change:
    lines = inspect.getsource(jitclass_base.register_class_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '005e6e2e89a47f77a19ba86305565050d4dbc2412fc4717395adf2da348671a9':
        warnings.warn('jitclass_base.register_class_type has changed')
jitclass_base.register_class_type = register_class_type


def ClassType__init__(self, class_def, ctor_template_cls, struct,
    jit_methods, jit_props, jit_static_methods, dist_spec=None):
    if dist_spec is None:
        dist_spec = {}
    self.class_name = class_def.__name__
    self.class_doc = class_def.__doc__
    self._ctor_template_class = ctor_template_cls
    self.jit_methods = jit_methods
    self.jit_props = jit_props
    self.jit_static_methods = jit_static_methods
    self.struct = struct
    self.dist_spec = dist_spec
    ijv__gzj = ','.join('{0}:{1}'.format(nvtk__ucegf, gprl__aoel) for 
        nvtk__ucegf, gprl__aoel in struct.items())
    rkngc__cxi = ','.join('{0}:{1}'.format(nvtk__ucegf, gprl__aoel) for 
        nvtk__ucegf, gprl__aoel in dist_spec.items())
    name = '{0}.{1}#{2:x}<{3}><{4}>'.format(self.name_prefix, self.
        class_name, id(self), ijv__gzj, rkngc__cxi)
    super(types.misc.ClassType, self).__init__(name)


if _check_numba_change:
    lines = inspect.getsource(types.misc.ClassType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '2b848ea82946c88f540e81f93ba95dfa7cd66045d944152a337fe2fc43451c30':
        warnings.warn('types.misc.ClassType.__init__ has changed')
types.misc.ClassType.__init__ = ClassType__init__


def jitclass(cls_or_spec=None, spec=None, **options):
    if cls_or_spec is not None and spec is None and not isinstance(cls_or_spec,
        type):
        spec = cls_or_spec
        cls_or_spec = None

    def wrap(cls):
        if numba.core.config.DISABLE_JIT:
            return cls
        else:
            from numba.experimental.jitclass.base import ClassBuilder
            return register_class_type(cls, spec, types.ClassType,
                ClassBuilder, **options)
    if cls_or_spec is None:
        return wrap
    else:
        return wrap(cls_or_spec)


if _check_numba_change:
    lines = inspect.getsource(jitclass_decorators.jitclass)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '265f1953ee5881d1a5d90238d3c932cd300732e41495657e65bf51e59f7f4af5':
        warnings.warn('jitclass_decorators.jitclass has changed')


def CallConstraint_resolve(self, typeinfer, typevars, fnty):
    assert fnty
    context = typeinfer.context
    nowcy__zmc = numba.core.typeinfer.fold_arg_vars(typevars, self.args,
        self.vararg, self.kws)
    if nowcy__zmc is None:
        return
    ayx__aolo, xygha__avmrf = nowcy__zmc
    for a in itertools.chain(ayx__aolo, xygha__avmrf.values()):
        if not a.is_precise() and not isinstance(a, types.Array):
            return
    if isinstance(fnty, types.TypeRef):
        fnty = fnty.instance_type
    try:
        sig = typeinfer.resolve_call(fnty, ayx__aolo, xygha__avmrf)
    except ForceLiteralArg as e:
        xblwj__pmb = (fnty.this,) + tuple(self.args) if isinstance(fnty,
            types.BoundFunction) else self.args
        folded = e.fold_arguments(xblwj__pmb, self.kws)
        twajh__ylq = set()
        fnz__jegk = set()
        ylj__yab = {}
        for rvf__yahzd in e.requested_args:
            fvw__tgrhb = typeinfer.func_ir.get_definition(folded[rvf__yahzd])
            if isinstance(fvw__tgrhb, ir.Arg):
                twajh__ylq.add(fvw__tgrhb.index)
                if fvw__tgrhb.index in e.file_infos:
                    ylj__yab[fvw__tgrhb.index] = e.file_infos[fvw__tgrhb.index]
            else:
                fnz__jegk.add(rvf__yahzd)
        if fnz__jegk:
            raise TypingError('Cannot request literal type.', loc=self.loc)
        elif twajh__ylq:
            raise ForceLiteralArg(twajh__ylq, loc=self.loc, file_infos=ylj__yab
                )
    if sig is None:
        gczl__ofzcs = 'Invalid use of {0} with parameters ({1})'
        args = [str(a) for a in ayx__aolo]
        args += [('%s=%s' % (nvtk__ucegf, gprl__aoel)) for nvtk__ucegf,
            gprl__aoel in sorted(xygha__avmrf.items())]
        ymij__tzom = gczl__ofzcs.format(fnty, ', '.join(map(str, args)))
        dpm__kao = context.explain_function_type(fnty)
        msg = '\n'.join([ymij__tzom, dpm__kao])
        raise TypingError(msg)
    typeinfer.add_type(self.target, sig.return_type, loc=self.loc)
    if isinstance(fnty, types.BoundFunction
        ) and sig.recvr is not None and sig.recvr != fnty.this:
        jyqh__pngs = context.unify_pairs(sig.recvr, fnty.this)
        if jyqh__pngs is None and fnty.this.is_precise(
            ) and sig.recvr.is_precise():
            msg = 'Cannot refine type {} to {}'.format(sig.recvr, fnty.this)
            raise TypingError(msg, loc=self.loc)
        if jyqh__pngs is not None and jyqh__pngs.is_precise():
            uiht__olpe = fnty.copy(this=jyqh__pngs)
            typeinfer.propagate_refined_type(self.func, uiht__olpe)
    if not sig.return_type.is_precise():
        target = typevars[self.target]
        if target.defined:
            rifl__rwacs = target.getone()
            if context.unify_pairs(rifl__rwacs, sig.return_type
                ) == rifl__rwacs:
                sig = sig.replace(return_type=rifl__rwacs)
    self.signature = sig
    self._add_refine_map(typeinfer, typevars, sig)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typeinfer.CallConstraint.resolve)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c78cd8ffc64b836a6a2ddf0362d481b52b9d380c5249920a87ff4da052ce081f':
        warnings.warn('numba.core.typeinfer.CallConstraint.resolve has changed'
            )
numba.core.typeinfer.CallConstraint.resolve = CallConstraint_resolve


def ForceLiteralArg__init__(self, arg_indices, fold_arguments=None, loc=
    None, file_infos=None):
    super(ForceLiteralArg, self).__init__(
        'Pseudo-exception to force literal arguments in the dispatcher',
        loc=loc)
    self.requested_args = frozenset(arg_indices)
    self.fold_arguments = fold_arguments
    if file_infos is None:
        self.file_infos = {}
    else:
        self.file_infos = file_infos


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b241d5e36a4cf7f4c73a7ad3238693612926606c7a278cad1978070b82fb55ef':
        warnings.warn('numba.core.errors.ForceLiteralArg.__init__ has changed')
numba.core.errors.ForceLiteralArg.__init__ = ForceLiteralArg__init__


def ForceLiteralArg_bind_fold_arguments(self, fold_arguments):
    e = ForceLiteralArg(self.requested_args, fold_arguments, loc=self.loc,
        file_infos=self.file_infos)
    return numba.core.utils.chain_exception(e, self)


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.
        bind_fold_arguments)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1e93cca558f7c604a47214a8f2ec33ee994104cb3e5051166f16d7cc9315141d':
        warnings.warn(
            'numba.core.errors.ForceLiteralArg.bind_fold_arguments has changed'
            )
numba.core.errors.ForceLiteralArg.bind_fold_arguments = (
    ForceLiteralArg_bind_fold_arguments)


def ForceLiteralArg_combine(self, other):
    if not isinstance(other, ForceLiteralArg):
        hesq__zye = '*other* must be a {} but got a {} instead'
        raise TypeError(hesq__zye.format(ForceLiteralArg, type(other)))
    return ForceLiteralArg(self.requested_args | other.requested_args,
        file_infos={**self.file_infos, **other.file_infos})


if _check_numba_change:
    lines = inspect.getsource(numba.core.errors.ForceLiteralArg.combine)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '49bf06612776f5d755c1c7d1c5eb91831a57665a8fed88b5651935f3bf33e899':
        warnings.warn('numba.core.errors.ForceLiteralArg.combine has changed')
numba.core.errors.ForceLiteralArg.combine = ForceLiteralArg_combine


def _get_global_type(self, gv):
    from bodo.utils.typing import FunctionLiteral
    ty = self._lookup_global(gv)
    if ty is not None:
        return ty
    if isinstance(gv, pytypes.ModuleType):
        return types.Module(gv)
    if isinstance(gv, pytypes.FunctionType):
        return FunctionLiteral(gv)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.context.BaseContext.
        _get_global_type)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '8ffe6b81175d1eecd62a37639b5005514b4477d88f35f5b5395041ac8c945a4a':
        warnings.warn(
            'numba.core.typing.context.BaseContext._get_global_type has changed'
            )
numba.core.typing.context.BaseContext._get_global_type = _get_global_type


def _legalize_args(self, func_ir, args, kwargs, loc, func_globals,
    func_closures):
    from numba.core import sigutils
    from bodo.utils.transform import get_const_value_inner
    if args:
        raise errors.CompilerError(
            "objectmode context doesn't take any positional arguments")
    yjbr__efilz = {}

    def report_error(varname, msg, loc):
        raise errors.CompilerError(
            f'Error handling objmode argument {varname!r}. {msg}', loc=loc)
    for nvtk__ucegf, gprl__aoel in kwargs.items():
        fho__dlooo = None
        try:
            tjwuu__iacjr = ir.Var(ir.Scope(None, loc), ir_utils.
                mk_unique_var('dummy'), loc)
            func_ir._definitions[tjwuu__iacjr.name] = [gprl__aoel]
            fho__dlooo = get_const_value_inner(func_ir, tjwuu__iacjr)
            func_ir._definitions.pop(tjwuu__iacjr.name)
            if isinstance(fho__dlooo, str):
                fho__dlooo = sigutils._parse_signature_string(fho__dlooo)
            if isinstance(fho__dlooo, types.abstract._TypeMetaclass):
                raise BodoError(
                    f"""objmode type annotations require full data types, not just data type classes. For example, 'bodo.DataFrameType((bodo.float64[::1],), bodo.RangeIndexType(), ('A',))' is a valid data type but 'bodo.DataFrameType' is not.
Variable {nvtk__ucegf} is annotated as type class {fho__dlooo}."""
                    )
            assert isinstance(fho__dlooo, types.Type)
            if isinstance(fho__dlooo, (types.List, types.Set)):
                fho__dlooo = fho__dlooo.copy(reflected=False)
            yjbr__efilz[nvtk__ucegf] = fho__dlooo
        except BodoError as tnpc__ypis:
            raise
        except:
            msg = (
                'The value must be a compile-time constant either as a non-local variable or an expression that refers to a Bodo type.'
                )
            if isinstance(fho__dlooo, ir.UndefinedType):
                msg = f'not defined.'
                if isinstance(gprl__aoel, ir.Global):
                    msg = f'Global {gprl__aoel.name!r} is not defined.'
                if isinstance(gprl__aoel, ir.FreeVar):
                    msg = f'Freevar {gprl__aoel.name!r} is not defined.'
            if isinstance(gprl__aoel, ir.Expr) and gprl__aoel.op == 'getattr':
                msg = 'Getattr cannot be resolved at compile-time.'
            report_error(varname=nvtk__ucegf, msg=msg, loc=loc)
    for name, typ in yjbr__efilz.items():
        self._legalize_arg_type(name, typ, loc)
    return yjbr__efilz


if _check_numba_change:
    lines = inspect.getsource(numba.core.withcontexts._ObjModeContextType.
        _legalize_args)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '867c9ba7f1bcf438be56c38e26906bb551f59a99f853a9f68b71208b107c880e':
        warnings.warn(
            'numba.core.withcontexts._ObjModeContextType._legalize_args has changed'
            )
numba.core.withcontexts._ObjModeContextType._legalize_args = _legalize_args


def op_FORMAT_VALUE_byteflow(self, state, inst):
    flags = inst.arg
    if flags & 3 != 0:
        msg = 'str/repr/ascii conversion in f-strings not supported yet'
        raise errors.UnsupportedError(msg, loc=self.get_debug_loc(inst.lineno))
    format_spec = None
    if flags & 4 == 4:
        format_spec = state.pop()
    value = state.pop()
    fmtvar = state.make_temp()
    res = state.make_temp()
    state.append(inst, value=value, res=res, fmtvar=fmtvar, format_spec=
        format_spec)
    state.push(res)


def op_BUILD_STRING_byteflow(self, state, inst):
    japsl__agvq = inst.arg
    assert japsl__agvq > 0, 'invalid BUILD_STRING count'
    strings = list(reversed([state.pop() for _ in range(japsl__agvq)]))
    tmps = [state.make_temp() for _ in range(japsl__agvq - 1)]
    state.append(inst, strings=strings, tmps=tmps)
    state.push(tmps[-1])


numba.core.byteflow.TraceRunner.op_FORMAT_VALUE = op_FORMAT_VALUE_byteflow
numba.core.byteflow.TraceRunner.op_BUILD_STRING = op_BUILD_STRING_byteflow


def op_FORMAT_VALUE_interpreter(self, inst, value, res, fmtvar, format_spec):
    value = self.get(value)
    ocer__gvfce = ir.Global('format', format, loc=self.loc)
    self.store(value=ocer__gvfce, name=fmtvar)
    args = (value, self.get(format_spec)) if format_spec else (value,)
    fsmpf__ehbla = ir.Expr.call(self.get(fmtvar), args, (), loc=self.loc)
    self.store(value=fsmpf__ehbla, name=res)


def op_BUILD_STRING_interpreter(self, inst, strings, tmps):
    japsl__agvq = inst.arg
    assert japsl__agvq > 0, 'invalid BUILD_STRING count'
    klwp__cbajc = self.get(strings[0])
    for other, rbf__tpljf in zip(strings[1:], tmps):
        other = self.get(other)
        ddt__egw = ir.Expr.binop(operator.add, lhs=klwp__cbajc, rhs=other,
            loc=self.loc)
        self.store(ddt__egw, rbf__tpljf)
        klwp__cbajc = self.get(rbf__tpljf)


numba.core.interpreter.Interpreter.op_FORMAT_VALUE = (
    op_FORMAT_VALUE_interpreter)
numba.core.interpreter.Interpreter.op_BUILD_STRING = (
    op_BUILD_STRING_interpreter)


def object_hasattr_string(self, obj, attr):
    from llvmlite import ir as lir
    gsi__xyk = self.context.insert_const_string(self.module, attr)
    fnty = lir.FunctionType(lir.IntType(32), [self.pyobj, self.cstring])
    fn = self._get_function(fnty, name='PyObject_HasAttrString')
    return self.builder.call(fn, [obj, gsi__xyk])


numba.core.pythonapi.PythonAPI.object_hasattr_string = object_hasattr_string


def _created_inlined_var_name(function_name, var_name):
    rftfi__hhs = mk_unique_var(f'{var_name}')
    azle__seamn = rftfi__hhs.replace('<', '_').replace('>', '_')
    azle__seamn = azle__seamn.replace('.', '_').replace('$', '_v')
    return azle__seamn


if _check_numba_change:
    lines = inspect.getsource(numba.core.inline_closurecall.
        _created_inlined_var_name)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '0d91aac55cd0243e58809afe9d252562f9ae2899cde1112cc01a46804e01821e':
        warnings.warn(
            'numba.core.inline_closurecall._created_inlined_var_name has changed'
            )
numba.core.inline_closurecall._created_inlined_var_name = (
    _created_inlined_var_name)


def resolve_number___call__(self, classty):
    import numpy as np
    from numba.core.typing.templates import make_callable_template
    import bodo
    ty = classty.instance_type
    if isinstance(ty, types.NPDatetime):

        def typer(val1, val2):
            bodo.hiframes.pd_timestamp_ext.check_tz_aware_unsupported(val1,
                'numpy.datetime64')
            if (val1 == bodo.hiframes.pd_timestamp_ext.
                pd_timestamp_tz_naive_type):
                if not is_overload_constant_str(val2):
                    raise_bodo_error(
                        "datetime64(): 'units' must be a 'str' specifying 'ns'"
                        )
                ivaoc__xjz = get_overload_const_str(val2)
                if ivaoc__xjz != 'ns':
                    raise BodoError("datetime64(): 'units' must be 'ns'")
                return types.NPDatetime('ns')
    else:

        def typer(val):
            if isinstance(val, (types.BaseTuple, types.Sequence)):
                fnty = self.context.resolve_value_type(np.array)
                sig = fnty.get_call_type(self.context, (val, types.DType(ty
                    )), {})
                return sig.return_type
            elif isinstance(val, (types.Number, types.Boolean, types.
                IntEnumMember)):
                return ty
            elif val == types.unicode_type:
                return ty
            elif isinstance(val, (types.NPDatetime, types.NPTimedelta)):
                if ty.bitwidth == 64:
                    return ty
                else:
                    msg = (
                        f'Cannot cast {val} to {ty} as {ty} is not 64 bits wide.'
                        )
                    raise errors.TypingError(msg)
            elif isinstance(val, types.Array
                ) and val.ndim == 0 and val.dtype == ty:
                return ty
            else:
                msg = f'Casting {val} to {ty} directly is unsupported.'
                if isinstance(val, types.Array):
                    msg += f" Try doing '<array>.astype(np.{ty})' instead"
                raise errors.TypingError(msg)
    return types.Function(make_callable_template(key=ty, typer=typer))


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.builtins.
        NumberClassAttribute.resolve___call__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fdaf0c7d0820130481bb2bd922985257b9281b670f0bafffe10e51cabf0d5081':
        warnings.warn(
            'numba.core.typing.builtins.NumberClassAttribute.resolve___call__ has changed'
            )
numba.core.typing.builtins.NumberClassAttribute.resolve___call__ = (
    resolve_number___call__)


def on_assign(self, states, assign):
    if assign.target.name == states['varname']:
        scope = states['scope']
        rbrak__aqvio = states['defmap']
        if len(rbrak__aqvio) == 0:
            ggglo__yjuot = assign.target
            numba.core.ssa._logger.debug('first assign: %s', ggglo__yjuot)
            if ggglo__yjuot.name not in scope.localvars:
                ggglo__yjuot = scope.define(assign.target.name, loc=assign.loc)
        else:
            ggglo__yjuot = scope.redefine(assign.target.name, loc=assign.loc)
        assign = ir.Assign(target=ggglo__yjuot, value=assign.value, loc=
            assign.loc)
        rbrak__aqvio[states['label']].append(assign)
    return assign


if _check_numba_change:
    lines = inspect.getsource(numba.core.ssa._FreshVarHandler.on_assign)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '922c4f9807455f81600b794bbab36f9c6edfecfa83fda877bf85f465db7865e8':
        warnings.warn('_FreshVarHandler on_assign has changed')
numba.core.ssa._FreshVarHandler.on_assign = on_assign


def get_np_ufunc_typ_lst(func):
    from numba.core import typing
    mln__zksr = []
    for nvtk__ucegf, gprl__aoel in typing.npydecl.registry.globals:
        if nvtk__ucegf == func:
            mln__zksr.append(gprl__aoel)
    for nvtk__ucegf, gprl__aoel in typing.templates.builtin_registry.globals:
        if nvtk__ucegf == func:
            mln__zksr.append(gprl__aoel)
    if len(mln__zksr) == 0:
        raise RuntimeError('type for func ', func, ' not found')
    return mln__zksr


def canonicalize_array_math(func_ir, typemap, calltypes, typingctx):
    import numpy
    from numba.core.ir_utils import arr_math, find_topo_order, mk_unique_var
    blocks = func_ir.blocks
    wsf__xoqf = {}
    jzx__fwc = find_topo_order(blocks)
    cuj__ykrp = {}
    for label in jzx__fwc:
        block = blocks[label]
        qwaym__qlfk = []
        for stmt in block.body:
            if isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr):
                dizzz__kevk = stmt.target.name
                uqxkt__czrf = stmt.value
                if (uqxkt__czrf.op == 'getattr' and uqxkt__czrf.attr in
                    arr_math and isinstance(typemap[uqxkt__czrf.value.name],
                    types.npytypes.Array)):
                    uqxkt__czrf = stmt.value
                    jvodv__becc = uqxkt__czrf.value
                    wsf__xoqf[dizzz__kevk] = jvodv__becc
                    scope = jvodv__becc.scope
                    loc = jvodv__becc.loc
                    dzu__gtiad = ir.Var(scope, mk_unique_var('$np_g_var'), loc)
                    typemap[dzu__gtiad.name] = types.misc.Module(numpy)
                    tmc__dft = ir.Global('np', numpy, loc)
                    frgne__burmm = ir.Assign(tmc__dft, dzu__gtiad, loc)
                    uqxkt__czrf.value = dzu__gtiad
                    qwaym__qlfk.append(frgne__burmm)
                    func_ir._definitions[dzu__gtiad.name] = [tmc__dft]
                    func = getattr(numpy, uqxkt__czrf.attr)
                    vkfb__dztb = get_np_ufunc_typ_lst(func)
                    cuj__ykrp[dizzz__kevk] = vkfb__dztb
                if (uqxkt__czrf.op == 'call' and uqxkt__czrf.func.name in
                    wsf__xoqf):
                    jvodv__becc = wsf__xoqf[uqxkt__czrf.func.name]
                    dhmev__kqn = calltypes.pop(uqxkt__czrf)
                    cfdt__tln = dhmev__kqn.args[:len(uqxkt__czrf.args)]
                    nojif__jwai = {name: typemap[gprl__aoel.name] for name,
                        gprl__aoel in uqxkt__czrf.kws}
                    yqay__sodxc = cuj__ykrp[uqxkt__czrf.func.name]
                    wym__zwcjf = None
                    for umhp__xruz in yqay__sodxc:
                        try:
                            wym__zwcjf = umhp__xruz.get_call_type(typingctx,
                                [typemap[jvodv__becc.name]] + list(
                                cfdt__tln), nojif__jwai)
                            typemap.pop(uqxkt__czrf.func.name)
                            typemap[uqxkt__czrf.func.name] = umhp__xruz
                            calltypes[uqxkt__czrf] = wym__zwcjf
                            break
                        except Exception as tnpc__ypis:
                            pass
                    if wym__zwcjf is None:
                        raise TypeError(
                            f'No valid template found for {uqxkt__czrf.func.name}'
                            )
                    uqxkt__czrf.args = [jvodv__becc] + uqxkt__czrf.args
            qwaym__qlfk.append(stmt)
        block.body = qwaym__qlfk


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.canonicalize_array_math)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b2200e9100613631cc554f4b640bc1181ba7cea0ece83630122d15b86941be2e':
        warnings.warn('canonicalize_array_math has changed')
numba.core.ir_utils.canonicalize_array_math = canonicalize_array_math
numba.parfors.parfor.canonicalize_array_math = canonicalize_array_math
numba.core.inline_closurecall.canonicalize_array_math = canonicalize_array_math


def _Numpy_Rules_ufunc_handle_inputs(cls, ufunc, args, kws):
    ksz__zto = ufunc.nin
    ssrpb__qcdgq = ufunc.nout
    fdl__vjc = ufunc.nargs
    assert fdl__vjc == ksz__zto + ssrpb__qcdgq
    if len(args) < ksz__zto:
        msg = "ufunc '{0}': not enough arguments ({1} found, {2} required)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), ksz__zto))
    if len(args) > fdl__vjc:
        msg = "ufunc '{0}': too many arguments ({1} found, {2} maximum)"
        raise TypingError(msg=msg.format(ufunc.__name__, len(args), fdl__vjc))
    args = [(a.as_array if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else a) for a in args]
    nogc__tyg = [(a.ndim if isinstance(a, types.ArrayCompatible) and not
        isinstance(a, types.Bytes) else 0) for a in args]
    ldqc__aplr = max(nogc__tyg)
    cmh__movbb = args[ksz__zto:]
    if not all(d == ldqc__aplr for d in nogc__tyg[ksz__zto:]):
        msg = "ufunc '{0}' called with unsuitable explicit output arrays."
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(isinstance(cojn__eolpq, types.ArrayCompatible) and not
        isinstance(cojn__eolpq, types.Bytes) for cojn__eolpq in cmh__movbb):
        msg = "ufunc '{0}' called with an explicit output that is not an array"
        raise TypingError(msg=msg.format(ufunc.__name__))
    if not all(cojn__eolpq.mutable for cojn__eolpq in cmh__movbb):
        msg = "ufunc '{0}' called with an explicit output that is read-only"
        raise TypingError(msg=msg.format(ufunc.__name__))
    hscmy__zxn = [(x.dtype if isinstance(x, types.ArrayCompatible) and not
        isinstance(x, types.Bytes) else x) for x in args]
    rkkh__pvt = None
    if ldqc__aplr > 0 and len(cmh__movbb) < ufunc.nout:
        rkkh__pvt = 'C'
        iqla__nqr = [(x.layout if isinstance(x, types.ArrayCompatible) and 
            not isinstance(x, types.Bytes) else '') for x in args]
        if 'C' not in iqla__nqr and 'F' in iqla__nqr:
            rkkh__pvt = 'F'
    return hscmy__zxn, cmh__movbb, ldqc__aplr, rkkh__pvt


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.npydecl.Numpy_rules_ufunc.
        _handle_inputs)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4b97c64ad9c3d50e082538795054f35cf6d2fe962c3ca40e8377a4601b344d5c':
        warnings.warn('Numpy_rules_ufunc._handle_inputs has changed')
numba.core.typing.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)
numba.np.ufunc.dufunc.npydecl.Numpy_rules_ufunc._handle_inputs = (
    _Numpy_Rules_ufunc_handle_inputs)


def DictType__init__(self, keyty, valty, initial_value=None):
    from numba.types import DictType, InitialValue, NoneType, Optional, Tuple, TypeRef, unliteral
    assert not isinstance(keyty, TypeRef)
    assert not isinstance(valty, TypeRef)
    keyty = unliteral(keyty)
    valty = unliteral(valty)
    if isinstance(keyty, (Optional, NoneType)):
        tcvh__zuxds = 'Dict.key_type cannot be of type {}'
        raise TypingError(tcvh__zuxds.format(keyty))
    if isinstance(valty, (Optional, NoneType)):
        tcvh__zuxds = 'Dict.value_type cannot be of type {}'
        raise TypingError(tcvh__zuxds.format(valty))
    self.key_type = keyty
    self.value_type = valty
    self.keyvalue_type = Tuple([keyty, valty])
    name = '{}[{},{}]<iv={}>'.format(self.__class__.__name__, keyty, valty,
        initial_value)
    super(DictType, self).__init__(name)
    InitialValue.__init__(self, initial_value)


if _check_numba_change:
    lines = inspect.getsource(numba.core.types.containers.DictType.__init__)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '475acd71224bd51526750343246e064ff071320c0d10c17b8b8ac81d5070d094':
        warnings.warn('DictType.__init__ has changed')
numba.core.types.containers.DictType.__init__ = DictType__init__


def _legalize_arg_types(self, args):
    for i, a in enumerate(args, start=1):
        if isinstance(a, types.Dispatcher):
            msg = (
                'Does not support function type inputs into with-context for arg {}'
                )
            raise errors.TypingError(msg.format(i))


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.ObjModeLiftedWith.
        _legalize_arg_types)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4793f44ebc7da8843e8f298e08cd8a5428b4b84b89fd9d5c650273fdb8fee5ee':
        warnings.warn('ObjModeLiftedWith._legalize_arg_types has changed')
numba.core.dispatcher.ObjModeLiftedWith._legalize_arg_types = (
    _legalize_arg_types)


def _overload_template_get_impl(self, args, kws):
    pmra__gffgq = self.context, tuple(args), tuple(kws.items())
    try:
        impl, args = self._impl_cache[pmra__gffgq]
        return impl, args
    except KeyError as tnpc__ypis:
        pass
    impl, args = self._build_impl(pmra__gffgq, args, kws)
    return impl, args


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.templates.
        _OverloadFunctionTemplate._get_impl)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '4e27d07b214ca16d6e8ed88f70d886b6b095e160d8f77f8df369dd4ed2eb3fae':
        warnings.warn(
            'numba.core.typing.templates._OverloadFunctionTemplate._get_impl has changed'
            )
numba.core.typing.templates._OverloadFunctionTemplate._get_impl = (
    _overload_template_get_impl)


def trim_empty_parfor_branches(parfor):
    grmya__twmm = False
    blocks = parfor.loop_body.copy()
    for label, block in blocks.items():
        if len(block.body):
            owdzj__nrty = block.body[-1]
            if isinstance(owdzj__nrty, ir.Branch):
                if len(blocks[owdzj__nrty.truebr].body) == 1 and len(blocks
                    [owdzj__nrty.falsebr].body) == 1:
                    vrauu__mvqk = blocks[owdzj__nrty.truebr].body[0]
                    ltmfq__ded = blocks[owdzj__nrty.falsebr].body[0]
                    if isinstance(vrauu__mvqk, ir.Jump) and isinstance(
                        ltmfq__ded, ir.Jump
                        ) and vrauu__mvqk.target == ltmfq__ded.target:
                        parfor.loop_body[label].body[-1] = ir.Jump(vrauu__mvqk
                            .target, owdzj__nrty.loc)
                        grmya__twmm = True
                elif len(blocks[owdzj__nrty.truebr].body) == 1:
                    vrauu__mvqk = blocks[owdzj__nrty.truebr].body[0]
                    if isinstance(vrauu__mvqk, ir.Jump
                        ) and vrauu__mvqk.target == owdzj__nrty.falsebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(vrauu__mvqk
                            .target, owdzj__nrty.loc)
                        grmya__twmm = True
                elif len(blocks[owdzj__nrty.falsebr].body) == 1:
                    ltmfq__ded = blocks[owdzj__nrty.falsebr].body[0]
                    if isinstance(ltmfq__ded, ir.Jump
                        ) and ltmfq__ded.target == owdzj__nrty.truebr:
                        parfor.loop_body[label].body[-1] = ir.Jump(ltmfq__ded
                            .target, owdzj__nrty.loc)
                        grmya__twmm = True
    return grmya__twmm


def remove_dead_parfor(parfor, lives, lives_n_aliases, arg_aliases,
    alias_map, func_ir, typemap):
    from numba.core.analysis import compute_cfg_from_blocks, compute_live_map, compute_use_defs
    from numba.core.ir_utils import find_topo_order
    from numba.parfors.parfor import _add_liveness_return_block, _update_parfor_get_setitems, dummy_return_in_loop_body, get_index_var, remove_dead_parfor_recursive, simplify_parfor_body_CFG
    with dummy_return_in_loop_body(parfor.loop_body):
        ehz__jvq = find_topo_order(parfor.loop_body)
    mrkko__earg = ehz__jvq[0]
    cspa__fzr = {}
    _update_parfor_get_setitems(parfor.loop_body[mrkko__earg].body, parfor.
        index_var, alias_map, cspa__fzr, lives_n_aliases)
    feqt__ilc = set(cspa__fzr.keys())
    for yjiah__jvqvq in ehz__jvq:
        if yjiah__jvqvq == mrkko__earg:
            continue
        for stmt in parfor.loop_body[yjiah__jvqvq].body:
            if (isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.
                Expr) and stmt.value.op == 'getitem' and stmt.value.index.
                name == parfor.index_var.name):
                continue
            uxks__oldd = set(gprl__aoel.name for gprl__aoel in stmt.list_vars()
                )
            crk__ycldd = uxks__oldd & feqt__ilc
            for a in crk__ycldd:
                cspa__fzr.pop(a, None)
    for yjiah__jvqvq in ehz__jvq:
        if yjiah__jvqvq == mrkko__earg:
            continue
        block = parfor.loop_body[yjiah__jvqvq]
        zzg__wipbn = cspa__fzr.copy()
        _update_parfor_get_setitems(block.body, parfor.index_var, alias_map,
            zzg__wipbn, lives_n_aliases)
    blocks = parfor.loop_body.copy()
    ggd__miz = max(blocks.keys())
    dwgh__juyj, keh__mvk = _add_liveness_return_block(blocks,
        lives_n_aliases, typemap)
    qrxg__jyc = ir.Jump(dwgh__juyj, ir.Loc('parfors_dummy', -1))
    blocks[ggd__miz].body.append(qrxg__jyc)
    pxp__htka = compute_cfg_from_blocks(blocks)
    sqv__isw = compute_use_defs(blocks)
    fqzfn__szywl = compute_live_map(pxp__htka, blocks, sqv__isw.usemap,
        sqv__isw.defmap)
    alias_set = set(alias_map.keys())
    for label, block in blocks.items():
        qwaym__qlfk = []
        pqoo__qbijr = {gprl__aoel.name for gprl__aoel in block.terminator.
            list_vars()}
        for tymrx__jrju, rwbdh__dqqw in pxp__htka.successors(label):
            pqoo__qbijr |= fqzfn__szywl[tymrx__jrju]
        for stmt in reversed(block.body):
            psocf__bfv = pqoo__qbijr & alias_set
            for gprl__aoel in psocf__bfv:
                pqoo__qbijr |= alias_map[gprl__aoel]
            if (isinstance(stmt, (ir.StaticSetItem, ir.SetItem)) and 
                get_index_var(stmt).name == parfor.index_var.name and stmt.
                target.name not in pqoo__qbijr and stmt.target.name not in
                arg_aliases):
                continue
            elif isinstance(stmt, ir.Assign) and isinstance(stmt.value, ir.Expr
                ) and stmt.value.op == 'call':
                iofg__jtp = guard(find_callname, func_ir, stmt.value)
                if iofg__jtp == ('setna', 'bodo.libs.array_kernels'
                    ) and stmt.value.args[0
                    ].name not in pqoo__qbijr and stmt.value.args[0
                    ].name not in arg_aliases:
                    continue
            pqoo__qbijr |= {gprl__aoel.name for gprl__aoel in stmt.list_vars()}
            qwaym__qlfk.append(stmt)
        qwaym__qlfk.reverse()
        block.body = qwaym__qlfk
    typemap.pop(keh__mvk.name)
    blocks[ggd__miz].body.pop()
    grmya__twmm = True
    while grmya__twmm:
        """
        Process parfor body recursively.
        Note that this is the only place in this function that uses the
        argument lives instead of lives_n_aliases.  The former does not
        include the aliases of live variables but only the live variable
        names themselves.  See a comment in this function for how that
        is used.
        """
        remove_dead_parfor_recursive(parfor, lives, arg_aliases, alias_map,
            func_ir, typemap)
        simplify_parfor_body_CFG(func_ir.blocks)
        grmya__twmm = trim_empty_parfor_branches(parfor)
    ovzxq__jfs = len(parfor.init_block.body) == 0
    for block in parfor.loop_body.values():
        ovzxq__jfs &= len(block.body) == 0
    if ovzxq__jfs:
        return None
    return parfor


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.remove_dead_parfor)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1c9b008a7ead13e988e1efe67618d8f87f0b9f3d092cc2cd6bfcd806b1fdb859':
        warnings.warn('remove_dead_parfor has changed')
numba.parfors.parfor.remove_dead_parfor = remove_dead_parfor
numba.core.ir_utils.remove_dead_extensions[numba.parfors.parfor.Parfor
    ] = remove_dead_parfor


def simplify_parfor_body_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.parfors.parfor import Parfor
    kevwd__xer = 0
    for block in blocks.values():
        for stmt in block.body:
            if isinstance(stmt, Parfor):
                kevwd__xer += 1
                parfor = stmt
                mkg__qnl = parfor.loop_body[max(parfor.loop_body.keys())]
                scope = mkg__qnl.scope
                loc = ir.Loc('parfors_dummy', -1)
                ywiw__xxfrm = ir.Var(scope, mk_unique_var('$const'), loc)
                mkg__qnl.body.append(ir.Assign(ir.Const(0, loc),
                    ywiw__xxfrm, loc))
                mkg__qnl.body.append(ir.Return(ywiw__xxfrm, loc))
                pxp__htka = compute_cfg_from_blocks(parfor.loop_body)
                for qoxrg__jtkic in pxp__htka.dead_nodes():
                    del parfor.loop_body[qoxrg__jtkic]
                parfor.loop_body = simplify_CFG(parfor.loop_body)
                mkg__qnl = parfor.loop_body[max(parfor.loop_body.keys())]
                mkg__qnl.body.pop()
                mkg__qnl.body.pop()
                simplify_parfor_body_CFG(parfor.loop_body)
    return kevwd__xer


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.parfor.simplify_parfor_body_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '437ae96a5e8ec64a2b69a4f23ba8402a1d170262a5400aa0aa7bfe59e03bf726':
        warnings.warn('simplify_parfor_body_CFG has changed')
numba.parfors.parfor.simplify_parfor_body_CFG = simplify_parfor_body_CFG


def simplify_CFG(blocks):
    from numba.core.analysis import compute_cfg_from_blocks
    from numba.core.ir_utils import merge_adjacent_blocks, rename_labels
    pxp__htka = compute_cfg_from_blocks(blocks)

    def find_single_branch(label):
        block = blocks[label]
        return len(block.body) == 1 and isinstance(block.body[0], ir.Branch
            ) and label != pxp__htka.entry_point()
    wxt__wjuqo = list(filter(find_single_branch, blocks.keys()))
    xwt__qvii = set()
    for label in wxt__wjuqo:
        inst = blocks[label].body[0]
        rwv__dhk = pxp__htka.predecessors(label)
        joehv__worzf = True
        for dqcu__avcj, vtp__rty in rwv__dhk:
            block = blocks[dqcu__avcj]
            if isinstance(block.body[-1], ir.Jump):
                block.body[-1] = copy.copy(inst)
            else:
                joehv__worzf = False
        if joehv__worzf:
            xwt__qvii.add(label)
    for label in xwt__qvii:
        del blocks[label]
    merge_adjacent_blocks(blocks)
    return rename_labels(blocks)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.simplify_CFG)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '0b3f2add05e5691155f08fc5945956d5cca5e068247d52cff8efb161b76388b7':
        warnings.warn('numba.core.ir_utils.simplify_CFG has changed')
numba.core.ir_utils.simplify_CFG = simplify_CFG


def _lifted_compile(self, sig):
    import numba.core.event as ev
    from numba.core import compiler, sigutils
    from numba.core.compiler_lock import global_compiler_lock
    from numba.core.ir_utils import remove_dels
    with ExitStack() as scope:
        cres = None

        def cb_compiler(dur):
            if cres is not None:
                self._callback_add_compiler_timer(dur, cres)

        def cb_llvm(dur):
            if cres is not None:
                self._callback_add_llvm_timer(dur, cres)
        scope.enter_context(ev.install_timer('numba:compiler_lock',
            cb_compiler))
        scope.enter_context(ev.install_timer('numba:llvm_lock', cb_llvm))
        scope.enter_context(global_compiler_lock)
        with self._compiling_counter:
            flags = self.flags
            args, return_type = sigutils.normalize_signature(sig)
            fdy__vqfz = self.overloads.get(tuple(args))
            if fdy__vqfz is not None:
                return fdy__vqfz.entry_point
            self._pre_compile(args, return_type, flags)
            hkt__amdji = self.func_ir
            cxhzq__nngeq = dict(dispatcher=self, args=args, return_type=
                return_type)
            with ev.trigger_event('numba:compile', data=cxhzq__nngeq):
                cres = compiler.compile_ir(typingctx=self.typingctx,
                    targetctx=self.targetctx, func_ir=hkt__amdji, args=args,
                    return_type=return_type, flags=flags, locals=self.
                    locals, lifted=(), lifted_from=self.lifted_from,
                    is_lifted_loop=True)
                if cres.typing_error is not None and not flags.enable_pyobject:
                    raise cres.typing_error
                self.add_overload(cres)
            remove_dels(self.func_ir.blocks)
            return cres.entry_point


if _check_numba_change:
    lines = inspect.getsource(numba.core.dispatcher.LiftedCode.compile)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '1351ebc5d8812dc8da167b30dad30eafb2ca9bf191b49aaed6241c21e03afff1':
        warnings.warn('numba.core.dispatcher.LiftedCode.compile has changed')
numba.core.dispatcher.LiftedCode.compile = _lifted_compile


def compile_ir(typingctx, targetctx, func_ir, args, return_type, flags,
    locals, lifted=(), lifted_from=None, is_lifted_loop=False, library=None,
    pipeline_class=Compiler):
    if is_lifted_loop:
        fapi__uidl = copy.deepcopy(flags)
        fapi__uidl.no_rewrites = True

        def compile_local(the_ir, the_flags):
            gyb__yubct = pipeline_class(typingctx, targetctx, library, args,
                return_type, the_flags, locals)
            return gyb__yubct.compile_ir(func_ir=the_ir, lifted=lifted,
                lifted_from=lifted_from)
        dqnrw__wwn = compile_local(func_ir, fapi__uidl)
        mlb__dgimn = None
        if not flags.no_rewrites:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', errors.NumbaWarning)
                try:
                    mlb__dgimn = compile_local(func_ir, flags)
                except Exception as tnpc__ypis:
                    pass
        if mlb__dgimn is not None:
            cres = mlb__dgimn
        else:
            cres = dqnrw__wwn
        return cres
    else:
        gyb__yubct = pipeline_class(typingctx, targetctx, library, args,
            return_type, flags, locals)
        return gyb__yubct.compile_ir(func_ir=func_ir, lifted=lifted,
            lifted_from=lifted_from)


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.compile_ir)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'c48ce5493f4c43326e8cbdd46f3ea038b2b9045352d9d25894244798388e5e5b':
        warnings.warn('numba.core.compiler.compile_ir has changed')
numba.core.compiler.compile_ir = compile_ir


def make_constant_array(self, builder, typ, ary):
    import math
    from llvmlite import ir as lir
    rtlj__sjfh = self.get_data_type(typ.dtype)
    jwl__det = 10 ** 7
    if self.allow_dynamic_globals and (typ.layout not in 'FC' or ary.nbytes >
        jwl__det):
        uqjiq__vwgt = ary.ctypes.data
        weh__topbt = self.add_dynamic_addr(builder, uqjiq__vwgt, info=str(
            type(uqjiq__vwgt)))
        svln__fsuh = self.add_dynamic_addr(builder, id(ary), info=str(type(
            ary)))
        self.global_arrays.append(ary)
    else:
        aic__xzsnr = ary.flatten(order=typ.layout)
        if isinstance(typ.dtype, (types.NPDatetime, types.NPTimedelta)):
            aic__xzsnr = aic__xzsnr.view('int64')
        val = bytearray(aic__xzsnr.data)
        jmymq__kxjgy = lir.Constant(lir.ArrayType(lir.IntType(8), len(val)),
            val)
        weh__topbt = cgutils.global_constant(builder, '.const.array.data',
            jmymq__kxjgy)
        weh__topbt.align = self.get_abi_alignment(rtlj__sjfh)
        svln__fsuh = None
    hqq__aypd = self.get_value_type(types.intp)
    wtq__qrr = [self.get_constant(types.intp, pyyl__eawid) for pyyl__eawid in
        ary.shape]
    sdin__trqsb = lir.Constant(lir.ArrayType(hqq__aypd, len(wtq__qrr)),
        wtq__qrr)
    ggqj__yghoa = [self.get_constant(types.intp, pyyl__eawid) for
        pyyl__eawid in ary.strides]
    yan__obrg = lir.Constant(lir.ArrayType(hqq__aypd, len(ggqj__yghoa)),
        ggqj__yghoa)
    piis__deg = self.get_constant(types.intp, ary.dtype.itemsize)
    nkvn__aoloh = self.get_constant(types.intp, math.prod(ary.shape))
    return lir.Constant.literal_struct([self.get_constant_null(types.
        MemInfoPointer(typ.dtype)), self.get_constant_null(types.pyobject),
        nkvn__aoloh, piis__deg, weh__topbt.bitcast(self.get_value_type(
        types.CPointer(typ.dtype))), sdin__trqsb, yan__obrg])


if _check_numba_change:
    lines = inspect.getsource(numba.core.base.BaseContext.make_constant_array)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5721b5360b51f782f79bd794f7bf4d48657911ecdc05c30db22fd55f15dad821':
        warnings.warn(
            'numba.core.base.BaseContext.make_constant_array has changed')
numba.core.base.BaseContext.make_constant_array = make_constant_array


def _define_atomic_inc_dec(module, op, ordering):
    from llvmlite import ir as lir
    from numba.core.runtime.nrtdynmod import _word_type
    ozjol__rurre = lir.FunctionType(_word_type, [_word_type.as_pointer()])
    nqixj__mlta = lir.Function(module, ozjol__rurre, name='nrt_atomic_{0}'.
        format(op))
    [atqi__yspzr] = nqixj__mlta.args
    hasf__jgku = nqixj__mlta.append_basic_block()
    builder = lir.IRBuilder(hasf__jgku)
    fzw__gxxw = lir.Constant(_word_type, 1)
    if False:
        awsg__vkn = builder.atomic_rmw(op, atqi__yspzr, fzw__gxxw, ordering
            =ordering)
        res = getattr(builder, op)(awsg__vkn, fzw__gxxw)
        builder.ret(res)
    else:
        awsg__vkn = builder.load(atqi__yspzr)
        brcs__pvl = getattr(builder, op)(awsg__vkn, fzw__gxxw)
        kaxf__brrqb = builder.icmp_signed('!=', awsg__vkn, lir.Constant(
            awsg__vkn.type, -1))
        with cgutils.if_likely(builder, kaxf__brrqb):
            builder.store(brcs__pvl, atqi__yspzr)
        builder.ret(brcs__pvl)
    return nqixj__mlta


if _check_numba_change:
    lines = inspect.getsource(numba.core.runtime.nrtdynmod.
        _define_atomic_inc_dec)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '9cc02c532b2980b6537b702f5608ea603a1ff93c6d3c785ae2cf48bace273f48':
        warnings.warn(
            'numba.core.runtime.nrtdynmod._define_atomic_inc_dec has changed')
numba.core.runtime.nrtdynmod._define_atomic_inc_dec = _define_atomic_inc_dec


def NativeLowering_run_pass(self, state):
    from llvmlite import binding as llvm
    from numba.core import funcdesc, lowering
    from numba.core.typed_passes import fallback_context
    if state.library is None:
        ghies__uuq = state.targetctx.codegen()
        state.library = ghies__uuq.create_library(state.func_id.func_qualname)
        state.library.enable_object_caching()
    library = state.library
    targetctx = state.targetctx
    qmta__kpxut = state.func_ir
    typemap = state.typemap
    lqnj__trvxu = state.return_type
    calltypes = state.calltypes
    flags = state.flags
    metadata = state.metadata
    wsrk__rxbc = llvm.passmanagers.dump_refprune_stats()
    msg = 'Function %s failed at nopython mode lowering' % (state.func_id.
        func_name,)
    with fallback_context(state, msg):
        fndesc = funcdesc.PythonFunctionDescriptor.from_specialized_function(
            qmta__kpxut, typemap, lqnj__trvxu, calltypes, mangler=targetctx
            .mangler, inline=flags.forceinline, noalias=flags.noalias,
            abi_tags=[flags.get_mangle_string()])
        targetctx.global_arrays = []
        with targetctx.push_code_library(library):
            cboim__pwui = lowering.Lower(targetctx, library, fndesc,
                qmta__kpxut, metadata=metadata)
            cboim__pwui.lower()
            if not flags.no_cpython_wrapper:
                cboim__pwui.create_cpython_wrapper(flags.release_gil)
            if not flags.no_cfunc_wrapper:
                for t in state.args:
                    if isinstance(t, (types.Omitted, types.Generator)):
                        break
                else:
                    if isinstance(lqnj__trvxu, (types.Optional, types.
                        Generator)):
                        pass
                    else:
                        cboim__pwui.create_cfunc_wrapper()
            env = cboim__pwui.env
            bdgp__fauv = cboim__pwui.call_helper
            del cboim__pwui
        from numba.core.compiler import _LowerResult
        if flags.no_compile:
            state['cr'] = _LowerResult(fndesc, bdgp__fauv, cfunc=None, env=env)
        else:
            ptui__byq = targetctx.get_executable(library, fndesc, env)
            targetctx.insert_user_function(ptui__byq, fndesc, [library])
            state['cr'] = _LowerResult(fndesc, bdgp__fauv, cfunc=ptui__byq,
                env=env)
        metadata['global_arrs'] = targetctx.global_arrays
        targetctx.global_arrays = []
        vaz__tlbji = llvm.passmanagers.dump_refprune_stats()
        metadata['prune_stats'] = vaz__tlbji - wsrk__rxbc
        metadata['llvm_pass_timings'] = library.recorded_timings
    return True


if _check_numba_change:
    lines = inspect.getsource(numba.core.typed_passes.NativeLowering.run_pass)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'a777ce6ce1bb2b1cbaa3ac6c2c0e2adab69a9c23888dff5f1cbb67bfb176b5de':
        warnings.warn(
            'numba.core.typed_passes.NativeLowering.run_pass has changed')
numba.core.typed_passes.NativeLowering.run_pass = NativeLowering_run_pass


def _python_list_to_native(typ, obj, c, size, listptr, errorptr):
    from llvmlite import ir as lir
    from numba.core.boxing import _NumbaTypeHelper
    from numba.cpython import listobj

    def check_element_type(nth, itemobj, expected_typobj):
        brh__gty = nth.typeof(itemobj)
        with c.builder.if_then(cgutils.is_null(c.builder, brh__gty), likely
            =False):
            c.builder.store(cgutils.true_bit, errorptr)
            banr__mmnst.do_break()
        cyz__yrmat = c.builder.icmp_signed('!=', brh__gty, expected_typobj)
        if not isinstance(typ.dtype, types.Optional):
            with c.builder.if_then(cyz__yrmat, likely=False):
                c.builder.store(cgutils.true_bit, errorptr)
                c.pyapi.err_format('PyExc_TypeError',
                    "can't unbox heterogeneous list: %S != %S",
                    expected_typobj, brh__gty)
                c.pyapi.decref(brh__gty)
                banr__mmnst.do_break()
        c.pyapi.decref(brh__gty)
    wng__bws, list = listobj.ListInstance.allocate_ex(c.context, c.builder,
        typ, size)
    with c.builder.if_else(wng__bws, likely=True) as (ioj__zeq, skjs__kwl):
        with ioj__zeq:
            list.size = size
            nzh__tstpg = lir.Constant(size.type, 0)
            with c.builder.if_then(c.builder.icmp_signed('>', size,
                nzh__tstpg), likely=True):
                with _NumbaTypeHelper(c) as nth:
                    expected_typobj = nth.typeof(c.pyapi.list_getitem(obj,
                        nzh__tstpg))
                    with cgutils.for_range(c.builder, size) as banr__mmnst:
                        itemobj = c.pyapi.list_getitem(obj, banr__mmnst.index)
                        check_element_type(nth, itemobj, expected_typobj)
                        zovgg__ddtj = c.unbox(typ.dtype, itemobj)
                        with c.builder.if_then(zovgg__ddtj.is_error, likely
                            =False):
                            c.builder.store(cgutils.true_bit, errorptr)
                            banr__mmnst.do_break()
                        list.setitem(banr__mmnst.index, zovgg__ddtj.value,
                            incref=False)
                    c.pyapi.decref(expected_typobj)
            if typ.reflected:
                list.parent = obj
            with c.builder.if_then(c.builder.not_(c.builder.load(errorptr)),
                likely=False):
                c.pyapi.object_set_private_data(obj, list.meminfo)
            list.set_dirty(False)
            c.builder.store(list.value, listptr)
        with skjs__kwl:
            c.builder.store(cgutils.true_bit, errorptr)
    with c.builder.if_then(c.builder.load(errorptr)):
        c.context.nrt.decref(c.builder, typ, list.value)


if _check_numba_change:
    lines = inspect.getsource(numba.core.boxing._python_list_to_native)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f8e546df8b07adfe74a16b6aafb1d4fddbae7d3516d7944b3247cc7c9b7ea88a':
        warnings.warn('numba.core.boxing._python_list_to_native has changed')
numba.core.boxing._python_list_to_native = _python_list_to_native


def make_string_from_constant(context, builder, typ, literal_string):
    from llvmlite import ir as lir
    from numba.cpython.hashing import _Py_hash_t
    from numba.cpython.unicode import compile_time_get_string_data
    ubrem__skthy, gqoj__ioo, wyx__qirux, eog__pgatb, zrk__uyh = (
        compile_time_get_string_data(literal_string))
    zcgt__ynb = builder.module
    gv = context.insert_const_bytes(zcgt__ynb, ubrem__skthy)
    return lir.Constant.literal_struct([gv, context.get_constant(types.intp,
        gqoj__ioo), context.get_constant(types.int32, wyx__qirux), context.
        get_constant(types.uint32, eog__pgatb), context.get_constant(
        _Py_hash_t, -1), context.get_constant_null(types.MemInfoPointer(
        types.voidptr)), context.get_constant_null(types.pyobject)])


if _check_numba_change:
    lines = inspect.getsource(numba.cpython.unicode.make_string_from_constant)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '525bd507383e06152763e2f046dae246cd60aba027184f50ef0fc9a80d4cd7fa':
        warnings.warn(
            'numba.cpython.unicode.make_string_from_constant has changed')
numba.cpython.unicode.make_string_from_constant = make_string_from_constant


def parse_shape(shape):
    pjf__wzia = None
    if isinstance(shape, types.Integer):
        pjf__wzia = 1
    elif isinstance(shape, (types.Tuple, types.UniTuple)):
        if all(isinstance(pyyl__eawid, (types.Integer, types.IntEnumMember)
            ) for pyyl__eawid in shape):
            pjf__wzia = len(shape)
    return pjf__wzia


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.npydecl.parse_shape)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'e62e3ff09d36df5ac9374055947d6a8be27160ce32960d3ef6cb67f89bd16429':
        warnings.warn('numba.core.typing.npydecl.parse_shape has changed')
numba.core.typing.npydecl.parse_shape = parse_shape


def _get_names(self, obj):
    if isinstance(obj, ir.Var) or isinstance(obj, str):
        name = obj if isinstance(obj, str) else obj.name
        if name not in self.typemap:
            return name,
        typ = self.typemap[name]
        if isinstance(typ, (types.BaseTuple, types.ArrayCompatible)):
            pjf__wzia = typ.ndim if isinstance(typ, types.ArrayCompatible
                ) else len(typ)
            if pjf__wzia == 0:
                return name,
            else:
                return tuple('{}#{}'.format(name, i) for i in range(pjf__wzia))
        else:
            return name,
    elif isinstance(obj, ir.Const):
        if isinstance(obj.value, tuple):
            return obj.value
        else:
            return obj.value,
    elif isinstance(obj, tuple):

        def get_names(x):
            okc__irac = self._get_names(x)
            if len(okc__irac) != 0:
                return okc__irac[0]
            return okc__irac
        return tuple(get_names(x) for x in obj)
    elif isinstance(obj, int):
        return obj,
    return ()


def get_equiv_const(self, obj):
    okc__irac = self._get_names(obj)
    if len(okc__irac) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_const(okc__irac[0])


def get_equiv_set(self, obj):
    okc__irac = self._get_names(obj)
    if len(okc__irac) != 1:
        return None
    return super(numba.parfors.array_analysis.ShapeEquivSet, self
        ).get_equiv_set(okc__irac[0])


if _check_numba_change:
    for name, orig, new, hash in ((
        'numba.parfors.array_analysis.ShapeEquivSet._get_names', numba.
        parfors.array_analysis.ShapeEquivSet._get_names, _get_names,
        '8c9bf136109028d5445fd0a82387b6abeb70c23b20b41e2b50c34ba5359516ee'),
        ('numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const',
        numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const,
        get_equiv_const,
        'bef410ca31a9e29df9ee74a4a27d339cc332564e4a237828b8a4decf625ce44e'),
        ('numba.parfors.array_analysis.ShapeEquivSet.get_equiv_set', numba.
        parfors.array_analysis.ShapeEquivSet.get_equiv_set, get_equiv_set,
        'ec936d340c488461122eb74f28a28b88227cb1f1bca2b9ba3c19258cfe1eb40a')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
numba.parfors.array_analysis.ShapeEquivSet._get_names = _get_names
numba.parfors.array_analysis.ShapeEquivSet.get_equiv_const = get_equiv_const
numba.parfors.array_analysis.ShapeEquivSet.get_equiv_set = get_equiv_set


def raise_on_unsupported_feature(func_ir, typemap):
    import numpy
    wvr__qtui = []
    for pco__ixlt in func_ir.arg_names:
        if pco__ixlt in typemap and isinstance(typemap[pco__ixlt], types.
            containers.UniTuple) and typemap[pco__ixlt].count > 1000:
            msg = (
                """Tuple '{}' length must be smaller than 1000.
Large tuples lead to the generation of a prohibitively large LLVM IR which causes excessive memory pressure and large compile times.
As an alternative, the use of a 'list' is recommended in place of a 'tuple' as lists do not suffer from this problem."""
                .format(pco__ixlt))
            raise errors.UnsupportedError(msg, func_ir.loc)
    for zcnv__mkbrq in func_ir.blocks.values():
        for stmt in zcnv__mkbrq.find_insts(ir.Assign):
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'make_function':
                    val = stmt.value
                    wwg__alsrp = getattr(val, 'code', None)
                    if wwg__alsrp is not None:
                        if getattr(val, 'closure', None) is not None:
                            jwu__dxfh = '<creating a function from a closure>'
                            ddt__egw = ''
                        else:
                            jwu__dxfh = wwg__alsrp.co_name
                            ddt__egw = '(%s) ' % jwu__dxfh
                    else:
                        jwu__dxfh = '<could not ascertain use case>'
                        ddt__egw = ''
                    msg = (
                        'Numba encountered the use of a language feature it does not support in this context: %s (op code: make_function not supported). If the feature is explicitly supported it is likely that the result of the expression %sis being used in an unsupported manner.'
                         % (jwu__dxfh, ddt__egw))
                    raise errors.UnsupportedError(msg, stmt.value.loc)
            if isinstance(stmt.value, (ir.Global, ir.FreeVar)):
                val = stmt.value
                val = getattr(val, 'value', None)
                if val is None:
                    continue
                prz__lzlm = False
                if isinstance(val, pytypes.FunctionType):
                    prz__lzlm = val in {numba.gdb, numba.gdb_init}
                if not prz__lzlm:
                    prz__lzlm = getattr(val, '_name', '') == 'gdb_internal'
                if prz__lzlm:
                    wvr__qtui.append(stmt.loc)
            if isinstance(stmt.value, ir.Expr):
                if stmt.value.op == 'getattr' and stmt.value.attr == 'view':
                    var = stmt.value.value.name
                    if isinstance(typemap[var], types.Array):
                        continue
                    qmko__khv = func_ir.get_definition(var)
                    kumzs__mgq = guard(find_callname, func_ir, qmko__khv)
                    if kumzs__mgq and kumzs__mgq[1] == 'numpy':
                        ty = getattr(numpy, kumzs__mgq[0])
                        if numpy.issubdtype(ty, numpy.integer
                            ) or numpy.issubdtype(ty, numpy.floating):
                            continue
                    fhz__mghp = '' if var.startswith('$') else "'{}' ".format(
                        var)
                    raise TypingError(
                        "'view' can only be called on NumPy dtypes, try wrapping the variable {}with 'np.<dtype>()'"
                        .format(fhz__mghp), loc=stmt.loc)
            if isinstance(stmt.value, ir.Global):
                ty = typemap[stmt.target.name]
                msg = (
                    "The use of a %s type, assigned to variable '%s' in globals, is not supported as globals are considered compile-time constants and there is no known way to compile a %s type as a constant."
                    )
                if isinstance(ty, types.ListType):
                    raise TypingError(msg % (ty, stmt.value.name, ty), loc=
                        stmt.loc)
            if isinstance(stmt.value, ir.Yield) and not func_ir.is_generator:
                msg = 'The use of generator expressions is unsupported.'
                raise errors.UnsupportedError(msg, loc=stmt.loc)
    if len(wvr__qtui) > 1:
        msg = """Calling either numba.gdb() or numba.gdb_init() more than once in a function is unsupported (strange things happen!), use numba.gdb_breakpoint() to create additional breakpoints instead.

Relevant documentation is available here:
https://numba.pydata.org/numba-doc/latest/user/troubleshoot.html/troubleshoot.html#using-numba-s-direct-gdb-bindings-in-nopython-mode

Conflicting calls found at:
 %s"""
        pgway__byab = '\n'.join([x.strformat() for x in wvr__qtui])
        raise errors.UnsupportedError(msg % pgway__byab)


if _check_numba_change:
    lines = inspect.getsource(numba.core.ir_utils.raise_on_unsupported_feature)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '237a4fe8395a40899279c718bc3754102cd2577463ef2f48daceea78d79b2d5e':
        warnings.warn(
            'numba.core.ir_utils.raise_on_unsupported_feature has changed')
numba.core.ir_utils.raise_on_unsupported_feature = raise_on_unsupported_feature
numba.core.typed_passes.raise_on_unsupported_feature = (
    raise_on_unsupported_feature)


@typeof_impl.register(dict)
def _typeof_dict(val, c):
    if len(val) == 0:
        raise ValueError('Cannot type empty dict')
    nvtk__ucegf, gprl__aoel = next(iter(val.items()))
    alyuo__hiof = typeof_impl(nvtk__ucegf, c)
    alg__fdb = typeof_impl(gprl__aoel, c)
    if alyuo__hiof is None or alg__fdb is None:
        raise ValueError(
            f'Cannot type dict element type {type(nvtk__ucegf)}, {type(gprl__aoel)}'
            )
    return types.DictType(alyuo__hiof, alg__fdb)


def unbox_dicttype(typ, val, c):
    from llvmlite import ir as lir
    from numba.typed import dictobject
    from numba.typed.typeddict import Dict
    context = c.context
    oln__sur = cgutils.alloca_once_value(c.builder, val)
    tmls__zcn = c.pyapi.object_hasattr_string(val, '_opaque')
    zwber__ldr = c.builder.icmp_unsigned('==', tmls__zcn, lir.Constant(
        tmls__zcn.type, 0))
    oyjm__duc = typ.key_type
    zvnc__whjav = typ.value_type

    def make_dict():
        return numba.typed.Dict.empty(oyjm__duc, zvnc__whjav)

    def copy_dict(out_dict, in_dict):
        for nvtk__ucegf, gprl__aoel in in_dict.items():
            out_dict[nvtk__ucegf] = gprl__aoel
    with c.builder.if_then(zwber__ldr):
        fsyhe__wyf = c.pyapi.unserialize(c.pyapi.serialize_object(make_dict))
        kwtaq__daa = c.pyapi.call_function_objargs(fsyhe__wyf, [])
        kcrl__sdy = c.pyapi.unserialize(c.pyapi.serialize_object(copy_dict))
        c.pyapi.call_function_objargs(kcrl__sdy, [kwtaq__daa, val])
        c.builder.store(kwtaq__daa, oln__sur)
    val = c.builder.load(oln__sur)
    bpw__rlh = c.pyapi.unserialize(c.pyapi.serialize_object(Dict))
    fdj__senpx = c.pyapi.object_type(val)
    bhxtr__gtvko = c.builder.icmp_unsigned('==', fdj__senpx, bpw__rlh)
    with c.builder.if_else(bhxtr__gtvko) as (wjm__egz, utb__sbran):
        with wjm__egz:
            anj__ejqw = c.pyapi.object_getattr_string(val, '_opaque')
            cqai__aqgzn = types.MemInfoPointer(types.voidptr)
            zovgg__ddtj = c.unbox(cqai__aqgzn, anj__ejqw)
            mi = zovgg__ddtj.value
            uodjk__tsbt = cqai__aqgzn, typeof(typ)

            def convert(mi, typ):
                return dictobject._from_meminfo(mi, typ)
            sig = signature(typ, *uodjk__tsbt)
            kgh__gzm = context.get_constant_null(uodjk__tsbt[1])
            args = mi, kgh__gzm
            sfis__uoub, umw__ztdpv = c.pyapi.call_jit_code(convert, sig, args)
            c.context.nrt.decref(c.builder, typ, umw__ztdpv)
            c.pyapi.decref(anj__ejqw)
            yyqg__pvy = c.builder.basic_block
        with utb__sbran:
            c.pyapi.err_format('PyExc_TypeError',
                "can't unbox a %S as a %S", fdj__senpx, bpw__rlh)
            uhtu__kxr = c.builder.basic_block
    kzl__almc = c.builder.phi(umw__ztdpv.type)
    lkfu__ichr = c.builder.phi(sfis__uoub.type)
    kzl__almc.add_incoming(umw__ztdpv, yyqg__pvy)
    kzl__almc.add_incoming(umw__ztdpv.type(None), uhtu__kxr)
    lkfu__ichr.add_incoming(sfis__uoub, yyqg__pvy)
    lkfu__ichr.add_incoming(cgutils.true_bit, uhtu__kxr)
    c.pyapi.decref(bpw__rlh)
    c.pyapi.decref(fdj__senpx)
    with c.builder.if_then(zwber__ldr):
        c.pyapi.decref(val)
    return NativeValue(kzl__almc, is_error=lkfu__ichr)


import numba.typed.typeddict
if _check_numba_change:
    lines = inspect.getsource(numba.core.pythonapi._unboxers.functions[
        numba.core.types.DictType])
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '5f6f183b94dc57838538c668a54c2476576c85d8553843f3219f5162c61e7816':
        warnings.warn('unbox_dicttype has changed')
numba.core.pythonapi._unboxers.functions[types.DictType] = unbox_dicttype


def op_DICT_UPDATE_byteflow(self, state, inst):
    value = state.pop()
    index = inst.arg
    target = state.peek(index)
    updatevar = state.make_temp()
    res = state.make_temp()
    state.append(inst, target=target, value=value, updatevar=updatevar, res=res
        )


if _check_numba_change:
    if hasattr(numba.core.byteflow.TraceRunner, 'op_DICT_UPDATE'):
        warnings.warn(
            'numba.core.byteflow.TraceRunner.op_DICT_UPDATE has changed')
numba.core.byteflow.TraceRunner.op_DICT_UPDATE = op_DICT_UPDATE_byteflow


def op_DICT_UPDATE_interpreter(self, inst, target, value, updatevar, res):
    from numba.core import ir
    target = self.get(target)
    value = self.get(value)
    ztz__rzi = ir.Expr.getattr(target, 'update', loc=self.loc)
    self.store(value=ztz__rzi, name=updatevar)
    ser__lvir = ir.Expr.call(self.get(updatevar), (value,), (), loc=self.loc)
    self.store(value=ser__lvir, name=res)


if _check_numba_change:
    if hasattr(numba.core.interpreter.Interpreter, 'op_DICT_UPDATE'):
        warnings.warn(
            'numba.core.interpreter.Interpreter.op_DICT_UPDATE has changed')
numba.core.interpreter.Interpreter.op_DICT_UPDATE = op_DICT_UPDATE_interpreter


@numba.extending.overload_method(numba.core.types.DictType, 'update')
def ol_dict_update(d, other):
    if not isinstance(d, numba.core.types.DictType):
        return
    if not isinstance(other, numba.core.types.DictType):
        return

    def impl(d, other):
        for nvtk__ucegf, gprl__aoel in other.items():
            d[nvtk__ucegf] = gprl__aoel
    return impl


if _check_numba_change:
    if hasattr(numba.core.interpreter.Interpreter, 'ol_dict_update'):
        warnings.warn('numba.typed.dictobject.ol_dict_update has changed')


def op_CALL_FUNCTION_EX_byteflow(self, state, inst):
    from numba.core.utils import PYVERSION
    if inst.arg & 1 and PYVERSION != (3, 10):
        errmsg = 'CALL_FUNCTION_EX with **kwargs not supported'
        raise errors.UnsupportedError(errmsg)
    if inst.arg & 1:
        varkwarg = state.pop()
    else:
        varkwarg = None
    vararg = state.pop()
    func = state.pop()
    res = state.make_temp()
    state.append(inst, func=func, vararg=vararg, varkwarg=varkwarg, res=res)
    state.push(res)


if _check_numba_change:
    lines = inspect.getsource(numba.core.byteflow.TraceRunner.
        op_CALL_FUNCTION_EX)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '349e7cfd27f5dab80fe15a7728c5f098f3f225ba8512d84331e39d01e863c6d4':
        warnings.warn(
            'numba.core.byteflow.TraceRunner.op_CALL_FUNCTION_EX has changed')
numba.core.byteflow.TraceRunner.op_CALL_FUNCTION_EX = (
    op_CALL_FUNCTION_EX_byteflow)


def op_CALL_FUNCTION_EX_interpreter(self, inst, func, vararg, varkwarg, res):
    func = self.get(func)
    vararg = self.get(vararg)
    if varkwarg is not None:
        varkwarg = self.get(varkwarg)
    ddt__egw = ir.Expr.call(func, [], [], loc=self.loc, vararg=vararg,
        varkwarg=varkwarg)
    self.store(ddt__egw, res)


if _check_numba_change:
    lines = inspect.getsource(numba.core.interpreter.Interpreter.
        op_CALL_FUNCTION_EX)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '84846e5318ab7ccc8f9abaae6ab9e0ca879362648196f9d4b0ffb91cf2e01f5d':
        warnings.warn(
            'numba.core.interpreter.Interpreter.op_CALL_FUNCTION_EX has changed'
            )
numba.core.interpreter.Interpreter.op_CALL_FUNCTION_EX = (
    op_CALL_FUNCTION_EX_interpreter)


@classmethod
def ir_expr_call(cls, func, args, kws, loc, vararg=None, varkwarg=None,
    target=None):
    assert isinstance(func, ir.Var)
    assert isinstance(loc, ir.Loc)
    op = 'call'
    return cls(op=op, loc=loc, func=func, args=args, kws=kws, vararg=vararg,
        varkwarg=varkwarg, target=target)


if _check_numba_change:
    lines = inspect.getsource(ir.Expr.call)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '665601d0548d4f648d454492e542cb8aa241107a8df6bc68d0eec664c9ada738':
        warnings.warn('ir.Expr.call has changed')
ir.Expr.call = ir_expr_call


@staticmethod
def define_untyped_pipeline(state, name='untyped'):
    from numba.core.compiler_machinery import PassManager
    from numba.core.untyped_passes import DeadBranchPrune, FindLiterallyCalls, FixupArgs, GenericRewrites, InlineClosureLikes, InlineInlinables, IRProcessing, LiteralPropagationSubPipelinePass, LiteralUnroll, MakeFunctionToJitFunction, ReconstructSSA, RewriteSemanticConstants, TranslateByteCode, WithLifting
    from numba.core.utils import PYVERSION
    wgur__ygro = PassManager(name)
    if state.func_ir is None:
        wgur__ygro.add_pass(TranslateByteCode, 'analyzing bytecode')
        if PYVERSION == (3, 10):
            wgur__ygro.add_pass(Bodo310ByteCodePass,
                'Apply Python 3.10 bytecode changes')
        wgur__ygro.add_pass(FixupArgs, 'fix up args')
    wgur__ygro.add_pass(IRProcessing, 'processing IR')
    wgur__ygro.add_pass(WithLifting, 'Handle with contexts')
    wgur__ygro.add_pass(InlineClosureLikes,
        'inline calls to locally defined closures')
    if not state.flags.no_rewrites:
        wgur__ygro.add_pass(RewriteSemanticConstants,
            'rewrite semantic constants')
        wgur__ygro.add_pass(DeadBranchPrune, 'dead branch pruning')
        wgur__ygro.add_pass(GenericRewrites, 'nopython rewrites')
    wgur__ygro.add_pass(MakeFunctionToJitFunction,
        'convert make_function into JIT functions')
    wgur__ygro.add_pass(InlineInlinables, 'inline inlinable functions')
    if not state.flags.no_rewrites:
        wgur__ygro.add_pass(DeadBranchPrune, 'dead branch pruning')
    wgur__ygro.add_pass(FindLiterallyCalls, 'find literally calls')
    wgur__ygro.add_pass(LiteralUnroll, 'handles literal_unroll')
    if state.flags.enable_ssa:
        wgur__ygro.add_pass(ReconstructSSA, 'ssa')
    wgur__ygro.add_pass(LiteralPropagationSubPipelinePass,
        'Literal propagation')
    wgur__ygro.finalize()
    return wgur__ygro


if _check_numba_change:
    lines = inspect.getsource(numba.core.compiler.DefaultPassBuilder.
        define_untyped_pipeline)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'fc5a0665658cc30588a78aca984ac2d323d5d3a45dce538cc62688530c772896':
        warnings.warn(
            'numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline has changed'
            )
numba.core.compiler.DefaultPassBuilder.define_untyped_pipeline = (
    define_untyped_pipeline)


def mul_list_generic(self, args, kws):
    a, fxwu__yduif = args
    if isinstance(a, types.List) and isinstance(fxwu__yduif, types.Integer):
        return signature(a, a, types.intp)
    elif isinstance(a, types.Integer) and isinstance(fxwu__yduif, types.List):
        return signature(fxwu__yduif, types.intp, fxwu__yduif)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.listdecl.MulList.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '95882385a8ffa67aa576e8169b9ee6b3197e0ad3d5def4b47fa65ce8cd0f1575':
        warnings.warn('numba.core.typing.listdecl.MulList.generic has changed')
numba.core.typing.listdecl.MulList.generic = mul_list_generic


@lower_builtin(operator.mul, types.Integer, types.List)
def list_mul(context, builder, sig, args):
    from llvmlite import ir as lir
    from numba.core.imputils import impl_ret_new_ref
    from numba.cpython.listobj import ListInstance
    if isinstance(sig.args[0], types.List):
        rpbxg__ruaz, myevu__wbrbd = 0, 1
    else:
        rpbxg__ruaz, myevu__wbrbd = 1, 0
    cjnd__jabhf = ListInstance(context, builder, sig.args[rpbxg__ruaz],
        args[rpbxg__ruaz])
    qfxfk__slbwy = cjnd__jabhf.size
    xlot__znrl = args[myevu__wbrbd]
    nzh__tstpg = lir.Constant(xlot__znrl.type, 0)
    xlot__znrl = builder.select(cgutils.is_neg_int(builder, xlot__znrl),
        nzh__tstpg, xlot__znrl)
    nkvn__aoloh = builder.mul(xlot__znrl, qfxfk__slbwy)
    hvg__hna = ListInstance.allocate(context, builder, sig.return_type,
        nkvn__aoloh)
    hvg__hna.size = nkvn__aoloh
    with cgutils.for_range_slice(builder, nzh__tstpg, nkvn__aoloh,
        qfxfk__slbwy, inc=True) as (dap__lanc, _):
        with cgutils.for_range(builder, qfxfk__slbwy) as banr__mmnst:
            value = cjnd__jabhf.getitem(banr__mmnst.index)
            hvg__hna.setitem(builder.add(banr__mmnst.index, dap__lanc),
                value, incref=True)
    return impl_ret_new_ref(context, builder, sig.return_type, hvg__hna.value)


def unify_pairs(self, first, second):
    from numba.core.typeconv import Conversion
    if first == second:
        return first
    if first is types.undefined:
        return second
    elif second is types.undefined:
        return first
    if first is types.unknown or second is types.unknown:
        return types.unknown
    mnnwa__qaws = first.unify(self, second)
    if mnnwa__qaws is not None:
        return mnnwa__qaws
    mnnwa__qaws = second.unify(self, first)
    if mnnwa__qaws is not None:
        return mnnwa__qaws
    hfi__ueql = self.can_convert(fromty=first, toty=second)
    if hfi__ueql is not None and hfi__ueql <= Conversion.safe:
        return second
    hfi__ueql = self.can_convert(fromty=second, toty=first)
    if hfi__ueql is not None and hfi__ueql <= Conversion.safe:
        return first
    if isinstance(first, types.Literal) or isinstance(second, types.Literal):
        first = types.unliteral(first)
        second = types.unliteral(second)
        return self.unify_pairs(first, second)
    return None


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.context.BaseContext.unify_pairs
        )
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'f0eaf4cfdf1537691de26efd24d7e320f7c3f10d35e9aefe70cb946b3be0008c':
        warnings.warn(
            'numba.core.typing.context.BaseContext.unify_pairs has changed')
numba.core.typing.context.BaseContext.unify_pairs = unify_pairs


def _native_set_to_python_list(typ, payload, c):
    from llvmlite import ir
    nkvn__aoloh = payload.used
    listobj = c.pyapi.list_new(nkvn__aoloh)
    wng__bws = cgutils.is_not_null(c.builder, listobj)
    with c.builder.if_then(wng__bws, likely=True):
        index = cgutils.alloca_once_value(c.builder, ir.Constant(
            nkvn__aoloh.type, 0))
        with payload._iterate() as banr__mmnst:
            i = c.builder.load(index)
            item = banr__mmnst.entry.key
            c.context.nrt.incref(c.builder, typ.dtype, item)
            itemobj = c.box(typ.dtype, item)
            c.pyapi.list_setitem(listobj, i, itemobj)
            i = c.builder.add(i, ir.Constant(i.type, 1))
            c.builder.store(i, index)
    return wng__bws, listobj


def _lookup(self, item, h, for_insert=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    wot__xilx = h.type
    lxyci__oze = self.mask
    dtype = self._ty.dtype
    igit__ypqv = context.typing_context
    fnty = igit__ypqv.resolve_value_type(operator.eq)
    sig = fnty.get_call_type(igit__ypqv, (dtype, dtype), {})
    qovvm__nzgrj = context.get_function(fnty, sig)
    fxcij__krj = ir.Constant(wot__xilx, 1)
    hpoi__bbpds = ir.Constant(wot__xilx, 5)
    ebk__tpfl = cgutils.alloca_once_value(builder, h)
    index = cgutils.alloca_once_value(builder, builder.and_(h, lxyci__oze))
    if for_insert:
        fubvj__rhqrn = lxyci__oze.type(-1)
        mqkm__xwazp = cgutils.alloca_once_value(builder, fubvj__rhqrn)
    hnnc__kjs = builder.append_basic_block('lookup.body')
    jstk__fvczk = builder.append_basic_block('lookup.found')
    ebq__doqpm = builder.append_basic_block('lookup.not_found')
    had__dsr = builder.append_basic_block('lookup.end')

    def check_entry(i):
        entry = self.get_entry(i)
        mbaty__pac = entry.hash
        with builder.if_then(builder.icmp_unsigned('==', h, mbaty__pac)):
            ryf__ejh = qovvm__nzgrj(builder, (item, entry.key))
            with builder.if_then(ryf__ejh):
                builder.branch(jstk__fvczk)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, mbaty__pac)):
            builder.branch(ebq__doqpm)
        if for_insert:
            with builder.if_then(numba.cpython.setobj.is_hash_deleted(
                context, builder, mbaty__pac)):
                imref__lfqw = builder.load(mqkm__xwazp)
                imref__lfqw = builder.select(builder.icmp_unsigned('==',
                    imref__lfqw, fubvj__rhqrn), i, imref__lfqw)
                builder.store(imref__lfqw, mqkm__xwazp)
    with cgutils.for_range(builder, ir.Constant(wot__xilx, numba.cpython.
        setobj.LINEAR_PROBES)):
        i = builder.load(index)
        check_entry(i)
        i = builder.add(i, fxcij__krj)
        i = builder.and_(i, lxyci__oze)
        builder.store(i, index)
    builder.branch(hnnc__kjs)
    with builder.goto_block(hnnc__kjs):
        i = builder.load(index)
        check_entry(i)
        dqcu__avcj = builder.load(ebk__tpfl)
        dqcu__avcj = builder.lshr(dqcu__avcj, hpoi__bbpds)
        i = builder.add(fxcij__krj, builder.mul(i, hpoi__bbpds))
        i = builder.and_(lxyci__oze, builder.add(i, dqcu__avcj))
        builder.store(i, index)
        builder.store(dqcu__avcj, ebk__tpfl)
        builder.branch(hnnc__kjs)
    with builder.goto_block(ebq__doqpm):
        if for_insert:
            i = builder.load(index)
            imref__lfqw = builder.load(mqkm__xwazp)
            i = builder.select(builder.icmp_unsigned('==', imref__lfqw,
                fubvj__rhqrn), i, imref__lfqw)
            builder.store(i, index)
        builder.branch(had__dsr)
    with builder.goto_block(jstk__fvczk):
        builder.branch(had__dsr)
    builder.position_at_end(had__dsr)
    prz__lzlm = builder.phi(ir.IntType(1), 'found')
    prz__lzlm.add_incoming(cgutils.true_bit, jstk__fvczk)
    prz__lzlm.add_incoming(cgutils.false_bit, ebq__doqpm)
    return prz__lzlm, builder.load(index)


def _add_entry(self, payload, entry, item, h, do_resize=True):
    context = self._context
    builder = self._builder
    ahpd__vztqr = entry.hash
    entry.hash = h
    context.nrt.incref(builder, self._ty.dtype, item)
    entry.key = item
    bwol__hed = payload.used
    fxcij__krj = ir.Constant(bwol__hed.type, 1)
    bwol__hed = payload.used = builder.add(bwol__hed, fxcij__krj)
    with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
        builder, ahpd__vztqr), likely=True):
        payload.fill = builder.add(payload.fill, fxcij__krj)
    if do_resize:
        self.upsize(bwol__hed)
    self.set_dirty(True)


def _add_key(self, payload, item, h, do_resize=True):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    prz__lzlm, i = payload._lookup(item, h, for_insert=True)
    ois__asqp = builder.not_(prz__lzlm)
    with builder.if_then(ois__asqp):
        entry = payload.get_entry(i)
        ahpd__vztqr = entry.hash
        entry.hash = h
        context.nrt.incref(builder, self._ty.dtype, item)
        entry.key = item
        bwol__hed = payload.used
        fxcij__krj = ir.Constant(bwol__hed.type, 1)
        bwol__hed = payload.used = builder.add(bwol__hed, fxcij__krj)
        with builder.if_then(numba.cpython.setobj.is_hash_empty(context,
            builder, ahpd__vztqr), likely=True):
            payload.fill = builder.add(payload.fill, fxcij__krj)
        if do_resize:
            self.upsize(bwol__hed)
        self.set_dirty(True)


def _remove_entry(self, payload, entry, do_resize=True):
    from llvmlite import ir
    entry.hash = ir.Constant(entry.hash.type, numba.cpython.setobj.DELETED)
    self._context.nrt.decref(self._builder, self._ty.dtype, entry.key)
    bwol__hed = payload.used
    fxcij__krj = ir.Constant(bwol__hed.type, 1)
    bwol__hed = payload.used = self._builder.sub(bwol__hed, fxcij__krj)
    if do_resize:
        self.downsize(bwol__hed)
    self.set_dirty(True)


def pop(self):
    context = self._context
    builder = self._builder
    igxa__yjjb = context.get_value_type(self._ty.dtype)
    key = cgutils.alloca_once(builder, igxa__yjjb)
    payload = self.payload
    with payload._next_entry() as entry:
        builder.store(entry.key, key)
        context.nrt.incref(builder, self._ty.dtype, entry.key)
        self._remove_entry(payload, entry)
    return builder.load(key)


def _resize(self, payload, nentries, errmsg):
    context = self._context
    builder = self._builder
    ewib__riotd = payload
    wng__bws = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(wng__bws), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (errmsg,))
    payload = self.payload
    with ewib__riotd._iterate() as banr__mmnst:
        entry = banr__mmnst.entry
        self._add_key(payload, entry.key, entry.hash, do_resize=False)
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(ewib__riotd.ptr)


def _replace_payload(self, nentries):
    context = self._context
    builder = self._builder
    with self.payload._iterate() as banr__mmnst:
        entry = banr__mmnst.entry
        context.nrt.decref(builder, self._ty.dtype, entry.key)
    self._free_payload(self.payload.ptr)
    wng__bws = self._allocate_payload(nentries, realloc=True)
    with builder.if_then(builder.not_(wng__bws), likely=False):
        context.call_conv.return_user_exc(builder, MemoryError, (
            'cannot reallocate set',))


def _allocate_payload(self, nentries, realloc=False):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    wng__bws = cgutils.alloca_once_value(builder, cgutils.true_bit)
    wot__xilx = context.get_value_type(types.intp)
    nzh__tstpg = ir.Constant(wot__xilx, 0)
    fxcij__krj = ir.Constant(wot__xilx, 1)
    sqpj__agnbz = context.get_data_type(types.SetPayload(self._ty))
    nwgl__qret = context.get_abi_sizeof(sqpj__agnbz)
    tzdkx__bjxs = self._entrysize
    nwgl__qret -= tzdkx__bjxs
    wfeu__xivtm, tbuah__hpek = cgutils.muladd_with_overflow(builder,
        nentries, ir.Constant(wot__xilx, tzdkx__bjxs), ir.Constant(
        wot__xilx, nwgl__qret))
    with builder.if_then(tbuah__hpek, likely=False):
        builder.store(cgutils.false_bit, wng__bws)
    with builder.if_then(builder.load(wng__bws), likely=True):
        if realloc:
            wiseu__run = self._set.meminfo
            atqi__yspzr = context.nrt.meminfo_varsize_alloc(builder,
                wiseu__run, size=wfeu__xivtm)
            nlxi__uce = cgutils.is_null(builder, atqi__yspzr)
        else:
            cqw__ckobq = _imp_dtor(context, builder.module, self._ty)
            wiseu__run = context.nrt.meminfo_new_varsize_dtor(builder,
                wfeu__xivtm, builder.bitcast(cqw__ckobq, cgutils.voidptr_t))
            nlxi__uce = cgutils.is_null(builder, wiseu__run)
        with builder.if_else(nlxi__uce, likely=False) as (kfink__nab, ioj__zeq
            ):
            with kfink__nab:
                builder.store(cgutils.false_bit, wng__bws)
            with ioj__zeq:
                if not realloc:
                    self._set.meminfo = wiseu__run
                    self._set.parent = context.get_constant_null(types.pyobject
                        )
                payload = self.payload
                cgutils.memset(builder, payload.ptr, wfeu__xivtm, 255)
                payload.used = nzh__tstpg
                payload.fill = nzh__tstpg
                payload.finger = nzh__tstpg
                vlt__jggj = builder.sub(nentries, fxcij__krj)
                payload.mask = vlt__jggj
    return builder.load(wng__bws)


def _copy_payload(self, src_payload):
    from llvmlite import ir
    context = self._context
    builder = self._builder
    wng__bws = cgutils.alloca_once_value(builder, cgutils.true_bit)
    wot__xilx = context.get_value_type(types.intp)
    nzh__tstpg = ir.Constant(wot__xilx, 0)
    fxcij__krj = ir.Constant(wot__xilx, 1)
    sqpj__agnbz = context.get_data_type(types.SetPayload(self._ty))
    nwgl__qret = context.get_abi_sizeof(sqpj__agnbz)
    tzdkx__bjxs = self._entrysize
    nwgl__qret -= tzdkx__bjxs
    lxyci__oze = src_payload.mask
    nentries = builder.add(fxcij__krj, lxyci__oze)
    wfeu__xivtm = builder.add(ir.Constant(wot__xilx, nwgl__qret), builder.
        mul(ir.Constant(wot__xilx, tzdkx__bjxs), nentries))
    with builder.if_then(builder.load(wng__bws), likely=True):
        cqw__ckobq = _imp_dtor(context, builder.module, self._ty)
        wiseu__run = context.nrt.meminfo_new_varsize_dtor(builder,
            wfeu__xivtm, builder.bitcast(cqw__ckobq, cgutils.voidptr_t))
        nlxi__uce = cgutils.is_null(builder, wiseu__run)
        with builder.if_else(nlxi__uce, likely=False) as (kfink__nab, ioj__zeq
            ):
            with kfink__nab:
                builder.store(cgutils.false_bit, wng__bws)
            with ioj__zeq:
                self._set.meminfo = wiseu__run
                payload = self.payload
                payload.used = src_payload.used
                payload.fill = src_payload.fill
                payload.finger = nzh__tstpg
                payload.mask = lxyci__oze
                cgutils.raw_memcpy(builder, payload.entries, src_payload.
                    entries, nentries, tzdkx__bjxs)
                with src_payload._iterate() as banr__mmnst:
                    context.nrt.incref(builder, self._ty.dtype, banr__mmnst
                        .entry.key)
    return builder.load(wng__bws)


def _imp_dtor(context, module, set_type):
    from llvmlite import ir
    nlcfh__qrw = context.get_value_type(types.voidptr)
    gthss__jidj = context.get_value_type(types.uintp)
    fnty = ir.FunctionType(ir.VoidType(), [nlcfh__qrw, gthss__jidj, nlcfh__qrw]
        )
    xlr__uum = f'_numba_set_dtor_{set_type}'
    fn = cgutils.get_or_insert_function(module, fnty, name=xlr__uum)
    if fn.is_declaration:
        fn.linkage = 'linkonce_odr'
        builder = ir.IRBuilder(fn.append_basic_block())
        ptoez__hcbg = builder.bitcast(fn.args[0], cgutils.voidptr_t.
            as_pointer())
        payload = numba.cpython.setobj._SetPayload(context, builder,
            set_type, ptoez__hcbg)
        with payload._iterate() as banr__mmnst:
            entry = banr__mmnst.entry
            context.nrt.decref(builder, set_type.dtype, entry.key)
        builder.ret_void()
    return fn


@lower_builtin(set, types.IterableType)
def set_constructor(context, builder, sig, args):
    set_type = sig.return_type
    jriu__osq, = sig.args
    svjlh__atcit, = args
    pds__ujrr = numba.core.imputils.call_len(context, builder, jriu__osq,
        svjlh__atcit)
    inst = numba.cpython.setobj.SetInstance.allocate(context, builder,
        set_type, pds__ujrr)
    with numba.core.imputils.for_iter(context, builder, jriu__osq, svjlh__atcit
        ) as banr__mmnst:
        inst.add(banr__mmnst.value)
        context.nrt.decref(builder, set_type.dtype, banr__mmnst.value)
    return numba.core.imputils.impl_ret_new_ref(context, builder, set_type,
        inst.value)


@lower_builtin('set.update', types.Set, types.IterableType)
def set_update(context, builder, sig, args):
    inst = numba.cpython.setobj.SetInstance(context, builder, sig.args[0],
        args[0])
    jriu__osq = sig.args[1]
    svjlh__atcit = args[1]
    pds__ujrr = numba.core.imputils.call_len(context, builder, jriu__osq,
        svjlh__atcit)
    if pds__ujrr is not None:
        qist__hnn = builder.add(inst.payload.used, pds__ujrr)
        inst.upsize(qist__hnn)
    with numba.core.imputils.for_iter(context, builder, jriu__osq, svjlh__atcit
        ) as banr__mmnst:
        hklp__hhsxt = context.cast(builder, banr__mmnst.value, jriu__osq.
            dtype, inst.dtype)
        inst.add(hklp__hhsxt)
        context.nrt.decref(builder, jriu__osq.dtype, banr__mmnst.value)
    if pds__ujrr is not None:
        inst.downsize(inst.payload.used)
    return context.get_dummy_value()


if _check_numba_change:
    for name, orig, hash in ((
        'numba.core.boxing._native_set_to_python_list', numba.core.boxing.
        _native_set_to_python_list,
        'b47f3d5e582c05d80899ee73e1c009a7e5121e7a660d42cb518bb86933f3c06f'),
        ('numba.cpython.setobj._SetPayload._lookup', numba.cpython.setobj.
        _SetPayload._lookup,
        'c797b5399d7b227fe4eea3a058b3d3103f59345699388afb125ae47124bee395'),
        ('numba.cpython.setobj.SetInstance._add_entry', numba.cpython.
        setobj.SetInstance._add_entry,
        'c5ed28a5fdb453f242e41907cb792b66da2df63282c17abe0b68fc46782a7f94'),
        ('numba.cpython.setobj.SetInstance._add_key', numba.cpython.setobj.
        SetInstance._add_key,
        '324d6172638d02a361cfa0ca7f86e241e5a56a008d4ab581a305f9ae5ea4a75f'),
        ('numba.cpython.setobj.SetInstance._remove_entry', numba.cpython.
        setobj.SetInstance._remove_entry,
        '2c441b00daac61976e673c0e738e8e76982669bd2851951890dd40526fa14da1'),
        ('numba.cpython.setobj.SetInstance.pop', numba.cpython.setobj.
        SetInstance.pop,
        '1a7b7464cbe0577f2a38f3af9acfef6d4d25d049b1e216157275fbadaab41d1b'),
        ('numba.cpython.setobj.SetInstance._resize', numba.cpython.setobj.
        SetInstance._resize,
        '5ca5c2ba4f8c4bf546fde106b9c2656d4b22a16d16e163fb64c5d85ea4d88746'),
        ('numba.cpython.setobj.SetInstance._replace_payload', numba.cpython
        .setobj.SetInstance._replace_payload,
        'ada75a6c85828bff69c8469538c1979801f560a43fb726221a9c21bf208ae78d'),
        ('numba.cpython.setobj.SetInstance._allocate_payload', numba.
        cpython.setobj.SetInstance._allocate_payload,
        '2e80c419df43ebc71075b4f97fc1701c10dbc576aed248845e176b8d5829e61b'),
        ('numba.cpython.setobj.SetInstance._copy_payload', numba.cpython.
        setobj.SetInstance._copy_payload,
        '0885ac36e1eb5a0a0fc4f5d91e54b2102b69e536091fed9f2610a71d225193ec'),
        ('numba.cpython.setobj.set_constructor', numba.cpython.setobj.
        set_constructor,
        '3d521a60c3b8eaf70aa0f7267427475dfddd8f5e5053b5bfe309bb5f1891b0ce'),
        ('numba.cpython.setobj.set_update', numba.cpython.setobj.set_update,
        '965c4f7f7abcea5cbe0491b602e6d4bcb1800fa1ec39b1ffccf07e1bc56051c3')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
        orig = new
numba.core.boxing._native_set_to_python_list = _native_set_to_python_list
numba.cpython.setobj._SetPayload._lookup = _lookup
numba.cpython.setobj.SetInstance._add_entry = _add_entry
numba.cpython.setobj.SetInstance._add_key = _add_key
numba.cpython.setobj.SetInstance._remove_entry = _remove_entry
numba.cpython.setobj.SetInstance.pop = pop
numba.cpython.setobj.SetInstance._resize = _resize
numba.cpython.setobj.SetInstance._replace_payload = _replace_payload
numba.cpython.setobj.SetInstance._allocate_payload = _allocate_payload
numba.cpython.setobj.SetInstance._copy_payload = _copy_payload


def _reduce(self):
    libdata = self.library.serialize_using_object_code()
    typeann = str(self.type_annotation)
    fndesc = self.fndesc
    fndesc.typemap = fndesc.calltypes = None
    referenced_envs = self._find_referenced_environments()
    hdwl__einl = {key: value for key, value in self.metadata.items() if (
        'distributed' in key or 'replicated' in key) and key !=
        'distributed_diagnostics'}
    return (libdata, self.fndesc, self.environment, self.signature, self.
        objectmode, self.lifted, typeann, hdwl__einl, self.reload_init,
        tuple(referenced_envs))


@classmethod
def _rebuild(cls, target_context, libdata, fndesc, env, signature,
    objectmode, lifted, typeann, metadata, reload_init, referenced_envs):
    if reload_init:
        for fn in reload_init:
            fn()
    library = target_context.codegen().unserialize_library(libdata)
    ptui__byq = target_context.get_executable(library, fndesc, env)
    pnx__xir = cls(target_context=target_context, typing_context=
        target_context.typing_context, library=library, environment=env,
        entry_point=ptui__byq, fndesc=fndesc, type_annotation=typeann,
        signature=signature, objectmode=objectmode, lifted=lifted,
        typing_error=None, call_helper=None, metadata=metadata, reload_init
        =reload_init, referenced_envs=referenced_envs)
    for env in referenced_envs:
        library.codegen.set_env(env.env_name, env)
    return pnx__xir


if _check_numba_change:
    for name, orig, hash in (('numba.core.compiler.CompileResult._reduce',
        numba.core.compiler.CompileResult._reduce,
        '5f86eacfa5202c202b3dc200f1a7a9b6d3f9d1ec16d43a52cb2d580c34fbfa82'),
        ('numba.core.compiler.CompileResult._rebuild', numba.core.compiler.
        CompileResult._rebuild,
        '44fa9dc2255883ab49195d18c3cca8c0ad715d0dd02033bd7e2376152edc4e84')):
        lines = inspect.getsource(orig)
        if hashlib.sha256(lines.encode()).hexdigest() != hash:
            warnings.warn(f'{name} has changed')
        orig = new
numba.core.compiler.CompileResult._reduce = _reduce
numba.core.compiler.CompileResult._rebuild = _rebuild
if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._IPythonCacheLocator.
        get_cache_path)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'eb33b7198697b8ef78edddcf69e58973c44744ff2cb2f54d4015611ad43baed0':
        warnings.warn(
            'numba.core.caching._IPythonCacheLocator.get_cache_path has changed'
            )
if os.environ.get('BODO_PLATFORM_CACHE_LOCATION') is not None:

    def _get_cache_path(self):
        return numba.config.CACHE_DIR
    numba.core.caching._IPythonCacheLocator.get_cache_path = _get_cache_path
if _check_numba_change:
    lines = inspect.getsource(numba.core.types.containers.Bytes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '977423d833eeb4b8fd0c87f55dce7251c107d8d10793fe5723de6e5452da32e2':
        warnings.warn('numba.core.types.containers.Bytes has changed')
numba.core.types.containers.Bytes.slice_is_copy = True
if _check_numba_change:
    lines = inspect.getsource(numba.core.caching._CacheLocator.
        ensure_cache_path)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '906b6f516f76927dfbe69602c335fa151b9f33d40dfe171a9190c0d11627bc03':
        warnings.warn(
            'numba.core.caching._CacheLocator.ensure_cache_path has changed')
if os.environ.get('BODO_PLATFORM_CACHE_LOCATION') is not None:
    import tempfile

    def _ensure_cache_path(self):
        from mpi4py import MPI
        qyt__hoibl = MPI.COMM_WORLD
        if qyt__hoibl.Get_rank() == 0:
            wuqt__thok = self.get_cache_path()
            os.makedirs(wuqt__thok, exist_ok=True)
            tempfile.TemporaryFile(dir=wuqt__thok).close()
    numba.core.caching._CacheLocator.ensure_cache_path = _ensure_cache_path


def _analyze_op_call_builtins_len(self, scope, equiv_set, loc, args, kws):
    from numba.parfors.array_analysis import ArrayAnalysis
    require(len(args) == 1)
    var = args[0]
    typ = self.typemap[var.name]
    require(isinstance(typ, types.ArrayCompatible))
    require(not isinstance(typ, types.Bytes))
    shape = equiv_set._get_shape(var)
    return ArrayAnalysis.AnalyzeResult(shape=shape[0], rhs=shape[0])


if _check_numba_change:
    lines = inspect.getsource(numba.parfors.array_analysis.ArrayAnalysis.
        _analyze_op_call_builtins_len)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '612cbc67e8e462f25f348b2a5dd55595f4201a6af826cffcd38b16cd85fc70f7':
        warnings.warn(
            'numba.parfors.array_analysis.ArrayAnalysis._analyze_op_call_builtins_len has changed'
            )
(numba.parfors.array_analysis.ArrayAnalysis._analyze_op_call_builtins_len
    ) = _analyze_op_call_builtins_len


def generic(self, args, kws):
    assert not kws
    val, = args
    if isinstance(val, (types.Buffer, types.BaseTuple)) and not isinstance(val,
        types.Bytes):
        return signature(types.intp, val)
    elif isinstance(val, types.RangeType):
        return signature(val.dtype, val)


if _check_numba_change:
    lines = inspect.getsource(numba.core.typing.builtins.Len.generic)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != '88d54238ebe0896f4s69b7347105a6a68dec443036a61f9e494c1630c62b0fa76':
        warnings.warn('numba.core.typing.builtins.Len.generic has changed')
numba.core.typing.builtins.Len.generic = generic
from numba.cpython import charseq


def _make_constant_bytes(context, builder, nbytes):
    from llvmlite import ir
    uhzop__lfzzz = cgutils.create_struct_proxy(charseq.bytes_type)
    zky__aipkt = uhzop__lfzzz(context, builder)
    if isinstance(nbytes, int):
        nbytes = ir.Constant(zky__aipkt.nitems.type, nbytes)
    zky__aipkt.meminfo = context.nrt.meminfo_alloc(builder, nbytes)
    zky__aipkt.nitems = nbytes
    zky__aipkt.itemsize = ir.Constant(zky__aipkt.itemsize.type, 1)
    zky__aipkt.data = context.nrt.meminfo_data(builder, zky__aipkt.meminfo)
    zky__aipkt.parent = cgutils.get_null_value(zky__aipkt.parent.type)
    zky__aipkt.shape = cgutils.pack_array(builder, [zky__aipkt.nitems],
        context.get_value_type(types.intp))
    zky__aipkt.strides = cgutils.pack_array(builder, [ir.Constant(
        zky__aipkt.strides.type.element, 1)], context.get_value_type(types.
        intp))
    return zky__aipkt


if _check_numba_change:
    lines = inspect.getsource(charseq._make_constant_bytes)
    if hashlib.sha256(lines.encode()).hexdigest(
        ) != 'b3ed23ad58baff7b935912e3e22f4d8af67423d8fd0e5f1836ba0b3028a6eb18':
        warnings.warn('charseq._make_constant_bytes has changed')
charseq._make_constant_bytes = _make_constant_bytes
