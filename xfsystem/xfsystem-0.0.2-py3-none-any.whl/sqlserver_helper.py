from pyspark.sql import DataFrame


def select_columns_from_pyspark_dataframe( dataframe: DataFrame, user_columns: list) -> DataFrame:    
    if len(user_columns) > 0:
        if not isinstance(user_columns, list):
            raise Exception("columns needs to be a valid python list(array), other data type was parsed")
        dataset_columns = list(dataset.columns)
        if not all(elem in dataset_columns  for elem in user_columns): 
            missing_elements = list(set(user_columns) - set(dataset_columns))
            raise Exception("Error : Following columns not in the table requested : " + str(missing_elements)) 
        else:
            return dataset.select(*user_columns)
    else:
        return dataframe


class SqlServer():
    def __init__(self, url:str, db_name:str, username:str, password:str, spark_sql_context):
        self.url = url
        self.username = username
        self.database = db_name
        self.password = password
        self.spark_sql_context = spark_sql_context
        self.connection_string = "jdbc:sqlserver://" + self.url + ";databaseName=" + self.database
        
    
    def get_table_dataframe(self, source_table:DataFrame ) -> DataFrame:
        dataset = self.spark_sql_context.read.format("jdbc") \
            .option("url", self.connection_string) \
            .option("dbtable", source_table) \
            .option("user", self.username) \
            .option("password", self.password) \
            .option("encrypt",True) \
            .option("trustServerCertificate",True) \
            .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
            .load()
        
        return dataset
    
    
    def append_dataframe_to_table(self, dataframe: DataFrame, destination_table: str):
        self.__write_dataframe_to_table(dataframe, destination_table, "append")
        
        
    def overwrite_dataframe_to_table(self, dataframe: DataFrame, destination_table: str):
        self.__write_dataframe_to_table(dataframe, destination_table, "overwrite")
    
    
    def __write_dataframe_to_table(self, dataframe: DataFrame, destination_table: str, write_mode: str):
        dataframe.write.mode(write_mode).format("jdbc") \
            .option("url", self.connection_string) \
            .option("dbtable", destination_table) \
            .option("user", self.username) \
            .option("password", self.password) \
            .option("encrypt",True) \
            .option("trustServerCertificate",True) \
            .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
            .save()

        #return True
