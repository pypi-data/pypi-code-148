from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import torch

from vtorch.data.transform import AbstractLabelIndexer
from vtorch.postprocessing.default import PredictionPostprocessor
from vtorch.predictors import ConfidencePredictor
from vtorch.predictors.model import ModelPredictor
from vtorch.predictors.utils import is_mention_supported, post_process_predictions_by_language

UNKNOWN_LANGUAGE = "other"  # if language is not provided, we will return empty list


class MultilangPredictor(ConfidencePredictor[str, Tuple[str, float]]):
    def __init__(
        self,
        model_predictor: ModelPredictor,
        label_indexer: AbstractLabelIndexer,
        language_post_processors: Dict[str, PredictionPostprocessor],
        default_value: str,
        default_confidence: float,
        missing_language: str = UNKNOWN_LANGUAGE,
    ) -> None:
        self.model_predictor = model_predictor
        self.label_indexer = label_indexer
        self._language_post_processors = language_post_processors
        self._default_value = default_value
        self._default_confidence = default_confidence
        self._missing_language = missing_language
        self._supported_languages = set(processors for processors in self._language_post_processors.keys())

    def predict_with_confidence(self, mentions: Sequence[Mapping[str, Any]]) -> Sequence[Tuple[str, float]]:
        supported_indices = [
            i
            for i, mention in enumerate(mentions)
            if is_mention_supported(mention, self._supported_languages, missing_language=self._missing_language)
        ]
        supported_mentions = [mentions[i] for i in supported_indices]
        predictions: List[Tuple[str, float]] = [(self._default_value, self._default_confidence) for _ in mentions]
        if len(supported_mentions) > 0:
            supported_mentions_languages = [
                mention.get("language", mention.get("lang", self._missing_language)) for mention in supported_mentions
            ]
            probabilities = self.model_predictor.predict(supported_mentions)
            postprocessed_probabilities = post_process_predictions_by_language(
                probabilities, supported_mentions_languages, language_post_processors=self._language_post_processors
            )
            labels_and_probabilities = get_classes_and_probabilities(
                predictions=postprocessed_probabilities,
                probabilities=probabilities,
                labels=self.label_indexer.vocab,
                default=self._default_value,
            )
            for i, prediction in zip(supported_indices, labels_and_probabilities):
                predictions[i] = prediction
        return predictions

    def predict(self, mentions: Sequence[Mapping[str, Any]]) -> Sequence[str]:
        return [prediction[0] for prediction in self.predict_with_confidence(mentions=mentions)]

    def languages(self) -> Iterable[str]:
        return self._supported_languages


def get_classes_and_probabilities(
    predictions: torch.Tensor, probabilities: torch.Tensor, labels: List[str], default: str
) -> List[Tuple[str, float]]:
    predicted_labels: List[Tuple[str, float]] = [(default, 0.0) for _ in predictions]
    for mention_serial_number, label_index in predictions.nonzero().tolist():  # type: ignore
        predicted_labels[mention_serial_number] = (
            labels[label_index],
            probabilities[mention_serial_number, label_index].item(),
        )
    return predicted_labels
