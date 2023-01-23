import json
from abc import ABC, abstractmethod
from typing import Dict, List, Union

import numpy as np
from loguru import logger


class RefuelJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        return json.JSONEncoder.default(self, o)


class BaseLoggingObj(ABC):
    def __init__(
        self, model_name: str, dataset_name: str, client_timestamp: str
    ) -> None:
        self.model_name = model_name
        self.dataset_name = dataset_name
        self.client_timestamp = client_timestamp

    @abstractmethod
    def serialize(self) -> Union[Dict, List]:
        # Not Implemented
        pass


class Event(BaseLoggingObj):
    def __init__(
        self,
        model_name: str,
        dataset_name: str,
        client_timestamp: str,
        x: Dict,
        y_pred: Dict,
        y_true: Dict,
        metadata: Dict,
    ) -> None:
        """
        Args:
            model_name (str): _description_
            x (dict): _description_
            y_pred (dict): _description_
            y_true (dict): _description_
            metadata (dict): _description_
            client_timestamp (str): _description_
        """
        super().__init__(model_name, dataset_name, client_timestamp)
        self.x = x
        self.y_pred = y_pred
        self.y_true = y_true
        self.metadata = metadata

    def serialize(self) -> Dict:
        if not self.model_name:
            logger.error(
                f"No model name specified for logging event: {self.model_name}"
            )
            return {}

        data = {
            "model_name": self.model_name,
            "dataset_name": self.dataset_name,
            "x": self.x,
            "y_pred": self.y_pred,
            "y_true": self.y_true,
            "metadata": self.metadata,
            "refuel_client_timestamp": self.client_timestamp,
        }
        return json.dumps(data, cls=RefuelJSONEncoder)


class EventBatch(BaseLoggingObj):
    def __init__(
        self, model_name: str, dataset_name: str, client_timestamp: str, events: List
    ) -> None:
        """_summary_

        Args:
            model_name (str): _description_
            client_timestamp (str): _description_
            events (List): _description_
        """
        super().__init__(model_name, dataset_name, client_timestamp)
        self.events = events

    def serialize(self) -> List:
        if not self.model_name:
            logger.error(
                f"No model name specified for logging event: {self.model_name}"
            )
            return []

        data = []
        for event in self.events:
            data.append(
                {
                    "model_name": self.model_name,
                    "dataset_name": self.dataset_name,
                    "x": event.get("x"),
                    "y_pred": event.get("y_pred"),
                    "y_true": event.get("y_true"),
                    "metadata": event.get("metadata"),
                    "refuel_client_timestamp": self.client_timestamp,
                }
            )
        return json.dumps(data, cls=RefuelJSONEncoder)


class DatasetEvent(BaseLoggingObj):
    def __init__(
        self,
        model_name: str,
        dataset_name: str,
        client_timestamp: str,
        cloud_uri: str,
        dataset_config: dict,
    ) -> None:
        """_summary_

        Args:
            model_name (str): model dataset belongs to
            dataset_name (str): name of the dataset
            client_timestamp (str): provided timestamp
            cloud_uri (str): cloud uri or pre-signed uri to dataset in cloud storage
        """
        super().__init__(model_name, dataset_name, client_timestamp)
        self.cloud_uri = cloud_uri
        self.dataset_config = dataset_config
        self.dataset_config.setdefault("type", "CSV")
        self.dataset_config.setdefault("delimiter", ",")

    def serialize(self) -> List:
        if not self.model_name:
            logger.error(
                f"No model name specified for logging event: {self.model_name}"
            )
            return {}

        data = {
            "model_name": self.model_name,
            "dataset_name": self.dataset_name,
            "cloud_uri": self.cloud_uri,
            "dataset_config": json.dumps(self.dataset_config),
            "refuel_client_timestamp": self.client_timestamp,
        }

        return json.dumps(data)
