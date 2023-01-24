"""
JIT support for Python's logging module
"""
import logging
import numba
from numba.core import types
from numba.core.imputils import lower_constant
from numba.core.typing.templates import bound_function
from numba.core.typing.templates import AttributeTemplate, infer_getattr, signature
from numba.extending import NativeValue, box, models, overload_attribute, overload_method, register_model, typeof_impl, unbox
from bodo.utils.typing import create_unsupported_overload, gen_objmode_attr_overload


class LoggingLoggerType(types.Type):

    def __init__(self, is_root=False):
        self.is_root = is_root
        super(LoggingLoggerType, self).__init__(name=
            f'LoggingLoggerType(is_root={is_root})')


@typeof_impl.register(logging.RootLogger)
@typeof_impl.register(logging.Logger)
def typeof_logging(val, c):
    if isinstance(val, logging.RootLogger):
        return LoggingLoggerType(is_root=True)
    else:
        return LoggingLoggerType(is_root=False)


register_model(LoggingLoggerType)(models.OpaqueModel)


@box(LoggingLoggerType)
def box_logging_logger(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(LoggingLoggerType)
def unbox_logging_logger(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@lower_constant(LoggingLoggerType)
def lower_constant_logger(context, builder, ty, pyval):
    eljq__xyuvg = context.get_python_api(builder)
    return eljq__xyuvg.unserialize(eljq__xyuvg.serialize_object(pyval))


gen_objmode_attr_overload(LoggingLoggerType, 'level', None, types.int64)
gen_objmode_attr_overload(LoggingLoggerType, 'name', None, 'unicode_type')
gen_objmode_attr_overload(LoggingLoggerType, 'propagate', None, types.boolean)
gen_objmode_attr_overload(LoggingLoggerType, 'disabled', None, types.boolean)
gen_objmode_attr_overload(LoggingLoggerType, 'parent', None,
    LoggingLoggerType())
gen_objmode_attr_overload(LoggingLoggerType, 'root', None,
    LoggingLoggerType(is_root=True))


@infer_getattr
class LoggingLoggerAttribute(AttributeTemplate):
    key = LoggingLoggerType

    def _resolve_helper(self, logger_typ, args, kws):
        kws = dict(kws)
        yntr__quwsr = ', '.join('e{}'.format(uqgxo__mgc) for uqgxo__mgc in
            range(len(args)))
        if yntr__quwsr:
            yntr__quwsr += ', '
        hea__cau = ', '.join("{} = ''".format(mehbj__rnz) for mehbj__rnz in
            kws.keys())
        ednv__ffsc = f'def format_stub(string, {yntr__quwsr} {hea__cau}):\n'
        ednv__ffsc += '    pass\n'
        juwi__rbd = {}
        exec(ednv__ffsc, {}, juwi__rbd)
        cqbr__vplxo = juwi__rbd['format_stub']
        xeohs__ijs = numba.core.utils.pysignature(cqbr__vplxo)
        sgvl__fgw = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, sgvl__fgw).replace(pysig=xeohs__ijs)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for unk__sjiw in ('logging.Logger', 'logging.RootLogger'):
        for gzx__iuwuc in func_names:
            ykt__jpoam = f'@bound_function("{unk__sjiw}.{gzx__iuwuc}")\n'
            ykt__jpoam += (
                f'def resolve_{gzx__iuwuc}(self, logger_typ, args, kws):\n')
            ykt__jpoam += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(ykt__jpoam)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for gvu__kmcp in logging_logger_unsupported_attrs:
        eywh__yjj = 'logging.Logger.' + gvu__kmcp
        overload_attribute(LoggingLoggerType, gvu__kmcp)(
            create_unsupported_overload(eywh__yjj))
    for jle__dqus in logging_logger_unsupported_methods:
        eywh__yjj = 'logging.Logger.' + jle__dqus
        overload_method(LoggingLoggerType, jle__dqus)(
            create_unsupported_overload(eywh__yjj))


_install_logging_logger_unsupported_objects()
