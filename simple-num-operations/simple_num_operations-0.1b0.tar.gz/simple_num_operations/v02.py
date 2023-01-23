from .buildutils_sno import is_expr
from colorama import Fore, init

init()


def calculate_simple(expression):
    if is_expr(expression) is False:
        return Fore.LIGHTRED_EX + 'Это не математическое выражение!' + Fore.RESET
    try:
        return Fore.LIGHTGREEN_EX + f'>>> {eval(expression)}' + Fore.RESET
    except ValueError:
        return Fore.LIGHTRED_EX + 'Ответ на выражение настолько большой, что лимит длины строки превышен!' + Fore.RESET
    except ZeroDivisionError:
        return Fore.LIGHTRED_EX + 'Нельзя делить на ноль!' + Fore.RESET
    except SyntaxError:
        return Fore.LIGHTRED_EX + 'Ошибка синтаксиса!' + Fore.RESET

