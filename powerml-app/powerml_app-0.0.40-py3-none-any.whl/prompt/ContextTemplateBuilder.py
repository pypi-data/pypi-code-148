from __future__ import annotations
from typing import List
from powerml.prompt.ContextTemplate import ContextTemplate


class ContextTemplateBuilder():
    string_examples = None
    question = None
    instruction = None 
    seperator = "\n\n"
    input_output_examples = None
    
    def generate_context_template(self,) -> ContextTemplate:
        template = ''
        seperator = self.seperator
        if self.question is not None:
          seperator += self.question + " "
          template += self.question + " "
        if self.instruction is not None:
          seperator += self.instruction + " "
          template += self.instruction + " "
        
        # Format the context 
        if self.string_examples is not None:
          template += seperator.join(self.string_examples)
          template += seperator

        # Format the context 
        if self.input_output_examples is not None:
          example_string_gen = (f'{e["input"]}\n{e["output"]}' for e in self.input_output_examples)
          template += seperator.join(example_string_gen)
          template += seperator
        
        # Oneshot
        # Format the question or instruction 
        template += "{{input}}" 
        return ContextTemplate(template=template, input_list=["input"])
    
    def add_string_examples(self, examples: List[str]):
        self.string_examples = examples

    def add_input_output_examples(self, examples):
        self.input_output_examples = examples

    def add_question(self, question: str):
        self.question = question

    def add_instruction(self, instruction: str):
        self.instruction = instruction

    def set_seperator(self, seperator: str):
        self.seperator = seperator



