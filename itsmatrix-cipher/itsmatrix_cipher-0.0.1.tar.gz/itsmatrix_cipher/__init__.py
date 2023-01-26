from random import seed, randint

def encode(string: str, key: int) -> str:
    output = ""

    for char in string:
        seed(key)
        output += chr(ord(char) + randint(1, 10))
        key += 1

    return output

def decode(string: str, key: int) -> str:
    output = ""

    for char in string:
        seed(key)
        output += chr(ord(char) - randint(1, 10))
        key += 1

    return output

def key_from_string(string: str) -> int:
    key = 1

    for char in string:
        key *= ord(char)

    return key

def decode_and_exec(string: str, key: int) -> None:
    exec(decode(string, key))
