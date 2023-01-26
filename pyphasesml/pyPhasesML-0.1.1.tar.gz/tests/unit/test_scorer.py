import unittest

import numpy as np
from sklearn.metrics import cohen_kappa_score, roc_auc_score, average_precision_score
from pyPhasesML.scorer.Scorer import Scorer


class TestScorer(unittest.TestCase):

    classes = np.array([0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0])
    prediction = np.array([0.1, 0.8, 0.8, 0.3, 0.6, 0.7, 0.8, 1, 0.3, 0.2, 0.1, 0.0])

    def getPredictedClasses(self):
        classes = self.prediction.copy()
        classes[classes >= 0.5] = 1
        classes[classes < 0.5] = 0
        return classes

    def hotEncodedPrediction(self):
        classes = np.empty((len(self.prediction), 2))
        classes[:, 0] = 1 - self.prediction
        classes[:, 1] = self.prediction
        return classes

    def hotEncodedTruth(self):
        classes = np.empty((len(self.classes), 2))
        classes[:, 0] = 1 - self.classes
        classes[:, 1] = self.classes
        return classes

    def testAUPRC(self):
        true = average_precision_score(self.classes, self.prediction)

        s = Scorer(2, trace=True)
        s.metrics = ["auprc"]

        r = s.score(self.classes, self.hotEncodedPrediction())
        assert r["auprc"] == true

    def testAUPRCCombine(self):
        classes = np.concatenate([self.classes, self.classes])
        predictions = np.concatenate([self.prediction, self.prediction])
        true = average_precision_score(classes, predictions)

        s = Scorer(2, trace=True)
        s.metrics = ["auprc"]

        s.score(self.classes, self.hotEncodedPrediction(), trace=True)
        s.score(self.classes, self.hotEncodedPrediction(), trace=True)
        assert s.scoreAllRecords()["auprc"] == true

    def testAUROC(self):
        true = roc_auc_score(self.classes, self.prediction)
        s = Scorer(2)
        s.metrics = ["auroc"]

        r = s.score(self.classes, self.hotEncodedPrediction())
        assert r["auroc"] == true

    def testKappa(self):
        assert len(self.classes) == len(self.prediction)
        assert len(self.classes) == len(self.getPredictedClasses())
        kappa = cohen_kappa_score(self.classes, self.getPredictedClasses())
        s = Scorer(2)
        s.metrics = ["kappa"]

        r = s.score(self.classes, self.getPredictedClasses())
        assert r["kappa"] == kappa
