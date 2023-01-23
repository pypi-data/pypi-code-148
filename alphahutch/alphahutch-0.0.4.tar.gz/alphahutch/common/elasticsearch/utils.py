import logging
import pandas as pd

from typing import Dict, Generator
from elasticsearch import Elasticsearch
from elasticsearch import helpers


def _gendata(df: pd.DataFrame, target_index: str) -> Generator[Dict, None, None]:
    df_iter = df.iterrows()
    for _, document in df_iter:
        yield {"_index": target_index, "_source": document.to_dict()}


class CustomSearcher:
    def __init__(
        self,
        username: str,
        password: str,
        hostname: str,
        port: str,
        index_name: str,
    ):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.port = port
        self.index_name = index_name
        self.endpoint = f"http://{self.hostname}:{self.port}/"
        self.conn = Elasticsearch(
            self.endpoint, http_auth=[self.username, self.password]
        )

        if self.conn.ping():
            logging.info(f"Connection to {self.endpoint} successful")
        else:
            logging.warning(f"Connection to {self.endpoint} unsuccessful")

    def index_dataframe(self, df: pd.DataFrame) -> None:
        """Index pandas dataframe into target elasticsearch instance. Ensures
        that only the columns that match the elasticsearch instance are indexed.

        Args:
            df (pd.DataFrame): pandas dataframe to index
        """

        logging.info(f"Starting to index dataframe in ElasticSearch")

        columns_to_keep = list(
            self.conn.indices.get_mapping()
            .get(self.index_name)
            .get("mappings")
            .get("properties")
            .keys()
        )
        columns_to_drop = [col for col in df.columns if col not in columns_to_keep]
        logging.info(
            f"Droping these columns since they have not been defined in the index: {columns_to_drop}"
        )
        df.drop(columns=columns_to_drop, inplace=True)

        helpers.bulk(self.conn, _gendata(df, target_index=self.index_name))
        logging.info(f"Finished indexing")

    def remove_dupes(self, df: pd.DataFrame, primary_key: str) -> pd.DataFrame:
        """Remove rows that already exist in the index by leveraging primary key column.

        Args:
            df (pd.DataFrame): pandas dataframe to index

        Returns:
            pd.DataFrame: unique dataframe
        """

        logging.info(f"Checking for duplicate ids")
        ids = df[primary_key].to_list()
        query = {"size": len(ids), "query": {"terms": {"url": ids}}}
        res = self.conn.search(index=self.index_name, body=query)
        existing_ids = [hit["_source"]["url"] for hit in res["hits"]["hits"]]
        logging.info(f"Dropping duplicate ids found: {existing_ids}")
 
        return df[~df["url"].isin(existing_ids)]
