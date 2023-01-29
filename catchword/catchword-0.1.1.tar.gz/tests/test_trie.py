import pytest

from catchword.trie import Trie


@pytest.fixture
def trie():
    test_search_term = "k"

    trie = Trie()
    trie.insert(test_search_term)

    return trie


def test_search(trie):
    test_firt_word = "ground"
    test_second_test_word = "sky"

    assert not trie.search_substring(test_firt_word)
    assert trie.search_substring(test_second_test_word)
