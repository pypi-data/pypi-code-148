from delta import DeltaTable
from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession
from typing import Callable

class Table:

    spark: SparkSession
    definition: [(str, str, str, str)] = []
    wh_name: str
    tbl_name: str
    wh_tbl_name: str

    table: Callable[[], DataFrame] = Method_Descriptor()

    def __init__(self, spark, wh_name):
        self.spark = spark
        self.wh_name = wh_name
        self.tbl_name = self.__class__.__name__.split('_')[0]
        self.wh_tbl_name = f'{self.wh_name}.{self.tbl_name}'

    def _get_table(self) -> DataFrame:
        return self.spark.table(self.wh_tbl_name)

    def create_table(self) -> None:
        dt = DeltaTable.createIfNotExists(self.spark).tableName(self.wh_tbl_name)
        for c in self.definition:
            dt.addColumn(*c[:-1], comment=c[-1])
        dt.execute()

    def drop_table(self) -> None:
        self.spark.sql(f'DROP TABLE IF EXISTS {self.wh_tbl_name}')

    def create_view(self) -> None:
        self.table().createOrReplaceTempView(self.tbl_name)

    def purge_table(self) -> None:
        self.spark.sql(f'DELETE FROM {self.wh_tbl_name} WHERE 1=1')
        DeltaTable.forName(self.spark, self.wh_tbl_name).vacuum()

    def set_table(self) -> None:
        self.table = self._get_table
