"""
A Printer which converts an expression into its semantic LaTeX equivalent.

See :ref:`sympy.printing` for the sympy printing subsystem.
"""
import builtins
import string
import logging
import sympy
from sympy import Symbol
from sympy.printing.latex import LatexPrinter

logger = logging.getLogger('sympy_to_sematic_latex')


def get_expression_type(expression):
    """
    Returns the expression type of a sympy expression.

    Usually `get_expression_type(expression)` is the same as `type(expression)`,
    but `get_expression_type` returns `sympy.core.function.AppliedUndef`
    for its subtypes representing sympy-functions instead of the subtype which is unique for each function.
    """
    expr_type = type(expression)
    if expr_type.__module__ == None:
        # Typen die nicht in einem Python-Modul definiert wurden zählen nicht
        # z.B. automatisch erzeugte Untertypen von AppliedUndef
        for supertype in expr_type.__mro__:
            if supertype.__module__:
                return supertype
    return expr_type


class SemanticLatexNotAvailableException(BaseException):
    """ Indicates a missing translation to semantic LaTeX. """

    def __init__(self, expression):
        """ Initialise a SemanticLatexNotAvailableException.

        Parameters
        ==========
        expression - the Sympy-expression which could not be converted
        """
        self.expression = expression

    def __str__(self):
        """ Return an error message for this Exception. """
        expr_type = get_expression_type(self.expression)
        return f'No semantic LaTeX translation is defined for the expression "{self.expression}" of type {expr_type.__module__}.{expr_type.__qualname__}.'

class FormatTemplate(string.Template):
    """ Extends string.Template for formatting semantic LaTeX representations of Sympy-expressions.

    This class uses numeric placeholders instead of alphanumeric ones.
    Each placeholder number is the index of an argument of the Sympy-expression,
    with 0 corresponding to the first argument.
    Each placeholders will be replaced by the semantic LaTeX representation
    of the corresponding argument.

    see :ref:`string.Template`
    """

    idpattern = "([0-9]*)"

class SemanticLatexPrinter(LatexPrinter):
    printmethod = "_semantic_latex"

    _default_settings = LatexPrinter._default_settings.copy()
    _default_settings["strict_mode"] = True
    _default_settings["generic_latex_table"] = [
        builtins.int,
        builtins.tuple,
        sympy.core.numbers.Integer,
        sympy.core.numbers.Float,
        sympy.core.symbol.Symbol,
        sympy.core.function.AppliedUndef,
        sympy.core.add.Add,
        sympy.core.mul.Mul,
        sympy.core.power.Pow,
        sympy.core.containers.Tuple,
    ]
    with sympy.evaluate(False):
        _default_settings['semantic_latex_table'] = {
            # trigonometric functions with their variants
            (sympy.functions.elementary.trigonometric.sin,1): (sympy.sin(Symbol("x0")),FormatTemplate(r"\sin@{$0}")),
            (sympy.functions.elementary.trigonometric.cos,1): (sympy.cos(Symbol("x0")),FormatTemplate(r"\cos@{$0}")),
            (sympy.functions.elementary.trigonometric.tan,1): (sympy.tan(Symbol("x0")),FormatTemplate(r"\tan@{$0}")),
            (sympy.functions.elementary.trigonometric.sec,1): (sympy.sec(Symbol("x0")),FormatTemplate(r"\sec@{$0}")),
            (sympy.functions.elementary.trigonometric.csc,1): (sympy.csc(Symbol("x0")),FormatTemplate(r"\csc@{$0}")),
            (sympy.functions.elementary.trigonometric.cot,1): (sympy.cot(Symbol("x0")),FormatTemplate(r"\cot@{$0}")),

            (sympy.functions.elementary.trigonometric.asin,1): (sympy.asin(Symbol("x0")),FormatTemplate(r"\asin@{$0}")),
            (sympy.functions.elementary.trigonometric.acos,1): (sympy.acos(Symbol("x0")),FormatTemplate(r"\acos@{$0}")),
            (sympy.functions.elementary.trigonometric.atan,1): (sympy.atan(Symbol("x0")),FormatTemplate(r"\atan@{$0}")),
            (sympy.functions.elementary.trigonometric.asec,1): (sympy.asec(Symbol("x0")),FormatTemplate(r"\asec@{$0}")),
            (sympy.functions.elementary.trigonometric.acsc,1): (sympy.acsc(Symbol("x0")),FormatTemplate(r"\acsc@{$0}")),
            (sympy.functions.elementary.trigonometric.acot,1): (sympy.acot(Symbol("x0")),FormatTemplate(r"\acot@{$0}")),

            (sympy.functions.elementary.hyperbolic.sinh,1): (sympy.sinh(Symbol("x0")),FormatTemplate(r"\sinh@{$0}")),
            (sympy.functions.elementary.hyperbolic.cosh,1): (sympy.cosh(Symbol("x0")),FormatTemplate(r"\cosh@{$0}")),
            (sympy.functions.elementary.hyperbolic.tanh,1): (sympy.tanh(Symbol("x0")),FormatTemplate(r"\tanh@{$0}")),
            (sympy.functions.elementary.hyperbolic.sech,1): (sympy.sech(Symbol("x0")),FormatTemplate(r"\sech@{$0}")),
            (sympy.functions.elementary.hyperbolic.csch,1): (sympy.csch(Symbol("x0")),FormatTemplate(r"\csch@{$0}")),
            (sympy.functions.elementary.hyperbolic.coth,1): (sympy.coth(Symbol("x0")),FormatTemplate(r"\coth@{$0}")),

            (sympy.functions.elementary.hyperbolic.asinh,1): (sympy.asinh(Symbol("x0")),FormatTemplate(r"\asinh@{$0}")),
            (sympy.functions.elementary.hyperbolic.acosh,1): (sympy.acosh(Symbol("x0")),FormatTemplate(r"\acosh@{$0}")),
            (sympy.functions.elementary.hyperbolic.atanh,1): (sympy.atanh(Symbol("x0")),FormatTemplate(r"\atanh@{$0}")),
            (sympy.functions.elementary.hyperbolic.asech,1): (sympy.asech(Symbol("x0")),FormatTemplate(r"\asech@{$0}")),
            (sympy.functions.elementary.hyperbolic.acsch,1): (sympy.acsch(Symbol("x0")),FormatTemplate(r"\acsch@{$0}")),
            (sympy.functions.elementary.hyperbolic.acoth,1): (sympy.acoth(Symbol("x0")),FormatTemplate(r"\acoth@{$0}")),

            # exponential function and logarithm
            (sympy.functions.elementary.exponential.log,1): (sympy.log(Symbol("x0")), FormatTemplate(r"\log@{$0}")),
            (sympy.functions.elementary.exponential.log,2): (sympy.log(Symbol("x0"),Symbol("x1")), FormatTemplate(r"\genlog{$0}@{$1}")),
            (sympy.functions.elementary.exponential.exp,1): (sympy.exp(Symbol("x0")), FormatTemplate(r"\exp@{$0}")),
            # That should suffice as defaults for now, the user can append to this dict as needed.
        }

    def tree_match(self, expression, template_expression):
        format_arguments = {}
        # x0, x1, ... durch die entsprechenden Teilausdrücke ersetzen
        if isinstance(template_expression,sympy.core.symbol.Symbol) and template_expression.name[0] == "x":
            number = template_expression.name[1:]
            if number.isdigit(): # could be multiple digits
                return {number: self._print(expression)}
        # Ausdruck vergleichen
        if expression.func != template_expression.func:
            return None
        if len(expression.args) != len(template_expression.args):
            return None
        # Teilausdrücke vergleichen
        for arg, template_arg in zip(expression.args,template_expression.args):
            arg_result = self.tree_match(arg,template_arg)
            if arg_result == None:
                return None
            format_arguments.update(arg_result)
        return format_arguments

    def _print(self, expression, exp=None):
        """ Extends Printer._print to look up the expression type first.

        Expression types specified in the semantic latex table will be translated as
        specified there without getting the LaTeX representation from LatexPrinter.

        Other expressions will be passed to LatexPrinter and the resulting
        generic LaTeX representation is used as semantic LaTeX representation.
        If the expression type is not found in the generic latex table however,
        a warning will be logged, and if strict mode is enabled
        a SemanticLatexNotAvailableException will be raised.

        see :ref:`sympy.printing.printer.Printer`
        see :ref:`sympy.printing.latex.LatexPrinter`
        """
        if exp != None:
            result = self._print(expression)
            result = self.parenthesize_super(result)
            return "{" + result + "}^{" + exp + "}"
        semantic_latex_table = self._settings['semantic_latex_table']
        generic_latex_table = self._settings['generic_latex_table']
        # use semantic latex table to format the expression
        expr_type = get_expression_type(expression)
        arg_count = len(getattr(expression, "args", ()))
        if (expr_type, arg_count) in semantic_latex_table:
            format_template = semantic_latex_table[(expr_type, arg_count)]
            if isinstance(format_template,tuple):
                logger.debug(f"Matching {expression} against {format_template[0]}...")
                format_arguments = self.tree_match(expression, format_template[0])
                format_template = format_template[1]
            else:
                format_arguments = {str(i): self._print(expression.args[i]) for i in range(arg_count)}
            if format_arguments != None:
                return format_template.substitute(format_arguments)
            logger.warning(f'Unable to translate "{expression}": Translation entry for {expr_type.__module__}.{expr_type.__qualname__} with {arg_count} arguments did not match.')

        # pass through to use the generic latex representation:
        # use method resolution order to check if the expression has an allowed type as superclass
        allowed = False
        for allowed_type in generic_latex_table:
            if isinstance(expression, allowed_type):
                allowed = True
        if not allowed:
            if not expr_type in (key[0] for key in semantic_latex_table.keys()):
                logger.warning(f'Unable to translate "{expression}": No translation entry for {expr_type.__module__}.{expr_type.__qualname__} found.')
            else:
                logger.warning(f'Unable to translate "{expression}": No translation entry for {expr_type.__module__}.{expr_type.__qualname__} with {arg_count} arguments found.')
                allowed_number_args = None
                for k, count in semantic_latex_table:
                    if k == expr_type:
                        logger.info(f'There is a translation entry for "{expr_type.__module__}.{expr_type.__qualname__}" with {count} arguments.')
            if self._settings['strict_mode']:
                raise SemanticLatexNotAvailableException(expression)
        return LatexPrinter._print(self, expression)

    def emptyPrinter(self, expression):
        """ Extends the fallback print method to raise an exception in strict mode.

        see :ref:`sympy.printing.printer.Printer.emptyPrinter`
        """
        expr_type = get_expression_type(expression)
        logger.warning(f'Reached fallback print method: No semantic latex translation for "{expression}" of type {expr_type.__module__}.{expr_type.__qualname__} with {len(expression.args)} arguments available.')
        if self._settings['strict_mode']:
            raise SemanticLatexNotAvailableException(expression)
        return LatexPrinter.emptyPrinter(self, expression)


@sympy.printing.printer.print_function(SemanticLatexPrinter)
def sympy_to_semantic_latex(expression, **settings):
    r"""Convert the given sympy-expression to a semantic LaTeX string representation.

    Parameters
    ==========
    strict_mode: boolean, optional
        If set to False, the regular LaTeX representation is used for expressions
        for which no translation to semantic LaTeX is known.
        If set to True, this fallback is disallowed and
        will cause a SemanticLatexNotAvailableException to be raised instead.
        
    generic_latex_table: list, optional
        Lists the expression types where the LaTeX representation
        can be used as semantic LaTeX representation.
        Printing of these expressions will be delegated to the superclass LatexPrinter,
        without issueing a warning or throwing an Exception.

    semantic_latex_table: dict, optional
        This dictionary defines how to print expressions as semantic LaTeX.
        The keys are tuples consisting of the type of expression and number of arguments.
        The values are tuples consisting of a template expression and a `FormatTemplate`
        for formatting the semantic LaTeX representation.
        In the template expression the variables `x0`, `x1`,… are used as placeholders
        for arbitrary subexpressions. These correspond to the placeholders "$0", "$1",…
        used in the FormatTemplate.

    The print settings for sympy.printing.latex.LatexPrinter are accepted as well.
    see :ref:`sympy.printing.latex.latex`

    Exceptions
    ==========
    SemanticLatexNotAvailableException
        Will be raised if strict mode is enabled and a subexpression is encountered
        for which the translation to semantic LaTeX is not known.
    """
    return SemanticLatexPrinter(settings).doprint(expression)

