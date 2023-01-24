#import requests
#import json
import pandas as pd
from pyspark.sql.types import *
import os
from pyspark.sql import DataFrame

class PandasToPyspark:
    def __init__(self, pandas_df, sql_context):
        self.pandas_dataframe = pandas_df
        self.pandas_dataframe_columns = list(self.pandas_dataframe.columns)
        self.pandas_dataframe_datatypes = list(self.pandas_dataframe.dtypes)
        self.sql_context = sql_context
        

    def equivalent_type(self, f):
        if f == 'datetime64[ns]':
            return TimestampType()
        elif f == 'int64':
            return LongType()
        elif f == 'int32':
            return IntegerType()
        elif f == 'float64':
            return DoubleType()
        elif f == 'float32':
            return FloatType()
        else:
            return StringType()

    def define_structure(self, string, format_type):
        try:
            typo = self.equivalent_type(self.format_type)
        except:
            typo = StringType()
        return StructField(string, typo)

    def pandas_to_pyspark(self) -> DataFrame:
        columns = self.pandas_dataframe_columns
        types = self.pandas_dataframe_datatypes
        struct_list = []
        for column, typo in zip(columns, types):
            struct_list.append(self.define_structure(column, typo))
        p_schema = StructType(struct_list)
        return self.sql_context.createDataFrame(self.pandas_dataframe, p_schema)
