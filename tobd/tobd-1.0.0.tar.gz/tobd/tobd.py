def info():
    n = int(input('Номер задачи '))
    if n == 2:
        ds = input('Dataset: y or n ')
        if ds == 'y':
            print(
                '''
address-book-q.xml:      addr_n() 3шт.
AnnaKarenina_.txt:       ann_n()  3шт.
Chinook_Sqlite:          sql_n()  3шт.
СебестоимостьА_в1.xlsx:  seb_n()  3шт.
sp_data2.csv:            sp()     1шт.
sp500hst.txt:            sp5_n()  4шт.
titanic.csv:             tit()    1шт.
                ''')
        else:
            print('''
n2_n() 8шт.
            ''')
    else:
        ds = input('Dataset: y or n ')
        if ds == 'y':
            print('''
all_k.zip:    alk_n() 4шт.
movies.zip:   mov_n() 3шт.
random.hdf5:  rnd_n() 4шт
            ''')
        else:
            print('''
n3_n() 2шт.
            ''')

def sql_1():
    print(
    '''
С помощью кода на Python с использованием sqlite3 и SQL решить задачу. Реализовать функции на Python:
Которая возвращает всех имеющихся артистов.
Которая по имени артиста возвращает все его альбомы с количеством треков в них.

import sqlite3
def find_artists():
    con = sqlite3.connect('Chinook_Sqlite.sqlite')
    cur = con.cursor()    
    cur.execute((тройные кавычки)
    SELECT DISTINCT Name
    FROM Artist(тройные кавычик))    
    artists=cur.fetchall()    
    ls=[]    
    for artist in artists:
        ls.append(artist[0])
    return ls
    cur.close()
    con.close()
find_artists()
def count_and_album(name):
    con = sqlite3.connect('Chinook_Sqlite.sqlite')
    cur = con.cursor()    
    cur.execute((тройные кавычки)
    select al.title, count(t.name)
    from Track t join Album al on t.albumid=al.AlbumId join Artist a on al.ArtistId=a.ArtistId


    GROUP by al.title
    HAVING a.name=?(тройные кавычки),(name,))    
    info=cur.fetchall()    
    for i in info:
        print('Альбом:',i[0],'Количество треков:',i[1])
    cur.close()
    con.close()
count_and_album('AC/DC')
    ''')

def sql_2():
    print('''
С помощью кода на Python с использованием sqlite3 и SQL решить задачу. Реализовать функции на Python:
Которая возвращает всех имеющиеся плейлисты.
Которая по имени плейлиста возвращает количество треков в нем и их суммарную продолжительность.

import sqlite3
def find_playlists():
    con = sqlite3.connect('Chinook_Sqlite.sqlite')
    cur = con.cursor()    
    cur.execute((тройные кавычки)
    SELECT DISTINCT Name
    FROM Playlist(тройные кавычки))    
    playlists=cur.fetchall()    
    ls=[]    
    for playlist in playlists:
        ls.append(playlist[0])
    return ls
    cur.close()
    con.close()
find_playlists()
def count_and_time(name):
    con = sqlite3.connect('Chinook_Sqlite.sqlite')
    cur = con.cursor()    
    cur.execute((тройные кавычки)
    select COUNT(pt.trackid), SUM(t.milliseconds) 
    from PlaylistTrack pt left JOIN Playlist p on pt.playlistid = p.playlistid
    LEFT join Track t on pt.trackid = t.trackid
    GROUP by p.name
    HAVING  p.Name = ?
    (тройные кавычки),(name,)
    )
    info=cur.fetchall()    
    print('Количество треков =',info[0][0])
    print('Суммарная продолжительность =',info[0][1])
    cur.close()
    con.close()
count_and_time('Music')
    ''')


def sql_3():
    print('''
С помощью кода на Python с использованием sqlite3 и SQL решить задачу. Реализовать функции на Python:
Которая по имени исполнителя возвращает все его альбомы.
Которая по имени исполнителя и имени альбома возвращает количество треков в альбоме и их суммарную продолжительность

import sqlite3
def find_album(name):
    con = sqlite3.connect('Chinook_Sqlite.sqlite')
    cur = con.cursor()    
    cur.execute((тройные кавычки)
    SELECT al.Title
    FROM Artist a left join Album al on a.ArtistId=al.ArtistId
    where a.name=?(тройные кавычки),(name,))    
    albums=cur.fetchall()    
    ls=[]    
    for album in albums:
        ls.append(album[0])
    return ls
    cur.close()
    con.close()
find_album('AC/DC')
def count_and_time(name_artist,name_album):
    con = sqlite3.connect('Chinook_Sqlite.sqlite')
    cur = con.cursor()    
    cur.execute((тройные кавычки)
    select count(t.name), sum(t.milliseconds)
    from Track t join Album al on t.albumid=al.AlbumId join Artist a on al.ArtistId=a.ArtistId
    where a.name=? and al.title=?(тройные кавычки),(name_artist,name_album,)
    )
    info=cur.fetchall()    
    print('Количество треков =',info[0][0])
    print('Суммарная продолжительность =',info[0][1])
    cur.close()
    con.close()
count_and_time('AC/DC','For Those About To Rock We Salute You')
    ''')


def ann_1():
    print('''
Найти в книге как минимум 3 пары близких, но не совпадающих коротких предложений. Редакционное расстояние между ними не должно превышать 3, длина предложений не должна быть более 40 символов. Рекомендация: для повышения скорости решения задачи учитывайте длину сравниваемых предложений при поиске близких предложений.

#Расстояние Левенштейна (редакционное расстояние, дистанция редактирования)
from nltk.metrics import *
import re

def is_roman_number(num):
    pattern = re.compile(r"""   
                                ^M{0,3}
                                (CM|CD|D?C{0,3})?
                                (XC|XL|L?X{0,3})?
                                (IX|IV|V?I{0,3})?$
            """, re.VERBOSE)
    return bool(re.match(pattern, num))

with open('AnnaKarenina_.txt') as f:
    text = []
    for i in f:
        i = re.sub('(обратный слэш)n','',i)
        if len(i)<=40 and len(i)>0:
            if not is_roman_number(i):
                text.append(i)
text
col = 0
for i in range(len(text)):
    for j in text[i+1:]:
        m = edit_distance(text[i],
                          j, substitution_cost=2, transpositions=True)
        if text[i]!=j and m<=3:
            col+=1
            print(text[i],j,m)
            if col==3:
                break
    if col==3:
        break

    ''')

def ann_2():
    print('''
Для имени собственного одного из главных персонажей книги найти частоту различных форм склонения имени по падежам. Вывести результат (словоформы имени и их частоты) на экран. При решении задачи использовать лемматизацию Рекомендация (не обязательная): для ускорения работы решения можно учитывать длину слов и использовать мемоизацию.

import nltk
import re
import os
import pymorphy2
import dask.bag as db
morph = pymorphy2.MorphAnalyzer()

text = db.read_text(‘...‘,encoding='Windows-1251')
text.take(20)

#inflect склоняет слово
name = 'Анна'
count_form_name_dict = {morph.parse(name)[0].inflect({padez})[0]:0
                        for padez in ('nomn', 'gent', 'datv', 'accs', 'ablt', 'loct')}

def count_name_forms_string(string,slovar):
    words = nltk.word_tokenize(string)
    for word in words:
        if word.lower() in slovar.keys():
            slovar[word.lower()]+=1
    return slovar

result = text.map(lambda x: count_name_forms_string(string=x, slovar=count_form_name_dict)).compute()

result[-1]
    ''')

def ann_3():
    print('''
Определить 200 самых частотных слов в тексте (вывести на экран эти слова и их частоты). Среди найденных слов определить слова, не входящие в стандартный список стоп-слов. Вывести эти слова на экран.

from nltk.metrics import *
import re
import nltk
from nltk import sent_tokenize
from nltk.corpus import stopwords

with open('/Users/marinavorobeva/Desktop/экзамен тобд/2 задание/AnnaKarenina_.txt',encoding='cp1251') as f:
    lines = f.readlines()
    lines = [line.rstrip('(обратный слэш)n') for line in lines]
    text = ' '.join(lines).replace('(обратный слэш)xa0', ' ').lower()
sents = nltk.sent_tokenize(text)

nltk.download('punkt')
nltk.download("stopwords")
from nltk.corpus import stopwords

spisok=[]
pattern = re.compile(re.compile(r"[^a-zA-ZA-ЯЁа-яё ]+"))#удалим цифры из описаний

for sent in sents:
    sent_new=re.sub(pattern,' ',sent)
    words = nltk.word_tokenize(str(sent_new))
    spisok.append(words)
spisok

spisok_to_freq = [] 
for sp in spisok:   
    for world in sp:
      spisok_to_freq.append(world)
spisok_to_freq

from nltk.probability import FreqDist
fdist_before_delete_stop = FreqDist(spisok_to_freq)

#топ-200 самых часто употребляемых слов до удаления стоп-слов
top=fdist_before_delete_stop.most_common(200)
top

rus_stop_words = set(stopwords.words('russian'))

slova_not_stop=[]
for i in top:
    if i[0] not in rus_stop_words:
        slova_not_stop.append(i[0])
slova_not_stop
    ''')


def tit():
    print('''
Заменить все пропущенные числовые значения возраста на значения, равные среднему значению для представителей этого класса пассажиров данного пола (не выполнять операцию, если неизвестен и возраст, и класс билета пассажира или его пол). Решить задачу средствами numpy и/или pandas. Не использовать циклы и конструкции стандартного Python там, где можно использовать возможности данных библиотек.

import pandas as pd

file = '/Users/aleksandrkormisenkov/Desktop/exam_datasets/task_2/titanic.csv'
titanic = pd.read_csv(file)
titanic.head()

titanic.info()

mean_age = pd.pivot_table(titanic,values=  'Age',index = 'Pclass', columns='Sex',aggfunc='mean')
mean_age

mean_age.loc[2,'male']


file = '/Users/aleksandrkormisenkov/Desktop/exam_datasets/task_2/titanic.csv'  #вот тут решение начинается
titanic_na = pd.read_csv(file)

def fill_na_age(age,pclass,sex,ages_data):
    if (pd.isnull(age) == True and pd.isnull(sex)== True) or (pd.isnull(age) == True and pd.isnull(pclass) == True):
        return np.nan
    else:
        return ages_data.loc[pclass,sex]


titanic_na['Age'] = titanic_na.apply(lambda x: fill_na_age(x['Age'],x['Pclass'],x['Sex'],mean_age),axis = 1)


titanic[titanic['Age'].isna()]

titanic_na[titanic['Age'].isna()]

    ''')

def addr_1():
    print('''
По данным из файла address-book-q.xml сформировать два списка кортежей. В первом будет информация только о мужчинах и кортеж будет состоять из имени, названия компании и рабочего телефона, а во втором списке будет только информация о женщинах и кортеж будет состоять из имени и личного телефона. Сохранить списки в два разных файла формата pickle и загрузить их оттуда.

from bs4 import BeautifulSoup
import pickle
with open('...','r',encoding='utf8') as fp:
  data=BeautifulSoup(fp,'xml')


list_m=[]
list_f=[]
for address in data.find_all('address'):
    if address.find('gender').text=='m':
        tup=(address.find('name').text, address.find('company').text, address.find('phone', type='work').text)
        list_m.append(tup)
    else:
        tup=(address.find('name').text, address.find('phone', type='personal').text)
        list_f.append(tup)


#  сохраняем в pickle
with open('list_m.pickle', 'wb') as file:
  pickle.dump(list_m, file)


# читаем из pickle
with open('list_m.pickle', 'rb') as file:
  p = pickle.load(file)
    ''')

def addr_2():
    print('''
По данным из файла address-book-q.xml сформировать словарь, в котором по должности можно получить список людей с данной должностью и для каждого человека по соответствующему ключу можно получить имя, компанию и список всех доступных телефонов. Сохранить данную структуру данных в файл формата json и прочитать ее, показав идентичность структуры данных после сохранения/загрузки.

from bs4 import BeautifulSoup
import pickle
with open('...','r',encoding='utf8') as fp:
  data=BeautifulSoup(fp,'xml')


slovar={}
for address in data.find_all('address'):
    position = address.find('position').text
    name = address.find('name').text
    company = address.find('company').text
    phones = address.find('phones').text.split('(обратный слэш)n')[1:-1]
    slovar[position] = slovar.get('position',[])+ [address['id']]
    slovar[address['id']] = {'name':name,'company':company,'phones':phones}


with open("slovar.json", "w") as write_file:
    json.dump(slovar, write_file)


with open("slovar.json", "r") as read_file:
    data = json.load(read_file)


data == slovar
    ''')

def addr_3():
    print('''
По данным из addres-book-q.xml сформировать 2 кортежа, у мужчин добавить имя компанию телефон рабочий, женщинам имя и телефон персональный Сохранить данную структуру данных в файл формата npy и считать его

from bs4 import BeautifulSoup
import numpy as np
with open(r'addres-book-q.xml') as f:
    abq = BeautifulSoup(f, 'xml')
mens = []
women = []
for p in abq.find_all('address'):
    if p.find('gender').next == 'm':
        mens.append((p.find('name').next, p.find('company').next, p.find('phone', type='work').next))
    else:
        women.append((p.find('name').next, p.find('phone', type="personal").next))
np.save('address-book-q.npy', mens, women)
np.load('address-book-q.npy')
with open('address-book-q.npy', 'wb') as f:
    np.save(f, mens)
    np.save(f, women)
with open('address-book-q.npy', 'rb') as f:
    mens = np.load(f)
    women = np.load(f)
    ''')

def sp5_1():
    print('''
Создать таблицу, в которой индексом являются даты торгов, столбцами - наименования тикеров, а в ячейках хранятся объемы торгов. Заполнить эту таблицу данными из sp500hst.txt (в случае отсутствия информации для определенных сочетаний тикер-дата, сохранить в ячейке пустое значение). Сохранить результат в новый CSV файл. Решить задачу средствами numpy и/или pandas. Не использовать циклы и конструкции стандартного Python там, где можно использовать возможности данных библиотек.

import numpy as np
import pandas as pd
sp500hst = (pd.read_csv('sp500hst.txt',header = None,parse_dates=[0],
                     names = ['date','ticker','open','high','low','close','volume']))
sp500hst

#создаём сводную таблицу
result_table = pd.pivot_table(sp500hst,values = 'volume',index='date',columns='ticker',aggfunc='sum',fill_value=0)
result_table.head()
result_table.to_csv('result.csv')
    ''')

def sp5_2():
    print('''
Рассчитать среднее значение за 2010 год для показателей каждого из столбцов 3-6 для одинаковых значений тикеров из столбца 2 и сохранить рассчитанную таблицу со столбцами Тикер, open , high, low, closing (где OHLC содержат среднее значение для данного тикера за 2010 год) в новом CSV файле. Решить задачу средствами numpy и/или pandas. Не использовать циклы и конструкции стандартного Python там, где можно использовать возможности данных библиотек.

import numpy as np
import pandas as pd
sp500hst = (pd.read_csv('sp500hst.txt',header = None,parse_dates=[0],
                     names = ['date','ticker','open','high','low','close','volume']))
sp500hst
sp500_2010_mean = sp500hst[sp500hst['date'].dt.year == 2010].groupby('ticker')[['open','high','low','close','volume']].mean()
sp500_2010_mean.to_csv('task_sp500.csv',index = False,sep = ',')
sp500_2010_mean
    ''')

def sp5_3():
    print('''
Создать DataFrame, в котором присутствует столбец, отражающий разницу в объемах торгов по NVDA и AAPL в одинаковые дни, и который содержит исходные данные об объеме торгов этими акциями. Создать модификацию этого DataFrame, в которой сохранены только строки для дней, когда и акции NVDA, и акции AAPL дорожали (цена закрытия была выше цены открытия). Решить задачу средствами numpy и/или pandas. Не использовать циклы и конструкции стандартного Python там, где можно использовать возможности данных библиотек.

file = 'sp500hst.txt'
sp500 = (pd.read_csv(file,header = None,parse_dates=[0],
                     names = ['date','ticker','open','high','low','close','volume']))
sp500.head()

df1 = (sp500[sp500['ticker'] == 'NVDA'].merge(sp500[sp500['ticker'] == 'AAPL'],how = 'inner',
                                             left_on = 'date',right_on = 'date',
                                             suffixes=('_NVDA', '_AAPL')))
df1['volume_diff'] = df1['volume_NVDA'] - df1['volume_AAPL']
df1['day_stonks_NVDA'] = df1['close_NVDA'] - df1['open_NVDA']
df1['day_stonks_AAPL'] = df1['close_AAPL'] - df1['close_NVDA']
df1_new = df1[(df1['day_stonks_NVDA'] > 0)&(df1['day_stonks_AAPL'] > 0)][['date','volume_NVDA','volume_AAPL','volume_diff']]

df1_new.head()
    ''')

def sp5_4():
    print('''
Для тикера NVDA посчитать, сколько дней прошло между максимальным и минимальным значением цены акции открытий рынка, и суммарный объем торгов за этот период (включая дни максимума и минимума). Решить задачу средствами nгmру/pandas. Не использовать циклы и конструкции стандартного Python там, где можно использовать возможности данных библиотек.

import numpy as np
import pandas as pd
file = 'sp500hst.txt'
sp500 = (pd.read_csv(file,header = None,parse_dates=[0],
                     names = ['date','ticker','open','high','low','close','volume']))
sp500_NVDA = sp500[sp500['ticker'] == 'NVDA']
sp500_NVDA.head()

sp500_NVDA['open'].plot(grid = True)

max_open_date = sp500_NVDA[sp500_NVDA['open'] == sp500_NVDA['open'].max()]['date']
min_open_date = sp500_NVDA[sp500_NVDA['open'] == sp500_NVDA['open'].min()]['date']

day_diff = np.abs((max_open_date.to_numpy()[0] - min_open_date.to_numpy()[0])/np.timedelta64(1,'D'))
print('кол-во дней прошедших между макс и мин значением цены открытия',int(day_diff))
sum_volume = (sp500_NVDA[(sp500_NVDA['date'] >= max_open_date.to_numpy()[0]) & 
            (sp500_NVDA['date'] <= min_open_date.to_numpy()[0])]['volume'].sum())
print('суммарный обхем торгов за этот период',int(sum_volume))
    ''')

def sp():
    print('''
Сохранить в sp500hst names.txt CSV с добавленным столбцом с расшифровкой названия тикера. Использовать для этого данные из файла sp_data2.csv. В случае нехватки данных об именах тикеров корректно обработать такую ситуацию (в новом столбце для этих случаев должно быть пустое значение). Решить задачу средствами numpy и/или pandas. Не использовать циклы и конструкции стандартного Python там, где можно использовать возможности данных библиотек.

import pandas as pd

sp_data2 = pd.read_csv('/Users/marinavorobeva/Desktop/экзамен тобд/2 задание/sp_data2.csv', sep = ';', names = ['Ticker','Name','Percent'])
sp_data2.head()

df_sp500 = pd.read_table('/Users/marinavorobeva/Desktop/экзамен тобд/2 задание/sp500hst.txt',sep = ',',header = None,names = ['Date','Ticker','Open','High','Low','Close','Volume'])
df_sp500.head()

sp_data2_new=sp_data2.iloc[:,:2]
sp_data2_new

df_sp500_ticker = df_sp500.merge(sp_data2.iloc[:,:2], on = 'Ticker', how = 'left')
df_sp500_ticker['Name'] = df_sp500_ticker['Name'].fillna('Отсутствует')

df_sp500_ticker

    ''')

def seb_1():
    print('''
С помощью кода на Python с использованием xlwings решить задачу. Вынести цены ресурсов (из всех таблиц на листе Рецептура) в новую таблицу на новом листе "Цена ресурсов". Заменить фиксированные цены ресурсов на листе "Рецептура" на ссылки на лист "Цена ресурсов".

import xlwings as xw
import numpy as np 
f = xw.Book('себестоимостьА_в1.xlsx')
sht = f.sheets['Рецептура']
f.sheets.add(name='Цена ресурсов', after='Рецептура') #name, before, after
sht2 = f.sheets['Цена ресурсов']
price1 = sht.range('G14').options(expand='right').value
price2 = sht.range('G31').options(expand='right').value
price3 = sht.range('G52').options(expand='right').value
price4 = sht.range('G73').options(expand='right').value
#price1, price2, price3, price4
sht2.range('A1').value = 'Цена ресурсов 1'
sht2.range('A2').value = 'Цена ресурсов 2'
sht2.range('A3').value = 'Цена ресурсов 3'
sht2.range('A4').value = 'Цена ресурсов 4'
sht2.range('B1').options(transpose=False).value = price1
sht2.range('B2').options(transpose=False).value = price2
sht2.range('B3').options(transpose=False).value = price3
sht2.range('B4').options(transpose=False).value = price4
sht.range('G14').formula = "='Цена ресурсов'!B1"
sht.range('G31').formula = "='Цена ресурсов'!B2"
sht.range('G52').formula = "='Цена ресурсов'!B3"
sht.range('G73').formula = "='Цена ресурсов'!B4"
# импортируем константу:
from xlwings.constants import AutoFillType
sht.range('G14').api.AutoFill(sht.range("G14:R14").api, AutoFillType.xlFillDefault)
sht.range('G31').api.AutoFill(sht.range("G31:Q31").api, AutoFillType.xlFillDefault)
sht.range('G52').api.AutoFill(sht.range("G52:AA52").api, AutoFillType.xlFillDefault)
sht.range('G73').api.AutoFill(sht.range("G73:AB73").api, AutoFillType.xlFillDefault)
    ''')

def seb_2():
    print('''
С помощью кода на Python с использованием xlwings решить задачу. В верхней таблице для строки "Средний физический расход ресурсов" пересчитать значения и сделать их равными среднему значению по рецептурам, содержащимся в данной таблице.

import xlwings as xw
import numpy as np 
f = xw.Book('себестоимостьА_в1.xlsx')
sht = f.sheets['Рецептура']
sht.range('G15').formula = "=AVERAGE(G7:G13)"
# импортируем константу:
from xlwings.constants import AutoFillType
sht.range('G15').api.AutoFill(sht.range("G15:O15").api, AutoFillType.xlFillDefault)
    ''')

def seb_3():
    print('''
С помощью кода на Python с использованием xlwings решить задачу. Вынести "Наименование продукции" (из всех таблиц на листе Рецептура) и соответствующие им значения "Доля" в новую таблицу на новом листе "Наименование". Значения из столбца «Доля» выбирать, не указывая явно в каком столбце для данной таблицы на листе "Рецептура" находится "Доля" (делать это динамически, в зависимости от ширины каждой из таблиц)..

import xlwings as xw
import numpy as np
import pandas as pd
from xlwings import constants
from xlwings.constants import AutoFillType
wb = xw.Book('себестоимостьА_в1.xlsx')
recipies = wb.sheets['Рецептура']
recipies.range('B20:R33').name = 'рцп_ржаной_хлеб'
recipies.range('B37:AB54').name = 'рцп_спец_рецепт'
recipies.range('B58:AC75').name = 'рцп_слоеная_выпечка'
recipe1 = recipies.range('рцп_пшеничный_хлеб').value[3:-3] + recipies.range('рцп_ржаной_хлеб').value[3:-3] + recipies.range('рцп_спец_рецепт').value[3:-3] + recipies.range('рцп_слоеная_выпечка').value[3:-3]


bread = []
part = []
for hleb in recipe1:
    if hleb[1] != None:
        bread.append(hleb[1])
        part.append(hleb[-1])
wb.sheets.add('Наименование')
ingred = wb.sheets['Наименование']
ingred.range('A1').options(transpose=True).value = bread
ingred.range('B1').options(transpose=True).value = part
    ''')

def n2_1():
    print('''
С помощью кода на Python с использованием регулярных выражений решить задачу. Реализовать функцию, которая ищет в текста все слова, представляющие из себя последовательности латинских букв в нижнем регистре, разделенных одним символом подчеркивания (“_”) и имеющие после подчеркивания один или более символ “@”.

import re
pattern = re.compile(r'[a-z]{1,}[_]{1}[@]{1,}[a-z]{0}')
primer='akaj jnk_@km fjfl_@ krk@'
def string(text,pat):
    return re.findall(pat,text)
string(primer,pattern)
pattern = re.compile(r'[a-z]+_@+')#типо еще вариант
s = 'asdfg_asfg_@'
re.findall(pattern,s)
s = 'asdfg_asfg_@_adgg_@@@'
re.findall(pattern,s)
s = 'asdfg_asfg__adgg_@@@'
re.findall(pattern,s)
s = 'asdfg_asfg__adg1_@af@@'
re.findall(pattern,s)
s = 'a1a_@_@'
re.findall(pattern,s)
s = 'a1a_@a__@@'
re.findall(pattern,s)
    ''')


def n2_2():
    print('''
Дан массив А. Построить массив В той же размерности, состоящий из элементов, являющихся суммой минимального элемента массива А по соответствующей строке
и минимального элемента А по соответствующему столбцу. Решить задачу средствами numpy/pandas.

import numpy as np
A = np.array([
    [8, 4, 15, 6, 9],
    [3, 16, 13, 8, 10],
    [0, 9, 18, 17, 5],
    [16, 2, 6, 0, 10],
    [18, 13, 9, 17, 8]])
B=np.resize(A.min(axis=1), (5,5)).transpose()+np.resize(A.min(axis=0), (5,5))
    ''')

def n2_3():
    print('''
Задать два двумерных массива ar1 и ar2 размерности (5,15), состоящих из случайных целых чисел в интервале от -5 до 5. Если значение в ar2 имеет тот же знак, что и соответствующие значение из ar1, то прибавить это значение к соответствующему значению ar1. Решить задачу средствами numpy/pandas. 

import numpy as np
ar1 = np.random.randint(-5,5,size = (5,15)) 
ar2 = np.random.randint(-5,5,size = (5,15))
ar2_positive = ((ar1>0)&(ar2>0)) * ar2
ar2_negative = ((ar1<0)&(ar2<0)) * ar2
ar1 + ar2_positive + ar2_negative
((ar1>0)&(ar2>0)) * ar2 #еще хрень какая-то
    ''')

def n2_4():
    print('''
Создать массив ‘arr’ размерности (10,4) из случайных чисел от 0 до 50. Найти самое частое число в массиве (вывести на экран его значение и информацию о расположении всех этих значений в исходном  массиве). Вернуть массив (3,4), содержащий 3 строки из исходного массива, в которых находится наибольшее количество самых частотных значений.

import numpy as np
arr = np.random.randint(0,51,(10,4))
#самая большая частота 
max_count = np.max(np.unique(arr, return_counts=True)[1])
#самые частотные числа
max_count_numbers = np.unique(arr, return_counts=True)[0][np.where(np.unique(arr, return_counts=True)[1] == max_count)]
#информация о расположении
rows_most_count_number, cols_most_count_number = np.where(arr == max_count_numbers[0])
#массив (3, 4), содержащий 3 строки из исходного массива, содержащие наибольшее количество самых частотных значений
arr[np.flip(np.argsort(np.sum(np.isin(arr, max_count_numbers),axis = 1)))[:3]]
    ''')

def n2_5():
    print('''
Приблизительно (с погрешностью порядка 1%) рассчитать на какой части прямоугольника  0<x<5,0<y<5  до значения функции  z(x,y)=xysin(x)cos(y)  больше 0.25.
Решить задачу средствами numpy и/или pandas.

n = 100
x = np.linspace(0, 5, n)
y = np.linspace(0, 5, n)
xx = np.vstack([x] * n)
yy = np.hstack([y.reshape(-1, 1)] * n)
z = xx * yy * np.sin(x).reshape(-1, 1) * np.cos(y)
indices = np.array((z > 0.25).nonzero()).T.astype(float)
indices[:, 0] = x[indices[:, 0].astype(int)]
indices[:, 1] = y[indices[:, 1].astype(int)]
indices
    ''')

def n2_6():
    print('''
Создать двумерный массив 30 на 4, содержащий случайные целые числа от 0 до 100. Интерпретируя массив как 30 векторов из 4х компонент, вернуть массив 5 на 4, состоящий из векторов с наибольшей длиной (евклидовой нормой).Решить задачу средствами numpy и/или pandas.

import numpy as np
arr = np.random.randint(low=0,high=101,size=(30,4))
#рассчитываем евклидову норму по формуле по каждой строке массива
norma=np.sqrt((arr**2).sum(axis=1))
#np.argsort сортирует элементы строки массива по возрастанию евклидовой нормы
#np.flip выводит в обратном порядке
arr_new = arr[np.flip(np.argsort(norma))[:5]]
    ''')

def n2_7():
    print('''
Построить "one-hot encoding" для одномерного массива numpy из целых неотрицательных чисел (длина массива и максимальное значение в массиве заранее неизвестно). Протестировать свое решение на случайно сгенерированном одномерном массиве, соответствующем условию.

ar2 = np.random.randint(4,10,size = 5)
ohe = np.zeros(shape = (ar2.shape[0],np.max(ar2)+1))
ohe[np.arange(ar2.shape[0]),ar2] = 1
ohe[:,np.unique(ar2)]
    ''')

def n2_8():
    print('''
Задан двухмерный массив ar1 размерности (25, 4) состоящий из случайных целых чисел в пределах от 0 до 15. Определить, в каких столбцах не менее 5 раз встречается значение, максимальное по своей строке (вывести индексы этих столбцов на экран с соответствующим комментарием). Для столбца, в котором таких значений наибольшее количество, заменить максимумы по строке на значения -1.

ar1 = np.random.randint(0,16,size = (25,4))
answ1 = np.where(np.sum((ar1 - np.max(ar1,axis=1).reshape(ar1.shape[0],1)) == 0,axis = 0) >= 5)
col_with_most_row_max = np.argmax(np.sum((ar1 - np.max(ar1,axis=1).reshape(ar1.shape[0],1)) == 0,axis = 0))
ar1[np.where(np.argmax(ar1,axis = 1) == col_with_most_row_max),col_with_most_row_max] = -1
ar1
    ''')


def n3_1():
    print('''
Необходимо найти все пары целых чисел от 1 до 3000, для которых sin от произведения чисел из пары будет иметь значение больше 0.99999999. Ответ представляет собой список пар (целое число1, целое число2, значение синуса для их произведения), для которых значение синуса удолетворяет условию.
Решение этой задачи распараллелить, используя multiprocessing Pool. Сравнить продолжительность последовательного и параллельного решения задачи.


import math
from multiprocessing import Pool
import multiprocessing as mp

digit = 0.99999999
l_r = range(1,3001)

%%time
generator = ((i, j ,math.sin(i*j)) for i in l_r for j in l_r)
result = list(filter(lambda x: math.sin(x[0] * x[1]) > digit, generator))
print(result)

%%file function.py
import math 
def function(x):
    digit = 0.99999999
    if math.sin(x[0] * x[1]) > digit:
        return x

from function import function
%%time

with Pool(processes = mp.cpu_count()) as pool:
    result = pool.map(function, ((i, j, math.sin(i * j)) for i in l_r for j in l_r))

list(filter(lambda x: x is not None, result))   #вывод На процессах дольше, тк мы тратим время, чтобы запустить планировщик mp для pool

ДРУГОЕ РЕШЕНИЕ 

сначала последовательное 
import numpy as np

def dotnums(a, b):
    return np.sin(a*b) > 0.99999999
def sindot(a, b):
    if dotnums(a, b):
        return (a, b, np.sin(a*b))

%%time
n = 3000
for i in range(1,n+1):
    for j in range(1,n+1):
        sindot(i,j)

потом паралельное 
%%file defs2.py
import numpy as np

def dotnums(a, b):
    return np.sin(a*b) > 0.99999999
def sindot(a, b):
    if dotnums(a, b):
        return (a, b, np.sin(a*b))

%%time
import multiprocessing as mp
import defs2

a = [(i, j) for i in range(1,3001) for j in range(1, 3001)]
with mp.Pool(5) as pool:
    tt = list(pool.starmap(defs2.sindot, a))
    ''')

def n3_2():
    print('''
Необходимо найти все целые числа от 1 до 400 000, для которых sin от этого числа будет иметь не менее 9 одинаковых цифр (например, sin(139198)=0.30763333543133703; sin(139198)=0.30763333543133703 т.е. имеет 9 троек). Ответ представляет собой список пар (целое число, значение синуса для него), для которых значение синуса удовлетворяет условию. Решение этой задачи распараллелить, используя multiprocessing Pool. Сравнить продолжительность последовательного и параллельного решения задачи.


import math
from multiprocessing import Pool
import multiprocessing as mp
from collections import Counter

l_r = range(1, 400_000)
def func(x):
    sin_x = math.sin(x)
    if max(Counter(str(sin_x)).values()) >= 9:
        return (x, math.sin(x))

%%time
with Pool(processes=mp.cpu_count()) as pool:
    result = pool.map(func, l_r)
res = list(filter(None, result))
res

%%time
res2 = [func(x) for x in l_r]
res2 = list(filter(None, res2))
res2

# отдельно замерка времени без учета фильтрации
%%time
with Pool(processes=mp.cpu_count()) as pool:
    result = pool.map(func, l_r)

%%time
res2 = [func(x) for x in l_r]
# На процессах дольше, тк мы тратим время, чтобы запустить планировщик mp для pool
# На маленьких данных нет смысла распараллеливать

ДРУГОЙ ВАРИАНТ РЕШЕНИЯ 


сначала последовательное 
import numpy as np
def parnums(a):
    nums = [str(i) for i in range(0,10)]
    ar1 = []
    for i in nums:
        ar1.append(str(np.sin(a)).count(i))
    s = int(max(ar1)) > 8
    return s

def sindist(a):
    if parnums(a):
        return (a, np.sin(a))

%%time
n = 400000
for i in range(1,n+1):
    sindist(i)

потом парелельное 

%%file defs1.py
import numpy as np

def parnums(a):
    nums = [str(i) for i in range(0,10)]
    ar1 = []
    for i in nums:
        ar1.append(str(np.sin(a)).count(i))
    s = int(max(ar1)) > 8
    return s
def sindist(a):
    if parnums(a):
        return (a, np.sin(a))

%%time
import multiprocessing as mp
import defs1
a = [i for i in range(1,400001)]
with mp.Pool() as pool:
    tt = list(pool.map(defs1.sindist, a))

    ''')

def alk_1():
    print('''
Подсчитать, сколько раз во всех текстовых файлах, лежащих в all_k.zip, встречаются реплики прямой речи, оформленные в виде диалога (В этом случае каждая реплика начинается с новой строки, перед репликами ставится тире (перед тире возможны различные пробельные символы)). Выполнить задание с использованием Dask, распараллелив процесс обработки данных.

import dask.bag as db
import re
import os
import nltk
path = 'all_k' 
files = [path+'/'+file for file in os.listdir(path)]
texts = db.read_text(files, encoding='Windows-1251')

texts.map(lambda x: len(re.findall(re.compile(r'^\s*[—–-]'),x))).sum().compute()
    ''')

def alk_2():
    print('''
Подсчитать, сколько раз встречается каждая из заглавный русских букв в текстовых файлах, лежащих в all_k.zip

import dask.bag as db
import re
import os
path = 'all_k' 
files = [path+'/'+file for file in os.listdir(path)]

texts = db.read_text(files, encoding='Windows-1251')

texts.map(lambda x: re.findall(r'[А-ЯЁ]', x)).flatten().frequencies().compute()
    ''')

def alk_3():
    print('''
Подсчитать сколько раз в текстовых файлах, лежащих в all_k.zip, встречаются предложения 3 видов : вопросительные(окончание ?), побудительные(окончание ! и не имеют ?) , повествовательные ( окончание . или … , учеть что нет точек которые для сокращения)

import dask.bag as db
import re

bag = db.read_text(urlpath = 'E:/ТОБД/Экзамен/all_k/*', encoding='Windows-1251')

def counter(data, p):
    return len(re.findall(p, data))

pattern1 = re.compile(r'[\?]')

pattern2 = re.compile(r'[^\?]![^\?]')

pattern3 = re.compile(r'[^\.]{2}\.\s|[^\.]{2}\.(обратный слэш)n|[\.]{3}')

#Вопросительные
bag.map(counter, pattern1).sum().compute()

#Восклицательные
bag.map(counter, pattern2).sum().compute()

#Утвердительные 
bag.map(counter, pattern3).sum().compute()

import graphviz

bag.map(counter, pattern3).sum().visualize()
    ''')

def alk_4():
    print('''
Подсчитать сколько раз встречается, каждое из из личных местоимений в именительном падеже (список: я , ты ….) в текстовых файлах лежащих в all_k.zip

import dask.bag as db
import re
import os
import nltk
path = 'all_k' 
files = [path+'/'+file for file in os.listdir(path)]

texts = db.read_text(files, encoding='Windows-1251')


pattern = re.compile(r'(обратный слэш)b(я|ты|он|она|оно|они|мы|вы)(обратный слэш)b')
#re.findall(pattern,'яблоко я мыло мы оно')

texts.map(lambda x: re.findall(pattern, x.lower())).flatten().frequencies().compute()
    ''')


def mov_1():
    print('''
Из названий фильмов, заданных в файле movies.txt, выделить первое слово, последнее слово (если оно отличается от первого) и остальные слова (для названий, состоящих из 3х и более слов). Словом считается любой выделенный разделителями набор символов, не относящихся к знакам препинания (отдельно стоящий символ "&" считается словом).
Найти по 2 самых длинных слова, относящихся к каждой из 3х групп. Сформировать из 6 найденных слов список. Распараллелить расчёт при помощи dask.delayed.


import dask
from collections import Counter
import nltk
file = 'movies.txt'
with open(file,'r') as f:
    movies = f.readlines()
    movies = [movie.rstrip('(обратный слэш)n') for movie in movies]
movies[:5]


def read_first_word(file):
    with open(file,'r') as f:
        movies = f.readlines()
        movies = [movie.rstrip('(обратный слэш)n').lower() for movie in movies]
    first_words = [nltk.word_tokenize(movie)[0] for movie in movies]    
    sort_first_words = sorted(first_words,key = lambda x: len(x),reverse=True)
    return sort_first_words[0],sort_first_words[1]


def read_last_word(file):
    with open(file,'r') as f:
        movies = f.readlines()
        movies = [movie.rstrip('(обратный слэш)n').lower() for movie in movies]

    last_words = [nltk.word_tokenize(movie)[-1] for movie in movies 
                  if  len(nltk.word_tokenize(movie))>1 and nltk.word_tokenize(movie)[-1] not in '.,?!:/' ]    

    sort_last_words = sorted(last_words,key = lambda x: len(x),reverse=True)
    return sort_last_words[0],sort_last_words[1]

def read_mid_word(file):
    with open(file,'r') as f:
        movies = f.readlines()
        movies = [movie.rstrip('(обратный слэш)n').lower() for movie in movies]

    mid_words = [] 

    for movie in movies:
        if len(nltk.word_tokenize(movie))>2:
            for word in nltk.word_tokenize(movie)[1:-1]:
                if word not in '.,?!:/':
                    mid_words.append(word)


    sort_mid_words = sorted(mid_words,key = lambda x: len(x),reverse=True)
    return sort_mid_words[0],sort_mid_words[1] 



result = []
result.append(dask.delayed(read_first_word)(file))
result.append(dask.delayed(read_last_word)(file))
result.append(dask.delayed(read_mid_word)(file))


results_dask = dask.compute(*result)
results_dask
    ''')


def mov_2():
    print('''
Из названий фильмов, заданных в файле movies.txt, выделить первое слово, второе слово, третье слово и остальные слова. Второе и последующие слова выделяются, если они имеются, остальные слова названия включают четвёртое и все последующие слова названия. Словом считается любой выделенный разделителями набор символов, не относящихся к знакам препинания (отдельно стоящий символ "&" считается словом).
Найти по 2 самых популярных слова, относящихся к каждой из 4х групп. Сформировать из 8 найденных слов список. Распараллелить расчёт при помощи dask.delayed.


import dask
from collections import Counter
import nltk
file = 'movies.txt'
with open(file,'r') as f:
    movies = f.readlines()
    movies = [movie.rstrip('(обратный слэш)n') for movie in movies]
movies
def read_first_word(file):
    with open(file,'r') as f:
        movies = f.readlines()
        movies = [movie.rstrip('(обратный слэш)n').lower() for movie in movies]
    first_words = [nltk.word_tokenize(movie)[0] for movie in movies]    
    two_popular = Counter(first_words).most_common(2)
    return two_popular[0][0],two_popular[1][0],Counter(first_words)
def read_second_word(file):
    with open(file,'r') as f:
        movies = f.readlines()
        movies = [movie.rstrip('(обратный слэш)n').lower() for movie in movies]

    sec_words = [nltk.word_tokenize(movie)[1] for movie in movies 
                  if  len(nltk.word_tokenize(movie))>1 and nltk.word_tokenize(movie)[1] not in '.,?!:/' ]    

    two_popular = Counter(sec_words).most_common(2)
    return two_popular[0][0],two_popular[1][0]
def read_third_word(file):
    with open(file,'r') as f:
        movies = f.readlines()
        movies = [movie.rstrip('(обратный слэш)n').lower() for movie in movies]

    third_words = [nltk.word_tokenize(movie)[2] for movie in movies 
                  if  len(nltk.word_tokenize(movie))>2 and nltk.word_tokenize(movie)[2] not in '.,?!:/' ]    

    two_popular = Counter(third_words).most_common(2)
    return two_popular[0][0],two_popular[1][0] 
def read_last_words(file):
    with open(file,'r') as f:
        movies = f.readlines()
        movies = [movie.rstrip('(обратный слэш)n').lower() for movie in movies]

    last_words = [] 

    for movie in movies:
        if len(nltk.word_tokenize(movie))>3:
            for word in nltk.word_tokenize(movie)[3:]:
                if word not in '.,?!:/':
                    last_words.append(word)


    two_popular = Counter(last_words).most_common(2)
    return two_popular[0][0],two_popular[1][0] 
result = []
result.append(dask.delayed(read_first_word)(file))
result.append(dask.delayed(read_second_word)(file))
result.append(dask.delayed(read_third_word)(file))
result.append(dask.delayed(read_last_words)(file))
results_dask = dask.compute(*result)
    ''')


def mov_3():
    print('''
Из названий фильмов, заданных в файле movies.txt, выделить первое слово, последнее слово (если оно отличается от первого) и остальные слова (для названий, состоящих из 3х и более слов). Словом считается любой выделенный разделителями набор символов, не относящихся к знакам препинания (отдельно стоящий символ "&" считается словом). Найти по 2 самых популярных слова, относящихся к каждой из 3х групп. Сформировать из 6 найденных слов список. Распараллелить расчёт при помощи dask.delayed

import dask
from collections import Counter
import nltk
file = 'movies.txt'
with open(file,'r') as f:
    movies = f.readlines()
    movies = [movie.rstrip('(обратный слэш)n') for movie in movies]
def read_first_word(file):
    with open(file,'r') as f:
        movies = f.readlines()
        movies = [movie.rstrip('(обратный слэш)n').lower() for movie in movies]
    first_words = [nltk.word_tokenize(movie)[0] for movie in movies]    
    two_popular = Counter(first_words).most_common(2)
    return two_popular[0][0],two_popular[1][0]
def read_last_word(file):
    with open(file,'r') as f:
        movies = f.readlines()
        movies = [movie.rstrip('(обратный слэш)n').lower() for movie in movies]

    last_words = [nltk.word_tokenize(movie)[-1] for movie in movies 
                  if  len(nltk.word_tokenize(movie))>1 and nltk.word_tokenize(movie)[-1] not in '.,?!:/' ]    

    two_popular = Counter(last_words).most_common(2)
    return two_popular[0][0],two_popular[1][0]
def read_mid_word(file):
    with open(file,'r') as f:
        movies = f.readlines()
        movies = [movie.rstrip('(обратный слэш)n').lower() for movie in movies]

    mid_words = [] 

    for movie in movies:
        if len(nltk.word_tokenize(movie))>2:
            for word in nltk.word_tokenize(movie)[1:-1]:
                if word not in '.,?!:/':
                    mid_words.append(word)


    two_popular = Counter(mid_words).most_common(2)
    return two_popular[0][0],two_popular[1][0]
result = []
result.append(dask.delayed(read_first_word)(file))
result.append(dask.delayed(read_last_word)(file))
result.append(dask.delayed(read_mid_word)(file))
results_dask = dask.compute(*result)
    ''')


def rnd_1():
    print('''
В массиве чисел, хранящихся в файле random.hdf5, посчитать долю значений, превышающих среднее значение более чем на 3 стандартных отклонения. Выполнить задание с использованием Dask.array, распараллелив процесс обработки данных (использование Dask должна приводить к истинной параллельной обработке данных).

import dask.array as da
import h5py

file = 'random.hdf5'
with h5py.File(file,'r') as hdf:

    for dataset_name in list(hdf.keys()):
        print(f"Dataset name={dataset_name},dataset size={hdf[dataset_name].shape}, metadata={dict(hdf[dataset_name].attrs.items())}")

    data = da.from_array(hdf['data_set_1'][:])   

data_mean = da.mean(data)
data_std = da.std(data)

da.sum((data - data_mean) > 3*data_std).compute() / (data.shape[0]*data.shape[1])
    ''')

def rnd_2():
    print('''
В массиве чисел, хранящихся в файле, найти строчку ( вывести её индекс и содерж. значения) , в которых более всего значений превышающих среднее значение по всему массиву

import dask.array as da
import h5py
import numpy as np

hdf = h5py.File('random.hdf5', 'r')
list(hdf.keys())  #получили тут название можно без этого 

with h5py.File("./data/random.hdf5") as fp:
    arr_d = da.array(fp["data_set_1"][:,:])
arr_d[(arr_d > arr_d.mean()).sum(axis=1).argmax()].compute()
    ''')


def rnd_3():
    print('''
В массиве чисел, хранящихся в файле, подсчитать количество строк, в которых более 600 значений, превышающих сред.значение по массиву

import numpy as np
import h5py
import dask.array as da

f = h5py.File('random.hdf5', 'r')
dataset = f['data_set_1']

da_set = da.from_array(dataset, chunks=(1000, 1000))

((da_set>da_set.mean()).sum(axis = 1)>600).sum().compute()

    ''')


def rnd_4():
    print('''
В массиве чисел, хранящихся в файле, подсчитать количество значение , не отклоняющихся от среднего значения более чем на 3 стандартных отклонений.

import dask.array as da
import h5py

file = 'random.hdf5'
with h5py.File(file,'r') as hdf:

    for dataset_name in list(hdf.keys()):
        print(f"Dataset name={dataset_name},dataset size={hdf[dataset_name].shape}, metadata={dict(hdf[dataset_name].attrs.items())}")

    data = da.from_array(hdf['data_set_1'][:])    

data_mean = da.mean(data)
data_std = da.std(data)

da.sum(da.absolute(data - data_mean) < 3*data_std).compute()
    ''')