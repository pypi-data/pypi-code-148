import requests, re, json, pymysql, csv
from tqdm import tqdm
from . import error


# ============================数据存储============================
class Save:

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')
        self.database = kwargs.get('databases')
        self.data = kwargs.get('data')
        self.table = kwargs.get('table')
        self.fields = kwargs.get('fields')
        self.drop = kwargs.get('drop')
        self.path = kwargs.get('path')
        self.conn = None
        self.cursor = None
        self.dataType = None  # 存储的数据类型

    # --------------------存储操作--------------------
    # 创建表
    def _createTable(self):
        # 1. 查看表是否已经存在
        self.table: str = self.table if self.table else self.dataType
        self.table = self.table.lower()

        self.cursor.execute('show tables')
        table_tuple = [self.cursor.fetchall()]
        for tables in table_tuple[0]:
            # 2.如果存在则不创建
            if self.table == tables[0]:
                return None

        keys = ','.join(map(lambda item: item + ' varchar(32)', self.data[0].keys()))
        # 3. 不存在则创建
        sql = f"""create table {self.table}(id int primary key auto_increment, {keys})charset='utf8'"""
        self.cursor.execute(sql)
        print(f'表: {self.table} 创建完毕 ----- OK')

    # 插入数据
    def _insertSql(self):
        for dic in tqdm(self.data):
            try:
                keys = ','.join(dic.keys())
                values = ','.join(dic.values())
                sql = f"""insert into {self.table}({keys}) values({values})"""
                self.cursor.execute(sql)
                self.conn.commit()

            except Exception as e:
                print(e)
                self.conn.rollback()

        self.cursor.close()
        self.conn.close()
        print(f'表: {self.table} 存储完毕 ----- OK')

    def _insertCSV(self):
        with open(self.path, mode='w', encoding='utf-8', newline='') as fp:
            keys = self.data[0].keys()
            writer = csv.writer(fp)
            writer.writerow(keys)

        with open(self.path, mode='a', encoding='utf-8', newline='') as fp:
            writer = csv.writer(fp)
            for dic in tqdm(self.data):
                values = dic.values()
                writer.writerow(values)

    # --------------------校验操作--------------------
    # 数据校验: 所有对象都必须是一个类别
    def _exDataType(self):
        if not self.data:  # 如果数据不存在则不进行后续操作
            return False
        types = [self.data[0].__name__]
        for obj in self.data:
            if obj.__name__ not in types:
                raise Exception('所有数据类型都必须是同一个')
        self.dataType = types[0]
        return True

    # 校验Sql
    def _exSql(self):
        # 1. 创建连接器
        self.conn = pymysql.connect(
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database
        )
        self.cursor = self.conn.cursor()
        # 2. 创建表
        self._createTable()

    # --------------------数据处理--------------------
    # 字段过滤
    def _fieldsFilter(self):
        data = list()
        for obj in self.data:
            # 是否清除数据中的空值
            obj = Spider._dropNan(obj) if self.drop else Spider._dict(obj)
            if self.fields:  # 判断是否需要过滤字段
                obj_ = dict()
                for key, value in obj.items():
                    if key in self.fields:
                        obj_[key] = value
                data.append(obj_)
            else:
                data.append(obj)
        self.data = data

    # 字段处理: key => `key`, value => `value`
    def _fieldsHandel(self):
        data = list()
        for obj in self.data:
            obj_ = dict()
            for key, value in obj.items():
                key = list(str(key))
                value = list(str(value))
                key.insert(0, '`')
                key.append('`')
                value.insert(0, '\'')
                value.append('\'')
                obj_[''.join(key)] = ''.join(value)
            data.append(obj_)
        self.data = data

    # 数据处理
    def _dataHandle_mysql(self):
        # 1. 查看是否指定了需要的指定, 没指定则保存所有字段
        self._fieldsFilter()
        # 2. 字段处理
        self._fieldsHandel()

    # --------------------存储--------------------
    def _saveMysql(self):
        # 1.数据校验
        if self._exDataType():
            # 2.数据处理
            self._dataHandle_mysql()
            # 3.表的校验
            self._exSql()
            # 4.插入数据
            self._insertSql()

    def _saveCSV(self):
        # 1. 数据类型校验
        if self._exDataType():
            # 2. 字段过滤
            self._fieldsFilter()
            # 3. 数据存储
            self._insertCSV()


# ============================数据爬取============================
class Spider:
    # --------------------获取数据--------------------
    @staticmethod
    def _spider_world():
        try:
            data: dict = Spider._get_api(url=Spider.__world_api, headers=Spider.__headers)
        except Exception as e:
            raise error.WorldData('抱歉数据无法获取，请等待修复')
        return Spider._parseWorld(data=data)

    @staticmethod
    def _spider_china():
        try:
            data: dict = Spider._get_api(url=Spider.__china_api, headers=Spider.__headers)
        except Exception as e:
            try:
                data: dict = Spider._get_china_api(url=Spider.__china_api, headers=Spider.__headers)
            except Exception as e:
                raise error.WorldData('抱歉数据无法获取，请等待修复')
        return Spider._parseChina(data=data)

    # --------------------api工具--------------------
    __china_api = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    __world_api = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign'
    __headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57'
    }

    # --------------------数据清理--------------------
    @staticmethod
    def _dropNan(obj: object):
        """ 将对象 -> 字典, 并且会清除空值 """
        obj = obj.__dict__
        item: dict = dict()
        for key, value in obj.items():
            if (value is not None) and (not re.search('^_[A-Za-z]*__', key)):
                item[key] = value
        return item

    @staticmethod
    def _dict(obj: object):
        """ 将对象 -> 字典, 不会清除空值 """
        obj = obj.__dict__
        item: dict = dict()
        for key, value in obj.items():
            if not re.search('^_[A-Za-z]*__', key):
                item[key] = value
        return item

    # --------------------数据解析--------------------
    # 解析国内数据
    @staticmethod
    def _parseChina(data: dict):
        china = data['areaTree'][0]['total']
        china['lastUpdateTime'] = data['lastUpdateTime']
        china['name'] = data['areaTree'][0]['name']
        china['children'] = data['areaTree'][0]['children']
        return Nation(**china)

    # 解析出世界数据
    @staticmethod
    def _parseWorld(data: dict):
        dic: dict = data['globalStatis']
        dic['foreignList'] = data['foreignList']
        return World(**dic)

    # 解析国家数据
    @staticmethod
    def _parseNation(data: list):
        lis: list = list()
        for nation in data:
            lis.append(Nation(**nation))
        return lis

    # 解析中国省份数据
    @staticmethod
    def _parseProvince_china(data: list):
        lis: list = list()
        for province in data:
            pro = province['total']
            pro['name'] = province['name']
            pro['children'] = province['children']
            lis.append(Province(**pro))
        return lis

    # 解析省份数据
    @staticmethod
    def _parseProvince(data: list):
        lis: list = list()
        for province in data:
            lis.append(Province(**province))
        return lis

    # 解析城市数据
    @staticmethod
    def _parseCity(data: list, province: str):
        lis: list = list()
        for city in data:
            c = city['total']
            c['name'] = city['name']
            c['province'] = province
            lis.append(City(**c))
        return lis

    # --------------------数据爬取--------------------
    # 爬取数据
    @staticmethod
    def _get_api(**kwargs):
        data: dict = requests.get(url=kwargs['url'], headers=kwargs['headers']).json()
        return json.loads(data['data'])

    @staticmethod
    def _get_china_api(**kwargs):
        data = requests.get(url=kwargs['url'], headers=kwargs['headers']).json()
        data = data['data']
        data = '{'.join(data.split('{')[:-2])[:-1] + ']}]}]}'
        return json.loads(data)


# ============================模型类============================

# --------------------全球--------------------
class World:
    __name__ = 'World'

    def __init__(self, **kwargs):
        self.name = '地球'
        self.nowConfirm = kwargs['nowConfirm']  # 现存
        self.confirm = kwargs['confirm']  # 累计
        self.heal = kwargs['heal']  # 治愈
        self.dead = kwargs['dead']  # 死亡
        self.lastUpdateTime = kwargs['lastUpdateTime']  # 最后更新时间
        self.__data = kwargs['foreignList']  # 国家存储数据

    def searchNation(self, *args):
        """
        搜寻国家, 不搜寻会默认获取所有国家
        :param nation: 国家名
        :return: list
        """
        nations = Spider._parseNation(data=self.__data)
        nations = filter(lambda nat: nat.name in args, nations) if args else nations
        return list(nations)

    # 搜索单个
    def searchNation_one(self, nation: str):
        nations = Spider._parseNation(data=self.__data)
        nations = filter(lambda nat: nat.name == nation, nations)
        nations = list(nations)
        nation: Nation = nations[0] if nations else None
        return nation

    def keys(self, drop=True):
        return Spider._dropNan(self).keys() if drop else Spider._dict(self).keys()

    def values(self, drop=True):
        return Spider._dropNan(self).values() if drop else Spider._dict(self).values()


# --------------------国家--------------------
class Nation:
    __name__ = 'Nation'

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.continent = kwargs.get('continent')
        self.y = kwargs.get('y')
        self.date = kwargs.get('date')
        self.confirmAdd = kwargs.get('confirmAdd')
        self.confirmAddCut = kwargs.get('confirmAddCut')
        self.confirm = kwargs.get('confirm')
        self.suspect = kwargs.get('suspect')
        self.dead = kwargs.get('dead')
        self.heal = kwargs.get('heal')
        self.nowConfirm = kwargs.get('nowConfirm')
        self.confirmCompare = kwargs.get('confirmCompare')
        self.nowConfirmCompare = kwargs.get('nowConfirmCompare')
        self.healCompare = kwargs.get('healCompare')
        self.deadCompare = kwargs.get('deadCompare')
        self.lastUpdateTime = kwargs.get('lastUpdateTime')
        self.__data = kwargs.get('children')  # 国家对应的省份

    def searchProvince(self, *args):
        """
        搜索对应国家下的省份
        不指定省份默认获取所有
        :param args: 指定省份
        :return: list
        """
        if not self.__data:
            return None

        provinces = Spider._parseProvince(data=self.__data) if self.name != '中国' else Spider._parseProvince_china(
            data=self.__data)
        provinces = filter(lambda pro: pro.name in args, provinces) if args else provinces
        return list(provinces)

    def searchProvince_one(self, province: str):
        provinces = Spider._parseProvince(data=self.__data) if self.name != '中国' else Spider._parseProvince_china(
            data=self.__data)
        provinces = filter(lambda pro: pro.name == province, provinces)
        provinces = list(provinces)
        province: Province = provinces[0] if provinces else None
        return province

    def keys(self, drop=True):
        return Spider._dropNan(self).keys() if drop else Spider._dict(self).keys()

    def values(self, drop=True):
        return Spider._dropNan(self).values() if drop else Spider._dict(self).values()


# --------------------省份--------------------
class Province:
    __name__ = 'Province'

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.date = kwargs.get('date')
        self.nameMap = kwargs.get('nameMap')
        self.confirmAdd = kwargs.get('confirmAdd')
        self.confirmAddCut = kwargs.get('confirmAddCut')
        self.confirm = kwargs.get('confirm')
        self.nowConfirm = kwargs.get('nowConfirm')
        self.healRate = kwargs.get('healRate')
        self.deadRate = kwargs.get('deadRate')
        self.suspect = kwargs.get('suspect')
        self.dead = kwargs.get('dead')
        self.heal = kwargs.get('heal')
        self.__data = kwargs.get('children')  # 省份对应的城市

    def searchCity(self, *args):
        """
        搜索对应省份下的城市
        不指定城市获取所有城市
        :param args: 指定城市
        :return: list
        """
        if self.__data is None:
            raise error.WorldData(f'很抱歉, {self.name}, 并未开放城市数据')

        city = Spider._parseCity(data=self.__data, province=self.name)
        city = filter(lambda c: c.name in args, city) if args else city
        return list(city)

    def searchCity_one(self, city: str):
        if self.__data is None:
            raise error.WorldData(f'很抱歉, {self.name}, 并未开放城市数据')

        citys = Spider._parseCity(data=self.__data, province=self.name)
        citys = filter(lambda c: c.name == city, citys)
        citys = list(citys)
        city: City = citys[0] if citys else None
        return city

    def keys(self, drop=True):
        return Spider._dropNan(self).keys() if drop else Spider._dict(self).keys()

    def values(self, drop=True):
        return Spider._dropNan(self).values() if drop else Spider._dict(self).values()


# --------------------城市--------------------
class City:
    __name__ = 'City'

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.nowConfirm = kwargs.get('nowConfirm')
        self.confirm = kwargs.get('confirm')
        self.suspect = kwargs.get('suspect')
        self.dead = kwargs.get('dead')
        self.deadRate = kwargs.get('deadRate')
        self.showRate = kwargs.get('showRate')
        self.heal = kwargs.get('heal')
        self.healRate = kwargs.get('healRate')
        self.province = kwargs.get('province')

    def keys(self, drop=True):
        return Spider._dropNan(self).keys() if drop else Spider._dict(self).keys()

    def values(self, drop=True):
        return Spider._dropNan(self).values() if drop else Spider._dict(self).values()
