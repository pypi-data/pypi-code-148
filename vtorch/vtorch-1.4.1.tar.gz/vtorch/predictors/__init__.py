from abc import ABC, abstractmethod
from typing import Any, Generic, Mapping, Sequence, TypeVar

Prediction = TypeVar("Prediction")
ConfidencePrediction = TypeVar("ConfidencePrediction")
Target = TypeVar("Target")

MODEL_DIR = "model"
VECTORIZER_DIR = "vectorizer"


class Predictor(Generic[Prediction], ABC):
    @abstractmethod
    def predict(self, mentions: Sequence[Mapping[str, Any]]) -> Sequence[Prediction]:
        pass


class IPredictorProvider(ABC):
    @abstractmethod
    def get(self) -> Predictor[Any]:
        pass


class ConfidencePredictor(Generic[Prediction, ConfidencePrediction], Predictor[Prediction], ABC):
    @abstractmethod
    def predict_with_confidence(self, mentions: Sequence[Mapping[str, Any]]) -> Sequence[ConfidencePrediction]:
        pass


class IConfidencePredictorProvider(IPredictorProvider):
    @abstractmethod
    def get(self) -> ConfidencePredictor[Any, Any]:
        pass
