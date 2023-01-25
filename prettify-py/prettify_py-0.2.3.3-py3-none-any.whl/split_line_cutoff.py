"""
Module to split lines 
"""
import time
import re

from typing import Tuple, Optional


def format_file_line_length(
    file_name: str, cutoff: int, new_file_name: Optional[str] = None
) -> None:

    if new_file_name is not None:
        write_file_name = new_file_name
    else:
        write_file_name = file_name
    lines = split_lines_after_len(
        file_name=file_name, cutoff=cutoff, pattern=" ")

    with open(write_file_name, "w", encoding="UTF-8") as file_out:
        file_out.writelines(lines)


def split_lines_after_len(file_name: str, cutoff: int, pattern: str) -> None:
    """
    The split_lines_after_len function takes in a file name, a cutoff length and a pattern.
    It then splits the lines of the file into two parts if they are longer than the cutoff length.
    The split is done at the first instance of pattern that occurs after (cutoff - len(pattern)) characters

    :param file_name:str: Used to Specify the file name of the text file that you want to split.
    :param cutoff:int: Used to Indicate the length of a line after which it should be split.
    :param pattern:str: Used to Specify the pattern to split on.
    :return: A list of lines.

    :doc-author: Julian M. Kleber
    """

    new_lines = []
    with open(file_name, "rb") as f:

        lines = f.readlines()
    lines = [line.decode("UTF-8").replace(" \n", "\n") for line in lines]
    run = True
    counter = 0
    curr_line = lines[counter]

    while run:
        if counter == 0:

            if len(curr_line) > cutoff:
                start_line, end_line = split_single_line(
                    line=curr_line, num=cutoff, pattern=pattern
                )
                new_lines.append(start_line)
                if len(lines) == 1:
                    run = False
                else:
                    curr_line = end_line + lines[counter + 1]
            else:
                new_lines.append(curr_line)
                curr_line = lines[counter + 1]
        elif counter < len(lines) - 1:

            if len(curr_line) > cutoff:

                start_line, end_line = split_single_line(
                    line=curr_line, num=cutoff, pattern=pattern
                )

                new_lines.append(start_line)
                curr_line = end_line + lines[counter + 1]
            else:

                new_lines.append(curr_line)
                curr_line = lines[counter + 1]

        elif (counter >= len(lines) - 1) and (len(curr_line) > cutoff):

            start_line, end_line = split_single_line(
                line=curr_line, num=cutoff, pattern=pattern
            )
            new_lines.append(start_line)
            curr_line = end_line

        elif (counter >= len(lines) - 1) and (len(curr_line) < cutoff):
            new_lines.append(curr_line)
            run = False
        else:
            print(curr_line)
            raise RuntimeError(
                "There is something wrong in the programming logic. Terminated the while loop"
            )
        counter += 1
    return new_lines


def split_single_line(line: str, num: int, pattern: str) -> Tuple[str, str]:
    """
    The split_single_line function takes a string, and splits it into two strings.
    The first string is the part of the original line that fits within a specified number of characters.
    The second string is the remainder of the original line that does not fit within this character limit.
    This function also takes an optional pattern argument, which specifies what type of characters to split on.

    :param line:str: Used to Pass in the line of text that is to be split.
    :param num:int: Used to Specify the cutoff point.
    :param pattern:str: Used to Determine where to split the line.
    :return: A tuple of two strings.

    :doc-author: Trelent
    """

    idx = get_last_char_before_cutoff(line=line, cutoff=num, pattern=pattern)
    end_line = line[idx:]
    start_line = line[:idx]

    return start_line, end_line


def get_last_char_before_cutoff(line: str, cutoff: int, pattern: str) -> int:
    """
    The get_last_char_before_cutoff function takes a string, a cutoff index, and a pattern.
    It returns the last character in the string that matches the pattern before the cutoff index.

    :param line:str: Used to Specify the string that will be searched for the pattern.
    :param cutoff:int: Used to Specify the cutoff point.
    :param pattern:str: Used to Specify the pattern that you want to find in the string.
    :return: The last index of the pattern in the line that is before cutoff.

    :doc-author: Trelent
    """

    indices_object = re.finditer(pattern=pattern, string=line)
    indices = [index.start() for index in indices_object]
    for i in range(len(indices) - 1, 0, -1):
        if indices[i] <= cutoff:

            return indices[i]


if __name__ == "__main__":
    file_name = "split_lines.txt"
    num = 100
    split_lines_after_len(file_name=file_name, cutoff=num, pattern=" ")
