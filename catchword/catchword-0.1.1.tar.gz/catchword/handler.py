"""This module handles file data

"""


def extract_word(source_text_list: list, num_words: int = 3) -> list:
    """Extracts words from "Source Text"

    It extracts words embedded in symbols, numbers, and spaces from the line.
    This function is implemented to extract only "a" - "z" (lowercase) characters.
    If there is a word in the sentence "Figure" then this function will extract only "igure".

    If we're going to extract both lower and upper cases then we need to think about
    case sensitivity in our function.
    Also, we need to think about how we will handle the Unicode characters such as "한글".

    Args:
        source_text_list: A list of lines
        num_words: A number of words in the single-line

    Returns:
        A 2D list including extracted words

    """

    word_list = []

    for source_text in source_text_list:
        tmp = [""]
        for character in source_text:
            if ord("a") <= ord(character) <= ord("z"):
                tmp[-1] += character
            elif tmp[-1]:
                tmp.append("")

        if not tmp[-1]:
            tmp.pop()

        if len(tmp) == num_words:
            word_list.append(tmp)

    return word_list
