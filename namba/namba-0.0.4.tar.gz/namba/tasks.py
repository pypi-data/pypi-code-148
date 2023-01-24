import json
import os
from typing import Dict, Any
from typing import Union
from typing import Optional
import string

import pathlib
from IPython.display import display, Markdown


class Task:
    class Fields:
        ID = "id"
        UNIT = "unit"
        TASK_TEXT = "task_text"
        TASK_SOLUTION_CODE_ANALYTICS = "task_solution_code_analytics"
        TASK_SOLUTION_CODE = "task_solution_code"

    def __init__(self, id: int = 0, unit: str = "test", task_text: str = "нет",
                 task_solution_code_analytics: str = "нет", task_solution_code: str = "нет"):
        self.id = id
        self.unit = unit
        self.task_text = task_text
        self.task_solution_code_analytics = task_solution_code_analytics
        self.task_solution_code = task_solution_code

    @staticmethod
    def deserialize(data: Dict[str, Any]) -> 'Task':
        return Task(
            id=data.get(Task.Fields.ID),
            unit=data.get(Task.Fields.UNIT),
            task_text=data.get(Task.Fields.TASK_TEXT),
            task_solution_code_analytics=data.get(Task.Fields.TASK_SOLUTION_CODE_ANALYTICS),
            task_solution_code=data.get(Task.Fields.TASK_SOLUTION_CODE)
        )


def help():
    print('1. namba.find_by_words("любое количество слов")')
    print('2. namba.get_task_by_id(выбранный_id)')
    print('''3. namba.find_by_unit(unit) unit: karenina|accounts|sp500hst|random|all_k|
                               adressbook|chinok|titanik|speach_parts|movies|money|other''')


def load_all_tasks():
    all_tasks = []
    with open(pathlib.Path(pathlib.Path(os.path.dirname(os.path.abspath(__file__)), "tasks_base.txt")),
              encoding="UTF8") as f:
        for row in f:
            all_tasks.append(Task.deserialize(json.loads(row)))
    return all_tasks


def get_task_by_id(id: int) -> Union[None, str]:
    all_tasks = load_all_tasks()
    for task in all_tasks:
        if task.id == id:
            eval(task.task_solution_code_analytics + "()")
            return

    return "fuck"


def find_by_words(words: str, unit: Optional[str] = None):
    words = words.split()
    words = [w.lower().replace("ё", "е") for w in words]
    all_tasks = load_all_tasks()
    counter = [0 for _ in range(max([task.id for task in all_tasks]) + 4)]
    for task in all_tasks:
        task_words = task.task_text.translate(str.maketrans('', '', string.punctuation))
        task_words = task_words.split(" ")
        task_words = [w.lower().replace("ё", "е") for w in task_words]
        for word in words:
            if word in task_words:
                counter[task.id] += 1
    all_tasks_by_id = {task.id: task for task in all_tasks}
    c = [[counter[i], i] for i in range(len(counter))]
    c.sort(reverse=True)
    for el in c:
        if el[0] > 0:
            i = el[1]
            task = all_tasks_by_id[i]
            text = task.task_text
            if unit:
                if task.unit == unit:
                    print(i, "\n".join([text[128 * i:128 * (i + 1)] for i in range(0, (len(text) - 1) // 128 + 1)]))
            else:
                print(i, "\n".join([text[128 * i:128 * (i + 1)] for i in range(0, (len(text) - 1) // 128 + 1)]))

def find_by_unit(unit: str):
    all_tasks = load_all_tasks()

    for task in all_tasks:
        if task.unit == unit:
            print(task.id, "\n".join([task.task_text[128 * i:128 * (i + 1)] for i in range(0, (len(task.task_text) - 1) // 128 + 1)]))


def solve():
    display(Markdown(r"""
```
a = 5
b = 7
print(a + b)
```
 """))

def sample_and_sample_choice_function():
    display(Markdown(r"""
    $ n\hat{F(x)}  \sim Bin(n, F(x)); F(x) = \frac{x-a}{b-a} $  

$ a)P((\hat{F(6)}=\hat{F(8)}) = P(X_i  \nsubseteq [5,8]) = (1-\frac{2}{3})^6 \approx 0,0014$  

$ б) Y = 6\hat{F(7)}\sim Bin(6, \frac{2}{3})  $  
$ P(\hat{F(7)})=\frac{1}{2} = P(Y=3) = С^3_6 p^3 (1-p)^3 = \frac{4 \cdot 5 \cdot 6}{6} \cdot (\frac{2}{3})^3 \cdot (\frac{1}{3})^3  \approx 0,2195$  
    """))

def task_Anna_Karenina_1():
    display(Markdown(r"""
```
regul = re.compile('^[а-яА-ЯёЁ]*$') 
with open('AnnaKarenina_.txt', encoding='cp1251') as f:
    book_tokens = [t.text.lower() for t in tokenize(f.read()) if regul.search(t.text)]

fdist = FreqDist(book_tokens)
fdist.most_common(200) #вывести

ru_stop_words = stopwords.words('russian')
ru_stop_words_s = set(ru_stop_words)

tokens_without_sw = [w for w in book_tokens if w not in ru_stop_words_s] 

fdist = FreqDist(tokens_without_sw)
fdist.most_common(200)
```    
"""))

def task_Anna_Karenina_2():
    display(Markdown(r"""
```
sents = []
with open('AnnaKarenina_.txt', encoding='cp1251') as f:
  for line in f:
    sents.extend([x.text for x in sentenize(line)])
sent = [re.sub(r'(–\xa0)|(\xa0)|(\n)|([^\w\s])', '', x.lower()) for x in sents if len(x) <= 40]
sent_less40 = np.unique(list(filter(None, sent)))

sent_less40 = np.unique(sent_less40)

dist = []
for i, j in combinations(range(len(sent_less40)), 2):
    sent1, sent2 = sent_less40[i], sent_less40[j]
    d = edit_distance(sent1, sent2)
    if d > 3:
        continue
    dist.append((d, sent1, sent2))
    if len(dist) > 3:
        break

dist
```    
"""))

def task_Anna_Karenina_3():
    display(Markdown(r"""
```
regular = re.compile('^[а-яА-ЯёЁ]*$') # re.compile('^[а-яА-ЯёЁ,\.]*$')
with open('AnnaKarenina_.txt', encoding='cp1251') as f:
    book_tokens = [t.text.lower() for t in tokenize(f.read()) if regular.search(t.text)] 


lemmatizer = pymorphy2.MorphAnalyzer()
def my_lemmatizer(word):
    lemma = lemmatizer.parse(word)[0].normal_form
    return lemma

lemms = {word: my_lemmatizer(word) for word in np.unique(book_tokens)}

df = pd.DataFrame.from_dict(lemms, orient='index', columns=['norm_word'])

[(form, Counter(book_tokens).get(form)) for form in df[df['norm_word'] == 'анна'].index]


```    
"""))

def task_accounts_1():
    display(Markdown(r"""
```
accounts = dd.read_csv(r'accounts.*.csv', dtype={'amount': 'float64'})

accounts_new = accounts[(accounts.amount % 5 == 0) & (accounts.amount % 10 != 0)]


max_id = accounts_new.groupby(accounts_new.id).count().amount.idxmax()
max_id.compute()

```    
"""))

def task_accounts_2():
    display(Markdown(r"""
```
accounts = dd.read_csv(r'accounts.*.csv', dtype={'amount': 'float64'})
accounts_new = accounts[(accounts.amount >= 1000) & (accounts.amount <= 1500)]
max_id = accounts_new.groupby(accounts_new.id).count().amount.idxmax()
max_id.compute()

```    
"""))

def task_accounts_3():
    display(Markdown(r"""
```
acc = dd.read_csv(r'accounts.*.csv', dtype={'amount': 'float64'})
acc_positive = acc[acc['amount'] > 0]

sum_amount = acc_positive.groupby('id').agg({'amount':'sum'})

sum_amount[sum_amount['amount'] == sum_amount['amount'].max()].compute()

sum_amount.idxmax().compute()

```    
"""))

def task_accounts_4():
    display(Markdown(r"""
```
acc = dd.read_csv(r'accounts.*.csv', dtype={'amount': 'float64'})

acc3 = acc[acc.amount % 3 == 0]

max_count = acc3.groupby(acc3.id).count().amount.idxmax()

max_count.compute()

```    
"""))

def task_sp500hst_1():
    display(Markdown(r"""
```
names = pd.read_csv('sp_data2.csv', names = ['ticker', 'company', 'persantage'], sep = ';')
data = pd.read_csv('sp500hst.txt', names=['date', 'ticker', 'open', 'high', 'low', 'close', 'volume'], parse_dates=['date'])
all_data = data.merge(names, on = 'ticker', how = 'left')[['date', 'ticker', 'open', 'high',
                                                           'low', 'close', 'volume', 'company']]
all_data
```    
"""))

def task_sp500hst_2():
    display(Markdown(r"""
```
data = pd.read_csv('sp500hst.txt', sep=',', 
                   names=["date", "ticker", "open", 
                          "high", "low", "close", "volume"], parse_dates=['date'])
data.head()

data_2010 = data[data['date'].dt.year==2010]
data_2010.head()

data_groupby = data_2010.groupby('ticker')['open', 'high', 'low', 'close', 'volume'].mean()
data_groupby.head()

data_groupby.to_csv('data_2010_mean.csv')
```    
"""))

def task_sp500hst_3():
    display(Markdown(r"""
```
data = pd.read_csv('sp500hst.txt', sep=',', 
                   names=["date", "ticker", "open", 
                          "high", "low", "close", "volume"], parse_dates=['date'])
data.head()

nvda = data[data['ticker']=='NVDA']
nvda.head()

nvda[nvda['open']==nvda['open'].max()]

nvda[nvda['open']==nvda['open'].min()]

# Количество дней
abs((nvda.loc[80700]['date'] - nvda.loc[80853]['date']).days)

# Суммарный объем торгов
nvda.loc[80700:80853]['volume'].sum()
```    
"""))

def task_sp500hst_4():
    display(Markdown(r"""
```
data = pd.read_csv(r"C:\Users\nkmeo\ТОБД22_датасеты\датасеты_к_заданию_2\sp500hst.txt",
                   encoding="utf-8",
                   header=None,
                   names=["date", "ticker", "open", 
                          "high", "low", "close", "volume"],
                   parse_dates=["date"])

pd.pivot_table(data, index="date", columns="ticker", values="volume")
```    
"""))

def task_sp500hst_5():
    display(Markdown(r"""
```
data = pd.read_csv(r"C:\Users\nkmeo\ТОБД22_датасеты\датасеты_к_заданию_2\sp500hst.txt", names=['date', 'ticker', 'open', 'high', 'low', 'close', 'volume'], parse_dates=['date'])
data

NVDA = data[data['ticker']=='NVDA']
AAPL = data[data['ticker']=='AAPL']

dt_NVDA_APPL = NVDA.merge(AAPL, on = 'date')
dt_NVDA_APPL['difference'] = abs(dt_NVDA_APPL.volume_x - dt_NVDA_APPL.volume_y)

modif_dt_NVDA_APPL = dt_NVDA_APPL[(dt_NVDA_APPL.open_x < dt_NVDA_APPL.close_x) & (dt_NVDA_APPL.open_y < dt_NVDA_APPL.close_y)]
modif_dt_NVDA_APPL
```    
"""))


def task_random_1():
    display(Markdown(r"""
```
data = pd.read_csv(r"C:\Users\nkmeo\ТОБД22_датасеты\датасеты_к_заданию_2\sp500hst.txt", names=['date', 'ticker', 'open', 'high', 'low', 'close', 'volume'], parse_dates=['date'])
data = data[data['date'].dt.year==2010]
data

res = pd.DataFrame(columns = ['Тикер', 'open', 'high', 'low', 'close', 'volume'])
tickers = data.ticker.unique()
res['Тикер'] = tickers
res

grouped = data.groupby('ticker')['open', 'high', 'low', 'close', 'volume'].mean()
res.open, res.high, res.low, res.close, res.volume = list(grouped.open), list(grouped.high), list(res.low), list(grouped.close), list(grouped.volume)
res
```    
"""))

def task_random_2():
    display(Markdown(r"""
```
p = r'C:\Users\nkmeo\ТОБД22_датасеты\датасеты_к_заданию_3\random.hdf5'
data_f  = h5py.File(p, 'r')
list(data_f.keys())

data_set = data_f['/data_set_1']

data_set.shape

data_set

data_set = np.array(data_set)
data_set

recipe_da = da.from_array(data_set, chunks=(1000, 1000))
recipe_da

mean_value = recipe_da.mean()

std_value = recipe_da.std()

(abs(recipe_da) - mean_value < 3*std_value).sum().compute()/(data_set.shape[0]*data_set.shape[1])
```    
"""))

def task_random_3():
    display(Markdown(r"""
```
data_f  = h5py.File(r'C:\Users\nkmeo\ТОБД22_датасеты\датасеты_к_заданию_3\random.hdf5', 'r')
list(data_f.keys())

data_set = data_f['/data_set_1']

data_set.shape

data_set = np.array(data_set)
data_set

data_da = da.from_array(data_set, chunks=(1000, 1000))
data_da

mean_value = data_da.mean()
mean_value.compute()

# нужен ли модуль у data_da?
(((data_da > mean_value).sum(axis=1)>600).sum()).compute()
```    
"""))

def task_random_4():
    display(Markdown(r"""
```
data_f  = h5py.File(r'C:\Users\nkmeo\ТОБД22_датасеты\датасеты_к_заданию_3\random.hdf5', 'r')
list(data_f.keys())

data_set = data_f['/data_set_1']

data_set = np.array(data_set)
data_set

data_da = da.from_array(data_set, chunks=(1000, 1000))
data_da

mean_value = data_da.mean()
mean_value.compute()

# нужен ли модуль у data_da?
indx = ((data_da > mean_value).sum(axis=1)).argmax().compute()
indx

data_da[indx].compute()
```    
"""))


def task__all_k_1():
    display(Markdown(r"""
```
data = db.read_text(r'datasets\all_k\*', encoding='cp1251')

def find_dialog(string):
    return len(re.findall(r'^\s*[—-]', string))

data.map(find_dialog).sum().compute()


data.foldby(key=find_dialog,
            binop=lambda t, x: t + 1, initial=0,
            combine=lambda t1, t2: t1 + t2, combine_initial=0).compute()
```    
"""))


def task__all_k_2():
    display(Markdown(r"""
```
bag = db.read_text('all_k\*', encoding='Windows-1251')

def q_pobud(data):
    return len(re.findall(r'(?!!\?)!', data))

def q_povestv(data):
    return len(re.findall(r'(\.)[ ][А-Я]|\.$|\.\\n', data))

def q_vopros(data):
    return len(re.findall(r'\?', data))

bag.map(q_pobud).sum().compute()

bag.map(q_povestv).sum().compute()

bag.map(q_vopros).sum().compute()
```    
"""))


def task__all_k_3():
    display(Markdown(r"""
```
bag = db.read_text('all_k\*',  encoding='Windows-1251')

def q_uppercase(list_string):
    uppercase = defaultdict(int)

    for string in list_string:
        for word in string.split():
            for letter in list(word):
                if letter.isupper() and bool(re.search('[А-Я]', letter)):
                    uppercase[letter] +=1
    return uppercase

q_uppercase(bag)
```    
"""))


def task__addres_book_1():
    display(Markdown(r"""
```
with open(r'datasets\addres-book-q.xml') as f:
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

```    
"""))


def task__addres_book_2():
    display(Markdown(r"""
```
with open('addres-book-q.xml') as f:
    ab = BeautifulSoup(f, 'xml')

    ab.address_book.country.address

    list_female = []
    list_male = []

    for person in ab.address_book.find_all("address"):
        g = person.find('gender').next
        name = person.find('name').next
        if g=='m':
            company = person.find('company').next
            phone = person.find('phone', type='work').next
            list_male.append((name, company, phone,))
        else:
            phone = person.find('phone', type='personal').next
            list_female.append((name, phone,))

    list_male

    list_female

    with open('address_book_male.pickle', 'wb') as f:
        pickle.dump(list_male, f)

    with open('address_book_female.pickle', 'wb') as f:
        pickle.dump(list_female, f)

    with open('address_book_female.pickle', 'rb') as f:
        ad_book_f = pickle.load(f)

    ad_book_f

    with open('address_book_male.pickle', 'rb') as f:
        ad_book_m = pickle.load(f)

    ad_book_m

```    
"""))


def task__addres_book_3():
    display(Markdown(r"""
```
with open('addres-book-q.xml') as f:
    ab = BeautifulSoup(f, 'xml')

positions_dic = dict()

for person in ab.address_book.find_all("address"):

    position = person.find('position').next
    name = person.find('name').next
    ph = [phones.next for phones in person.phones.find_all("phone")]
    company = person.find('company').next

    if position not in positions_dic.keys():
        positions_dic[str(position)] = {str(name):{'name': name, "company": company, 'phones': ph}}
    else:
        positions_dic[str(position)][str(name)] = {'name': name, "company": company, 'phones': ph}

    positions_dic

    with open('addres_book_positions.json', mode='w', encoding='utf-8') as f: # открываем файл на запись
        json.dump(positions_dic, f, indent=2)

    positions_data

```  
"""))


def task_chinok_sqlite_1():
    display(Markdown(r"""
path = '/content/drive/MyDrive/'

def get_artists():

    try:
        sqlite_connection = sqlite3.connect(path)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = '''SELECT Name
                                 FROM Artist'''''

        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for row in records:
            print(row[0])

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

get_artists() 


def album_and_count_track(name):
    try:
        sqlite_connection = sqlite3.connect(path)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = '''SELECT COUNT(Track.Name), Title
                                 FROM Album JOIN Artist USING(ArtistId)
                                 JOIN Track USING(AlbumId)
                                 GROUP BY Title
                                 HAVING Artist.Name = ?'''

        cursor.execute(sqlite_select_query, (name,))
        records = cursor.fetchall()

        for row in records:
            print('Количество треков в альбоме: ', row[0], '\tНазвание альбома: ', row[1])

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if sqlite_connection:

            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

album_and_count_track('AC/DC')
"""))


def task_chinok_sqlite_2():
    display(Markdown(r'''
path = '/content/drive/MyDrive/'
def find_albom(name):
    try:
        sqlite_connection = sqlite3.connect(path)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT Title
                                 FROM Album JOIN Artist USING(ArtistId)
                                 WHERE Name = ?"""

        cursor.execute(sqlite_select_query, (name,))
        records = cursor.fetchall()

        for row in records:
            print(row[0])

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

find_albom('Alice In Chains')  # 1 'AC/DC' (альбомов 2) 5 'Alice In Chains' (альбомов 1)

def count_and_time(name, album):
    try:
        sqlite_connection = sqlite3.connect(path)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT COUNT(*), SUM(Milliseconds)
                                 FROM Album JOIN Artist USING(ArtistId)
                                 JOIN Track USING(AlbumId)
                                 WHERE Artist.Name = ? AND Title = ?"""

        cursor.execute(sqlite_select_query, (name, album))
        records = cursor.fetchall()

        for row in records:
            print('Количество треков в альбоме: ', row[0], '\nСуммарная продолжительность: ', row[1])

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if sqlite_connection:

            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

count_and_time('Alice In Chains', 'Facelift')
'''))


def task_chinok_sqlite_3():
    display(Markdown(r'''

def find_playlists():

    try:
        sqlite_connection = sqlite3.connect('Chinook_Sqlite.sqlite')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT DISTINCT Name
                                 FROM Playlist"""

        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for row in records:
            print(row[0])

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

find_playlists()

def count_and_time(playlist_name):

    try:
        sqlite_connection = sqlite3.connect('Chinook_Sqlite.sqlite')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT COUNT(*), SUM(t.Milliseconds)
                                 FROM Playlist p JOIN PlaylistTrack pt ON p.PlaylistId = pt.PlaylistId
                                 JOIN Track t ON pt.TrackId = t.TrackId
                                 WHERE p.Name = ?"""

        cursor.execute(sqlite_select_query, (playlist_name,))
        records = cursor.fetchall()

        for row in records:
            print('Количество треков в плейлисте: ', row[0], '\nСуммарная продолжительность: ', row[1])

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if sqlite_connection:

            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

count_and_time('Music')
'''))

def task_titanic_1():
  display(Markdown(r'''
df = pd.read_csv(r'datasets\titanic.csv')
df.Age[df.Age.isna() & (df.Sex == 'male') & (df.Pclass == 1)] = df.Age[(df.Sex == 'male') & (df.Pclass == 1)].fillna(df.Age[(df.Sex == 'male') & (df.Pclass == 1)].mean())
df.Age[df.Age.isna() & (df.Sex == 'male') & (df.Pclass == 2)] = df.Age[(df.Sex == 'male') & (df.Pclass == 2)].fillna(df.Age[(df.Sex == 'male') & (df.Pclass == 2)].mean())
df.Age[df.Age.isna() & (df.Sex == 'male') & (df.Pclass == 3)] = df.Age[(df.Sex == 'male') & (df.Pclass == 3)].fillna(df.Age[(df.Sex == 'male') & (df.Pclass == 3)].mean())
df.Age[df.Age.isna() & (df.Sex == 'female') & (df.Pclass == 1)] = df.Age[(df.Sex == 'female') & (df.Pclass == 1)].fillna(df.Age[(df.Sex == 'female') & (df.Pclass == 1)].mean())
df.Age[df.Age.isna() & (df.Sex == 'female') & (df.Pclass == 2)] = df.Age[(df.Sex == 'female') & (df.Pclass == 2)].fillna(df.Age[(df.Sex == 'female') & (df.Pclass == 2)].mean())
df.Age[df.Age.isna() & (df.Sex == 'female') & (df.Pclass == 3)] = df.Age[(df.Sex == 'female') & (df.Pclass == 3)].fillna(df.Age[(df.Sex == 'female') & (df.Pclass == 3)].mean())
'''))

def task_out_of_ds_1():
    display(Markdown(r"""
```

def get_pos_tag(sent):
    func = lambda token: token not in punctuation
    res = pos_tag(list(filter(func, word_tokenize(sent))))
    part_of_speech = [x[1] for x in res]
    word = [x[0] for x in res]
    s = ''
    for i in range(len(part_of_speech)):
        s += f'{part_of_speech[i]:^5}' 
    s += '\n' + ' '.join(word)
    return s

sent = sent_tokenize("i was very sad to play football")
print(get_pos_tag(sent[0]))

```    
"""))


def task_movies_1():
    display(Markdown(r"""
```

def list_word(filename):
    with open(filename, 'r') as f:
        reader = f.readlines()
        word = [[],[],[]]
        for line in reader:
            if len(reader[1].split())>2:
                word[0].append(line.split()[0])
                word[1]+=line.split()[1:-1]
                word[2].append(line.split()[-1])
            elif len(reader[1].split())==2:
                word[0].append(line.split()[0])
                word[2].append(line.split()[-1])
            else: word[0].append(line.split()[0])

        word_list = []
        for i in word:
            word_list += sorted(i, key=len)[-2:]
    return word_list

%%time
list_word('датасеты_к_заданию_3/movies.txt')

list_word_dask = dask.delayed(list_word)
x1 = list_word_dask('датасеты_к_заданию_3/movies.txt')

%%time
x2 = dask.compute(x1, scheduler = 'processes', num_workers = 3)

%%time
x3 = dask.compute(x1, scheduler = 'threads', num_workers = 3)

```    
"""))

def task_movies_2():
    display(Markdown(r"""
```
def get_words():
    with open('датасеты_к_заданию_3/movies.txt') as f:
        first = []
        second = []
        third = []
        other = []
        for line in f:
            words = line.split()
            first.append(words[0])  # добавили первое 
            if len(words) > 1:
                second.append(words[1])  # добавили второе, если есть
            if len(words) > 2:
                third.append(words[2])  # добавили тертье, если есть
            if len(words) > 3:
                third.extend(words[3:])  # добавили остальные, если есть


    w = []
    for list_words in [first, second, third, other]:
        w += sorted(list_words, key=len, reverse=True)[:2]
    return w
    
%%time
get_words()

list_word_dask = dask.delayed(get_words)
x1 = list_word_dask()

%%time
x2 = dask.compute(x1, scheduler='processes', num_workers=3)

%%time
x3 = dask.compute(x1, scheduler='threads', num_workers=3)

```    
"""))


def task_money_1():
    display(Markdown(r"""
```
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
```    
"""))

def task_money_2():
    display(Markdown(r"""
```
f = xw.Book('себестоимостьА_в1.xlsx')
sht = f.sheets['Рецептура']

sht.range('G15').formula = "=AVERAGE(G7:G13)"

# импортируем константу:
from xlwings.constants import AutoFillType

sht.range('G15').api.AutoFill(sht.range("G15:O15").api, AutoFillType.xlFillDefault)

```    
"""))

def task_money_3():
    display(Markdown(r"""
```
f = xw.Book('себестоимостьА_в1.xlsx')
sht = f.sheets['Рецептура']

bread1 = sht.range('C7').options(expand='down').value
bread2 = sht.range('C23').options(expand='down').value
bread3 = sht.range('C40').options(expand='down').value
bread4 = sht.range('C61').options(expand='down').value
bread1 + bread2 + bread3 + bread4

f.sheets.add(name='Наименование', after='Рецептура') #name, before, after
sht2 = f.sheets['Наименование']

sht2.range('A1').value = 'Наименование продукции'
sht2.range('B1').value = 'Доля'
sht2.range('A2').options(transpose=True).value = bread1 + bread2 + bread3 + bread4

rng_name = xw.Range('C7').expand('table').address
rng_name

```    
"""))



def task_other_1():
    display(Markdown(r"""
```

import numpy as np
arr = np.array([2,3,2,2,2,1])
arr


def ohe(x):  # Я и Саша решили, что это плохое решение, тк используется словарь. Но это лучше, чем ничего...
    n = np.unique(x)
    shape = (x.size, n.shape[0])
    one_hot = np.zeros(shape)
    rows = np.arange(x.size)
    d = dict(zip(n, range(len(n))))
    func = lambda val: d.get(val)
    vfunc = np.vectorize(func)
    ind = vfunc(x)
    one_hot[rows, ind] = 1
    return one_hot
    
ohe(arr)

arr2 = np.array([0, 2, 3, 2, 2, 2, 1]) 
ohe(arr2)

arr3

arr3 = np.random.randint(0, 100, size=(12,))
ohe(arr3)
```    
"""))

def task_other_2():
    display(Markdown(r"""
```
A = np.array([
    [8, 4, 15, 6, 9],
    [3, 16, 13, 8, 10],
    [0, 9, 18, 17, 5],
    [16, 2, 6, 0, 10],
    [18, 13, 9, 17, 8]])
    
np.resize(A.min(axis=1), (5,5))

np.resize(A.min(axis=1), (5,5)).transpose()

A.min(axis=0)

B = np.resize(A.min(axis=1), (5,5)).transpose() + A.min(axis=0)
B

```    
"""))

def task_other_3():
    display(Markdown(r"""
```
import numpy as np


main_data = np.random.randint(0, 15, size = (25, 4))
tmp_data = main_data.copy()

print("Сгенерированный массив: ")
print(main_data)


max_num = np.amax(main_data, axis = 1)
main_data[main_data == max_num[:,None]] = -1


max_in_col = np.array([np.sum(main_data[:,i] == -1) for i in range(4)])
max_cols_count = np.sum(max_in_col == np.amax(max_in_col))
ind_to_reset = np.argpartition(max_in_col, -max_cols_count)[:-max_cols_count]

main_data[:,ind_to_reset] = tmp_data[:,ind_to_reset]

for i in range(4):
    if max_in_col[i] > 5:
        print(f"Столбец {i} содержит более 5 максимумов")

print("Итоговый массив: ")
print(main_data)
```    
"""))

def task_other_4():
    display(Markdown(r"""
```
def finder(text):
    word = re.compile(r'[a-z]+[\_][@]+')
    return re.findall(word, text)
    
t = 'dfdty_@@ghgrty_@hr'
finder(t)

t = 'dfdty_@@ghgrty_@hr__@'
finder(t)
```    
"""))

def task_other_5():
    display(Markdown(r"""
```
import numpy as np
ar1 = np.random.randint(-5, 6, size=(5, 15))
ar2 = np.random.randint(-5, 6, size=(5, 15))

# поскольку np.putmask сразу изменяет исходный массив, создадим копию массива ar2
a = np.copy(ar2)
# если знак элементов на одинаковых позициях отличается, на этом месте ставим 0 
# 0 считаю нейтральным элементом
np.putmask(a, ar1*ar2<0, 0)
a

ar1 = ar1+a
ar1
```    
"""))

def task_other_6():
    display(Markdown(r"""
```
import numpy as np
ar1 = np.random.randint(0, 101, size=(30, 4))
ar1



def evk_norm(x):
    return np.sqrt(sum(i**2 for i in x))
    
ar1_norm = np.apply_along_axis(evk_norm, 1, ar1)
ar1_norm #евклидова норма для каждого вектора

ar1_new = np.take(ar1, np.argsort(ar1_norm)[::-1][:5], axis=0)
ar1_new
```    
"""))

def task_other_7():
    display(Markdown(r"""
```
import numpy as np
arr = np.random.randint(0, 50, size=(10, 4))
arr



unique, counts = np.unique(arr, return_counts=1)
unique, counts

most_freq = unique[counts == counts.max()]
most_freq

arr_mf = np.in1d(arr, most_freq).reshape(10, 4)
arr_mf

np.where(arr_mf, 1, 0)

freqstr = arr_mf.sum(axis=1)
freqstr

mostfrstr = freqstr.argsort()[-3:]
mostfrstrmostfrstr = freqstr.argsort()[-3:]
mostfrstr
```    
"""))


def task_other_8():
    display(Markdown(r"""
```
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
    
list(filter(lambda x: x is not None, result))
```    
"""))

def task_other_9x():
    display(Markdown(r"""
```
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


%%time
res2 = [func(x) for x in l_r]
res2 = list(filter(None, res2))

res2

%%time
with Pool(processes=mp.cpu_count()) as pool:
    result = pool.map(func, l_r)
    
%%time
res2 = [func(x) for x in l_r]
```    
"""))