from __future__ import annotations
from powerml.model.PowerML import PowerML


class ContextTemplate():
    def __init__(self, template: str, input_list: list[str]):
        self.template = template 
        self.input_list = input_list
        self.examples = []

    def set_examples(self, examples):
        self.examples = examples

    def get_prompt_template(self,):
        return "\n\n".join(self.examples) + self.template

    @classmethod
    def from_file(
        cls, template_file: str, input_list: list[str]
    ) -> ContextTemplate:
        with open(template_file, "r") as f:
            template = f.read()
        return cls(template=template, input_list=input_list)

