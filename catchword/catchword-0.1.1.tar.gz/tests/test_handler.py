import pytest

from catchword.handler import extract_word


def test_extract_word():

    test_first_lines = [
        "908^one)-234@923two22three",
        "55t55)-234s@$!äet",
        "term",
    ]
    test_second_lines = ["term"]

    assert extract_word(test_first_lines, 3) == [
        ["one", "two", "three"],
        ["t", "s", "et"],
    ]

    assert extract_word(test_second_lines) == []
