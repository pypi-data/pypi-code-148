'''Программа-клиент'''
import argparse
import os
import sys
import logging

from Crypto.PublicKey import RSA

from common.errors import ServerError
from common.variables import *
from common.decos import log

from PyQt5.QtWidgets import QApplication, QMessageBox
from clients.transport import ClientTransport
from clients.data_clients import ClientDatabase
from clients.main_window import ClientMainWindow
from clients.start_dialog import UserNameDialog

# Инициализация логера для клиентской части
Client_logger = logging.getLogger('client_dist')


@log
def arg_parser():
    '''
    Создаём парсер аргументов коммандной строки
    и читаем параметры, возвращаем 3 параметра
    '''
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    my_parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    my_parser.add_argument('-n', '--name', default=None, nargs='?')
    my_parser.add_argument('-p', '--password', default='', nargs='?')
    namespace = my_parser.parse_args(sys.argv[1:])
    address = namespace.addr
    port = namespace.port
    name = namespace.name
    pswd = namespace.password

    # проверим подходящий номер порта
    if not 1023 < port < 65536:
        Client_logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    return address, port, name, pswd


if __name__ == '__main__':
    # Загружаем параметы коммандной строки
    address, port, name, pswd = arg_parser()
    Client_logger.debug('Args loaded')

    # Создаём клиентокое приложение
    client_app = QApplication(sys.argv)

    # Если имя пользователя не было указано в командной строке то запросим его
    start_dialog = UserNameDialog()
    if not name or pswd:
        client_app.exec_()
        # Если пользователь ввёл имя и нажал ОК, то сохраняем ведённое
        # и удаляем объект, инааче выходим
        if start_dialog.ok_pressed:
            name = start_dialog.client_name.text()
            pswd = start_dialog.client_passwd.text()
            Client_logger.debug(f'Using USERNAME = {name}, PASSWD = {pswd}.')
        else:
            exit(0)

    # Записываем логи
    Client_logger.info(
        f'Запущен клиент с парамертами: адрес сервера: {address} , '
        f'порт: {port}, имя пользователя: {name}')

    # Загружаем ключи с файла, если же файла нет, то генерируем новую пару.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    key_file = os.path.join(dir_path, f'{name}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    # !!!keys.publickey().export_key()
    Client_logger.debug("Keys sucsessfully loaded.")
    # Создаём объект базы данных
    database = ClientDatabase(name)

    # Создаём объект - транспорт и запускаем транспортный поток
    try:
        transport = ClientTransport(port, address, database, name, pswd, keys)
        Client_logger.debug("Transport ready.")
    except ServerError as error:
        message = QMessageBox()
        message.critical(start_dialog, 'Ошибка сервера', error.text)
        exit(1)
    transport.setDaemon(True)
    transport.start()

    # Удалим объект диалога за ненадобностью
    del start_dialog

    # Создаём GUI
    main_window = ClientMainWindow(database, transport, keys)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат Программа alpha release - {name}')
    client_app.exec_()

    # Раз графическая оболочка закрылась, закрываем транспорт
    transport.transport_shutdown()
    transport.join()
