import json
from os import path as ospath

script_path = ospath.realpath(__file__)
script_dir_path = ospath.dirname(script_path)


def load_json(f):
    with open(f, 'r') as of:
        return json.load(of)


def get_data_file_path(file):
    return ospath.join(script_dir_path, 'datasets', file)


def get_lang_codes() -> dict:
    return load_json(get_data_file_path('lang.json'))

