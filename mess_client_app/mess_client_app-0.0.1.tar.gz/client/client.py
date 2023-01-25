"""Программа-клиент"""
import argparse
import os
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from pack_client.client.client.main_window import ClientMainWindow
from pack_client.client.client.transport import ClientTransport
from pack_client.client.client.start_dialog import UserNameDialog
from pack_client.client.client.database import ClientDatabase
from pack_server.server.common import ServerError
from pack_server.server.common import log
from Cryptodome.PublicKey import RSA

# Инициализация логгера
CLIENT_LOGGER = logging.getLogger('client')


@log
def arg_parser():
    """Парсер аргументов коммандной строки
    и читаем параметры, проверяем корректность порта и
    возвращаем кортеж из 4х параметров
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    parser.add_argument('-p', '--password', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name
    client_passwd = namespace.password

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(f'Некорректный номер порта: {server_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    return server_address, server_port, client_name, client_passwd


def main():
    """Основная функция клиента"""
    print('Консольный мессенджер. Клиентский модуль.')
    # Загружаем параметы коммандной строки
    server_address, server_port, client_name, client_passwd = arg_parser()

    # Создаём клиентское приложение
    client_app = QApplication(sys.argv)

    # Если имя пользователя не было задано, необходимо его запросить
    starting_dialog = UserNameDialog()
    if not client_name or not client_passwd:
        client_app.exec_()
        # Если пользователь ввёл имя и пароль и нажал ОК, то сохраняем ведённое и удаляем объект, иначе выходим
        if starting_dialog.ok_pressed:
            client_name = starting_dialog.client_name.text()
            client_passwd = starting_dialog.client_passwd.text()
            # del starting_dialog
        else:
            sys.exit(0)

    # Записываем логи
    CLIENT_LOGGER.info(f'Запущен клиент {client_name} с парамертами: адрес: {server_address} , порт: {server_port}')

    # Загружаем ключи с файла, если же файла нет, то генерируем новую пару.
    dir_path = os.getcwd()
    key_file = os.path.join(dir_path, f'{client_name}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    # keys.publickey().export_key()
    CLIENT_LOGGER.debug("Ключ загружен.")

    # Создаём объект базы данных
    database = ClientDatabase(client_name)
    CLIENT_LOGGER.debug("БД создана.")

    # Создаём объект - транспорт и запускаем транспортный поток
    try:
        transport = ClientTransport(
            server_port,
            server_address,
            database,
            client_name,
            client_passwd,
            keys)
    except ServerError as error:
        CLIENT_LOGGER.info(error.text)
        message = QMessageBox()
        message.critical(UserNameDialog(), 'Ошибка сервера', error.text)
        sys.exit(1)
    transport.setDaemon(True)
    transport.start()

    # Удалим объект диалога за ненадобностью
    del starting_dialog

    # Создаём GUI
    main_window = ClientMainWindow(database, transport, keys)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат Программа alpha release - {client_name}')
    client_app.exec_()

    # Раз графическая оболочка закрылась, закрываем транспорт
    transport.transport_shutdown()
    transport.join()


if __name__ == '__main__':
    main()
