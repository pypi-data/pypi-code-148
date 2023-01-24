"""English checks and related utilities."""

import string

from spellchecker import SpellChecker


def strip_to_ascii_letters(initial_string: str) -> str:
    """Remove non-ASCII-letter characters from a string.

    Returns a new `str` stripped of any characters that do not occur
    in `string.ascii_letters`. All whitespace is preserved (as
    determined by str.issspace()).
    """
    result = ""

    for char in initial_string:
        if (char in string.ascii_letters) or (char.isspace()):
            result += char

    return result


def is_english_word(word: str, checker: SpellChecker) -> bool:
    """Check whether a string is an English word.

    Note that a 'word' is defined here as a sequence of
    whitespace-separated ASCII characters; this includes alphanumerics.
    Thus, if `word` contains several of such 'words', this will return
    `False`.

    Understandably, the result of this function can be unpredictable
    for various inflections. It is therefore advised to call this for
    the simplest possible form of a word; e.g. singulars over plurals,
    and infinitives over other conjugations.

    Keyword arguments:
        word: The string to test.
        checker: An instance of pyspellchecker.Spellchecker
    """
    sanitised_word = word.casefold().strip()

    return sanitised_word in checker.known([sanitised_word])


def contains_english(string: str, checker: SpellChecker) -> bool:
    """Returns `True` if the given string contains English text.

    See `is_english_word` for the definition of a 'word'.

    Keyword arguments:
        word: A string to test.
        checker: An instance of pyspellchecker.Spellchecker
    """
    words = string.split(" ")
    words_ascii_letters_only = [strip_to_ascii_letters(word.strip()) for word in words]

    return any([is_english_word(word, checker) for word in words_ascii_letters_only])


