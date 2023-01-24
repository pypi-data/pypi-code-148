"""Unit tests for English checks."""

import unittest

import spellchecker

from .. import english


class TestEnglish(unittest.TestCase):
    def setUp(self):
        self.spell_checker = spellchecker.SpellChecker()

    def test_strip_to_ascii_letters_valid(self):
        test_string = "A!"
        result = english.strip_to_ascii_letters(test_string)

        self.assertEqual(result, "A")

    def test_strip_to_ascii_letters_preserves_whitespace(self):
        test_string = "a a!"
        result = english.strip_to_ascii_letters(test_string)

        self.assertEqual(result, "a a")

    def test_is_english_word_true_for_english(self):
        test_word = "the"
        result = english.is_english_word(test_word, self.spell_checker)

        self.assertTrue(result)

    def test_is_english_word_false_for_non_english(self):
        test_word="q"
        result = english.is_english_word(test_word, self.spell_checker)

        self.assertFalse(result)

    def test_is_english_word_false_for_empty(self):
        empty_string = ""
        result = english.is_english_word(empty_string, self.spell_checker)

        self.assertFalse(result)

    def test_contains_english_true_for_english(self):
        test_word = "the"
        result = english.contains_english(test_word, self.spell_checker)

        self.assertTrue(result)

    def test_contains_english_false_for_non_english(self):
        test_word="q"
        result = english.contains_english(test_word, self.spell_checker)

        self.assertFalse(result)

    def test_contains_english_false_for_empty(self):
        empty_string = ""
        result = english.contains_english(empty_string, self.spell_checker)

        self.assertFalse(result)

    def test_contains_english_true_for_mixed(self):
        mixed_string = "q the"
        result = english.contains_english(mixed_string, self.spell_checker)

        self.assertTrue(result)

    def test_contains_english_true_for_mixed_non_letters(self):
        mixed_string = "; the"
        result = english.contains_english(mixed_string, self.spell_checker)

        self.assertTrue(result)


