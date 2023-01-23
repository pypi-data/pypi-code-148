from violetSpider.core.model import *

__version__ = '1.1.3'

# 返回世界数据
def find_world():
    return Spider._spider_world()


# 返回中国数据
def find_china():
    return Spider._spider_china()


# 清理对象中的缺失值, 并返回一个字典
def drop_nan(obj: object):
    return Spider._dropNan(obj)


# 将对象转化为一个完整的字典, 注意该方法不会去除空值
def to_dict(obj: object):
    return Spider._dict(obj)


# 将数据插入mysql
def save_mysql(
    username: str,
    password: str,
    host: str,
    port: int,
    databases: str,
    data: list,  # 要存入的数据
    table=None,  # 是否指定表
    fields=None,  # 指定保存的字段
    drop=True  # 只要有一个字段的值为空, 那么便不保存这个字段
):
    Save(**locals())._saveMysql()


# 将数据存入csv当中
def save_csv(
    path: str,
    data: list,
    fields=None,
    drop=True
):
    Save(**locals())._saveCSV()