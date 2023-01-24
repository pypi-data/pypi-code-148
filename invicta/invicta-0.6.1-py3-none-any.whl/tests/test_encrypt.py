"""Unit testing for encryption functionality."""

import unittest

from .. import cipher


class TestCaesarEncrypt(unittest.TestCase):
    def test_caesar_encrypt_positive_char(self):
        char = "a"
        positive_shift = 1

        result = cipher.caesar_encrypt_char(char, positive_shift)

        self.assertEqual(result, "b")

    def test_caesar_encrypt_negative_char(self):
        char = "a"
        negative_shift = -1

        result = cipher.caesar_encrypt_char(char, negative_shift)
        
        self.assertEqual(result, "z")

    def test_caesar_encrypt_char_upper_preserves_case(self):
        upper_char = "A"
        result = cipher.caesar_encrypt_char(upper_char, 1)
        
        self.assertEqual(result, "B")

    def test_caesar_encrypt_positive_text(self):
        string = "aa"
        positive_shift = 1

        result = cipher.caesar_encrypt_text(string, positive_shift)

        self.assertEqual(result, "bb")

    def test_caesar_encrypt_negative_text(self):
        string = "aa"
        negative_shift = -1

        result = cipher.caesar_encrypt_text(string, negative_shift)

        self.assertEqual(result, "zz")

    def test_caesar_encrypt_text_upper_preserves_case(self):
        upper_string = "AA"
        result = cipher.caesar_encrypt_text(upper_string, 1)

        self.assertEqual(result, "BB")

    def test_caesar_encrypt_fractional_shift_is_rounded(self):
        string = "aa"
        fractional_shift = 1.2

        result = cipher.caesar_encrypt_text(string, fractional_shift)

        self.assertEqual(result, "bb")

    def test_caesar_encrypt_empty_string_returns_empty(self):
        empty_str = ""
        result = cipher.caesar_encrypt_text(empty_str, 1)

        self.assertEqual(result, empty_str)

    def test_caesar_encrypt_non_ascii_chars_preserved(self):
        non_ascii_str = "→⁷∴°"
        result = cipher.caesar_encrypt_text(non_ascii_str, 1)

        self.assertEqual(result, non_ascii_str)

    def test_caesar_encrypt_control_chars_preserved(self):
        control_str = "\x16\x1E\x7F"
        result = cipher.caesar_encrypt_text(control_str, 1)

        self.assertEqual(result, control_str)


