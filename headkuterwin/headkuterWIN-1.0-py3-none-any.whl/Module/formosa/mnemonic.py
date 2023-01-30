#
# Copyright (c) 2013 Pavol Rusnak
# Copyright (c) 2017 mruddy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import os
import hashlib
import hmac
import itertools
import json
from pathlib import Path
from typing import AnyStr, List, Sequence, TypeVar, Union
import unicodedata


_T = TypeVar("_T")
PBKDF2_ROUNDS = 2048


class ConfigurationError(Exception):
    pass


# Refactored code segments from <https://github.com/keis/base58>
def b58encode(v: bytes) -> str:
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    p, acc = 1, 0
    for c in reversed(v):
        acc += p * c
        p = p << 8

    string = ""
    while acc:
        acc, idx = divmod(acc, 58)
        string = alphabet[idx: idx + 1] + string
    return string


def verify_file(words_dictionary: dict):
    """
        This function does the complete check in the lists and keys of the dictionary according to the Formosa standard

    Parameters
    ----------
    words_dictionary :
        This is the base dictionary containing all lists of words in Formosa standard
    """
    for filling_order_word in words_dictionary["FILLING_ORDER"]:

        current_dict = words_dictionary[filling_order_word]
        # Test if the sequence of restrictions are consistent
        if not words_dictionary[filling_order_word]["RESTRICTED_BY"] == "NONE":
            if not (
                (words_dictionary["FILLING_ORDER"].index(current_dict["RESTRICTED_BY"]) <
                 words_dictionary["FILLING_ORDER"].index(filling_order_word))
            ):
                raise ConfigurationError(
                    "List sequence inconsistent restriction order for %s. (restricted_by checking)."
                    % filling_order_word
                )
        # For every syntactic function restricted by current one
        for restricted_syntax1 in current_dict["RESTRICTS"]:
            for image_word in current_dict[restricted_syntax1]["IMAGE"]:
                for restricted_syntax2 in words_dictionary[restricted_syntax1]["RESTRICTS"]:
                    if not (image_word in list(words_dictionary[restricted_syntax1][restricted_syntax2]["MAPPING"])):
                        raise ConfigurationError(
                            "The word \"%s\" from the image list of \"%s\" is not contained in the keys list"
                            % (image_word, restricted_syntax1)
                        )

            for key in list(current_dict[restricted_syntax1]["MAPPING"]):
                if not (key in current_dict["TOTAL_LIST"]):
                    raise ConfigurationError(
                        "List of keys should be the same, but it is not, "
                        "the key \"%s\" in dictionary of \"%s\" in \"%s\" keys."
                        % (key, filling_order_word, restricted_syntax1)
                    )
            if not (words_dictionary["FILLING_ORDER"].index(restricted_syntax1) >
                    words_dictionary["FILLING_ORDER"].index(filling_order_word)):
                raise ConfigurationError(
                    "List sequence inconsistent restriction order for %s. (restricts checking)."
                    % restricted_syntax1
                )
            # Check there are enough sublists
            if not len(current_dict[restricted_syntax1]["MAPPING"]) >= 2 ** current_dict["BIT_LENGTH"]:
                raise ConfigurationError(
                    "Wordlist of %s should contain %d key words in %s list, but it contains %d key words."
                    % (filling_order_word, 2 ** current_dict["BIT_LENGTH"],
                       restricted_syntax1, len(current_dict[restricted_syntax1]["MAPPING"]))
                )
            # For each syntactic function restricted by current one
            line_bits_length = 2 ** words_dictionary[restricted_syntax1]["BIT_LENGTH"]
            # For each line in the sublist
            for line_key in current_dict[restricted_syntax1]["MAPPING"]:
                list_length = (len(current_dict[restricted_syntax1]["MAPPING"][line_key]))
                # Check whether length has correct value
                if (
                    list_length != line_bits_length
                ):
                    raise ConfigurationError(
                        "Key \"%s\", in \"%s\" restriction, should contain %d words, but it contains %d words."
                        % (line_key, restricted_syntax1, line_bits_length, list_length)
                    )
                for word in current_dict[restricted_syntax1]["MAPPING"][line_key]:
                    if not(word in words_dictionary[restricted_syntax1]["TOTAL_LIST"]):
                        raise ConfigurationError(
                            "Word \"%s\" not found in list of total words in \"%s\"."
                            % (word, restricted_syntax1)
                        )


def concat_idx_of_words(
    passphrase: list,
    concat_bits: list,
    words_dictionary: dict,
    phrase_len: int
) -> list:
    """
        This function maps each word to each index in the restriction list in form of concatenated bits

    Parameters
    ----------
    passphrase : list
        This is the list of words used in Formosa standard
    concat_bits :list
        This is an empty list to be returned as concatenated bits
    words_dictionary : dict
        This is the base dictionary from which the word lists are consulted
    phrase_len : int
        This is the size of phrase used in the Formosa standard

    Returns
    -------
    list
        Returns the concatenated bits mapped from the passphrase
    """
    bit_idx = 0
    restricting_word = ""

    for sentence_idx in range(len(passphrase) // phrase_len):

        current_sentence = passphrase[phrase_len * sentence_idx: phrase_len * (sentence_idx + 1)]

        for syntactic_key in words_dictionary["FILLING_ORDER"]:
            restricted_by = words_dictionary[syntactic_key]["RESTRICTED_BY"]
            natural_word_position = words_dictionary["NATURAL_ORDER"].index(syntactic_key)
            len_word = words_dictionary[syntactic_key]["BIT_LENGTH"]
            current_word = current_sentence[natural_word_position]
            if restricted_by != "NONE":
                restricting_idx = words_dictionary["NATURAL_ORDER"].index(restricted_by)
                restricting_word = current_sentence[restricting_idx]

            wdict_idx = (
                words_dictionary[syntactic_key]["TOTAL_LIST"].index(current_word)
                if words_dictionary[syntactic_key]["RESTRICTED_BY"] == "NONE" else
                words_dictionary[restricted_by][syntactic_key]["MAPPING"][restricting_word].index(current_word)
            )
            if wdict_idx == -1:
                raise LookupError("Unable to find \"%s\" in the \"%s\" word list." % (current_word, restricted_by))

            for wbit_idx in range(len_word):
                concat_bits[bit_idx] = (wdict_idx & (1 << (len_word - 1 - wbit_idx))) != 0
                bit_idx += 1
    return concat_bits


class Mnemonic(object):
    def __init__(self, theme: str):
        
        with open(
            (self._get_directory() / "themes" / ("%s.json" % theme))
        ) as json_file:
            
            self.words_dictionary = json.load(json_file)
            

        verify_file(self.words_dictionary)

    @staticmethod
    def _get_directory() -> Path:
        """
            This method finds out in which directory the code is running

        Returns
        -------
        path
            Returns the absolute path found of the file
        """
        return Path(__file__).parent.absolute()

    @classmethod
    def list_languages(cls) -> List[str]:
        return [
            f.split(".")[0]
            for f in os.listdir(cls._get_directory())
            if f.endswith(".txt")
        ]

    @staticmethod
    def normalize_string(txt: AnyStr) -> str:
        if isinstance(txt, bytes):
            utxt = txt.decode("utf8")
        elif isinstance(txt, str):
            utxt = txt
        else:
            raise TypeError("String value expected")

        return unicodedata.normalize("NFKD", utxt)

    @classmethod
    def detect_language(cls, code: str) -> str:
        #        ------------------------hardcoded------------------------
        #         Returns 'enslish' for temporary list of words
        return "english"
        
#        code = cls.normalize_string(code)
#        first = code.split(" ")[0]
#        languages = cls.list_languages()
#        print(languages)
#
#        for lang in languages:
#            mnemo = cls(lang)
#            if first in mnemo.wordlist:
#                return lang
#
#        raise ConfigurationError("Language not detected")
#        ------------------------hardcoded------------------------

    def generate(self, strength: int = 128) -> str:
        if strength not in range(128, 257, 32):  # [128, 160, 192, 224, 256]:
            raise ValueError(
                "Strength should be one of the following [128, 160, 192, 224, 256], but it is %d."
                % strength
            )
        return self.to_mnemonic(os.urandom(strength // 8))

    # Adapted from <http://tinyurl.com/oxmn476>
    def to_entropy(self, passphrase: Union[List[str], str]) -> bytearray:
        """
            This method extract an entropy and checksum values from passphrase in Formosa standard

        Parameters
        ----------
        passphrase : list or str
            This is the passphrase that is desired to extract entropy from

        Returns
        -------
        bytearray
            Returns a bytearray with the entropy and checksum values extracted from a passphrase in a Formosa standard
        """
        if not isinstance(passphrase, list):
            passphrase = passphrase.split(" ")
        if len(passphrase) not in range(6, 55, 6):
            raise ValueError(
                "Number of words must be one of the following:"
                " 6, 12, 18, 24, 30, 36, 42, 48 or 54, but it is \"%d\"."
                % (len(passphrase))
            )
        phrase_len = len(self.words_dictionary["FILLING_ORDER"])
        # Look up all the words in the list and construct the
        # concatenation of the original entropy and the checksum.

        # Determining strength of password
        entropy_length_bits = len(passphrase) * 32 // 6
        checksum_length_bits = entropy_length_bits // 32
        concat_len_bits = checksum_length_bits + entropy_length_bits

        concat_bits = [False] * concat_len_bits
        concat_bits = (concat_idx_of_words(
            passphrase, concat_bits, self.words_dictionary, phrase_len
        )
        )

        # Extract original entropy as bytes.
        entropy = bytearray(entropy_length_bits // 8)

        # For every entropy byte
        for entropy_idx in range(len(entropy)):
            # For every entropy bit
            for bit_idx in range(8):
                bit_int = 1 if concat_bits[(entropy_idx * 8) + bit_idx] else 0
                entropy[entropy_idx] |= bit_int << (8 - 1 - bit_idx)
        hash_bytes = hashlib.sha256(entropy).digest()
        hash_bits = list(
            itertools.chain.from_iterable(
                [checksum_byte & (1 << (8 - 1 - bit_idx)) != 0
                 for bit_idx in range(8)
                 ] for checksum_byte in hash_bytes
            )
        )

        # Test checksum
        valid = True
        for bit_idx in range(checksum_length_bits):
            valid &= concat_bits[entropy_length_bits + bit_idx] == hash_bits[bit_idx]
        if not valid:
            raise ValueError("Failed checksum.")

        return entropy

    def to_mnemonic(self, data: bytes) -> str:
        """
            This method creates a passphrase in Formosa standard from an entropy and checksum values

        Parameters
        ----------
        data : bytes
            This is the entropy and checksum that is desired to build passphrase from

        Returns
        -------
        str
            Returns a passphrase in a Formosa standard built from a bytes with the entropy and checksum values
        """
        if len(data) not in range(4, 45, 4):
            raise ValueError(
                "Number of phrases should be 1 to 11, but it is \"%d\"."
                % (len(data)//4)
            )
        h = hashlib.sha256(data).hexdigest()
        # Concatenation of string
        b = (
            # String of entropy bits
            bin(int.from_bytes(data, byteorder="big"))[2:].zfill(len(data) * 8)
            # String of checksum bits
            + bin(int(h, 16))[2:].zfill(256)[: len(data) * 8 // 32]
        )

        bit_idx = 0
        ret_list = []
        last_word = ""
        for phrase_idx in range(len(b) // 33):
            current_sentence = ["", "", "", "", "", ""]
            for syntactic_key in self.words_dictionary["FILLING_ORDER"]:
                restricted_by = self.words_dictionary[syntactic_key]["RESTRICTED_BY"]
                syntactic_order = self.words_dictionary["NATURAL_ORDER"].index(syntactic_key)
                len_word = self.words_dictionary[syntactic_key]["BIT_LENGTH"]

                if restricted_by != "NONE":
                    last_idx = self.words_dictionary["NATURAL_ORDER"].index(restricted_by)
                    last_word = current_sentence[last_idx]

                list_of_words = (
                    self.words_dictionary[syntactic_key]["TOTAL_LIST"]
                    if self.words_dictionary[syntactic_key]["RESTRICTED_BY"] == "NONE"
                    else self.words_dictionary[restricted_by][syntactic_key]["MAPPING"][last_word]
                )

                # Integer from substring of zeroes and ones representing index of current word within its list
                wdict_idx = int(b[bit_idx: bit_idx + len_word], 2)
                bit_idx += len_word
                current_sentence[syntactic_order] = list_of_words[wdict_idx]

            ret_list += current_sentence
        ret = " ".join(ret_list)
#        ------------------------hardcoded------------------------
#        if (
#            self.detect_language(" ".join(result)) == "japanese"
#        ):  # Japanese must be joined by ideographic space.
#            result_phrase = u"\u3000".join(result)
#        else:
#            result_phrase = " ".join(result)
#        result_phrase = " ".join(result)
#        ------------------------hardcoded------------------------
        return ret

#    ------------------------hardcoded------------------------
    def check_item(self, mnemonic: str) -> bool:
        mnemonic_list = self.normalize_string(mnemonic).split(" ")
        # list of valid mnemonic lengths
        if len(mnemonic_list) not in range(12, 25, 3):
            return False
        try:
            idx = map(
                lambda x: bin(self.wordlist.index(x))[2:].zfill(11), mnemonic_list
            )
            b = "".join(idx)
        except ValueError:
            return False
        l = len(b)  # noqa: E741
        d = b[: l // 33 * 32]
        h = b[-l // 33:]
        nd = int(d, 2).to_bytes(l // 33 * 4, byteorder="big")
        nh = bin(int(hashlib.sha256(nd).hexdigest(), 16))[2:].zfill(256)[: l // 33]
        return h == nh
#       ------------------------hardcoded------------------------

    def expand_word(self, prefix: str) -> str:
        for i in range(4):
            self.wlist = str(self.wordlist[i][:])
            if prefix in self.wlist:
                return prefix
            else:
                matches = [word for word in self.wlist if word.startswith(prefix)]
                if len(matches) == 1:  # matched exactly one word in the wordlist
                    return matches[0]
                else:
                    # exact match not found.
                    # this is not a validation routine, just return the input
                    return prefix
#       ------------------------hardcoded------------------------

    def expand(self, mnemonic: str) -> str:
        return " ".join(map(self.expand_word, mnemonic.split(" ")))
#   ------------------------hardcoded------------------------

    @classmethod
    def to_seed(cls, mnemonic: str, passphrase: str = "") -> bytes:
        mnemonic = cls.normalize_string(mnemonic)
        passphrase = cls.normalize_string(passphrase)
        passphrase = "mnemonic" + passphrase
        mnemonic_bytes = mnemonic.encode("utf-8")
        passphrase_bytes = passphrase.encode("utf-8")
        stretched = hashlib.pbkdf2_hmac(
            "sha512", mnemonic_bytes, passphrase_bytes, PBKDF2_ROUNDS
        )
        return stretched[:64]

    @staticmethod
    def to_hd_master_key(seed: bytes, testnet: bool = False) -> str:
        if len(seed) != 64:
            raise ValueError("Provided seed should have length of 64")

        # Compute HMAC-SHA512 of seed
        seed = hmac.new(b"Bitcoin seed", seed, digestmod=hashlib.sha512).digest()

        # Serialization format can be found at:
        # https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#Serialization_format
        xprv = b"\x04\x88\xad\xe4"  # Version for private mainnet
        if testnet:
            xprv = b"\x04\x35\x83\x94"  # Version for private testnet
        xprv += b"\x00" * 9  # Depth, parent fingerprint, and child number
        xprv += seed[32:]  # Chain code
        xprv += b"\x00" + seed[:32]  # Master key

        # Double hash using SHA256
        hashed_xprv = hashlib.sha256(xprv).digest()
        hashed_xprv = hashlib.sha256(hashed_xprv).digest()

        # Append 4 bytes of checksum
        xprv += hashed_xprv[:4]

        # Return base58
        return b58encode(xprv)


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        hex_data = sys.argv[1]
    else:
        hex_data = sys.stdin.readline().strip()
    data = bytes.fromhex(hex_data)
    m = Mnemonic("english")
    print(m.to_mnemonic(data))


if __name__ == "__main__":
    main()
