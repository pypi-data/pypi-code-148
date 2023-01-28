import re as __re

def __indent(__str:str):
    return len(__str) - len(__str.lstrip())

def __first_letter_match(__str:str):
    return __re.search("[a-zA-Z]", __str)

def __from_match_start(__str:str,__match:__re.Match):
    return __str[__match.start() if __match else 0 :]

def __from_first_letter(__str:str):
    match = __first_letter_match(__str)
    return __from_match_start(__str,match)

def from_first_letter(__str:str):
    return __from_first_letter(__str)

def indent(__str:str):
    return __indent(__str)
