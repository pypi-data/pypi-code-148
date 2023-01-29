import sqlite3
import time
from aiogram import types

class Column():
    '''
    Use this class for create column in sqlite3 table.\n
    Use "_dict_" at the beginning of the name for auto eval dictionary type string.\n
    Use "_list_" at the beginning of the name for auto split list type string.\n
    Use "_time_" at the beginning of the name for auto update this attribute every post in unix time [s]\n
    \n
    For example:\n
    col_ex1 = Column(table='users', name='id', type='integer', primary_key=True, meaning=self.id)\n
    col_ex2 = Column(table='users', name='_dict_text', type='text', meaning=str({"key":meaning}))\n
    col_ex3 = Column(table='users', name='_list_text', type='text', meaning=str({"key":meaning}))\n
    col_ex4 = Column(table='users', name='_time_last_active', type='integer', meaning=int(time.time()))\n
    self._list_column=[col_ex1, col_ex2, col_ex3, col_ex4]
    '''
    def __init__(self, 
                table: str, 
                name: str, 
                type: str = 'text', 
                primary_key: bool = False, 
                meaning='none'):

        self.name=table
        self.name=name
        self.type=type
        self.primary_key=primary_key
        self.meaning=meaning

class Table():
    '''
    Use this class for create table in sqlite3 table
    '''
    def __init__(self, 
                name: str, 
                list_columns: list, 
                primary_column: int =0,
                foreign_mode: bool = False,
                foreign_key=None,
                foreign_table=None,
                foreign_table_key=None):
        self.name=name
        self.list_columns=list_columns
        self.primary_column=primary_column
        self.foreign_mode=foreign_mode
        self.foreign_key=foreign_key
        self.foreign_table=foreign_table
        if foreign_table_key==None:
            self.foreign_table_key=self.foreign_key
        else:
            self.foreign_table_key=foreign_table_key
    
    def text_frame_table(self, list_columns):
        list_text=[]
        i=0
        for x in list_columns:
            list_text.append(x.name)
            list_text.append(x.type)
            if x.primary_key==True:
                list_text.append(' PRIMARY KEY')
            i+=1
            if i!= len(list_columns):
                list_text[-1]+=', '
        text=' '.join(list_text)
        return(text)

    def create_table(self, base: str = 'database.db'):
        text=self.text_frame_table(self.list_columns)
        con = sqlite3.connect(base)
        cursorObj = con.cursor()
        if self.foreign_mode==False:
            cursorObj.execute(f"CREATE TABLE IF NOT EXISTS {self.name}({text})")
        else:
            cursorObj.execute(f"CREATE TABLE IF NOT EXISTS {self.name}({text}, FOREIGN KEY ({self.foreign_key}) REFERENCES {self.foreign_table} ({self.foreign_table_key}))")
        con.commit()
        print(log_time(), f" success create table {self.name} in base {base}")

class Table_string(Table):
    '''
    Use this class for create table in sqlite3 table
    '''
    def __init__(self, 
                table: str, 
                list_columns: list,):
        self.table=table
        self.list_columns=list_columns
    
    def text_names_of_columns(self, list_columns):
        list_text=[]
        i=0
        for x in list_columns:
            list_text.append(x.name)
            i+=1
            if i!= len(list_columns):
                list_text[-1]+=', '
        text=' '.join(list_text)
        return(text)

    def create_object(self, base: str = 'database.db'):
        list_entities=[]
        for x in self.list_columns:
            list_entities.append(x.meaning)
        text=self.text_names_of_columns(self.list_columns)
        con = sqlite3.connect(base)
        cursorObj = con.cursor()
        cursorObj.execute(f"INSERT INTO {self.table}({text}) VALUES({'?, '*(len(list_entities)-1)+'?)'}", list_entities)
        con.commit()
        print(log_time(), f" success insert object {self} in base {base}")
    
    def import_object(self, table: str, list_columns: list, base: str = 'database.db'):
        text=self.text_names_of_columns(list_columns)
        con = sqlite3.connect(base)
        cursorObj = con.cursor()
        query=f"SELECT {text} FROM {table} WHERE {self._list_columns[0].name}='{self._list_columns[0].meaning}'"
        cursorObj.execute(query)
        tuple_self=(cursorObj.fetchall())[0] #list of tuple
        i=0
        for x in list_columns:
            e=str(x.name[0:6])
            if e=='_dict_' or e=='_list_':
                meaning=eval(tuple_self[i])
            else:
                meaning=tuple_self[i]
            setattr(self, x.name, meaning)
            i+=1
        con.commit()
        print(log_time(), f" success import object {self} from base {base}")
    
    def post_object(self, table: str, list_columns: list, base: str = 'database.db'):
        list_v=[]
        for x in list_columns:
            atr=getattr(self, x.name)
            e=str(x.name[0:6])
            if e=='_dict_' or  e=='_list_':
                list_v.append(str(atr))
            elif e=='_time_':
                list_v.append(int(time.time()))
            else:
                list_v.append(atr)
        con = sqlite3.connect(base)
        cursorObj = con.cursor()
        i=1
        str_set=''
        for x in list_columns:
            if i!=len(list_columns):
                x_str=str(x.name)+'=?, '
                i+=1
            else:
                x_str=str(x.name)+'=?'
            str_set=str_set+x_str
        query=f"UPDATE {table} SET {str_set} WHERE {self._list_columns[0].name}='{self._list_columns[0].meaning}'"
        cursorObj.execute(query, list_v)
        con.commit()
        print(log_time(), f" success post object {self} to base {base}")
    
class Bm(Table_string):
    
    def __init__(self, obj):
        self.find_id_in_obj(obj)
        self.comb_base()

    def find_id_in_obj(self, obj):
        if isinstance(obj, types.CallbackQuery): self.id=obj.message.chat.id
        elif isinstance(obj, types.Message): self.id=obj.chat.id
        elif isinstance(obj, int): self.id=obj
        else: self.id=int(obj)

    def comb_base(self):
        con = sqlite3.connect(self._base)
        cursorObj = con.cursor()
        sql_select_table = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self._table}'"
        cursorObj.execute(sql_select_table)
        answer=len(cursorObj.fetchall()) #list of tuple
        con.commit()
        if answer==0:
            self.bm(type='create_table')
            self.bm(type='create_object')
        else:
            sql_select_key = f"SELECT {self._list_columns[0].name} from {self._table} WHERE {self._list_columns[0].name}='{self._list_columns[0].meaning}'"
            cursorObj.execute(sql_select_key)
            answer=len(cursorObj.fetchall()) #list of tuple
            con.commit()
            if answer==0:
                self.bm(type='create_object')
            else:
                self.bm(type='import_object')

    def post(self):
        self.bm(type='post_object')

    def bm(self, type):
        if type=='create_table':
            if self._foreign_mode==False:
                self._foreign_key=None
                self._foreign_table=None
                self._foreign_table_key=None
            else:
                try:
                    atr=getattr(self, '_foreign_table_key')
                except AttributeError:
                    setattr(self, '_foreign_table_key', self._foreign_key)
            table_route=Table(
                            name=self._table, 
                            list_columns=self._list_columns, 
                            foreign_mode=self._foreign_mode,
                            foreign_key=self._foreign_key,
                            foreign_table=self._foreign_table,
                            foreign_table_key=self._foreign_table_key)
            table_route.create_table(base=self._base)
        elif type=='create_object':
            str_route=Table_string(table=self._table, list_columns=self._list_columns)
            str_route.create_object(base=self._base)
            self.import_object(base=self._base, table=self._table, list_columns=self._list_columns)
        elif type=='import_object':
            self.import_object(base=self._base, table=self._table, list_columns=self._list_columns)
        elif type=='post_object':
            self.post_object(base=self._base, table=self._table, list_columns=self._list_columns)

#____________________________________________Function____________________________________________
def log_time():
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime('%d/%m/%Y, %H:%M:%S', named_tuple)
    return(time_string)