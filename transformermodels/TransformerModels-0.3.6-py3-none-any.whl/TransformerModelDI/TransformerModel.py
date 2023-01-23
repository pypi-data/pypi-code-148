from setfit import SetFitModel
import os
import pandas as pd


class TransformerModel:
    def __init__(self, classifier=None):
      
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'transformer_model_new_env')
        print(path)
        self.classifier = SetFitModel.from_pretrained(path)
        
    def predict(self, documents):
        text = [d['text'] for d in documents]
        ids = [d['id'] for d in documents]
        predictions = self.classifier(text)
        return [{'id': v[0],'text':v[1],'label': v[2]} for v in zip(ids,text,predictions)]

    def __call__(self, documents, *args, **kwargs):
        return self.predict(documents)
