from powerml import PowerML
import logging
import re

logger = logging.getLogger(__name__)


class ExtractMenuItemsModel:
    def __init__(self, config={}, max_output_tokens=32, temperature=0.0, threshold=28.92):
        self.max_output_tokens = max_output_tokens
        self.model = PowerML(config, "presto/del-taco-menu/v2")
        self.temperature = temperature
        self.threshold = threshold
        self.examples = []

    def fit(self, examples=[]):
        """
        Parameters
        ----------
        examples : list
            Takes a list of dictionaries where each dictionary has a key:
            "conversation" with a transcript and a key "order" with the resulting order the user had.
        """
        self.examples = examples

    def predict(self, conversation):
        """
        Parameters
        ----------
        conversation : str
            Transcript of conversation of customer ordering from restaurant

        Returns
        -------
        str : The extracted menu items from the conversation
        """
        prompt = {"{{examples}}": "\n\n".join(["CONVERSATION:\n" +
                                               example["conversation"] +
                                               "\nORDER:\n" +
                                               example["order"] for example in self.examples]), "{{input}}": conversation}
        output, probability = self.model.predict_with_probability(
            prompt,
            max_tokens=self.max_output_tokens,
            temperature=self.temperature,
        )
        return self.__post_process(output, probability)

    def __post_process(self, output, probability):
        # TODO: replace with stop tokens
        results = re.split('END', output)
        result = results[0].strip()
        if result.find("0") == 0:
            return None
        if probability < self.threshold:
            return None
        return result
