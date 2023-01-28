import requests
import json
from functions import get_dict
import ast

class OpenAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/completions"

    def summarize(self, text, model="text-ada-001", temperature=0.5, max_tokens=1000, stop="."):
        payload = {
            "model": model,
            "prompt": "Sumarize the following text and give the output strictly in the format [\"X\"] and don't forget the closing bracket where X is the summary: "+ text,
            "temperature": temperature,
            "max_tokens":max_tokens,
            "stop": stop
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.post(self.base_url, json=payload, headers=headers)
        response = json.loads(response.text)
        try:
            return ast.literal_eval(response['choices'][0]['text'])
        except:
            return ast.literal_eval(response['choices'][0]['text']+"\"]")

    def get_prompt(self, text, model="text-ada-001", temperature=0.5, max_tokens=100, stop="."):
        payload = {
            "model": model,
            "prompt": "Write a prompt and print it in the format [\"X\"] where X is your output to generate an image based on summary of:  "+ text,
            "temperature": temperature,
            "max_tokens":max_tokens,
            "stop": stop
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.post(self.base_url, json=payload, headers=headers)
        response = json.loads(response.text)
        try:
            return ast.literal_eval(response['choices'][0]['text'])
        except:
            return ast.literal_eval(response['choices'][0]['text']+"\"]")

    def ner(self, text, model="text-ada-001", temperature=0.5, max_tokens=100, stop="."):
        payload = {
            "model": model,
            "prompt": "Recognize different entitites from the following text a give the result strictly in the format [[\"X\", \"Y\"]] where X is the category or type of entity and Y is the word captured: "+ text,
            "temperature": temperature,
            "max_tokens":max_tokens,
            "stop": stop
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.post(self.base_url, json=payload, headers=headers)
        response = json.loads(response.text)
        return get_dict(response['choices'][0]['text'])

    def generate_questions(self, text, model="text-ada-001", temperature=0.5, max_tokens=100, stop=".", questions=5):
        payload = {
            "model": model,
            "prompt": "Analyze the following text and prepare a set of "+str(questions)+" questions and answers. The ouput format is strictly only [[\"Q\", \"A\"]] where Q is the question and A the answer. The next part is the text: "+ text,
            "temperature": temperature,
            "max_tokens":max_tokens,
            "stop": stop
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        # print(payload['prompt'])
        response = requests.post(self.base_url, json=payload, headers=headers)
        response = json.loads(response.text)
        # print(response)
        return get_dict(response['choices'][0]['text']+"\"]]")