import csv

from loguru import logger
from sqlalchemy import create_engine, text

from . import utils


class Database(object):

    engine = create_engine('sqlite://')

    def __init__(self, engine_url, engine_options=None):
        '''Initiation'''
        if utils.vTrue(engine_options, dict):
            self.engine = create_engine(engine_url, **engine_options)
        else:
            self.engine = create_engine(engine_url)

    def initializer(self):
        '''ensure the parent proc's database connections are not touched in the new connection pool'''
        self.engine.dispose(close=False)

    def connect_test(self):
        info = '数据库连接测试'
        try:
            logger.info(f'{info}......')
            self.engine.connect()
            logger.success(f'{info}[成功]')
            return True
        except Exception as e:
            logger.error(f'{info}[失败]')
            logger.error(e)
            return False

    def metadata_create_all(self, base, init=None):
        info = '初始化所有表'
        try:
            logger.info(f'{info}......')
            if init == True:
                base.metadata.drop_all(self.engine)
            base.metadata.create_all(self.engine)
            logger.success(f'{info}[成功]')
            return True
        except Exception as e:
            logger.error(f'{info}[失败]')
            logger.error(e)
            return False

    # 私有函数, 保存 execute 的结果到 CSV 文件
    def _result_save(self, file, data):
        try:
            outcsv = csv.writer(file)
            outcsv.writerow(data.keys())
            outcsv.writerows(data)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def execute(self, sql=None, sql_file=None, sql_file_kwargs=None, csv_file=None, csv_file_kwargs=None):

        info_prefix = '[执行SQL]'

        # ------------------------------------------------------------

        # 提取 SQL
        # 如果 sql 和 sql_file 同时存在, 优先执行 sql
        sql_object = None
        info = f'{info_prefix}提取SQL'
        try:
            logger.info(f'{info}......')
            if utils.vTrue(sql, str):
                sql_object = sql
            elif utils.vTrue(sql_file, str):
                # 判断文件是否存在
                if utils.stat(sql_file, 'file') == False:
                    logger.error(f'文件不存在: {sql_file}')
                    return False
                # 读取文件内容
                if utils.vTrue(sql_file_kwargs, dict):
                    with open(sql_file, 'r', **sql_file_kwargs) as _file:
                        sql_object = _file.read()
                else:
                    with open(sql_file, 'r') as _file:
                        sql_object = _file.read()
            else:
                logger.error(f'{info}[失败]')
                logger.error(f'{info_prefix}SQL 或 SQL文件 错误')
                return False
            logger.success(f'{info}[成功]')
        except Exception as e:
            logger.error(f'{info}[失败]')
            logger.error(e)
            return False

        # ------------------------------------------------------------

        # 执行 SQL
        info = f'{info_prefix}执行SQL'
        try:
            logger.info(f'{info}......')
            with self.engine.connect() as connect:
                # 执行SQL
                result = connect.execute(text(sql_object))
                if csv_file == None:
                    # 如果 csv_file 没有定义, 则直接返回结果
                    logger.success(f'{info}[成功]')
                    return result
                else:
                    # 如果 csv_file 有定义, 则保存结果到 csv_file
                    info_of_save = f'{info_prefix}保存结果到文件: {csv_file}'
                    logger.info(f'{info_of_save} .......')
                    # 保存结果
                    if utils.vTrue(csv_file_kwargs, dict):
                        with open(csv_file, 'w', **csv_file_kwargs) as _file:
                            result_of_save = self._result_save(_file, result)
                    else:
                        with open(csv_file, 'w') as _file:
                            result_of_save = self._result_save(_file, result)
                    # 检查保存结果
                    if result_of_save == True:
                        logger.success(f'{info_of_save} [成功]')
                        logger.success(f'{info}[成功]')
                        return True
                    else:
                        logger.error(f'{info_of_save} [失败]')
                        logger.error(f'{info}[失败]')
                        return False
        except Exception as e:
            logger.error(f'{info}[失败]')
            logger.error(e)
            return False

    def insert_one(self, table, field, data):
        info = '插入数据'
        try:
            logger.info(f'{info}......')
            with self.engine.connect() as connection:
                connection.execute(f'''INSERT INTO {table} ({field}) VALUES ({data})''')
                logger.success(f'{info}[成功]')
                return True
        except Exception as e:
            logger.error(f'{info}[失败]')
            logger.error(e)
            return False
