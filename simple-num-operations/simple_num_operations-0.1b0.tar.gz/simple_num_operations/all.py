from colorama import Fore, init
from .exceptions_all import NotMathsExpression
from .buildutils_sno import is_expr

init()


def calculate(expression):
    if is_expr(expression) is False:
        raise NotMathsExpression('Input data is not expression!')
    return eval(expression)


def calculate_simple(expression):
    if is_expr(expression) is False:
        return Fore.LIGHTRED_EX + '>>> Это не математическое выражение!'
    return Fore.LIGHTGREEN_EX + f'>>> {eval(expression)}'


# def calculate_exr(expression: str) -> str:
#     try:
#         return Fore.LIGHTGREEN_EX + f'>>> {evaluate(expression)}'
#     except KeyboardInterrupt:
#         return Fore.LIGHTYELLOW_EX + '\n>>> Программа остановлена.'
#     except TypeError:
#         return Fore.LIGHTRED_EX + '>>> Операция невыполнима! Это программа, а не выражение!'
#     except KeyError:
#         return Fore.LIGHTRED_EX + '>>> Процесс завершился ошибкой KeyError, значит, это не математическое выражение.'
#     except SyntaxError:
#         return '>>> Это программа, да к тому же, с ошибкой синтаксиса)'
#     except OverflowError:
#         return Fore.LIGHTRED_EX + '>>> У выражения слишком большой ответ...'
