import pickle
import unittest

import tsaugmentation as tsag

from gpforecaster.model.gpf import GPF


class TestModel(unittest.TestCase):
    def setUp(self):
        self.data = tsag.preprocessing.PreprocessDatasets(
            "prison", sample_perc=0.5
        ).apply_preprocess()
        self.n = self.data["predict"]["n"]
        self.s = self.data["train"]["s"]
        self.res_type = 'fitpred'
        self.res_measure = 'mean'
        self.input_dir = './results/gpf/'
        self.gpf = GPF("tourism", self.data, input_dir=self.input_dir)
