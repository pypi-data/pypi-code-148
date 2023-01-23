from .exceptions_all import NotMathsExpression
from .buildutils_sno import is_expr


def calculate(expression):
    if is_expr(expression) is False:
        raise NotMathsExpression('Input data is not expression!')
    return eval(expression)
