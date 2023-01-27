
import logging
import csv
import re
import sympy

from printer import SemanticLatexPrinter, FormatTemplate, get_expression_type

logger = logging.getLogger('sympy_to_semantic_latex')
replacement_dict = {"diff": "Derivative", "integrate": "Integral", "summation": "Sum", "product": "Product", "limit": "Limit"} #TODO: add further cases


def load_csv_file(filename):
    csv_semantic_latex_table = {}
    with open(filename) as file:
        reader = csv.reader(file, delimiter=";")
        for line in reader:
            if line == []: continue
            if line[0] != '' and line[2].isdigit():
                translation_as_FormatTemplate = FormatTemplate(line[1])
                # substitute ($0, $1, ...) with (x0, x1, ...)
                sympy_expression = line[0].replace('$',' x')
                expr_func = sympy_expression.partition('(')[0]
                if expr_func in replacement_dict.keys():
                    sympy_expression = sympy_expression.replace(expr_func, replacement_dict[expr_func], 1)
                    logger.warning(f'{expr_func} is not a sympy symbolic function: replaced {expr_func} \
with {replacement_dict[expr_func]} to make function correctly translatable.')
                with sympy.evaluate(True):
                    expr = sympy.sympify(sympy_expression,evaluate=False)
                expr_func = get_expression_type(expr)
                arg_count = len(getattr(expr, "args", ()))
                csv_semantic_latex_table[(expr_func, arg_count)] = (expr, translation_as_FormatTemplate)
    return csv_semantic_latex_table

def load_csv_file_for_printer(filename, printer : SemanticLatexPrinter = None):
    semantic_latex_table = load_csv_file(filename)
    if printer == None:
        # set the default table for SemanticLatexPrinter
        SemanticLatexPrinter._global_settings['semantic_latex_table'] = semantic_latex_table
    else:
        # only change the table for the given printer
        printer._settings['semantic_latex_table'] = semantic_latex_table
