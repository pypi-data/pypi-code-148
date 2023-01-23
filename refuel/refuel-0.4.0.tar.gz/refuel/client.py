import concurrent.futures as pyfutures
import copy
import json
import math
import os
from concurrent.futures import as_completed
from datetime import datetime
from typing import Dict, List

import pandas as pd
from loguru import logger
from requests_futures.sessions import FuturesSession

from refuel.types import DatasetEvent, Event, EventBatch
from refuel.utils import DATE_FOURTEEN_DAYS_AGO, DATE_TOMORROW


class RefuelClient:
    # Default config settings
    API_BASE_URL = "https://api.refuel.ai"
    API_KEY_ENV_VARIABLE = "REFUEL_API_KEY"
    TIMEOUT_SECS = 15
    MAX_RETRIES = 3
    MAX_WORKERS = 4
    DT_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    MAX_BYTES_PER_BATCH = 3000000  # 3 MB
    MAX_EVENTS_PER_BATCH = 100
    DEFAULT_QUEUE_NAME = "default"
    DEFAULT_DATASET_NAME = "default"
    DEFAULT_ORDERING = "recent"
    DEFAULT_MAX_QUERY_EVENTS = 1000000
    QUERY_STEP_SIZE = 100

    def __init__(
        self,
        api_key: str = None,
        api_base_url: str = API_BASE_URL,
        timeout: int = TIMEOUT_SECS,
        max_retries: int = MAX_RETRIES,
        max_workers: int = MAX_WORKERS,
    ) -> None:
        """
        Args:
            api_key (str, optional): Refuel API Key. Defaults to None.
            api_base_url (str, optional): Base URL of the Refuel API endpoints. Defaults to API_BASE_URL.
            timeout (int, optional): Timeout (secs) for a given API call. Defaults to TIMEOUT_SECS.
            max_retries (int, optional): Max num retries. Defaults to MAX_RETRIES.
            max_workers (int, optional): Max number of concurrent tasks in the ThreadPoolExecutor
        """
        # initialize variables
        self._api_key = api_key or os.environ.get(self.API_KEY_ENV_VARIABLE)
        self._api_base_url = api_base_url
        self._timeout = timeout
        self._header = {"Content-Type": "application/json", "x-api-key": self._api_key}
        # initialize request session
        adapter_kwargs = {"max_retries": max_retries}
        self._session = FuturesSession(
            max_workers=max_workers, adapter_kwargs=adapter_kwargs
        )

        # Get initialization context from Refuel
        if not self._api_key or not isinstance(self._api_key, str):
            logger.error(f"API Key is absent or invalid: {self._api_key}. logged")
            self._init_context = {}
        else:
            init_response = self._get(url=self._api_base_url + "/init").result()
            self._init_context = init_response.json()

    def _get(self, url: str, params: Dict = None) -> pyfutures.Future:
        # print(self._session.get(url, headers=self._header, params=params).url())
        return self._session.get(url, headers=self._header, params=params)

    def _post(self, url: str, body: str) -> pyfutures.Future:
        return self._session.post(
            url, headers=self._header, timeout=self._timeout, data=body
        )

    def _delete(self, url: str, params: Dict = None) -> pyfutures.Future:
        return self._session.delete(url, headers=self._header, params=params)

    def _chunkify_events(self, events: List) -> List:
        if len(events) == 0:
            return []
        # approximate how large is each event
        bytes_per_event = len(json.dumps(events[0]).encode("utf-8"))
        # calculate num events in each chunk
        nbytes = bytes_per_event * len(events)
        nchunks = math.floor(nbytes / self.MAX_BYTES_PER_BATCH) + 1
        width = math.floor(len(events) / nchunks) + 1
        width = min(width, self.MAX_EVENTS_PER_BATCH)
        # chunkify
        return [events[i : i + width] for i in range(0, len(events), width)]

    def log(
        self,
        model_name: str,
        x: Dict,
        y_pred: Dict = None,
        y_true: Dict = None,
        metadata: Dict = None,
        dataset_name: str = DEFAULT_DATASET_NAME,
    ) -> pyfutures.Future:
        """
        Log individual events to the Refuel platform.

        Args:
            model_name (str): _description_
            dataset_name (str): _description_
            x (dict): _description_
            y_pred (dict): _description_. Defaults to None.
            y_true (dict, optional): _description_. Defaults to None.
            metadata (dict, optional): _description_. Defaults to None.

        Returns:
            pyfutures.Future: _description_
        """
        if not self._api_key:
            logger.error(
                f"API Key is absent or invalid: {self._api_key}. No event was logged"
            )
            return None
        if model_name not in self._init_context.get("models", []):
            logger.error(f"Model name: {model_name} does not exist for this team")
            return None

        client_timestamp = datetime.utcnow().strftime(self.DT_FORMAT)
        event = Event(
            model_name, dataset_name, client_timestamp, x, y_pred, y_true, metadata
        )
        return self._post(url=self._api_base_url + "/log", body=event.serialize())

    def log_batch(
        self, model_name: str, events: List, dataset_name: str = DEFAULT_DATASET_NAME
    ) -> List[pyfutures.Future]:
        """_summary_

        Args:
            model_name (str): _description_
            dataset_name (str): _description_
            events (List): _description_

        Returns:
            List[pyfutures.Future]: _description_
        """
        if not self._api_key:
            logger.error(
                f"API Key is absent or invalid: {self._api_key}. No event was logged"
            )
            return None
        if model_name not in self._init_context.get("models", []):
            logger.error(f"Model name: {model_name} does not exist for this team")
            return None

        client_timestamp = datetime.utcnow().strftime(self.DT_FORMAT)
        chunks = self._chunkify_events(events)
        futures = []
        for chunk in chunks:
            batch = EventBatch(model_name, dataset_name, client_timestamp, chunk)
            futures.append(
                self._post(
                    url=self._api_base_url + "/log_batch", body=batch.serialize()
                )
            )
        return futures

    def log_dataset(
        self, model_name: str, dataset_name: str, cloud_uri: str, dataset_config: dict
    ) -> pyfutures.Future:
        """Log dataset to the Refuel platform.

        Args:
            model_name (str): model to log dataset to
            dataset_name (str): name of dataset
            cloud_uri (str): cloud uri or presigned url to dataset
            dataset_config (dict): configuration for the dataset

        Returns:
            pyfutures.Future:
        """
        if not self._api_key:
            logger.error(
                f"API Key is absent or invalid: {self._api_key}. No event was logged"
            )
            return None
        if model_name not in self._init_context.get("models", []):
            logger.error(f"Model name: {model_name} does not exist for this team")
            return None

        client_timestamp = datetime.utcnow().strftime(self.DT_FORMAT)

        dataset_event = DatasetEvent(
            model_name, dataset_name, client_timestamp, cloud_uri, dataset_config
        )

        return self._post(
            url=self._api_base_url + "/log_dataset", body=dataset_event.serialize()
        )

    def _event_count_helper(self, url: str, params: Dict = None) -> int:
        model_name = params.get("model_name", None)
        if not self._api_key:
            logger.error(
                f"API Key is absent or invalid: {self._api_key}. No event was logged"
            )
            return None
        if model_name not in self._init_context.get("models", []):
            logger.error(f"Model name: {model_name} does not exist for this team")
            return None

        # construct parallel requests
        request_params = copy.deepcopy(params)
        request_params["offset"] = 0
        request_params["max_events"] = 0

        response = self._get(url=url, params=request_params).result()
        if response.status_code != 200:
            logger.error(
                "Status code: {} received with response: {}",
                response.status_code,
                response.text,
            )
        response_json = response.json()
        return response_json.get("count", self.DEFAULT_MAX_QUERY_EVENTS)

    def _query_helper(
        self, url: str, params: Dict = None, verbose: bool = False
    ) -> pd.DataFrame:
        self._event_count_helper(url, params)
        model_name = params.get("model_name", None)
        if not self._api_key:
            logger.error(
                f"API Key is absent or invalid: {self._api_key}. No event was logged"
            )
            return None
        if model_name not in self._init_context.get("models", []):
            logger.error(f"Model name: {model_name} does not exist for this team")
            return None

        max_events = min(
            params.get("max_events"), self._event_count_helper(url, params)
        )
        offset = params.get("offset", 0)

        # construct parallel requests
        logger.info(f"Started fetching data. Will fetch {max_events} events ...")
        futures = []
        offset_starts = list(
            range(offset, offset + max_events, RefuelClient.QUERY_STEP_SIZE)
        )
        for batch_num, offset_start in enumerate(offset_starts):
            request_params = copy.deepcopy(params)
            request_params["offset"] = offset_start
            request_params["max_events"] = min(
                max_events - offset_start, RefuelClient.QUERY_STEP_SIZE
            )
            future_obj = self._get(url=url, params=request_params)
            future_obj.batch_num = batch_num
            futures.append(future_obj)

        # parse response from each request
        batch_idx_to_events = {}
        num_fetched = 0
        for future in as_completed(futures):
            response = future.result()
            if response.status_code != 200:
                logger.error(
                    "Status code: {} received with response: {}",
                    response.status_code,
                    response.text,
                )
            else:
                json_response = response.json()
                result = json_response.get("result", [])
                batch_idx_to_events[future.batch_num] = result
                num_fetched += len(result)
                if verbose:
                    logger.info(f"Fetched {num_fetched} events so far.")

        sorted_by_batch_idx = [item[1] for item in sorted(batch_idx_to_events.items())]
        events = [item for sublist in sorted_by_batch_idx for item in sublist]
        logger.info(f"Completed fetching data. {len(events)} events were fetched.")
        return pd.DataFrame.from_records(events)

    def query_events(
        self,
        model_name: str,
        dataset_name: str = DEFAULT_DATASET_NAME,
        time_start: str = DATE_FOURTEEN_DAYS_AGO,
        time_end: str = DATE_TOMORROW,
        filters: List[Dict] = [],
        order_by: str = DEFAULT_ORDERING,
        offset: int = 0,
        max_events: int = DEFAULT_MAX_QUERY_EVENTS,
        include_embeddings: bool = False,
        embedding_column: str = None,
        verbose: bool = False,
    ) -> pd.DataFrame:
        """
        Query events from the Refuel platform.

        Args:
            model_name (str): Refuel model to query
            dataset_name (str): dataset within model to query

        Returns:
            pd.DataFrame: Dataframe containing events for the Refuel model
        """
        if (
            dataset_name
            not in self._init_context.get("datasets", {model_name: []})[model_name]
        ):
            logger.error(
                f"Dataset name: {dataset_name} does not exist for model {model_name}"
            )
            return None

        params = {
            "model_name": model_name,
            "dataset_name": dataset_name,
            "time_start": time_start,
            "time_end": time_end,
            "order_by": order_by,
            "offset": offset,
            "max_events": max_events,
            "filters": json.dumps(filters),
        }
        if include_embeddings:
            params["include_embeddings"] = True
        if embedding_column:
            params["embedding_column"] = embedding_column
        return self._query_helper(
            url=self._api_base_url + "/query", params=params, verbose=verbose
        )

    def query_annotation_queue(
        self,
        model_name: str,
        queue_name: str = DEFAULT_QUEUE_NAME,
        time_start: str = DATE_FOURTEEN_DAYS_AGO,
        time_end: str = DATE_TOMORROW,
        filters: List[Dict] = [],
        order_by: str = DEFAULT_ORDERING,
        offset: int = 0,
        max_events: int = DEFAULT_MAX_QUERY_EVENTS,
        verbose: bool = False,
    ) -> pd.DataFrame:
        """
        Query events from the review queue for a Refuel model.

        Args:
            model_name (str): Refuel model to query

        Returns:
            pd.DataFrame: Dataframe containing events for the Refuel model
        """
        params = {
            "model_name": model_name,
            "queue_name": queue_name,
            "time_start": time_start,
            "time_end": time_end,
            "order_by": order_by,
            "offset": offset,
            "max_events": max_events,
            "filters": json.dumps(filters),
        }
        return self._query_helper(
            url=self._api_base_url + "/query_annotation_queue",
            params=params,
            verbose=verbose,
        )

    def clear_annotation_queue(
        self,
        model_name: str,
        queue_name: str = DEFAULT_QUEUE_NAME,
    ) -> pd.DataFrame:
        """
        Clear all events from a review queue for a Refuel model.

        Args:
            model_name (str): Refuel model to query
            queue_name (str): Name of queue to clear

        Returns:
            pyfutures.Future:
        """
        params = {
            "model_name": model_name,
            "queue_name": queue_name,
            "refuel_uuids": [],
            "clear_queue": True,
        }
        return self._delete(
            url=self._api_base_url + "/clear_annotation_queue",
            params=params,
        )

    def delete_from_annotation_queue(
        self,
        model_name: str,
        queue_name: str = DEFAULT_QUEUE_NAME,
        refuel_uuids: list = [],
    ) -> pd.DataFrame:
        """
        Delete events with specified refuel_uuids from a review queue for a Refuel model.

        Args:
            model_name (str): Refuel model to query
            queue_name (str): Name of queue to clear
            refuel_uuids (list): List of refuel_uuids to clear

        Returns:
            pyfutures.Future:
        """
        params = {
            "model_name": model_name,
            "queue_name": queue_name,
            "refuel_uuids": refuel_uuids,
            "clear_queue": False,
        }
        return self._delete(
            url=self._api_base_url + "/clear_annotation_queue",
            params=params,
        )

    def query_similar_events(
        self,
        model_name: str,
        refuel_uuid: str,
        embedding_column: str = None,
        dataset_name: str = DEFAULT_DATASET_NAME,
        time_start: str = DATE_FOURTEEN_DAYS_AGO,
        time_end: str = DATE_TOMORROW,
        filters: List[Dict] = [],
        max_events: int = DEFAULT_MAX_QUERY_EVENTS,
        verbose: bool = False,
    ) -> pd.DataFrame:
        """
        Query events from the review queue for a Refuel model.

        Args:
            model_name (str): Refuel model to query

        Returns:
            pd.DataFrame: Dataframe containing events for the Refuel model
        """
        if (
            dataset_name
            not in self._init_context.get("datasets", {model_name: []})[model_name]
        ):
            logger.error(
                f"Dataset name: {dataset_name} does not exist for model {model_name}"
            )
            return None

        params = {
            "model_name": model_name,
            "refuel_uuid": refuel_uuid,
            "embedding_column": embedding_column,
            "dataset_name": dataset_name,
            "time_start": time_start,
            "time_end": time_end,
            "max_events": max_events,
            "fitlers": json.dumps(filters),
        }
        return self._query_helper(
            url=self._api_base_url + "/query_similar_events",
            params=params,
            verbose=verbose,
        )
