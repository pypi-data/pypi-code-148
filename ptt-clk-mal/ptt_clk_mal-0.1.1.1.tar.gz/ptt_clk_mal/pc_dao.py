"""
Description: 
Author: MALossov
Date: 2023-01-27 16:51:30
LastEditTime: 2023-01-27 16:57:35
LastEditors: MALossov
Reference: 
"""
import sqlite3
from typing import Any
import os

db_name = os.path.dirname(os.path.abspath(__file__))+"/static/potatoclock.db"


def create_table():
    # 如果当前文件夹下没有potatoclock.db,就创建一个
    conn = sqlite3.connect(db_name)
    # 创建一个游标
    c = conn.cursor()
    # 执行sql语句,创建一个表
    c.execute(
        """CREATE TABLE IF NOT EXISTS pttClk
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    aim TEXT,
                    period INTEGER)"""
    )
    # 提交事务
    conn.commit()
    # 关闭连接
    conn.close()


def insert_potato(pttperiod, pttaim, pttdate):
    # 如果当前文件夹下没有potatoclock.db,就创建一个
    conn = sqlite3.connect(db_name)
    # 创建一个游标
    c = conn.cursor()
    c.execute(
        """INSERT INTO pttClk (period,aim,date)
                    VALUES (?,?,?)""",
        (pttperiod, pttaim, pttdate),
    )
    # 提交事务
    conn.commit()
    # 关闭连接
    conn.close()


def query_factory(sql: str) -> object:
    """

    :rtype: object
    """
    # 如果当前文件夹下没有potatoclock.db,就创建一个
    conn = sqlite3.connect(db_name)
    # 创建一个游标
    c = conn.cursor()
    c.execute(sql)
    # 提交事务
    conn.commit()
    # 关闭连接
    data: list[Any] = c.fetchall()
    conn.close()
    return data


def query_potato():
    return query_factory("""SELECT * FROM pttClk ORDER BY date DESC""")


def query_by_groups(groups: list):
    # merge list into SQL DML string in 'or', which column is 'aim'
    return query_factory(
        "SELECT * FROM pttClk WHERE aim = '"
        + "' or aim = '".join(groups)
        + "' ORDER BY date DESC"
    )


def query_last_xdays(x: int):
    return query_factory(
        """SELECT * FROM pttClk WHERE date > date('now','-{} day') ORDER BY date DESC""".format(
            x
        )
    )


def query_xdays_and_groups(x: int, groups: list):
    return query_factory(
        """SELECT * FROM pttClk WHERE date > date('now','-{} day') AND (aim = '{}""".format(
            x, "' or aim = '".join(groups)
        )
        + "') ORDER BY date DESC"
    )


def clean_table():
    conn = sqlite3.connect(db_name)
    # 创建一个游标
    c = conn.cursor()
    c.execute("""DELETE FROM pttClk WHERE TRUE""")
    # 提交事务
    conn.commit()
    # 关闭连接
    conn.close()


if __name__ == "__main__":
    create_table()
    print("Aborted!")
