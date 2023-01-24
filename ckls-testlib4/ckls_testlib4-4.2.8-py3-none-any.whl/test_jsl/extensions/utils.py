import os
from pyspark.sql import SparkSession





from test_jsl.util import SparkContextForTest



def get_spark_session():

    return SparkContextForTest.spark



