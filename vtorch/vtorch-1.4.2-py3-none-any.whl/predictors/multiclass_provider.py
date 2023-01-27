from pathlib import Path
from typing import Dict, Optional

from torch.nn import Module

from vtorch.data.iterators import DataIterator
from vtorch.data.transform import MultiClassLabelIndexer, Vectorizer
from vtorch.models.model import IModel
from vtorch.nn.utils import move_to_device
from vtorch.postprocessing import MulticlassPostprocessor
from vtorch.postprocessing.default import PredictionPostprocessor
from vtorch.predictors import MODEL_DIR, VECTORIZER_DIR, IConfidencePredictorProvider
from vtorch.predictors.model import ModelPredictor
from vtorch.predictors.multiclass import MultilangPredictor


class MultilangMulticlassPredictorProvider(IConfidencePredictorProvider):
    def __init__(
        self,
        serialization_dir: str,
        iterator: DataIterator,
        language_threshold: Dict[str, float],
        default_value: str,
        default_confidence: float,
        text_namespace: str = "text",
        label_namespace: str = "labels",
        cuda_device: int = -1,
        model_postprocessor: Optional[Module] = None,
    ):
        self.serialization_dir = Path(serialization_dir)
        self.iterator = iterator
        self.language_threshold = language_threshold
        self.default_value = default_value
        self.default_confidence = default_confidence
        self.text_namespace = text_namespace
        self.label_namespace = label_namespace
        self.cuda_device = cuda_device
        self.model_postprocessor = model_postprocessor

    def get(self) -> MultilangPredictor:
        vectorizers = Vectorizer.load(str(self.serialization_dir / VECTORIZER_DIR))

        label_indexer: MultiClassLabelIndexer = vectorizers.namespace_feature_extractors[self.label_namespace]

        language_post_processors: Dict[str, PredictionPostprocessor] = {
            language: MulticlassPostprocessor(  # works with probabilities as well as with logits
                {label_name: i for i, label_name in enumerate(label_indexer.vocab)},
                default_threshold=threshold,
                default_label=self.default_value,
            )
            for language, threshold in self.language_threshold.items()
        }
        vectorizers.namespace_feature_extractors.pop(self.label_namespace)
        return MultilangPredictor(
            ModelPredictor(
                model=move_to_device(IModel.load(str(self.serialization_dir / MODEL_DIR)), self.cuda_device),
                vectorizer=vectorizers,
                iterator=self.iterator,
                activation=self.model_postprocessor,
            ),
            label_indexer=label_indexer,
            language_post_processors=language_post_processors,
            default_value=self.default_value,
            default_confidence=self.default_confidence,
        )
