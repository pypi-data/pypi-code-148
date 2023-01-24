"""Unit tests for validating Caesar encryption."""

import unittest

from .. import cipher


class TestCanCaesarEncrypt(unittest.TestCase):
    def test_can_caesar_encrypt_valid_returns_true(self):
        valid_plaintext = "Hello, world"
        result = cipher.can_caesar_encrypt(valid_plaintext)

        self.assertTrue(result)

    def test_can_encrypt_invalid_returns_false(self):
        invalid_plaintext = "1"
        result = cipher.can_caesar_encrypt(invalid_plaintext)

        self.assertFalse(result)

    def test_can_encrypt_empty_returns_false(self):
        empty_str = ""
        result = cipher.can_caesar_encrypt(empty_str)

        self.assertFalse(result)

    def test_can_encrypt_control_returns_false(self):
        control_char_str = "\x01\x13\x07"
        result = cipher.can_caesar_encrypt(control_char_str)
        
        self.assertFalse(result)

    def test_can_encrypt_multi_returns_true(self):
        mixed_str = "a1"
        result = cipher.can_caesar_encrypt(mixed_str)

        self.assertTrue(result)


