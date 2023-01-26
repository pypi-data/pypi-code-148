from powerml.model.PowerML import PowerML
from powerml.prompt.ContextTemplate import ContextTemplate


class LLM:
    '''
    Each instance of the LLM class represents an LLM 
    accessible through the PowerML API.
    '''

    def __init__(self, config={}, model="text-davinci-003", stop="", max_tokens=256, temperature=0.0 ):
        self.model = PowerML(config, model)
        self.stop = stop
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.context = None

    def predict(self, **kwargs,) -> str:
        """
        Prompt the model to return a completion. 
        """
        extra_args = set(kwargs.keys()) - set(self.context.input_list)
        if extra_args:
            raise Exception("Missing inputs in context: " + str(extra_args))
        if not self.context.input_list:
            prompt = ""
            return self.model.predict(prompt,
                             max_tokens=self.max_tokens,
                             stop=self.stop,
                             temperature=self.temperature,
                             )
        # kwargs does not have any args outside of the input list
        if self.context.input_list == ["input"]:
            # if the input list is only "input"
            if "input" not in kwargs:
                raise Exception("Missing `input` in call to predict")
            prompt = kwargs["input"]
            return self.model.predict(prompt,
                             max_tokens=self.max_tokens,
                             stop=self.stop,
                             temperature=self.temperature,
                             )
        
        prompt = {f"{{{{{key}}}}}": "" for key in self.context.input_list}
        for key,val in kwargs.items():
          prompt[f"{{{{{key}}}}}"] = val
        return self.model.predict(prompt,
                             max_tokens=self.max_tokens,
                             stop=self.stop,
                             temperature=self.temperature,
                             )

    def fit(self,
            context: ContextTemplate,):
        """
        Set the model's context
        """
        self.context = context
        template_string = context.get_prompt_template()
        model_details = self.model.set_prompt(template_string)
        return model_details