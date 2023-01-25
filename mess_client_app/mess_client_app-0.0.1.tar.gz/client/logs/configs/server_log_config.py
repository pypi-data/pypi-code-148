import logging.handlers
import os
import sys
sys.path.append('../..')
# sys.path.append(os.path.join(os.getcwd(), '../..'))
from common.variables import LOGGING_LEVEL

# настраиваем формат выводимого сообщения
SERVER_FORMATTER = logging.Formatter("%(asctime)s %(levelname)s %(module)s %(message)s")

# подготовка имени файла для логирования - из абсолютного пути до файла берем директорию
# и добавляем к ней имя файла для логирования
PATH = os.path.dirname(os.getcwd())
PATH = os.path.join(PATH, 'log_files/server.log')

# создаем обработчики вывода в поток и в файл
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(SERVER_FORMATTER)
STREAM_HANDLER.setLevel(logging.INFO)
FILE_HANDLER = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D')
FILE_HANDLER.setFormatter(SERVER_FORMATTER)
SIMPLE_FILE_HANDLER = logging.FileHandler(PATH, encoding='utf-8')
SIMPLE_FILE_HANDLER.setFormatter(SERVER_FORMATTER)


# создаем объект логгера, подключаем обработчики и устанавливаем уровень важности
logger = logging.getLogger('server')
logger.addHandler(STREAM_HANDLER)
logger.addHandler(SIMPLE_FILE_HANDLER)
logger.addHandler(FILE_HANDLER)
logger.setLevel(LOGGING_LEVEL)


if __name__ == '__main__':
    logger.critical('Critical error')
    logger.error('Error')
    logger.debug('Debug')
    logger.info('Information')
