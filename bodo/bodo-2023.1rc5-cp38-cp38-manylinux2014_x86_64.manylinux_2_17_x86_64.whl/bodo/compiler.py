"""
Defines Bodo's compiler pipeline.
"""
import os
import warnings
from collections import namedtuple
import numba
from numba.core import ir, ir_utils, types
from numba.core.compiler import DefaultPassBuilder
from numba.core.compiler_machinery import AnalysisPass, FunctionPass, register_pass
from numba.core.errors import NumbaExperimentalFeatureWarning, NumbaPendingDeprecationWarning
from numba.core.inline_closurecall import inline_closure_call
from numba.core.ir_utils import build_definitions, find_callname, get_definition, guard
from numba.core.registry import CPUDispatcher
from numba.core.typed_passes import DumpParforDiagnostics, InlineOverloads, IRLegalization, NopythonTypeInference, ParforPass, PreParforPass
from numba.core.untyped_passes import MakeFunctionToJitFunction, ReconstructSSA, WithLifting
import bodo
import bodo.hiframes.dataframe_indexing
import bodo.hiframes.datetime_datetime_ext
import bodo.hiframes.datetime_timedelta_ext
import bodo.io
import bodo.libs
import bodo.libs.array_kernels
import bodo.libs.int_arr_ext
import bodo.libs.re_ext
import bodo.libs.spark_extra
import bodo.transforms
import bodo.transforms.series_pass
import bodo.transforms.untyped_pass
import bodo.utils
import bodo.utils.table_utils
import bodo.utils.typing
from bodo.transforms.series_pass import SeriesPass
from bodo.transforms.table_column_del_pass import TableColumnDelPass
from bodo.transforms.typing_pass import BodoTypeInference
from bodo.transforms.untyped_pass import UntypedPass
from bodo.utils.utils import is_assign, is_call_assign, is_expr
warnings.simplefilter('ignore', category=NumbaExperimentalFeatureWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)
inline_all_calls = False


class BodoCompiler(numba.core.compiler.CompilerBase):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=True,
            inline_calls_pass=inline_all_calls)

    def _create_bodo_pipeline(self, distributed=True, inline_calls_pass=
        False, udf_pipeline=False):
        lryk__ecws = 'bodo' if distributed else 'bodo_seq'
        lryk__ecws = (lryk__ecws + '_inline' if inline_calls_pass else
            lryk__ecws)
        pm = DefaultPassBuilder.define_nopython_pipeline(self.state, lryk__ecws
            )
        if inline_calls_pass:
            pm.add_pass_after(InlinePass, WithLifting)
        if udf_pipeline:
            pm.add_pass_after(ConvertCallsUDFPass, WithLifting)
        add_pass_before(pm, BodoUntypedPass, ReconstructSSA)
        replace_pass(pm, BodoTypeInference, NopythonTypeInference)
        remove_pass(pm, MakeFunctionToJitFunction)
        add_pass_before(pm, BodoSeriesPass, PreParforPass)
        if distributed:
            pm.add_pass_after(BodoDistributedPass, ParforPass)
        else:
            pm.add_pass_after(LowerParforSeq, ParforPass)
            pm.add_pass_after(LowerBodoIRExtSeq, LowerParforSeq)
        add_pass_before(pm, BodoTableColumnDelPass, IRLegalization)
        pm.add_pass_after(BodoDumpDistDiagnosticsPass, DumpParforDiagnostics)
        pm.finalize()
        return [pm]


def add_pass_before(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for bnqf__ifv, (amndv__vfwd, fhfg__hmlg) in enumerate(pm.passes):
        if amndv__vfwd == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.insert(bnqf__ifv, (pass_cls, str(pass_cls)))
    pm._finalized = False


def replace_pass(pm, pass_cls, location):
    assert pm.passes
    pm._validate_pass(pass_cls)
    pm._validate_pass(location)
    for bnqf__ifv, (amndv__vfwd, fhfg__hmlg) in enumerate(pm.passes):
        if amndv__vfwd == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes[bnqf__ifv] = pass_cls, str(pass_cls)
    pm._finalized = False


def remove_pass(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for bnqf__ifv, (amndv__vfwd, fhfg__hmlg) in enumerate(pm.passes):
        if amndv__vfwd == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes.pop(bnqf__ifv)
    pm._finalized = False


@register_pass(mutates_CFG=True, analysis_only=False)
class InlinePass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        inline_calls(state.func_ir, state.locals)
        state.func_ir.blocks = ir_utils.simplify_CFG(state.func_ir.blocks)
        return True


def _convert_bodo_dispatcher_to_udf(rhs, func_ir):
    msju__igi = guard(get_definition, func_ir, rhs.func)
    if isinstance(msju__igi, (ir.Global, ir.FreeVar, ir.Const)):
        qlys__vsvsk = msju__igi.value
    else:
        dztic__cab = guard(find_callname, func_ir, rhs)
        if not (dztic__cab and isinstance(dztic__cab[0], str) and
            isinstance(dztic__cab[1], str)):
            return
        func_name, func_mod = dztic__cab
        try:
            import importlib
            htyd__amj = importlib.import_module(func_mod)
            qlys__vsvsk = getattr(htyd__amj, func_name)
        except:
            return
    if isinstance(qlys__vsvsk, CPUDispatcher) and issubclass(qlys__vsvsk.
        _compiler.pipeline_class, BodoCompiler
        ) and qlys__vsvsk._compiler.pipeline_class != BodoCompilerUDF:
        qlys__vsvsk._compiler.pipeline_class = BodoCompilerUDF
        qlys__vsvsk.recompile()


@register_pass(mutates_CFG=True, analysis_only=False)
class ConvertCallsUDFPass(FunctionPass):
    _name = 'inline_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        for block in state.func_ir.blocks.values():
            for hquk__vwn in block.body:
                if is_call_assign(hquk__vwn):
                    _convert_bodo_dispatcher_to_udf(hquk__vwn.value, state.
                        func_ir)
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoUntypedPass(FunctionPass):
    _name = 'bodo_untyped_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        miusm__wzd = UntypedPass(state.func_ir, state.typingctx, state.args,
            state.locals, state.metadata, state.flags, isinstance(state.
            pipeline, BodoCompilerSeq))
        miusm__wzd.run()
        return True


def _update_definitions(func_ir, node_list):
    pdh__yxbh = ir.Loc('', 0)
    pgk__fxd = ir.Block(ir.Scope(None, pdh__yxbh), pdh__yxbh)
    pgk__fxd.body = node_list
    build_definitions({(0): pgk__fxd}, func_ir._definitions)


_series_inline_attrs = {'values', 'shape', 'size', 'empty', 'name', 'index',
    'dtype'}
_series_no_inline_methods = {'to_list', 'tolist', 'rolling', 'to_csv',
    'count', 'fillna', 'to_dict', 'map', 'apply', 'pipe', 'combine',
    'bfill', 'ffill', 'pad', 'backfill', 'mask', 'where'}
_series_method_alias = {'isnull': 'isna', 'product': 'prod', 'kurtosis':
    'kurt', 'is_monotonic': 'is_monotonic_increasing', 'notnull': 'notna'}
_dataframe_no_inline_methods = {'apply', 'itertuples', 'pipe', 'to_parquet',
    'to_sql', 'to_csv', 'to_json', 'assign', 'to_string', 'query',
    'rolling', 'mask', 'where'}
TypingInfo = namedtuple('TypingInfo', ['typingctx', 'targetctx', 'typemap',
    'calltypes', 'curr_loc'])


def _inline_bodo_getattr(stmt, rhs, rhs_type, new_body, func_ir, typingctx,
    targetctx, typemap, calltypes):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import compile_func_single_block
    if isinstance(rhs_type, SeriesType) and rhs.attr in _series_inline_attrs:
        nenij__somyq = 'overload_series_' + rhs.attr
        tny__iyqze = getattr(bodo.hiframes.series_impl, nenij__somyq)
    if isinstance(rhs_type, DataFrameType) and rhs.attr in ('index', 'columns'
        ):
        nenij__somyq = 'overload_dataframe_' + rhs.attr
        tny__iyqze = getattr(bodo.hiframes.dataframe_impl, nenij__somyq)
    else:
        return False
    func_ir._definitions[stmt.target.name].remove(rhs)
    dtqoq__uilb = tny__iyqze(rhs_type)
    sux__reehx = TypingInfo(typingctx, targetctx, typemap, calltypes, stmt.loc)
    jffdw__smo = compile_func_single_block(dtqoq__uilb, (rhs.value,), stmt.
        target, sux__reehx)
    _update_definitions(func_ir, jffdw__smo)
    new_body += jffdw__smo
    return True


def _inline_bodo_call(rhs, i, func_mod, func_name, pass_info, new_body,
    block, typingctx, targetctx, calltypes, work_list):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.utils.transform import replace_func, update_locs
    func_ir = pass_info.func_ir
    typemap = pass_info.typemap
    if isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        SeriesType) and func_name not in _series_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        if (func_name in bodo.hiframes.series_impl.explicit_binop_funcs or 
            func_name.startswith('r') and func_name[1:] in bodo.hiframes.
            series_impl.explicit_binop_funcs):
            return False
        rhs.args.insert(0, func_mod)
        otoze__wibj = tuple(typemap[tpzeu__xpird.name] for tpzeu__xpird in
            rhs.args)
        wesv__pmhtc = {lryk__ecws: typemap[tpzeu__xpird.name] for 
            lryk__ecws, tpzeu__xpird in dict(rhs.kws).items()}
        dtqoq__uilb = getattr(bodo.hiframes.series_impl, 'overload_series_' +
            func_name)(*otoze__wibj, **wesv__pmhtc)
    elif isinstance(func_mod, ir.Var) and isinstance(typemap[func_mod.name],
        DataFrameType) and func_name not in _dataframe_no_inline_methods:
        if func_name in _series_method_alias:
            func_name = _series_method_alias[func_name]
        rhs.args.insert(0, func_mod)
        otoze__wibj = tuple(typemap[tpzeu__xpird.name] for tpzeu__xpird in
            rhs.args)
        wesv__pmhtc = {lryk__ecws: typemap[tpzeu__xpird.name] for 
            lryk__ecws, tpzeu__xpird in dict(rhs.kws).items()}
        dtqoq__uilb = getattr(bodo.hiframes.dataframe_impl, 
            'overload_dataframe_' + func_name)(*otoze__wibj, **wesv__pmhtc)
    else:
        return False
    uwbnj__gsf = replace_func(pass_info, dtqoq__uilb, rhs.args, pysig=numba
        .core.utils.pysignature(dtqoq__uilb), kws=dict(rhs.kws))
    block.body = new_body + block.body[i:]
    ekfrq__ojt, fhfg__hmlg = inline_closure_call(func_ir, uwbnj__gsf.glbls,
        block, len(new_body), uwbnj__gsf.func, typingctx=typingctx,
        targetctx=targetctx, arg_typs=uwbnj__gsf.arg_types, typemap=typemap,
        calltypes=calltypes, work_list=work_list)
    for nxa__dtbi in ekfrq__ojt.values():
        nxa__dtbi.loc = rhs.loc
        update_locs(nxa__dtbi.body, rhs.loc)
    return True


def bodo_overload_inline_pass(func_ir, typingctx, targetctx, typemap, calltypes
    ):
    zyjs__fugun = namedtuple('PassInfo', ['func_ir', 'typemap'])
    pass_info = zyjs__fugun(func_ir, typemap)
    uybt__jtrhb = func_ir.blocks
    work_list = list((jkri__lmcqc, uybt__jtrhb[jkri__lmcqc]) for
        jkri__lmcqc in reversed(uybt__jtrhb.keys()))
    while work_list:
        dpgwh__dpb, block = work_list.pop()
        new_body = []
        wdpn__olxra = False
        for i, stmt in enumerate(block.body):
            if is_assign(stmt) and is_expr(stmt.value, 'getattr'):
                rhs = stmt.value
                rhs_type = typemap[rhs.value.name]
                if _inline_bodo_getattr(stmt, rhs, rhs_type, new_body,
                    func_ir, typingctx, targetctx, typemap, calltypes):
                    continue
            if is_call_assign(stmt):
                rhs = stmt.value
                dztic__cab = guard(find_callname, func_ir, rhs, typemap)
                if dztic__cab is None:
                    new_body.append(stmt)
                    continue
                func_name, func_mod = dztic__cab
                if _inline_bodo_call(rhs, i, func_mod, func_name, pass_info,
                    new_body, block, typingctx, targetctx, calltypes, work_list
                    ):
                    wdpn__olxra = True
                    break
            new_body.append(stmt)
        if not wdpn__olxra:
            uybt__jtrhb[dpgwh__dpb].body = new_body
    func_ir.blocks = ir_utils.simplify_CFG(func_ir.blocks)


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoDistributedPass(FunctionPass):
    _name = 'bodo_distributed_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        from bodo.transforms.distributed_pass import DistributedPass
        qcoqe__grtby = DistributedPass(state.func_ir, state.typingctx,
            state.targetctx, state.typemap, state.calltypes, state.
            return_type, state.metadata, state.flags)
        state.return_type = qcoqe__grtby.run()
        return True


@register_pass(mutates_CFG=True, analysis_only=False)
class BodoSeriesPass(FunctionPass):
    _name = 'bodo_series_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        assert state.func_ir
        hpz__gdqpk = SeriesPass(state.func_ir, state.typingctx, state.
            targetctx, state.typemap, state.calltypes, state.locals)
        apnz__jcmkh = hpz__gdqpk.run()
        bbaxn__ebhh = apnz__jcmkh
        if bbaxn__ebhh:
            bbaxn__ebhh = hpz__gdqpk.run()
        if bbaxn__ebhh:
            hpz__gdqpk.run()
        return apnz__jcmkh


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoDumpDistDiagnosticsPass(AnalysisPass):
    _name = 'bodo_dump_diagnostics_pass'

    def __init__(self):
        AnalysisPass.__init__(self)

    def run_pass(self, state):
        vvq__qoxdz = 0
        idm__gsbpi = 'BODO_DISTRIBUTED_DIAGNOSTICS'
        try:
            vvq__qoxdz = int(os.environ[idm__gsbpi])
        except:
            pass
        if vvq__qoxdz > 0 and 'distributed_diagnostics' in state.metadata:
            state.metadata['distributed_diagnostics'].dump(vvq__qoxdz,
                state.metadata)
        return True


class BodoCompilerSeq(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False,
            inline_calls_pass=inline_all_calls)


class BodoCompilerUDF(BodoCompiler):

    def define_pipelines(self):
        return self._create_bodo_pipeline(distributed=False, udf_pipeline=True)


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerParforSeq(FunctionPass):
    _name = 'bodo_lower_parfor_seq_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        bodo.transforms.distributed_pass.lower_parfor_sequential(state.
            typingctx, state.func_ir, state.typemap, state.calltypes, state
            .metadata)
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class LowerBodoIRExtSeq(FunctionPass):
    _name = 'bodo_lower_ir_ext_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        from bodo.transforms.distributed_pass import distributed_run_extensions
        from bodo.transforms.table_column_del_pass import remove_dead_table_columns
        from bodo.utils.transform import compile_func_single_block
        from bodo.utils.typing import decode_if_dict_array, to_str_arr_if_dict_array
        state.func_ir._definitions = build_definitions(state.func_ir.blocks)
        sux__reehx = TypingInfo(state.typingctx, state.targetctx, state.
            typemap, state.calltypes, state.func_ir.loc)
        remove_dead_table_columns(state.func_ir, state.typemap, sux__reehx)
        for block in state.func_ir.blocks.values():
            new_body = []
            for hquk__vwn in block.body:
                if type(hquk__vwn) in distributed_run_extensions:
                    ysqbs__mnhbr = distributed_run_extensions[type(hquk__vwn)]
                    if isinstance(hquk__vwn, bodo.ir.parquet_ext.ParquetReader
                        ) or isinstance(hquk__vwn, bodo.ir.sql_ext.SqlReader
                        ) and hquk__vwn.db_type in ('iceberg', 'snowflake'):
                        skss__dta = ysqbs__mnhbr(hquk__vwn, None, state.
                            typemap, state.calltypes, state.typingctx,
                            state.targetctx, is_independent=True,
                            meta_head_only_info=None)
                    else:
                        skss__dta = ysqbs__mnhbr(hquk__vwn, None, state.
                            typemap, state.calltypes, state.typingctx,
                            state.targetctx)
                    new_body += skss__dta
                elif is_call_assign(hquk__vwn):
                    rhs = hquk__vwn.value
                    dztic__cab = guard(find_callname, state.func_ir, rhs)
                    if dztic__cab == ('gatherv', 'bodo') or dztic__cab == (
                        'allgatherv', 'bodo'):
                        kxbk__ctyl = state.typemap[hquk__vwn.target.name]
                        sfjqi__roxuk = state.typemap[rhs.args[0].name]
                        if isinstance(sfjqi__roxuk, types.Array
                            ) and isinstance(kxbk__ctyl, types.Array):
                            mwj__oglfo = sfjqi__roxuk.copy(readonly=False)
                            fwbf__fhq = kxbk__ctyl.copy(readonly=False)
                            if mwj__oglfo == fwbf__fhq:
                                new_body += compile_func_single_block(eval(
                                    'lambda data: data.copy()'), (rhs.args[
                                    0],), hquk__vwn.target, sux__reehx)
                                continue
                        if (kxbk__ctyl != sfjqi__roxuk and 
                            to_str_arr_if_dict_array(kxbk__ctyl) ==
                            to_str_arr_if_dict_array(sfjqi__roxuk)):
                            new_body += compile_func_single_block(eval(
                                'lambda data: decode_if_dict_array(data)'),
                                (rhs.args[0],), hquk__vwn.target,
                                sux__reehx, extra_globals={
                                'decode_if_dict_array': decode_if_dict_array})
                            continue
                        else:
                            hquk__vwn.value = rhs.args[0]
                    new_body.append(hquk__vwn)
                else:
                    new_body.append(hquk__vwn)
            block.body = new_body
        return True


@register_pass(mutates_CFG=False, analysis_only=True)
class BodoTableColumnDelPass(AnalysisPass):
    _name = 'bodo_table_column_del_pass'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        phv__kbt = TableColumnDelPass(state.func_ir, state.typingctx, state
            .targetctx, state.typemap, state.calltypes)
        return phv__kbt.run()


def inline_calls(func_ir, _locals, work_list=None, typingctx=None,
    targetctx=None, typemap=None, calltypes=None):
    if work_list is None:
        work_list = list(func_ir.blocks.items())
    lsf__ibydt = set()
    while work_list:
        dpgwh__dpb, block = work_list.pop()
        lsf__ibydt.add(dpgwh__dpb)
        for i, iaqcv__etw in enumerate(block.body):
            if isinstance(iaqcv__etw, ir.Assign):
                spw__iixb = iaqcv__etw.value
                if isinstance(spw__iixb, ir.Expr) and spw__iixb.op == 'call':
                    msju__igi = guard(get_definition, func_ir, spw__iixb.func)
                    if isinstance(msju__igi, (ir.Global, ir.FreeVar)
                        ) and isinstance(msju__igi.value, CPUDispatcher
                        ) and issubclass(msju__igi.value._compiler.
                        pipeline_class, BodoCompiler):
                        cep__xedoh = msju__igi.value.py_func
                        arg_types = None
                        if typingctx:
                            unhp__okei = dict(spw__iixb.kws)
                            lix__hhsiv = tuple(typemap[tpzeu__xpird.name] for
                                tpzeu__xpird in spw__iixb.args)
                            lgwdu__cvktg = {gzqkv__tfada: typemap[
                                tpzeu__xpird.name] for gzqkv__tfada,
                                tpzeu__xpird in unhp__okei.items()}
                            fhfg__hmlg, arg_types = (msju__igi.value.
                                fold_argument_types(lix__hhsiv, lgwdu__cvktg))
                        fhfg__hmlg, iluc__nzs = inline_closure_call(func_ir,
                            cep__xedoh.__globals__, block, i, cep__xedoh,
                            typingctx=typingctx, targetctx=targetctx,
                            arg_typs=arg_types, typemap=typemap, calltypes=
                            calltypes, work_list=work_list)
                        _locals.update((iluc__nzs[gzqkv__tfada].name,
                            tpzeu__xpird) for gzqkv__tfada, tpzeu__xpird in
                            msju__igi.value.locals.items() if gzqkv__tfada in
                            iluc__nzs)
                        break
    return lsf__ibydt


def udf_jit(signature_or_function=None, **options):
    bcw__ocqbo = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    return numba.njit(signature_or_function, parallel=bcw__ocqbo,
        pipeline_class=bodo.compiler.BodoCompilerUDF, **options)


def is_udf_call(func_type):
    return isinstance(func_type, numba.core.types.Dispatcher
        ) and func_type.dispatcher._compiler.pipeline_class == BodoCompilerUDF


def is_user_dispatcher(func_type):
    return isinstance(func_type, numba.core.types.functions.ObjModeDispatcher
        ) or isinstance(func_type, numba.core.types.Dispatcher) and issubclass(
        func_type.dispatcher._compiler.pipeline_class, BodoCompiler)


@register_pass(mutates_CFG=False, analysis_only=True)
class DummyCR(FunctionPass):
    _name = 'bodo_dummy_cr'

    def __init__(self):
        FunctionPass.__init__(self)

    def run_pass(self, state):
        state.cr = (state.func_ir, state.typemap, state.calltypes, state.
            return_type)
        return True


def remove_passes_after(pm, location):
    assert pm.passes
    pm._validate_pass(location)
    for bnqf__ifv, (amndv__vfwd, fhfg__hmlg) in enumerate(pm.passes):
        if amndv__vfwd == location:
            break
    else:
        raise bodo.utils.typing.BodoError('Could not find pass %s' % location)
    pm.passes = pm.passes[:bnqf__ifv + 1]
    pm._finalized = False


class TyperCompiler(BodoCompiler):

    def define_pipelines(self):
        [pm] = self._create_bodo_pipeline()
        remove_passes_after(pm, InlineOverloads)
        pm.add_pass_after(DummyCR, InlineOverloads)
        pm.finalize()
        return [pm]


def get_func_type_info(func, arg_types, kw_types):
    typingctx = numba.core.registry.cpu_target.typing_context
    targetctx = numba.core.registry.cpu_target.target_context
    cpjlm__bsbvl = None
    suvuz__lni = None
    _locals = {}
    xlwlm__mkp = numba.core.utils.pysignature(func)
    args = bodo.utils.transform.fold_argument_types(xlwlm__mkp, arg_types,
        kw_types)
    kgsqi__lymmf = numba.core.compiler.Flags()
    onw__lqmre = {'comprehension': True, 'setitem': False, 'inplace_binop':
        False, 'reduction': True, 'numpy': True, 'stencil': False, 'fusion':
        True}
    fbf__ejw = {'nopython': True, 'boundscheck': False, 'parallel': onw__lqmre}
    numba.core.registry.cpu_target.options.parse_as_flags(kgsqi__lymmf,
        fbf__ejw)
    kaxss__uamuc = TyperCompiler(typingctx, targetctx, cpjlm__bsbvl, args,
        suvuz__lni, kgsqi__lymmf, _locals)
    return kaxss__uamuc.compile_extra(func)
