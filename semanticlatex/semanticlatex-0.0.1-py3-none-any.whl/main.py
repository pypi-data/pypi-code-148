#!/usr/bin/python3
"""
main file of the module
This file adds the method semanticLatex to sympy.core.Basic
for translating Sympy-expressions to semantic latex.
Calling .semanticLatex() on a Sympy-expression is equivalent
to calling sympy_to_semantic_latex with the expression as argument.
see :ref:`sympy.core.Basic`
see :ref:`sympy_to_semantic_latex`
"""
import sympy.core
from printer import SemanticLatexPrinter, sympy_to_semantic_latex, SemanticLatexNotAvailableException
from csv_loader import load_csv_file, load_csv_file_for_printer

def sympy_to_semantic_latex_wrapper(expression,**settings):
    """ wrapper function for calling sympy_to_semantic_latex as a method
    The @PrintFunction decorator somehow interferes with sympy_to_semantic_latex
    being callable as a method. This wrapper transforms the method call to a regular call. """
    return sympy_to_semantic_latex(expression,**settings)

sympy.core.Basic.semanticLatex = sympy_to_semantic_latex_wrapper


if __name__ == "__main__":
    # == Logger configuration ==
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('sympy_to_sematic_latex')
    logger.setLevel(logging.INFO)

    # == other setup ==
    try:
        import readline
    except ModuleNotFoundError:
        printer.logger.info('The module "readline" is not available.')

    from sympy.parsing import sympy_parser
    from sympy.printing.repr import srepr
    import sys
    if len(sys.argv) > 1:
        load_csv_file_for_printer(sys.argv[1])
        #for entry in SemanticLatexPrinter._global_settings["semantic_latex_table"].items():
        #    print(entry)

    # == main loop ==
    try:
        while True:
            expression = sympy_parser.parse_expr(input("Enter a Sympy-expression: "),evaluate=False)
            #print(srepr(expression))
            try:
                print(sympy_to_semantic_latex(expression))
            except SemanticLatexNotAvailableException as ex:
                print("Translation failed:",ex)
    except (EOFError, IndexError):
        # EOFError occurs when the prompt is answered with end-of-file (CTRL-D or on Windows CTRL-Z),
        # IndexError occurs when an empty expression is given (by pressing Enter immediately after the prompt)
        # Either case is taken as indication that the user wants to exit the program.
        pass
