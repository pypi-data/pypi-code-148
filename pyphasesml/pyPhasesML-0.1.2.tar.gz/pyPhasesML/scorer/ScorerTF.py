import tensorflow as tf

from .Scorer import Scorer


class ScorerTF(Scorer):
    
    def toNumpy(self, x):
        if tf.is_tensor(x):
            return x.numpy()
        return x
        
    def prepareInput(self, inputArray):
        if tf.is_tensor(inputArray):
            inputArray = inputArray.numpy()
        return super().prepareInput(inputArray)
        
    # def beforeLoss(self, x, y):
    #     return self.toNumpy(x), self.toNumpy(y)
    
    # def score(self, truth, prediction, recordName=None, trace=True):
    #     truth, prediction = self.toNumpy(truth), self.toNumpy(prediction)
    #     return super().score(truth, prediction, recordName=recordName, trace=trace)


    # def scoreMetric(self, metricName, truth, prediction):
    #     truth, prediction = self.toNumpy(truth), self.toNumpy(prediction)
    #     return super().scoreMetric(metricName, truth, prediction)