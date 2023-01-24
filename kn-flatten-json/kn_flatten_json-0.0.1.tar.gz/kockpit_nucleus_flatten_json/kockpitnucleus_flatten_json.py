from pyspark.sql.functions import *
from pyspark.sql.types import *
def kn_flatten_json(df,sep="_"):

    complex_fields = dict(
        [
            (field.name, field.dataType)
            for field in df.schema.fields
            if type(field.dataType) == ArrayType
            or type(field.dataType) == StructType
            or type(field.dataType) == MapType
        ]
    )
    while len(complex_fields) != 0:
        col_name = list(complex_fields.keys())[0]
        if type(complex_fields[col_name]) == StructType:
            expanded = [
                col(col_name + "." + k).alias(col_name + sep + k)
                for k in [n.name for n in complex_fields[col_name]]
            ]
            df = df.select("*", *expanded).drop(col_name)

        elif type(complex_fields[col_name]) == ArrayType:
            df = df.withColumn(col_name, explode_outer(col_name))
        elif type(complex_fields[col_name]) == MapType:
            keys_df = df.select(explode_outer(map_keys(col(col_name)))).distinct()
            keys = list(map(lambda row: row[0], keys_df.collect()))
            key_cols = list(
                map(
                    lambda f: col(col_name).getItem(f).alias(str(col_name + sep + f)),
                    keys,
                )
            )
            drop_column_list = [col_name]
            df = df.select(
                [
                    col_name
                    for col_name in df.columns
                    if col_name not in drop_column_list
                ]
                + key_cols
            )
        complex_fields = dict(
            [
                (field.name, field.dataType)
                for field in df.schema.fields
                if type(field.dataType) == ArrayType
                or type(field.dataType) == StructType
                or type(field.dataType) == MapType
            ]
        )

    return df
