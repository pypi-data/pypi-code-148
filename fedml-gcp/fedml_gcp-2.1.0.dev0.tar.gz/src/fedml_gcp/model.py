import numpy as np
import pandas as pd
import joblib


class Model:
    def __init__(self, model):
        msg = "model load fail"
        try:
            self.model = model
            print("model loaded")
        except:
            print(msg)

    def predict(self, data):
        inputs = np.asarray(data["instances"])
        results = self.model.predict(inputs)
        return results
