import json
import logging
from typing import Dict, List, Optional, Union

import boto3
import pyspark
from botocore.exceptions import ClientError
from py4j.protocol import Py4JError
from pyspark.context import SparkContext
from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession

sc = SparkContext.getOrCreate()
spark = SparkSession(sc)
LOG = logging.getLogger(__name__)


class ArenaDatabricks:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        read_bucket: str,
    ):
        self.read_bucket = read_bucket

        try:
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )
        except Exception:
            raise ValueError("Access and secret provided are not valid!")

        self.alias_map = S3JsonInput(access_key, secret_key, read_bucket, "arena-integrations/aliases").read()
        try:
            sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", access_key)
            sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", secret_key)
        except Py4JError:
            spark.conf.set("fs.s3a.access.key", access_key)
            spark.conf.set("fs.s3a.secret.key", secret_key)

    def load_dataset(self, dataset: str, date: Optional[str] = None) -> DataFrame:
        s3_key = self.resolve_alias(dataset)
        if date is None:
            return spark.read.parquet(f"s3a://{self.read_bucket}/{s3_key}")
        else:
            try:
                return spark.read.parquet(f"s3a://{self.read_bucket}/{s3_key}/date={date}")
            except pyspark.sql.utils.AnalysisException:
                raise ValueError(f"date {date} not found for {dataset}. date must be in the format YYYY-mm-dd")

    def resolve_alias(self, alias: str) -> str:
        dataset = self.alias_map.get(alias)  # type: ignore
        existing_aliases = self.alias_map.keys()  # type: ignore
        if dataset is None:
            raise ValueError(f"Dataset {alias} not found! Existing datasets: {existing_aliases}")
        return dataset


class ArenaIntegrations:
    @classmethod
    def databricks(cls, access_key: str, secret_key: str, read_bucket: str) -> ArenaDatabricks:
        return ArenaDatabricks(access_key=access_key, secret_key=secret_key, read_bucket=read_bucket)


class S3JsonInput:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        key: str,
        encoding: str = "utf-8",
        return_none_if_missing: bool = False,
    ) -> None:
        """Read and parse a JSON file from S3.

        Parameters
        ----------
        bucket_name : str
            Name of the S3 bucket.
        key : str
            Path to file relative to bucket (should include .json extension).
        encoding : str
            Encoding to use when reading the file.
        return_none_if_missing : bool
            If True, return None if the file is missing. Otherwise, raise an
            error.
        """
        self.s3_resource = boto3.resource("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        self._bucket_name, self._key = bucket_name, key
        self.encoding = encoding
        self.return_none_if_missing = return_none_if_missing

    @property
    def key(self) -> str:
        """Return the input path (relative to the input bucket)."""
        return self._key

    @property
    def bucket_name(self) -> str:
        """Return the input bucket name."""
        return self._bucket_name

    def read(self, jsonify_input: bool = True) -> Union[Dict, List, str, None]:  # type: ignore
        """Read the file from S3, if it exists.

        Parameters
        ----------
        jsonify_input : bool
            If True, return the file as a dict. Otherwise, return the raw JSON
            string.
        """
        try:
            file = self.s3_resource.Object(self.bucket_name, self.key).get()["Body"].read().decode(self.encoding)
        except ClientError as e:
            if e.response["Error"]["Code"] in ["NoSuchBucket", "NoSuchKey"]:
                if self.return_none_if_missing:
                    return None
                else:
                    raise FileNotFoundError(f"File not found: {self.bucket_name}/{self.key}") from e
            else:
                LOG.error("Uncaught error, response: %s", e.response)
                raise e
        else:
            if jsonify_input:
                return json.loads(file)
            else:
                return file
