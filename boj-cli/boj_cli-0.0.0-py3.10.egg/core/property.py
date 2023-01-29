import os

DIR = '/.boj-cli'
BOJ_URL = 'https://acmicpc.net'
KEY_NAME = 'key'
CREDENTIAL_NAME = 'credential'

def temp_dir():
    return str(os.getenv('HOME')) + DIR

def home_url():
    return BOJ_URL

def submit_url():
    return BOJ_URL + "/submit"

def key_file_path():
    return temp_dir() + "/" + KEY_NAME

def credential_file_path():
    return temp_dir() + "/" + CREDENTIAL_NAME
