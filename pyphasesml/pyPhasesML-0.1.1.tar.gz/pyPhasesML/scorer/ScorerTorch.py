import torch
from .Scorer import Scorer


class ScorerTorch(Scorer):
    def beforeLoss(self, x, y):
        return torch.from_numpy(x), torch.from_numpy(y)

    def score(self, truth, prediction, recordName=None, trace=True):
        if isinstance(truth, torch.Tensor):
            truth = truth.detach().cpu().numpy()
        if isinstance(prediction, torch.Tensor):
            prediction = prediction.detach().cpu().numpy()
        return super().score(truth, prediction, recordName=recordName, trace=trace)

