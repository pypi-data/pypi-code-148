from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession
from delta.tables import DeltaTable
from pyspark.sql.types import StructType, DateType
from pyspark.sql.functions import col, lit, from_json, explode


class TableStreamTgt:

    spark: SparkSession
    definition: [(str, DateType, bool, str)] = []
    df: DataFrame
    table: DeltaTable
    header_key: str = ""

    def __init__(self, spark):
        self.spark: SparkSession = spark
        self.tbl_name = self.__class__.__name__.split('_')[0]
        self.wh_tbl_name = '.'.join('pt_stage', self.tbl_name)

    def get_df(self) -> DataFrame:
        return self.spark.table(self.wh_tbl_name)

    def get_table(self) -> DeltaTable:
        return DeltaTable.forName(self.spark, self.wh_tbl_name)

    def get_json_schema(self) -> StructType:
        schema = StructType()
        for kv in [{'field': argv[0], 'data_type': argv[1], 'nullable': argv[2]} for argv in self.definition
                   if argv[0] not in ['file_name', 'batch_id']]:
            schema.add(**kv)
        return schema

    def get_batch_merge_function(self) -> object:
        header_key = self.header_key
        schema = self.get_json_schema()
        table_tgt = self.get_table()

        def merge_function(df: DataFrame, batch_id: int):
            src = df.filter(col('header_key') == lit(header_key)) \
                    .select(col('file_name'),
                            explode(col('json_payload')).alias('json_exploded')) \
                    .select(col('file_name'),
                            from_json(col('json_exploded'), schema).alias('exploded_struct')) \
                    .select(col('file_name'),
                            lit(batch_id).alias('batch_id'),
                            col('exploded_struct.*')).alias('src')
            table_tgt.merge(src, "1 != 1") \
                     .whenNotMatchedInsertAll() \
                     .execute()
        return merge_function

    def create_table(self) -> None:
        dt = DeltaTable.createIfNotExists(self.spark).tableName(self.wh_tbl_name)
        for c in self.definition:
            dt.addColumn(*c[:-1], comment=c[-1])
        dt.execute()

    def drop_table(self) -> None:
        self.spark.sql(f'DROP TABLE IF EXISTS {self.wh_tbl_name}')

    def create_view(self) -> None:
        self.df.createOrReplaceTempView(self.tbl_name)

    def purge_table(self) -> None:
        self.spark.sql(f'DELETE FROM {self.wh_tbl_name} WHERE 1=1')
        DeltaTable.forName(self.spark, self.wh_tbl_name).vacuum()

    def set_table(self) -> None:
        self.table = self.get_table()

    def set_df(self) -> None:
        self.df = self.get_df()