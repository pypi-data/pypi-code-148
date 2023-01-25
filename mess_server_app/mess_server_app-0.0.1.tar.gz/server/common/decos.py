import logging
import sys
import socket
sys.path.append('../../HW/')



# метод определения модуля из которого запущена функция (в нашем случае client или server)
# метод find() возвращает индекс первого вхождения искомой подстроки, или -1 если подстрока не найдена
# если в исполнямом модуле нет подстроки 'client', то модуль относится к серверу => получаем логгер server
if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


# Функция декоратор
def log(logged_function):
    """Декоратор, выполняющий логирование вызовов функций."""
    def wrapper(*args, **kwargs):
        LOGGER.debug(f'Была вызвана функция {logged_function.__name__} из модуля {logged_function.__module__}. ')
        # f'Из функции {traceback.format_stack()[0].strip().split()[-1]} '
        # f'Из функции {inspect.stack()[1][3]}', stacklevel=2)
        res = logged_function(*args, **kwargs)
        return res
    return wrapper

# # Декоратор в виде класса с перегрузкой метода __call__
# class Log:
#
#     def __call__(self, logged_function):
#
#         def wrapper(*args, **kwargs):
#             result = logged_function(*args, **kwargs)
#             LOGGER.debug(
#                 f'Была вызвана функция {logged_function.__name__} с позиционными параметрами {args}, '
#                 f'именнованными параметрами {kwargs}'
#                 f'Вызов был выполнен из модуля {logged_function}'
#                 f'Из функции {traceback.format_stack()[0].strip().split()[-1]}'
#                 f'Из функции {inspect.stack()[1][3]}', stacklevel=2
#             )
#             return result
#         return wrapper


def login_required(func):
    """
    Декоратор, проверяющий, что клиент авторизован на сервере.
    Проверяет, что передаваемый объект сокета находится в
    списке авторизованных клиентов.
    """
    def checker(*args, **kwargs):
        # проверяем, что первый аргумент - экземпляр MessageProcessor
        # Импортить необходимо тут, иначе ошибка рекурсивного импорта.
        from pack_server.server import MessageProcessor
        from common.variables import ACTION, PRESENCE
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    # Проверяем, что данный сокет есть в списке names класса MessageProcessor
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True

            # Теперь надо проверить, что передаваемые аргументы не presence сообщение.
            # Если presence, то разрешаем
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True
            # Если не не авторизован и не сообщение начала авторизации, то вызываем исключение.
            if not found:
                raise TypeError
        return func(*args, **kwargs)

    return checker
