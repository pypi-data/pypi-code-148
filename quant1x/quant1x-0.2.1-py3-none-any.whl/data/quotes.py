#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import os.path

import akshare as ak
import mootdx.utils.holiday as mooUtils
import pandas
from mootdx.quotes import Quotes
from tqdm import tqdm

from quant1x.data import *


class DataHandler:
    """
    数据
    """

    def __init__(self):
        """
        无参数构造函数
        """
        self.__root = os.path.expanduser(quant1x_home)
        self.__data_cn = os.path.expanduser(quant1x_data_cn)
        self.__data_hk = os.path.expanduser(quant1x_data_hk)
        self.__info_cn = os.path.expanduser(quant1x_info_cn)
        self.__info_hk = os.path.expanduser(quant1x_info_hk)

        # 根路径
        if not os.path.exists(self.__root):
            os.makedirs(self.__root)
        # 数据路径
        self.__path = os.path.expanduser(quant1x_data)
        if not os.path.exists(self.__data_cn):
            os.makedirs(self.__data_cn)
        if not os.path.exists(self.__data_hk):
            os.makedirs(self.__data_hk)
        # 咨询路径
        self.__info = os.path.expanduser(quant1x_info)
        if not os.path.exists(self.__info_cn):
            os.makedirs(self.__info_cn)
        if not os.path.exists(self.__info_hk):
            os.makedirs(self.__info_hk)

        self.__stock_list = {}
        # 自选股csv文件路径
        # 从自选股中获取证券代码列表
        # stock_list.columns = [
        #     "market",
        #     "code",
        #     "name",
        # ]
        zxg_csv = self.__path + '/zxg.csv'
        self.__stock_list = pandas.read_csv(zxg_csv)
        # print(self.__stock_list)

        # 标准市场
        self.__client = Quotes.factory(market='std', multithread=True, heartbeat=True)

    def __NotExistsToMake(self, path):
        """
        如果不存在则创建路径
        :param path:
        :return:
        """
        if not os.path.exists(path):
            os.makedirs(path)

    def apply(self, func_name: str, func) -> pandas.DataFrame:
        """
        自选股迭代
        :param func_name:
        :param func:
        :return:
        """
        total = len(self.__stock_list)
        print("自选股[%s]处理, 共计[%d]:" % (func_name, total))
        values = enumerate(self.__stock_list.values)
        pbar = tqdm(values, total=total)
        df = pandas.DataFrame()
        for key, value in pbar:
            # if key == 2:
            #     break

            code = value[1][2:]
            name = value[2]
            try:
                pbar.set_description_str("[%s]进行中" % code)
                s = func(code, name)
                # df = df.append(s, ignore_index=True)
                df1 = pandas.DataFrame([s])
                df = pandas.concat([df, df1], ignore_index=True)
            except ValueError:
                pass
            finally:
                pbar.set_description_str("[%s]完成" % code)
        pbar.close()
        print("自选股[%s], 处理完成." % func_name)
        return df

    def holiday(self, dt: datetime):
        """
        判断datetime是否假日
        :param dt:
        :return:
        """
        # date = dt.fromtimestamp("%Y-%m-%d")
        date = dt.strftime("%Y-%m-%d")
        return mooUtils.holiday(date)

    def __kline_cn(self, code):
        """
        获取全量历史K线数据
        """
        symbol = code[-6:]
        data = ak.stock_zh_a_hist(symbol=symbol, period="daily", adjust="qfq")
        return data

    def update_history(self):
        """
        更新全量历史数据
        :return:
        """
        total = len(self.__stock_list)
        print("自选股历史K线数据, 共计[%d]:" % total)
        values = enumerate(self.__stock_list.values)
        pbar = tqdm(values, total=total)
        for key, value in pbar:
            # print('key:', key, ', value: ', value)
            code = value[1][2:]
            # print("code:%s" % code)
            pbar.set_description_str("同步[%s]进行中" % code)
            data = self.__kline_cn(code)
            data.to_csv(self.__data_cn + '/' + code + '.csv', index=False)
            pbar.set_description_str("同步[%s]完成" % code)

        pbar.close()
        print("自选股历史K线数据, 处理完成.\n")

    def dataset(self, code) -> pandas.DataFrame:
        """
        读取历史数据
        :param code:
        :return:
        """
        filename = self.__data_cn + '/' + code + '.csv'
        if not os.path.exists(filename):
            data = self.__kline_cn(code)
            data.to_csv(self.__data_cn + '/' + code + '.csv', index=False)
        df = pandas.read_csv(filename)
        # 选择列, 是为了改变表头
        df = df[["日期", "开盘", "收盘", "最高", "最低", "成交量", "成交额"]]
        # 变更表头
        df.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount']
        # 更正排序
        df['date'] = pandas.to_datetime(df['date'])
        #df.set_index('date', inplace=True)

        return df

    def __finance(self, code):
        """
        获取个股基本信息
        :param code:
        :return:
        """
        symbol = code[-6:]
        data = self.__client.finance(symbol=symbol)
        return data

    def update_info(self):
        """
        更新全量个股信息
        :return:
        """

        total = len(self.__stock_list)
        print("自选股基本面信息, 共计[%d]:" % total)
        values = enumerate(self.__stock_list.values)
        pbar = tqdm(values, total=total)
        for key, value in pbar:
            # print('key:', key, ', value: ', value)
            code = value[1][2:]
            # print("code:%s" % code)
            pbar.set_description_str("同步[%s]进行中" % code)
            data = self.__finance(code=code)
            data.to_csv(self.__info_cn + '/' + code + '.csv', index=False)
            pbar.set_description_str("同步[%s]完成" % code)

        pbar.close()
        print("自选股基本面信息, 处理完成.\n")

    def finance(self, code):
        """
        读取本地基本面
        :param code:
        :return:
        """
        filename = self.__info_cn + '/' + code + '.csv'
        if not os.path.exists(filename):
            return
        df = pandas.read_csv(filename)
        return df
