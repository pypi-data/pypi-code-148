import logging
import sys

# метод определения модуля, источника запуска.
if sys.argv[0].find('client') == -1:
    # если не клиент то сервер!
    logger = logging.getLogger('server')
else:
    # ну, раз не сервер, то клиент
    logger = logging.getLogger('client')


# Дескриптор для описания порта:
class Port:
    # сеттер значения для нашего порта
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            logger.critical(f'Некоректный порт {value}. Допустимы адреса с 1024 до 65535.')
            raise TypeError('Некорректрый номер порта')
        # Если порт корректный, добавляем его в словарь атрибутов экземпляра
        instance.__dict__[self.name] = value

    # устанавливаем имя порта по значению
    def __set_name__(self, owner, name):
        # owner - <class '__main__.Server'>
        # name - port
        self.name = name
