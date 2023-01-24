from pyspark.sql import DataFrame
from pyspark.sql.functions import col, array, explode, lit, struct, udf
from pyspark.sql.types import StringType
from typing import Iterable


def rename_multiple_columns(dataframe : DataFrame, column_names: dict ) -> DataFrame:
    for key, value in column_names.items():
        dataframe = dataframe.withColumnRenamed(key, value)
    return dataframe


def transform_dataframe_melt(dataframe, columns_to_melt: Iterable[str], columns_to_transform: Iterable[str],
                             old_column_name: str = "variable", new_column_name: str = "value") -> DataFrame:
    vars_and_vals = array(*(
        struct(lit(c).alias(old_column_name), col(c).alias(new_column_name))
        for c in columns_to_transform))

    df_tmp = dataframe.withColumn("_vars_and_vals", explode(vars_and_vals))

    cols = columns_to_melt + [col("_vars_and_vals")[x].alias(x) for x in [old_column_name, new_column_name]]
    return df_tmp.select(*cols)


def replace_value(column : str, old_value, new_value) -> DataFrame:
    return when(column != old_value, column).otherwise(lit(new_value))


def replace_column_value(dataframe:DataFrame, column : str, old_value, new_value ) -> DataFrame:
    dataframe = dataframe.withColumn(column, replace_value(col(column), old_value, new_value))
    return dataframe