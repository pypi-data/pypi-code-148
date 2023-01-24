import json
from hdbcli import dbapi
import datetime
from .logger import Logger
from pkg_resources import resource_stream



class DbConnection:

    def __init__(self, package_name=None,url=None):
        self.logger = Logger.get_instance()
        if package_name is not None:
            try:
                self.config = json.load(resource_stream(package_name, 'config.json'))
            except Exception as e:
                self.logger.error('Error loading config.json in package: %s', e)
                raise
        else:
            if url is None:
                url = 'config.json'
            try:
                with open(url, 'r') as f:
                    self.config = json.load(f)
            except Exception as e:
                self.logger.error("Unable to load the config.json from the url '{}'".format(url))
                self.logger.error(e)
                raise
        self.connection = self._get_connection()
        self.cursor = None

    def _get_connection(self):

        #optional arguments
        if "encrypt" not in self.config:
            self.config["encrypt"] = "true"
        if "sslValidateCertificate" not in self.config:
            self.config["sslValidateCertificate"] = "false"
        if "disableCloudRedirect" not in self.config:
            self.config["disableCloudRedirect"] = "true"
        if "communicationTimeout" not in self.config:
            self.config["communicationTimeout"] = "0"
        if "autocommit" not in self.config:
            self.config["autocommit"] = "true"
        if "sslUseDefaultTrustStore" not in self.config:
            self.config["sslUseDefaultTrustStore"] = "true"

        return dbapi.connect(
            address=self.config["address"],
            port=self.config["port"],
            user=self.config["user"],
            password=self.config["password"],
            schema=self.config["schema"],
            encrypt=self.config["encrypt"],
            sslValidateCertificate=self.config["sslValidateCertificate"],
            disableCloudRedirect=self.config["disableCloudRedirect"],
            communicationTimeout=self.config["communicationTimeout"],
            autocommit=self.config["autocommit"],
            sslUseDefaultTrustStore=self.config["sslUseDefaultTrustStore"]
        )

    # def _commit(self):
    #     self.connection.commit()

    # def _close(self):
    #     self.connection.close()

    # def _rollback(self):
    #     self.connection.rollback()

    # def _get_cursor(self):
    #     if self.connection.isconnected():
    #         self.cursor = self.connection.cursor()
    #     else:
    #         raise Exception("Failed to get cursor")

    def get_schema_views(self):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        try:
            query = "SELECT %s, %s  FROM %s WHERE %s = '%s' " % ("VIEW_NAME", "VIEW_TYPE", "VIEWS", "SCHEMA_NAME", self.config['schema'])  
            cursor.execute(query)
            res = cursor.fetchall()
            column_headers = [i[0] for i in cursor.description]
        except Exception as e:
            self.logger.error('error occured during query %s', e)
            self.connection.rollback()
        return  res, column_headers

    def get_table_size(self, table_name):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            # raise connectionError('Database is not connected')
            self._get_connection()
            cursor = self.connection.cursor()
        schema = self.config['schema']
        sqlQuery = f'SELECT COUNT(*) FROM "{schema}"."{table_name}"'
        try:
            cursor.execute(sqlQuery)
            res = cursor.fetchall()
            return res
        except Exception as e:
            self.logger.error('error occured during update, doing rollback %s', e)
            self.connection.rollback()

    def get_data_with_headers(self, table_name, size=1):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        rows = self.get_table_size(table_name)
        dataset_size = int(rows[0][0]*size)
        schema = self.config['schema']
        sqlQuery = f'SELECT TOP {str(dataset_size)} * FROM "{schema}"."{table_name}"'
        try:
            cursor.execute(sqlQuery)
            res = cursor.fetchall()
            column_headers = [i[0] for i in cursor.description]
            return res, column_headers
        except Exception as e:
            self.logger.error('error occured during update, doing rollback. %s', e)
            self.connection.rollback()
    
    def execute_query(self, query):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            res = cursor.fetchall()
            column_headers = [i[0] for i in cursor.description]
            return res, column_headers
        except Exception as e:
            self.logger.error('error occured during update, doing rollback %s', e)
            self.connection.rollback()

    def create_table(self, query):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        try:
            if 'INSERTED_AT' in query:
                raise Exception('\nQuery Error: A column name provided was a duplicate of the automatically added INSERTED_AT timestamp column.\nPlease refer to documentation on more information about this generated column and/or change the name of the duplicated column provided in the query.')
            timestamp_column = ', INSERTED_AT TIMESTAMP NOT NULL'
            query = query[:-1] + timestamp_column + ')'
            self.logger.info("creating table...")
            self.logger.info(query)
            cursor.execute(query)
            if self.connection.getautocommit() == False:
                self.connection.commit()
        except Exception as e:
            self.logger.error('error occured during update, doing rollback %s', e)
            self.connection.rollback()

    def drop_table(self, table_name):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        try:
            query = 'DROP TABLE ' + table_name
            self.logger.info("deleting table...")
            cursor.execute(query)
            if self.connection.getautocommit() == False:
                self.connection.commit()
        except Exception as e:
            self.logger.error('error occured during update, doing rollback %s', e)
            self.connection.rollback()
            
#     def insert_row_into_table(self, table_name, table_values):
#         if (self.connection.isconnected()):
#             cursor = self.connection.cursor()
#         else:
#             self._get_connection()
#             cursor = self.connection.cursor()
#         try:
#             self.logger.info('inserting into table...')
#             column_names = ", ".join(list(table_values.keys()))
#             column_values = str(list(table_values.values()))[1:-1]
#             query = 'INSERT INTO %s (%s) VALUES (%s)' % (table_name,column_names,column_values)
#             cursor.execute(query)
#         except Exception as e:
#             self.logger.info('error occured during update, doing rollback', e)
#             self.connection.rollback()
            
    def insert_into_table(self, table_name, table_values):
        if (self.connection.isconnected()):
            cursor = self.connection.cursor()
        else:
            self._get_connection()
            cursor = self.connection.cursor()
        try:
            self.logger.info('inserting into table...')
            column_names = ', '.join(list(table_values.columns))
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            bound_values = column_names.replace(', ', ', ' + ':')
            bound_values = ':' + bound_values + ', :INSERTED_AT'
            sql = 'INSERT INTO ' + table_name + ' (' + column_names + ', INSERTED_AT) VALUES (' + bound_values + ')'
            self.logger.info(sql)
            for index, row in table_values.iterrows():
                temp_dict = row.to_dict()
                temp_dict['INSERTED_AT'] = timestamp
                cursor.execute(sql, temp_dict)
            if self.connection.getautocommit() == False:
                self.connection.commit()
        except Exception as e:
            self.logger.error('error occured during update, doing rollback %s', e)
            self.connection.rollback()