import logging
logging.basicConfig(level=logging.INFO)

import sys
import pathlib
import boto3
import pandas
import uuid

class DataLake():
    """
    Data Lake Utils
    This class instanciates an object to handle read/write operations on an 
    specific bucket on Amazon S3 working as a Data Lake, with folders splitted
    into the following hierarchy:
    - schema/
        - table/
            - partition[0]/
                - partition[1]/
                    ...
                        - partition[n]/
                            - object
    .
    """

    def __init__(self, bucket_name: str, schema: str, table: str, partitions: list, profile_name: str = None):
        """
        Constructor method

        :bucket_name: name of Amazon S3 bucket
        :schema: name of schema
        :table: name of table
        :partitions: list of key/value pairs of partitions to be used
        :profile_name: name of AWS Credentials profile to be used
        :return: void
        """
        if profile_name is None:
            self.session = boto3.Session()
        else:
            self.session = boto3.Session(profile_name=profile_name)

        self.bucket_name = bucket_name
        self.schema = schema
        self.table = table
        self.partitions = partitions
        self.object_name_prefix = self.__concat_object_name_prefix()

    def __concat_object_name_prefix(self):
        object_partitions = "/".join("{partition}={value}".format(
            partition=partition["key"],
            value=partition["value"]
        ) for partition in self.partitions
        )
        object_name_prefix = "{schema}/{table}/{object_partitions}/".format(
            schema=self.schema,
            table=self.table,
            object_partitions=object_partitions
        )
        # Object name returned already has a slash '/' at the end of string
        return object_name_prefix

    def append_to_s3(self, data: pandas.DataFrame, file_format: str):
        if data is not None:
            logging.info("INSERTING DATA INTO S3...")
            if file_format == "json":
                object_name = self.object_name_prefix + \
                    str(uuid.uuid1()) + ".json.gz"
                data.to_json(
                    path_or_buf="s3://{bucket_name}/{object_name}".format(
                        bucket_name=self.bucket_name,
                        object_name=object_name,
                    ),
                    orient="records",
                    lines=True,
                    compression="gzip",
                )
            elif file_format == "parquet":
                object_name = self.object_name_prefix + \
                    str(uuid.uuid1()) + ".parquet.gz"
                data.to_parquet(
                    path="s3://{bucket_name}/{object_name}".format(
                        bucket_name=self.bucket_name,
                        object_name=object_name,
                    ),
                    compression='gzip',
                )
            else:
                logging.error("FILE FORMAT {file_format} NOT SUPPORTED".format(
                    file_format=str.upper(file_format)
                ))
                sys.exit(1)

            insert_count = len(data)
            logging.info("{0} RECORDS INSERTED INTO S3".format(insert_count))
            logging.info("(+) {0}".format(object_name))
        else:
            logging.info("NO DATA TO BE INSERTED")

    def delete_from_s3(self):
        logging.info("DELETING DATA FROM S3 IF EXISTS...")
        objects_to_delete = {'Objects': []}
        try:
            s3 = self.session.client('s3')
            objects = s3.list_objects(
                Bucket=self.bucket_name,
                Prefix=self.object_name_prefix)
        except:
            raise
        else:
            if objects.get('Contents') is not None:
                objects_to_delete['Objects'] = [{'Key': k} for k in [
                    obj['Key'] for obj in objects.get('Contents', [])]]
                s3.delete_objects(
                    Bucket=self.bucket_name,
                    Delete=objects_to_delete)

                delete_count = len(objects_to_delete["Objects"])
                logging.info("{0} FILES DELETED FROM S3".format(delete_count))

                for item in objects_to_delete["Objects"]:
                    logging.info("(-) {0}".format(item["Key"]))
            else:
                logging.info("NO FILES TO BE DELETED FROM S3")

    def read_from_s3(self, file_format: str) -> pandas.DataFrame:
        logging.info("READING DATA FROM S3...")
        try:
            s3 = self.session.client('s3')
            objects = s3.list_objects(
                Bucket=self.bucket_name,
                Prefix=self.object_name_prefix)
        except:
            raise
        else:
            if objects.get('Contents') is not None:
                if file_format == "json":
                    data = pandas.DataFrame()
                    for object in objects.get('Contents'):
                        logging.info(object.get('Key'))
                        
                        file_data = pandas.read_json(
                            path_or_buf="s3://{bucket}/{object}".format(
                                bucket=self.bucket_name,
                                object=object.get("Key"),
                            ),
                            orient="records",
                            lines=True,
                            compression="gzip" if ".gzip" in object.get('Key') else "infer",
                        )
                        data = pandas.concat([data, file_data])

                elif file_format == "parquet":
                    data = pandas.read_parquet(
                        path="s3://{bucket}/{object}".format(
                            bucket=self.bucket_name,
                            object=self.object_name_prefix,
                        ),
                    )

                else:
                    logging.error("FILE FORMAT {file_format} NOT SUPPORTED".format(
                        file_format=str.upper(file_format)
                    ))
                    sys.exit(1)

                read_count = len(data)
                logging.info("{0} RECORDS READ FROM S3".format(read_count))
                return data
            else:
                logging.info("NO DATA WAS FOUND ON S3")
                return None
