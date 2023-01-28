import random
import string
import uuid
from key_generator.key_generator import generate
from .convert import list2str2


def rannum(number1, number2):
    try:
        output = random.randint(int(number1), int(number2))
        return output
    except ValueError:
        print("Please enter a number1 to number2")

def ranstr(charset):
    try:
        char_set = string.ascii_uppercase + string.digits
        output = ''.join(random.sample(char_set * int(charset), int(charset)))
        return output
    except ValueError:
        print("Please enter a number charset")

def ranuuid(uuid_type='uuid1'):
    if uuid_type == "uuid1":
        return uuid.uuid1()
    elif uuid_type == "uuid4":
        return uuid.uuid4()

def ranchoice(list):
    try:
        output = random.choice(list)
        return output
    except ValueError:
        print("Please enter a list")

def ranchoices(list, number):
    try:
        output = random.choices(list, k=number)
        return output
    except ValueError:
        print("Please enter a list")

def ranshuffle(list):
    try:
        output = random.shuffle(list)
        return output
    except ValueError:
        print("Please enter a list")

def ranuniform(number1, number2):
    try:
        output = random.uniform(number1, number2)
        return output
    except ValueError:
        print("Please enter a number1 to number2")

def ranrandint(number1, number2):
    try:
        output = random.randint(number1, number2)
        return output
    except ValueError:
        print("Please enter a number1 to number2")

def ranrandrange(number1, number2):
    try:
        output = random.randrange(number1, number2)
        return output
    except ValueError:
        print("Please enter a number1 to number2")

def rankeygen(min, max, seed=None):
    if seed is None:
        try:
            return generate(max_atom_len=max, min_atom_len=min).get_key()
        except ValueError:
            print("Please enter a key_type and key_length")
    else:
        try:
            return generate(max_atom_len=max, min_atom_len=min, seed=seed).get_key()
        except ValueError:
            print("Please enter a key_type and key_length")

def rancolor():
    """RGB"""
    return (rannum(1, 255), rannum(1, 255), rannum(1, 255))

def rantextuplow(text):
    nct = list(text)
    ct = []
    for i in nct:
        r = rannum(1, 2)
        if r == 1:
            ct.append(str(i).lower())
        elif r == 2:
            ct.append(str(i).upper())
    return list2str2(ct)

def ranstruplow(charset):
    return rantextuplow(ranstr(charset))

def randistro():
    return f'https://discord.gift/{ranstruplow(23)}'