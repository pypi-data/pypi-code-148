from flask import Response, request
import logging
import pandas as pd


from kortical.app import get_config
from kortical.app import requests
from module_placeholder.authentication import safe_api_call

logger = logging.getLogger(__name__)

app_config = get_config(format='yaml')
model_name = app_config['model_name']


def register_routes(app):

    @app.route('/health', methods=['get'])
    def health():
        return {"result": "success"}

    @app.route('/predict', methods=['post'])
    @safe_api_call
    def predict():
        input_text = request.json['input_text']
        request_data = {
            'text': [input_text]
        }
        df = pd.DataFrame(request_data)
        # Do custom pre-processing (data cleaning / feature creation)
        df = requests.predict(model_name, df)
        # Do custom post-processing
        predicted_category = df['predicted_category'][0]

        return Response(predicted_category)
