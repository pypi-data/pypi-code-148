import requests
import json
from Genr.functions import get_dict, ensure_format_dict, ensure_format_list
import ast

class OpenAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/completions"

    def summarize(self, text, model="text-davinci-003", temperature=1, max_tokens=1000, stop="."):
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
        # print(response)
        response = response['choices'][0]['text'].strip()
        # print(response)
        # print(response[:2])
        # print(response[-2:])
        # if response[:2]=="[\"" and response[-2:]=="\"]":
        #     return ast.literal_eval(response)
        # elif response[:2]=="[\"" and response[-2:]!="\"]":
        #     # print("Here")
        #     # print(response['choices'][0]['text']+"\"]")
        #     return ast.literal_eval(response+"\"]")
        # elif response[:2]!="[\"" and response[-2:]=="\"]":
        #     return ast.literal_eval("[\""+response)
        # else:
        #     return ast.literal_eval("[\""+response+"\"]")
        return ast.literal_eval(ensure_format_list(response))

    def get_prompt(self, text, model="text-davinci-003", temperature=1, max_tokens=1000, stop="."):
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
        response = response['choices'][0]['text'].strip()
        # print(response)
        # print(response[:2])
        # print(response[-2:])
        # if response[:2]=="[\"" and response[-2:]=="\"]":
        #     return ast.literal_eval(response)
        # elif response[:2]=="[\"" and response[-2:]!="\"]":
        #     # print("Here")
        #     # print(response['choices'][0]['text']+"\"]")
        #     return ast.literal_eval(response+"\"]")
        # elif response[:2]!="[\"" and response[-2:]=="\"]":
        #     return ast.literal_eval("[\""+response)
        # else:
        #     return ast.literal_eval("[\""+response+"\"]")
        return ast.literal_eval(ensure_format_list(response))

    def ner(self, text, model="ttext-davinci-003", temperature=1, max_tokens=1000, stop="."):
        payload = {
            "model": model,
            "prompt": "Recognize different entitites from the following text a give the result strictly in the format [\"X\", \"Y\"] where X is the category or type of entity and Y is the word captured: "+ text,
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
        response = response['choices'][0]['text'].strip()
        # if response[:2]=="[[\"" and response[-2:]=="\"]]":
        #     return get_dict(response)
        # elif response[:2]=="[[\"" and response[-2:]!="\"]]":
        #     # print("Here")
        #     # print(response['choices'][0]['text']+"\"]")
        #     return get_dict(response+"\"]]")
        # elif response[:2]!="[[\"" and response[-2:]=="\"]]":
        #     return get_dict("[[\""+response)
        # else:
        #     return get_dict("[[\""+response+"\"]]")
        return get_dict(ensure_format_dict(response))

    def generate_questions(self, text, model="text-davinci-003", temperature=1, max_tokens=1000, stop=".", questions=5):
        payload = {
            "model": model,
            "prompt": "Analyze the following text and prepare a set of "+str(questions)+" questions and answers. The ouput format is strictly only [[\"A\", \"B\"]] where A is the question and B the answer. No need to specify which is what. The next part is the text: "+ text,
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
        response = response['choices'][0]['text'].strip()
        # if response[:2]=="[[\"" and response[-2:]=="\"]]":
        #     return get_dict(response)
        # elif response[:2]=="[[\"" and response[-2:]!="\"]]":
        #     # print("Here")
        #     # print(response['choices'][0]['text']+"\"]")
        #     return get_dict(response+"\"]]")
        # elif response[:2]!="[[\"" and response[-2:]=="\"]]":
        #     return get_dict("[[\""+response)
        # else:
        #     return get_dict("[[\""+response+"\"]]")
        return get_dict(ensure_format_dict(response)[3:])
        
    def list_models(self):
        return ["text-davinci-003", "text-curie-001", "text-babbage-001", "text-ada-001"]