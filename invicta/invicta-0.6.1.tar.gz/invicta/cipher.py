"""Caesar encryption."""

import string

ALPHABET_LENGTH = 26


def can_caesar_encrypt(text: str) -> bool:
    """Check whether the given `str` is Caesar-modifiable.

    Returns `True` if any character in `text` is present in
    `string.ascii_letters`.
    """
    for char in text:
        if char in string.ascii_letters:
            return True

    return False

def caesar_encrypt_char(char: str, shift: int) -> str:
    """Apply Caesar encryption to a character.

    Keyword arguments:
        char (str): A string of length 1.
        shift (int): The number of alphabet positions to shift by. This
            value can be negative, and will be rounded to the nearest
            integer.

    Returns a `str` containing the resulting ciphertext.

    See the equation described in
        https://en.wikipedia.org/wiki/Caesar_cipher#Example.
    """

    ZERO_SHIFT = 65

    if not can_caesar_encrypt(char):
        return char

    # In this algorithm, we will use the following scheme:
    # A → 0, B → 1, C → 2, ...

    # Convert the plaintext to uppercase, as this corresponds with our scheme.
    char_upper = char.upper()

    # Subtract a fixed "zero shift" value from the char's ASCII value, to
    # enumerate it according to our scheme. For instance, "A" → 0.
    zero_shifted = ord(char_upper) - ZERO_SHIFT

    # Apply the Caesar Cipher formula to find the post-encryption ASCII value.
    # The modulo operation ensures no overflow occurs (i.e. a value over 26),
    # and allows a loop-back sort of encryption, such as Z forward to B by 
    # a shift of +3.
    zero_shifted_encrypted = (zero_shifted + round(shift)) % ALPHABET_LENGTH
    char_encrypted = chr(zero_shifted_encrypted + ZERO_SHIFT)

    if char.islower():
        return char_encrypted.lower()

    return char_encrypted


def caesar_encrypt_text(text: str, shift: int) -> str:
    """Apply Caesar encryption to the given string.

    Keyword arguments.
        text (str): The plaintext to encrypt.
        shift (int): The number of alphabet positions to shift by. This
        value can be negative.

    Returns a `str` containing the resulting ciphertext.
    """
    result = ""

    # Yes, a map() or list comprehension is appropriate here, but I consider
    # this more readable.
    for char in text:
        result += caesar_encrypt_char(char, shift)

    return result


def caesar_decrypt_text(text: str) -> list[str]:
    """Decrypt the given Caesar ciphertext.

    Returns a `list[str]` containing all possibilities for the original
        plaintext.
    """
    result = []

    # We only need 1 shift for each letter in the alphabet, as duplicates
    # will occur after this.
    for i in range(1, ALPHABET_LENGTH):
        result.append(caesar_encrypt_text(text, i))

    return result


