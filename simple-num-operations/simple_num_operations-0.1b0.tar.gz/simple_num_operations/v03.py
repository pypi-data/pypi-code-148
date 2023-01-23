# from numexpr import evaluate
# from colorama import Fore, init
#
# init()
#
#
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
