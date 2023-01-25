import logging
import os
import sys
#sys.path.append(os.path.join(os.getcwd(), '../..'))
sys.path.append('../..')
from common.variables import LOGGING_LEVEL


# настраиваем формат выводимого сообщения
CLIENT_FORMATTER = logging.Formatter("%(asctime)s %(levelname)s %(module)s %(message)s")

# подготовка имени файла для логирования - из абсолютного пути до файла берем директорию
# и добавляем к ней имя файла для логирования
PATH = os.path.dirname(os.getcwd())
PATH = os.path.join(PATH, 'log_files/client.log')

# создаем обработчики вывода в поток и в файл
STREAM_HANDLER = logging.StreamHandler(sys.stdout)
STREAM_HANDLER.setFormatter(CLIENT_FORMATTER)
STREAM_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER = logging.FileHandler(PATH, encoding='utf-8')
FILE_HANDLER.setFormatter(CLIENT_FORMATTER)

# создаем объект логгера, подключаем обработчики и устанавливаем уровень важности
LOGGER = logging.getLogger('client')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(LOGGING_LEVEL)


if __name__ == '__main__':
    LOGGER.critical('Critical error')
    LOGGER.error('Error')
    LOGGER.debug('Debug')
    LOGGER.info('Information')
