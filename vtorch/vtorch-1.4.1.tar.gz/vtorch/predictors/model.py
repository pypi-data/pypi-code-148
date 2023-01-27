from collections import defaultdict
from typing import Any, Dict, List, Mapping, Optional, Sequence

import torch
from torch.nn import Identity

from ..common.utils import argsort
from ..data.iterators.base import DataIterator
from ..data.transform import Vectorizer
from ..models.model import IModel
from ..nn.utils import get_module_device, move_to_device


class ModelPredictor:
    def __init__(
        self,
        model: IModel,
        vectorizer: Vectorizer,
        iterator: DataIterator,
        activation: Optional[torch.nn.Module] = None,
    ) -> None:
        self._model = model
        self._model.eval()
        self.vectorizer = vectorizer
        self._iterator = iterator
        self._cuda_device = get_module_device(self._model)
        self.activation = activation if activation else Identity()
        self.activation = move_to_device(self.activation, self._cuda_device)

    def predict(
        self, inputs: Sequence[Mapping[str, Any]], additional_batch_params: Optional[Dict[str, Any]] = None
    ) -> torch.Tensor:
        instances = [self.vectorizer.vectorize(mention) for mention in inputs]
        data_generator = self._iterator(instances, shuffle=False)
        not_sorted_predictions = []
        serial_indexes: List[int] = []
        with torch.no_grad():
            for batch, ids in data_generator:
                serial_indexes.extend(ids)
                batch = move_to_device(batch, self._cuda_device)
                if additional_batch_params is not None:
                    batch.update(additional_batch_params)
                not_sorted_predictions.append(self.activation(self._model(**batch)[0]).cpu())
        not_sorted_predictions_tensor = torch.cat(not_sorted_predictions)
        sorted_predictions = not_sorted_predictions_tensor[argsort(serial_indexes)]
        return sorted_predictions


class MultitaskModelPredictor:
    def __init__(
        self,
        model: IModel,
        vectorizer: Vectorizer,
        iterator: DataIterator,
        activation: Optional[torch.nn.Module] = None,
    ) -> None:
        self._model = model
        self._model.eval()
        self.vectorizer = vectorizer
        self._iterator = iterator
        self._cuda_device = get_module_device(self._model)
        self.activation = activation if activation else Identity()
        self.activation = move_to_device(self.activation, self._cuda_device)

    def predict(
        self, inputs: Sequence[Mapping[str, Any]], additional_batch_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, torch.Tensor]:
        instances = [self.vectorizer.vectorize(mention) for mention in inputs]
        data_generator = self._iterator(instances, shuffle=False)
        not_sorted_predictions: Dict[str, List[torch.Tensor]] = defaultdict(list)
        serial_indexes: List[int] = []
        with torch.no_grad():
            for batch, ids in data_generator:
                serial_indexes.extend(ids)
                batch = move_to_device(batch, self._cuda_device)
                if additional_batch_params is not None:
                    batch.update(additional_batch_params)
                for namespace, probabilities_and_loss in self._model(**batch).items():
                    not_sorted_predictions[namespace].append(self.activation(probabilities_and_loss[0]).cpu())

        sorted_predictions = {
            namespace: torch.cat(predictions)[argsort(serial_indexes)]
            for namespace, predictions in not_sorted_predictions.items()
        }

        return sorted_predictions
