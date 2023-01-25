from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
import os
import sys
# sys.path.append('../')
from common.variables import *
import datetime
from sqlalchemy.sql import default_comparator


class ClientDatabase:
    """
    Класс - оболочка для работы с базой данных клиента.
    Использует SQLite базу данных, реализован с помощью
    SQLAlchemy ORM и используется классический подход.
    """
    class KnownUsers:
        """Класс - отображение таблицы всех известных пользователей."""
        def __init__(self, user):
            self.id = None
            self.username = user

    class MessageHistory:
        """Класс - отображение таблицы истории сообщений"""
        def __init__(self, contact, direction, message):
            self.id = None
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.datetime.now()

    class Contacts:
        """Класс - отображение списка контактов"""
        def __init__(self, contact):
            self.id = None
            self.name = contact

    # Конструктор класса:
    def __init__(self, name):
        # Создаём движок БД, поскольку разрешено несколько клиентов одновременно, каждый должен иметь свою БД
        # Поскольку клиент мультипоточный необходимо отключить проверки на подключения с разных потоков,
        # иначе sqlite3.ProgrammingError
        path = os.getcwd()
        filename = f'client_{name}.db3'
        # {'check_same_thread': False} - отключаем проверки на подключения с разных потоков
        self.database_engine = create_engine(
            f'sqlite:///{os.path.join(path, filename)}',
            echo=False,
            pool_recycle=7200,
            connect_args={'check_same_thread': False})

        # Создаём объект MetaData
        self.metadata = MetaData()

        # Создаём таблицы классическим вариантом (в server_database.py - декларативный вариант)
        # Создаём таблицу известных пользователей
        users = Table('known_users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('username', String))

        # Создаём таблицу истории сообщений
        history = Table('message_history', self.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('contact', String),
                        Column('direction', String),
                        Column('message', Text),
                        Column('date', DateTime))

        # Создаём таблицу контактов
        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True))

        # Создаём все таблицы внутри БД
        self.metadata.create_all(self.database_engine)

        # Создаём отображения, соединяем таблицы с оотображениями
        mapper(self.KnownUsers, users)
        mapper(self.MessageHistory, history)
        mapper(self.Contacts, contacts)

        # Создаём сессию
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        # Необходимо очистить таблицу контактов, т.к. при запуске они подгружаются с сервера.
        self.session.query(self.Contacts).delete()
        self.session.commit()

    def add_contact(self, contact):
        """
        Функция добавления контактов в БД
        :param contact: выбранный для добавления контакт
        """
        # если еще не в списке контактов
        if not self.session.query(self.Contacts).filter_by(name=contact).count():
            contact_row = self.Contacts(contact)
            self.session.add(contact_row)
            self.session.commit()

    def contacts_clear(self):
        """Метод очищающий таблицу со списком контактов."""
        self.session.query(self.Contacts).delete()

    def del_contact(self, contact):
        """
        Функция удаления контактов
        :param contact: выбранный для удаления контакт
        """
        self.session.query(self.Contacts).filter_by(name=contact).delete()

    def add_users(self, users_list):
        """
        Функция добавления списка известных пользователей.
        Пользователи получаются только с сервера, поэтому таблица сначала очищается.
        :param users_list: список пользователей для добавления
        :return:
        """
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            user_row = self.KnownUsers(user)
            self.session.add(user_row)
        self.session.commit()

    def save_message(self, contact, direction, message):
        """
        Функция сохраняющяя сообщения в MessageHistory
        :param contact: собеседник
        :param direction: входящее или исходящее
        :param message: само сообщение
        """
        message_row = self.MessageHistory(contact, direction, message)
        self.session.add(message_row)
        self.session.commit()

    def get_contacts(self):
        """Функция возвращающяя список известных контактов"""
        return [contact[0] for contact in self.session.query(self.Contacts.name).all()]

    def get_users(self):
        """Функция возвращающяя список известных пользователей"""
        return [user[0] for user in self.session.query(self.KnownUsers.username).all()]

    def check_user(self, user):
        """
        Функция проверяющяя наличие пользователя в известных
        :param user: искомый пользователь
        :return: True - если найден
        """
        if self.session.query(self.KnownUsers).filter_by(username=user).count():
            return True
        else:
            return False

    def check_contact(self, contact):
        """
        Функция проверяющяя наличие пользователя в контактах
        :param contact: искомый пользователь
        :return: True - если найден
        """
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        else:
            return False

    # def get_history(self, from_who=None, to_who=None):
    #     """
    #     Функция возвращающая историю переписки
    #     :param from_who: отправитель
    #     :param to_who: получатель
    #     :return: список всех сообщений от отправителя к получателю
    #     """""
    #     query = self.session.query(self.MessageHistory)
    #     if from_who:
    #         query = query.filter_by(contact=from_who)
    #     if to_who:
    #         query = query.filter_by(direction=to_who)
    #     return [(history_row.from_user, history_row.to_user, history_row.message, history_row.date)
    #             for history_row in query.all()]

    def get_history(self, contact):
        """
        Функция возвращающая историю переписки
        :param contact: клиент, чью историю нужно получить
        :return:
        """
        query = self.session.query(self.MessageHistory).filter_by(contact=contact)
        return [(history_row.contact, history_row.direction, history_row.message, history_row.date)
                for history_row in query.all()]


# отладка
if __name__ == '__main__':
    test_db = ClientDatabase('test1')
    for i in ['test3', 'test4', 'test5']:
       test_db.add_contact(i)
    test_db.add_contact('test4')
    test_db.add_users(['test1', 'test2', 'test3', 'test4', 'test5'])
    test_db.save_message('test2', 'in', f'Привет! я тестовое сообщение от {datetime.datetime.now()}!')
    test_db.save_message('test2', 'out', f'Привет! я другое тестовое сообщение от {datetime.datetime.now()}!')
    print(test_db.get_contacts())
    print(test_db.get_users())
    print(test_db.check_user('test1'))
    print(test_db.check_user('test10'))
    print(sorted(test_db.get_history('test2'), key=lambda item: item[3]))
    test_db.del_contact('test4')
    print(test_db.get_contacts())
