import threading
import logging
import select
import socket
import json
import hmac
import binascii
import os
# sys.path.append(os.path.join(os.getcwd(), '..'))
# sys.path.append('../')
from common.descryptors import Port
from common.variables import *
from pack_server.server.common.utils import send_message, get_message
from common.decos import login_required

# Загрузка логера
logger = logging.getLogger('server')


class MessageProcessor(threading.Thread):
    """
    Основной класс сервера. Принимает содинения, словари - пакеты
    от клиентов, обрабатывает поступающие сообщения.
    Работает в качестве отдельного потока.
    """
    # дескриптор порта
    port = Port()

    def __init__(self, listen_address, listen_port, database):
        # Инициализируем паратметры сервера. Принимаем порт, адрес и БД.
        self.addr = listen_address
        self.port = listen_port
        self.database = database
        # Сокет, через который будет осуществляться работа
        self.sock = None
        # Список подключённых клиентов.
        self.clients = []
        # Сокеты
        self.listen_sockets = None      # ожидающие сообщения от сервера
        self.error_sockets = None
        # Флаг продолжения работы
        self.running = True
        # Словарь содержащий сопоставленные имена и соответствующие им сокеты.
        self.names = dict()
        # Конструктор предков - позволяет работать с атрибутами класса родителя
        super().__init__()

    def run(self):
        """Метод - основной цикл потока - в бесконечном цикле принимаем и разбираем подключения"""
        # Инициализация Сокета
        self.init_socket()
        logger.info('Инициализирован сокет сервера')

        # Основной цикл программы сервера
        while self.running:
            # Ждём подключения, если таймаут вышел а подключния нет - ловим исключение.
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                logger.info(f'Установлено соедение с ПК {client_address} в core.py')
                client.settimeout(5)
                self.clients.append(client)

            receive_data_lst = []
            # выше заменили на self.listen_sockets, self.error_sockets
            # send_data_lst = []
            # err_lst = []

            # проверяем наличие новых подключений или новых данных от уже имеющихся
            try:
                # в self.clients сейчас подключившиеся к нашему серверу сокеты клиентов,
                # проверяем кто из них ждет данные а кто отпавляет
                if self.clients:
                    receive_data_lst, self.listen_sockets, self.error_sockets = select.select(
                        self.clients, self.clients, [], 0)
            except OSError as err:
                logger.error(f'core.py - Ошибка работы с сокетами: {err.errno}')

            # если есть новые сокеты отправляющие нам сообщения - принимаем сообщения и если ошибка, исключаем клиента.
            if receive_data_lst:
                for client_with_message in receive_data_lst:
                    try:
                        # функция разбора сообщения от клиента
                        self.process_client_message(get_message(client_with_message), client_with_message)
                    except (OSError, json.JSONDecodeError, TypeError):
                        #  если ошибка - удаляем неактивного клиента из подключившихся
                        self.remove_client(client_with_message)

    def remove_client(self, client):
        """
        Метод обработчик клиента с которым прервана связь.
        Ищет клиента и удаляет его из списка подключенных клиентов и базы:
        """
        # getpeername() возвращает адрес машины, подключившейся к сокету
        logger.info(f'Клиент {client.getpeername()} отключился от сервера')
        for name in self.names:
            if self.names[name] == client:
                self.database.user_logout(name)
                del self.names[name]
                break
        self.clients.remove(client)
        client.close()

    def init_socket(self):
        """Метод инициализатор сокета."""
        # Готовим сокет
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.addr, self.port))
        transport.settimeout(0.5)

        # Начинаем слушать сокет.
        self.sock = transport
        self.sock.listen(MAX_CONNECTIONS)
        logger.info(f'Запущен сервер, порт: {self.port}, адрес: {self.addr}')

    def process_message(self, message):
        """Метод отправки сообщения клиенту. Принимает словарь сообщений"""
        if message[DESTINATION] in self.names and self.names[message[DESTINATION]] in self.listen_sockets:
            try:
                send_message(self.names[message[DESTINATION]], message)
                logger.info(f'Отправлено сообщение для {message[DESTINATION]} от {message[SENDER]}.')
            except OSError:
                self.remove_client(message[DESTINATION])
        elif message[DESTINATION] in self.names and self.names[message[DESTINATION]] not in self.listen_sockets:
            logger.error(f'Связь с клиентом {message[DESTINATION]} потеряна. Соединение закрыто, доставка невозможна.')
            self.remove_client(self.names[message[DESTINATION]])
        else:
            logger.error(f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере')

    @login_required        # декоратор проверяет, прошел ли текущий пользователь аутентификацию
    def process_client_message(self, message, client):
        """ Обработчик сообщений от клиентов, принимает словарь -
        сообщение от клиента, проверяет корректность,
        возвращает словарь-ответ для клиента
        """
        logger.debug(f'Разбор сообщения от клиента : {message} (core.py)')
        # Если это сообщение о присутствии, принимаем и отвечаем
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
            # Если сообщение о присутствии то вызываем функцию авторизации.
            self.autorize_user(message, client)

        # Если это сообщение, то отправляем его получателю.
        elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and TIME in message \
                and SENDER in message and MESSAGE_TEXT in message and self.names[message[SENDER]] == client:
            if message[DESTINATION] in self.names:
                # database.process_message ведет статистику сообщений
                self.database.process_message(message[SENDER], message[DESTINATION])
                # отправлем сообщение, адресат в словаре
                self.process_message(message)
                try:
                    send_message(client, {RESPONSE: 200})
                except OSError:
                    self.remove_client(client)
            else:
                response = {RESPONSE: 400, ERROR: 'Пользователь не зарегистрирован на сервере'}
                try:
                    send_message(client, response)
                except OSError:
                    pass
            return

        # Если клиент выходит
        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            self.remove_client(client)

        # Если это запрос контакт-листа
        elif ACTION in message and message[ACTION] == GET_CONTACTS and USER in message and \
                self.names[message[USER]] == client:
            response = {RESPONSE: 202, LIST_INFO: self.database.get_contacts(message[USER])}
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

        # Если это добавление контакта
        elif ACTION in message and message[ACTION] == ADD_CONTACT and ACCOUNT_NAME in message and USER in message \
                and self.names[message[USER]] == client:
            self.database.add_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_message(client, {RESPONSE: 200})
            except OSError:
                self.remove_client(client)

        # Если это удаление контакта
        elif ACTION in message and message[ACTION] == REMOVE_CONTACT and ACCOUNT_NAME in message and USER in message \
                and self.names[message[USER]] == client:
            self.database.remove_contact(message[USER], message[ACCOUNT_NAME])
            try:
                send_message(client, {RESPONSE: 200})
            except OSError:
                self.remove_client(client)

        # Если это запрос известных пользователей
        elif ACTION in message and message[ACTION] == USERS_REQUEST and ACCOUNT_NAME in message \
                and self.names[message[ACCOUNT_NAME]] == client:
            response = {RESPONSE: 202, LIST_INFO: [user[0] for user in self.database.users_list()]}
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

        # Если это запрос публичного ключа пользователя
        elif ACTION in message and message[ACTION] == PUBLIC_KEY_REQUEST and ACCOUNT_NAME in message:
            # 511 Network Authentication Required («требуется сетевая аутентификация»)
            response = {RESPONSE: 511, DATA: self.database.get_pubkey(message[ACCOUNT_NAME])}
            # может быть, что ключа ещё нет (пользователь никогда не логинился) - тогда шлём 400)
            if response[DATA]:
                try:
                    send_message(client, response)
                except OSError:
                    self.remove_client(client)
            else:
                response = {RESPONSE: 400, ERROR: 'Нет публичного ключа для данного пользователя'}
                try:
                    send_message(client, response)
                except OSError:
                    self.remove_client(client)

        # Иначе отдаём Bad request
        else:
            response = {RESPONSE: 400, ERROR: 'Запрос некорректен.'}
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

    def autorize_user(self, message, sock):
        """Метод реализующий авторизцию пользователей."""
        # Если имя пользователя уже занято то возвращаем 400
        logger.debug(f'Запущен процесс аутентификации для {message[USER][ACCOUNT_NAME]}')
        if message[USER][ACCOUNT_NAME] in self.names.keys():
            response = {RESPONSE: 400, ERROR: 'Имя пользователя уже занято.'}
            try:
                send_message(sock, response)
            except OSError:
                pass
            self.clients.remove(sock)
            sock.close()
        # Проверяем что пользователь зарегистрирован на сервере.
        elif not self.database.check_user(message[USER][ACCOUNT_NAME]):
            response = {RESPONSE: 400, ERROR: 'Пользователь не зарегистрирован на сервере.'}
            logger.debug(f'Пользователь {message[USER][ACCOUNT_NAME]} не зарегистрирован на сервере')
            try:
                send_message(sock, response)
            except OSError:
                pass
            self.clients.remove(sock)
            sock.close()
        else:
            # Иначе отвечаем 511 и проводим процедуру авторизации
            # Словарь - заготовка
            message_auth = {RESPONSE: 511, DATA: None}
            # Набор байтов в hex представлении
            random_str = binascii.hexlify(os.urandom(64))
            # В словарь байты нельзя, декодируем (json.dumps -> TypeError)
            message_auth[DATA] = random_str.decode('ascii')
            # Создаём хэш пароля и связки с рандомной строкой, сохраняем серверную версию ключа
            hash = hmac.new(self.database.get_hash(message[USER][ACCOUNT_NAME]), random_str, 'MD5')
            digest = hash.digest()
            try:
                # Обмен с клиентом
                send_message(sock, message_auth)
                ans = get_message(sock)
            except OSError as err:
                logger.debug('core.py 269 Ошибка аутентификации:', exc_info=err)
                sock.close()
                return
            client_digest = binascii.a2b_base64(ans[DATA])
            # Если ответ клиента корректный, то сохраняем его в список пользователей.
            if RESPONSE in ans and ans[RESPONSE] == 511 and hmac.compare_digest(digest, client_digest):
                self.names[message[USER][ACCOUNT_NAME]] = sock
                client_ip, client_port = sock.getpeername()
                try:
                    send_message(sock, {RESPONSE: 200})
                except OSError:
                    self.remove_client(message[USER][ACCOUNT_NAME])
                # добавляем пользователя в список активных и если у него изменился открытый ключ сохраняем новый
                self.database.user_login(message[USER][ACCOUNT_NAME], client_ip, client_port, message[USER][PUBLIC_KEY])
            else:
                response = {RESPONSE: 400, ERROR: 'Неверный пароль.'}
                try:
                    send_message(sock, response)
                except OSError:
                    pass
                self.clients.remove(sock)
                sock.close()

    def service_update_lists(self):
        """Метод реализующий отправки сервисного сообщения 205 клиентам."""
        for client in self.names:
            try:
                # 205 Reset Content - сбросить содержимое
                send_message(self.names[client], {RESPONSE: 205})
            except OSError:
                self.remove_client(self.names[client])
