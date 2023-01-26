import io
from typing import List, Tuple
import jsonlines
from powerml.utils.run_ai import query_powerml, mutation_powerml_train, query_powerml_with_probability
import logging

logger = logging.getLogger(__name__)


class PowerML:
    '''
    Each instance of the PowerML class represents an LLM 
    accessible through the PowerML API.
    '''

    def __init__(self, config={}, model="text-davinci-003"):
        self.config = config
        self.current_model = model
        self.foundational_model = model 

    def predict(self,
                prompt,
                stop: str = "",
                max_tokens: int = 128,
                temperature: float = 0.0,
                ) -> str:
        """
        Prompt the model to return a completion
        """
        model = self.current_model
        logger.debug("Predict using model: " + model)
        return query_powerml(prompt,
                             max_tokens=max_tokens,
                             model=model,
                             stop=stop,
                             temperature=temperature,
                             config=self.config,
                             )

    def predict_with_probability(self,
                                 prompt,
                                 stop: str = "",
                                 max_tokens: int = 128,
                                 temperature: float = 0.0,
                                 ) -> Tuple[str, float]:
        """
        Prompt the model to return a completion and the confidence of that completion
        """
        model = self.current_model
        logger.debug("Predict using model: " + model)
        return query_powerml_with_probability(prompt,
                                              max_tokens=max_tokens,
                                              model=model,
                                              stop=stop,
                                              temperature=temperature,
                                              config=self.config,
                                              )

    def fit(self,
            data: List[str],
            name: str = None,
            is_public: bool = False):
        """
        Finetune a model 
        """
        # TODO: fit and set_prompt only works on foundational models
        logger.debug("Fit using model: " + self.foundational_model)
        dataset = self.__make_dataset_string(data)
        response = mutation_powerml_train(dataset, name, self.foundational_model, is_public, self.config)
        model_details = response.json()['model']
        self.current_model = model_details["model_name"]
        return model_details

    def set_prompt(self,
            prompt: str,
            name: str = None,
            is_public: bool = False):
        """
        Set the model's prompt
        """
        # TODO: fit and set_prompt only works on foundational models
        logger.debug("Fit using model: " + self.foundational_model)
        dataset = self.__make_dataset_string([prompt])
        response = mutation_powerml_train(dataset, name, self.foundational_model, is_public, self.config)
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
