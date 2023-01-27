from itertools import chain
from typing import Any, Dict, List, Mapping, Sequence, Tuple

import torch

from vtorch.data.transform import AbstractLabelIndexer
from vtorch.postprocessing.default import PredictionPostprocessor
from vtorch.predictors import ConfidencePredictor
from vtorch.predictors.model import ModelPredictor, MultitaskModelPredictor
from vtorch.predictors.utils import is_mention_supported, post_process_predictions_by_language

UNKNOWN_LANGUAGE = "other"  # if language is not provided, we will return empty list


class MultilangPredictor(ConfidencePredictor[Sequence[str], Sequence[Tuple[str, float]]]):
    def __init__(
        self,
        model_predictor: ModelPredictor,
        label_indexer: AbstractLabelIndexer,
        language_post_processors: Dict[str, PredictionPostprocessor],
        missing_language: str = UNKNOWN_LANGUAGE,
    ) -> None:
        self.model_predictor = model_predictor
        self.label_indexer = label_indexer
        self._missing_language = missing_language
        self._language_post_processors = language_post_processors
        self._supported_languages = set(processors for processors in self._language_post_processors.keys())

    def predict_with_confidence(self, mentions: Sequence[Mapping[str, Any]]) -> Sequence[Sequence[Tuple[str, float]]]:
        supported_indices: List[int] = [
            i
            for i, mention in enumerate(mentions)
            if is_mention_supported(mention, self._supported_languages, missing_language=self._missing_language)
        ]
        supported_mentions = [mentions[i] for i in supported_indices]
        predictions: List[List[Tuple[str, float]]] = [[] for _ in mentions]
        if len(supported_mentions) > 0:
            supported_mentions_languages = [
                mention.get("language", mention.get("lang", self._missing_language)) for mention in supported_mentions
            ]
            probabilities = self.model_predictor.predict(supported_mentions)
            postprocessed_probabilities = post_process_predictions_by_language(
                probabilities, supported_mentions_languages, language_post_processors=self._language_post_processors
            )
            labels_and_probabilities = get_labels_and_probabilities(
                predictions=postprocessed_probabilities, probabilities=probabilities, labels=self.label_indexer.vocab
            )
            for i, prediction in zip(supported_indices, labels_and_probabilities):
                predictions[i] = prediction
        return predictions

    def predict(self, mentions: Sequence[Mapping[str, Any]]) -> Sequence[Sequence[str]]:
        return [
            [prediction[0] for prediction in predictions]
            for predictions in self.predict_with_confidence(mentions=mentions)
        ]


class MultilangMultitaskPredictor(
    ConfidencePredictor[Mapping[str, Sequence[str]], Mapping[str, Sequence[Tuple[str, float]]]]
):
    def __init__(
        self,
        model_predictor: MultitaskModelPredictor,
        label_indexer: Dict[str, AbstractLabelIndexer],
        language_post_processors: Dict[str, Dict[str, PredictionPostprocessor]],  # firstly namespace, then language
        missing_language: str = UNKNOWN_LANGUAGE,
    ) -> None:
        self.model_predictor = model_predictor
        self.label_indexer = label_indexer
        self._language_post_processors = language_post_processors
        self._missing_language = missing_language
        self._supported_languages = set(
            chain.from_iterable(processors.keys() for processors in self._language_post_processors.values())
        )

    def predict_with_confidence(
        self, mentions: Sequence[Mapping[str, Any]]
    ) -> Sequence[Mapping[str, Sequence[Tuple[str, float]]]]:
        supported_indices = [
            i
            for i, mention in enumerate(mentions)
            if is_mention_supported(mention, self._supported_languages, missing_language=self._missing_language)
        ]
        supported_mentions = [mentions[i] for i in supported_indices]
        predictions: List[Dict[str, List[Tuple[str, float]]]] = [dict() for _ in mentions]
        if len(supported_mentions) > 0:
            supported_mentions_languages = [
                mention.get("language", mention.get("lang", self._missing_language)) for mention in supported_mentions
            ]
            namespace_probabilities = self.model_predictor.predict(
                supported_mentions, additional_batch_params=dict(namespaces=self._language_post_processors.keys())
            )
            for namespace, probabilities in namespace_probabilities.items():
                namespace_predictions = post_process_predictions_by_language(
                    probabilities,
                    supported_mentions_languages,
                    language_post_processors=self._language_post_processors[namespace],
                )
                labels_and_probabilities = get_labels_and_probabilities(
                    predictions=namespace_predictions,
                    probabilities=probabilities,
                    labels=self.label_indexer[namespace].vocab,
                )
                for i, prediction in zip(supported_indices, labels_and_probabilities):
                    predictions[i][namespace] = prediction
        return predictions

    def predict(self, mentions: Sequence[Mapping[str, Any]]) -> Sequence[Mapping[str, Sequence[str]]]:
        return [
            {namespace: [prediction[0] for prediction in predictions]}
            for namespace, predictions in self.predict_with_confidence(mentions=mentions)
        ]


def get_labels_and_probabilities(
    predictions: torch.Tensor, probabilities: torch.Tensor, labels: List[str]
) -> List[List[Tuple[str, float]]]:
    predicted_labels: List[List[Tuple[str, float]]] = [[] for _ in predictions]
    for mention_serial_number, label_index in predictions.nonzero().tolist():  # type: ignore
        predicted_labels[mention_serial_number].append(
            (labels[label_index], probabilities[mention_serial_number, label_index].item())
        )
    return predicted_labels
