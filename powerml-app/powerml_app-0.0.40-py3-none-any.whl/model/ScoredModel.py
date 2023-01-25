from powerml import PowerML
import logging

logger = logging.getLogger(__name__)


class ScoredModel:
    def __init__(self, config={}, max_output_tokens=256, temperature=0.7, threshold=0.33):
        self.max_output_tokens = max_output_tokens
        self.model = PowerML(config, "scored/seo_title/v0")
        self.temperature = temperature
        self.threshold = threshold

    def fit(self, examples, generate_key, score_key, metadata_keys, higher_is_better=True):
        """
        Parameters
        ----------
        examples : list
            Takes a list of dictionaries where each dictionary has keys as specified by the following three parameters:
        generate_key: maps to the key to be generated as output from .predict
        score_key: maps to the key to be used to calibrate model predictions
        metadata_keys: maps to a list of keys to be used as input to .predict
        higher_is_better: True if examples with higher scores are better than those with lower scores, otherwise False
        """
        self.examples = examples
        self.generate_key = generate_key
        self.score_key = score_key
        self.metadata_keys = metadata_keys
        self.higher_is_better = higher_is_better

    def predict(self, metadata):
        """
        Parameters
        ----------
        metadata : dict
            Takes a dictionary where each key corresponds to keys in the {metadata_key} list passed to .fit
        Returns
        str : A string corresponding to the {generate_key} key passed to .fit
        """
        positive_score = 1
        negative_score = 0
        examples = ''
        if self.examples:
            threshold = sorted([example[self.score_key] for example in self.examples], reverse=self.higher_is_better)[int(len(self.examples)*self.threshold)]
        for example in self.examples:
            for key in self.metadata_keys:
                examples += f"{example[key]}\n"
            if self.higher_is_better:
                score = positive_score if example[self.score_key] >= threshold else negative_score
            else: # lower is better
                score = positive_score if example[self.score_key] <= threshold else negative_score
            examples += f"score {score}: {example[self.generate_key]}\n\n"
        input = ''
        for key in self.metadata_keys:
            input += f"{metadata[key]}\n"
        score = int(self.higher_is_better)
        input += f"score {score}:"
        prompt = {
            '{{examples}}': examples,
            '{{input}}': input,
        }
        output = self.model.predict(
            prompt,
            max_tokens=self.max_output_tokens,
            temperature=self.temperature,
        )
        return self.__post_process(output)

    def __post_process(self, output):
        return output.strip()
