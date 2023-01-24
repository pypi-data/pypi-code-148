from prettytable import PrettyTable
from .asynchat import Server




class Table():

    def __init__(self):

        self.__table__ = PrettyTable()
        self.title = []
        self.sort = ''
        self.align = 'r'


    def show(self):

        self.__table__.field_names = self.title
        self.__table__.sortby = self.sort
        self.__table__.align = self.align


    def add(self, options):

        self.__table__.add_row(options)


    def table(self):

        return self.__table__

