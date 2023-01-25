'''Программа-сервер'''
import argparse
import configparser
import os
import sys
import logging
from common.decos import log
from common.variables import DEFAULT_PORT
from my_server.core import MessageProcessor
from my_server.database_serv import ServerStorage
from my_server.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt


# Инициализация логирования сервера.
Serv_log = logging.getLogger('server_dist')


@log
def arg_parser(default_port, default_address):
    '''
    Парсер аргументов коммандной строки
    '''
    Serv_log.debug(f'Инициализация парсера аргументов коммандной строки: {sys.argv}')
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-p', default=default_port, type=int, nargs='?')
    my_parser.add_argument('-a', default=default_address, nargs='?')
    my_parser.add_argument('--no_gui', action='store_true')
    namespace = my_parser.parse_args(sys.argv[1:])
    address = namespace.a
    port = namespace.p
    gui_flag = namespace.no_gui
    Serv_log.debug('Аргументы успешно загружены.')
    return address, port, gui_flag


# Загрузка файла конфигурации
@log
def config_load():
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read(f"{dir_path}/{'server.ini'}")
    # Если конфиг файл загружен правильно, запускаемся, иначе конфиг по умолчанию.
    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'Default_port', str(DEFAULT_PORT))
        config.set('SETTINGS', 'Listen_Address', '')
        config.set('SETTINGS', 'Database_path', '')
        config.set('SETTINGS', 'Database_file', 'server_database.db3')
        return config


@log
def main():
    # Загрузка файла конфигурации сервера
    config = config_load()

    # Загрузка параметров командной строки, если нет параметров, то задаём
    # значения по умоланию.
    address, port, gui_flag = arg_parser(
        config['SETTINGS']['Default_port'], config['SETTINGS']['Listen_Address'])

    # Инициализация базы данных
    database = ServerStorage(
        os.path.join(
            config['SETTINGS']['Database_path'],
            config['SETTINGS']['Database_file']))

    # Создание экземпляра класса - сервера и его запуск:
    server = MessageProcessor(address, port, database)
    server.daemon = True
    server.start()

    # Если  указан параметр без GUI то запускаем простенький обработчик
    # консольного ввода
    if gui_flag:
        while True:
            command = input('Введите exit для завершения работы сервера.')
            if command == 'exit':
                # Если выход, то завршаем основной цикл сервера.
                server.running = False
                server.join()
                break

    # Если не указан запуск без GUI, то запускаем GUI:
    else:
        # Создаём графическое окуружение для сервера:
        server_app = QApplication(sys.argv)
        server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        main_window = MainWindow(database, server, config)

        # Запускаем GUI
        server_app.exec_()

        # По закрытию окон останавливаем обработчик сообщений
        server.running = False


if __name__ == '__main__':
    main()
