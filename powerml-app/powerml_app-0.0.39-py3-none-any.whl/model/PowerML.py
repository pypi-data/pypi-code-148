import io
from typing import Tuple
import jsonlines
from powerml.utils.run_ai import query_powerml, mutation_powerml_train, query_powerml_with_probability
import logging

logger = logging.getLogger(__name__)

MAX_TEMPLATE_TOKENS = 3072
MAX_TOTAL_TOKENS = 4097


class PowerML:
    '''
    hex_data = get_data()
    powerml = PowerML()
    completion = powerml.predict(model="hex/model_for_hex", prompt)
    powerml.fit(hex_data, model="hex/model_for_hex")
    '''

    def __init__(self, config={}):
        self.config = config
        self.current_model = "text-davinci-003"

    def predict(self,
                prompt,
                model: str = None,
                stop: str = "",
                max_tokens: int = 128,
                temperature: float = 0.0,
                ) -> str:
        if model == "" or model is None:
            model = self.current_model
        logger.debug("Predict using model: " + model)
        # if the model is one of our models, then hit our api
        return query_powerml(prompt,
                             max_tokens=max_tokens,
                             model=model,
                             stop=stop,
                             temperature=temperature,
                             config=self.config,
                             )

    def predict_with_probability(self,
                                 prompt,
                                 model: str = None,
                                 stop: str = "",
                                 max_tokens: int = 128,
                                 temperature: float = 0.0,
                                 ) -> Tuple[str, float]:
        if model == "" or model is None:
            model = self.current_model
        logger.debug("Predict using model: " + model)
        # if the model is one of our models, then hit our api
        return query_powerml_with_probability(prompt,
                                              max_tokens=max_tokens,
                                              model=model,
                                              stop=stop,
                                              temperature=temperature,
                                              config=self.config,
                                              )

    def fit(self,
            data: list[str],
            model: str = None,
            name: str = None,
            is_public: bool = False):
        if model == "" or model is None:
            model = self.current_model
        logger.debug("Fit using model: " + model)
        dataset = self.__make_dataset_string(data)
        response = mutation_powerml_train(dataset, name, model, is_public, self.config)
        model_details = response.json()['model']
        self.current_model = model_details["model_name"]
        return model_details

    def __make_dataset_string(self, training_data):
        string = io.StringIO()
        with jsonlines.Writer(string) as writer:
            for item in training_data:
                writer.write({"prompt": item})
        val = string.getvalue()
        return val
