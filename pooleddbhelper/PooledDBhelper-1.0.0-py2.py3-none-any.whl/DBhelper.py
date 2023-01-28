# -*- encoding: utf-8 -*-
"""
@Author  : cy1
@File    : PooledDBhelper.py
@Time    : 2023/1/28 14:48
@email   : 13777808792@163.com
@Software: PyCharm
"""

import pymysql
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB


class PooledDBhelper:
    def __init__(self, dbconfig: {}):
        '''
        :param dbconfig: {
            'host': '192.168.0.1',
            'user': 'username',
            'password': 'password',
            'port': 3306,
            'db': 'db_name'
        }
        '''
        self.pool = self.connectionPool(dbconfig)

    def connectionPool(self, dbconfig):
        try:
            pool = PooledDB(
                creator=pymysql,
                maxconnections=10,  # 连接池允许的最大连接数，0和None表示不限制连接数
                mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
                blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                host=dbconfig['host'],
                user=dbconfig['user'],
                passwd=dbconfig['password'],
                db=dbconfig['db'],
                cursorclass=DictCursor
            )
            return pool
        except Exception as e:
            raise Exception("数据库链接失败(create connect failed):{}".format(e))

    def insert_many(self, many_data, table_name):
        '''
        :param [{"k1":"v1","k2":"v2"},{"k1":"v3","k2":"v4"}]:
        :param table_name:
        :return: affected_rows
        '''
        values = [tuple(i.values()) for i in many_data]
        keys = list(many_data[-1].keys())
        sql_1 = "insert into `{}`(`{}`) values({})".format(table_name, '`,`'.join(many_data[-1].keys()),
                                                           ','.join([''.join('%s') for _ in keys]))
        try:
            with self.pool.connection() as conn:
                with conn.cursor() as cursor:
                    row_number = cursor.executemany(sql_1, values)
                    conn.commit()
            return "Successful affected_rows: {}".format(row_number)
        except Exception as e:
            conn.rollback()
            return "ERROR:{}".format(e)

    def task(self, sql, *args):
        '''
        fetchall
        :param sql:
        :param args:
        :return:
        '''
        conn = self.pool.connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql, args)
            data = cursor.fetchall()
        except Exception as e:
            raise ("SQL execution failure", e)
        else:
            return data
        finally:
            cursor.close()
            conn.close()

    def fetchone(self, sql):
        with self.pool.connection() as connection:
            connection.autocommit = True
            with connection.cursor() as cursor:
                '''
                在创建连接的时候，增加参数 autocommit = 1 ，当发生update等操作时，会实时更新到数据库内。避免 conn.commit() 来提交到数据库
                如果没有设置自动提交，也没有手动提交，当进行插入或更新等操作时，只在本地客户端能看到更新，在其他客户端或数据库内，数据无变化。
                适合实时操作，随时少量、频繁的更新'''
                row=cursor.execute(sql)
                result = cursor.fetchone()
                connection.commit()
        return result


if __name__ == "__main__":
    # pool=PooledDBhelper({
    #     'host': '192.168.0.1',
    #     'user': 'username',
    #     'password': 'password',
    #     'port': 3306,
    #     'db': 'db_name'
    # })

    # data_list= [{"name":'a', 'info':'1'}, {"name":'b', 'info':'2'},{"name":'none', 'info':'3'}]
    # rows=pool.insert_many(data_list,"cy_self_test")
    # print(rows)

    # result_list=pool.task("select * from cy_self_test")
    # print(result_list)

    # query = "insert into `cy_self_test`({}) values {}".format("`name`,`info`", ("cy","world"))
    # pool.fetchone(query)

    # query="select  * from cy_self_test where id=1"
    # result=pool.fetchone(query)
    # print(result)

    pass