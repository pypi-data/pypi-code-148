from pyspark.sql import SparkSession
import findspark

findspark.init()

postgres_driver_file_path = "drivers/postgresql-42.4.0.jar"
sql_driver_file_path = "drivers/mssql-jdbc-10.2.1.jre8.jar"


"""
import os
post_path = os.getcwd() + postgres_driver_file_path
print("************")
print("post :", post_path)
print("************")
"""

def get_spark_postgres_conf():
    return SparkSession \
        .builder \
        .master('local') \
        .appName('mamba-postgres') \
        .config("spark.driver.extraClassPath", postgres_driver_file_path) \
        .config("spark.sql.debug.maxToStringFields", 255) \
        .config("spark.ui.port", "4060") \
        .config('spark.sql.codegen.wholeStage', 'false') \
        .getOrCreate()


def get_spark_sql_conf():
    return SparkSession \
        .builder \
        .master('local') \
        .appName('mamba') \
        .config("spark.driver.extraClassPath", sql_driver_file_path) \
        .config('spark.sql.codegen.wholeStage', 'false') \
        .enableHiveSupport() \
        .getOrCreate()

