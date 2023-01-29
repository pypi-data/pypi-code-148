"""This main module

"""
import argparse
import os

from catchword import trie
from catchword import handler


def read_file(filepath: str) -> list:
    """Reads a file returns a list of lines from the file

    This function only supports ".txt" file and the file should fit in the memory.

    I implemented this solution assuming that "Search Term" exists on the last line of the file at all times.
    So this solution needs to have error handling in case there is no "Search Term"

    If the file is too big, we could try:
        1. Separate the file into smaller files, find the "Search Term" and do the process.
        2. If we know what the "Search Term" looks like, we could simply find the "Search Term",
            store it, and do the process by reading the file line by line
        ...

    Args:
        filepath: Absolute path of a file

    Returns:
        A list containing lines from the file

    Raises:
        TypeError: If filename extension is not .txt

    """

    file_extension = os.path.splitext(filepath)[1]

    match file_extension:
        case ".txt" | ".TXT":
            with open(filepath, "r", encoding="utf-8") as file:
                lines = file.readlines()

        case _:
            raise TypeError(
                f"Error occured! '{file_extension}' is not supported, expected file of '.txt'."
            )

    return lines


def main():
    """Main function

    This takes an argument (file path), reads the file, extracts words,
    finds the matches, and prints the output.

    """

    parser = argparse.ArgumentParser(
        description="This is solution for coding test!",
        usage="solution [FILEPATH]",
    )

    parser.add_argument("filepath")

    args = parser.parse_args()

    num_words_in_source_text = 3

    file_path = args.filepath

    text_lines = read_file(file_path)

    try:
        source_text = text_lines[:-1]

        search_term = text_lines[-1]

    except IndexError:
        print("Error! File is empty or file can not be read. Please check your file.")
        source_text = []
        search_term = ""

    words_in_line = handler.extract_word(source_text, num_words_in_source_text)

    tree = trie.Trie()

    tree.insert(search_term)

    result = []

    for words in words_in_line:
        for word in words:
            if tree.search_substring(word):
                result.append(words)
                break

    if not result:
        print("There is no word that matches with Search Term")

    else:
        for matched_word in result:
            print("[" + " ".join(matched_word) + "]")

    return 0


if __name__ == "__main__":
    main()
