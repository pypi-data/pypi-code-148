from pyspark.sql.session import SparkSession
from datetime import date
from .pt_raw import PTRaw

class Guide:

    spark: SparkSession
    mth: int
    pt_raw: PTRaw

    def __init__(self, mth=None):
        """

        :param mth: INT identifying which month the guide is set
        """
        self.spark = SparkSession.builder.getOrCreate()
        self.mth = mth if mth is not None else int(date.today().strftime('%Y%m'))
        self.pt_raw = PTRaw()
