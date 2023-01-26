from pyspark.sql.session import SparkSession
import os
from datetime import date
from pyspark.sql.functions import col, lit
from pyspark.sql import functions as F
from pyspark.sql import DataFrame


class PTRaw:

    in_network_files: DataFrame
    in_network_meta: DataFrame

    def __init__(self, mth: int = None, location_uri=None, spark=None):
        """
        Meta is a class that consolidates all pt_raw metadata.
        Note: currently this class assumes hive_metastore is used
        """
        self.spark = spark if spark is not None else SparkSession.builder.getOrCreate()
        self.name = "pt_raw"
        self.locationUri = location_uri if location_uri is not None else self.get_locationUri()
        self.mth = mth if mth is not None else int(date.today().strftime('%Y%m'))
        self.set_files()
        self.set_metas()

    def get_locationUri(self):
        """
        We want to always get location Uri from the catalog so that we don't risk use of a custom location
        For now we will only accepts pt_raw as the raw database name
        """
        database = [d for d in self.spark.catalog.listDatabases() if d.name == "pt_raw"]
        if len(database) == 0:
            print(f'WARNING: {self.name} database does not exist. Run PTRaw.create_raw_database().')
            location_uri = None
        else:
            location_uri = database[0].locationUri
        return location_uri

    def create_raw_database(self):
        # TODO: check if database already exists
        if self.locationUri is None:
            self.spark.sql(f'CREATE DATABASE IF NOT EXISTS {self.name}')
        else:
            self.spark.sql(f'CREATE DATABASE IF NOT EXISTS {self.name} LOCATION {self.locationUri}')
        self.locationUri = self.get_locationUri()

    def create_raw_directory(self):
        """
        The raw directory is required for a location to put raw files. Since it will not be a table,
        we will provide it with a _ prefix to avoid potential managed table conflicts
        Currently this path is not argumented.
        Currently this path generation is done only by local fs os operations to avoid dependency on dbutils.
        """
        path = self.locationUri.replace('dbfs:', '/dbfs') + '/_raw'
        if os.path.exists(path):
            print(f'{path} already exists.')
        else:
            os.mkdir(path)
            print(f'{path} created.')

    def create_raw_mth_directory(self):
        """
        This will simply create a new month with sub directories to put more files.
        This will eventually satisfy all schema, but for now, will only create partition for in_network files
        """
        path = self.locationUri.replace('dbfs:', '/dbfs') + f'/_raw/mth={self.mth}'
        if os.path.exists(path):
            print(f'{path} already exists.')
        else:
            os.mkdir(path)
            print(f'{path} created.')
            os.mkdir(path + '/schema=in_network')
            print(f'{path}/schema=in_network created.')
        pass

    def set_files(self):
        """
        Files will be real time definition of files in the raw directory.
        This is intended to help with the state of ingest.
        """
        files = self.spark.read.format("binaryFile") \
            .option("pathGlobFilter", "*.json") \
            .load(self.locationUri + '/_raw') \
            .filter(col('mth') == lit(self.mth)) \
            .drop('content')

        self.in_network_files = files.filter(F.col('schema') == lit("in_network")) \
            .select(col('mth'),
                    col('schema'),
                    F.element_at(F.split(col('path'), '/'), -1).alias('file'),
                    col('length'),
                    col('modificationTime'))

    def set_metas(self):
        """
        meta delta tables will be
        """
        in_network_header = self.spark.table('pt_stage.inr_header') \
            .groupBy(col('file_name')) \
            .agg(F.first(col('reporting_entity_name'), ignorenulls=True).alias('reporting_entity_name'),
                 F.first(col('last_updated_on'), ignorenulls=True).alias('last_updated_on'))

        self.in_network_meta = self.in_network_files.alias('files') \
            .join(in_network_header.alias('header'),
                  col('file') == col('file_name'), 'left') \
            .select(col('files.*'),
                    F.when(col('header.file_name').isNotNull(), lit(True)).otherwise(lit(False)).alias('ingested'),
                    col('reporting_entity_name'),
                    col('last_updated_on'))
