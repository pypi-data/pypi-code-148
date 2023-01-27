import torch

from .default import PredictionPostprocessor, PredictionPostprocessorI


class MultilabelPostprocessor(PredictionPostprocessor):
    def postprocess(self, probabilities: torch.Tensor) -> torch.Tensor:
        thresholds_with_logits_shape = torch.ones_like(probabilities) * self.thresholds
        predictions: torch.Tensor = torch.where(  # type: ignore
            probabilities >= thresholds_with_logits_shape,
            torch.tensor([1.0], dtype=probabilities.dtype),
            torch.tensor([0.0], dtype=probabilities.dtype),
        )
        return predictions


class MultilabelPostprocessorWithLogits(MultilabelPostprocessor):
    def postprocess(self, logits: torch.Tensor) -> torch.Tensor:
        return super().postprocess(logits.sigmoid())


MultilabelPostprocessorWithSigmoid = MultilabelPostprocessorWithLogits


class RawLogitsMultilabelPostprocessor(PredictionPostprocessorI):
    def postprocess(self, logits: torch.Tensor) -> torch.Tensor:
        return (logits > 0).float()  # type: ignore
