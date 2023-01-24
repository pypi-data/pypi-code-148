"""Unit tests for Caesar decryption."""

import unittest

from .. import cipher


class TestDecrypt(unittest.TestCase):
    def test_caesar_decrypt_word_in_plaintexts(self):
        plaintext = "a"
        encrypted = cipher.caesar_encrypt_text(plaintext, 1)

        self.assertIn(plaintext, cipher.caesar_decrypt_text(encrypted))

    def test_decrypt_words_in_plaintexts(self):
        """Test for multiple words."""
        plaintext = "a b"
        encrypted = cipher.caesar_encrypt_text(plaintext, 1)

        self.assertIn(plaintext, cipher.caesar_decrypt_text(encrypted))


