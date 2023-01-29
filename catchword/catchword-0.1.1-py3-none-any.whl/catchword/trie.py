"""This module implement and use prefix tree data structure.

See details at
https://en.wikipedia.org/wiki/Trie

Typical usage example:
    trie = Trie()
    trie.insert(str)
    result = trie.search(str)
"""


class TrieNode:
    """Implements a node for prefix tree.

    Attributes:
        children: A dictionary indicating children of the current node.
        end_of_word: A boolean indicating if it is the end of a word.
    """

    def __init__(self):
        self.children = {}
        self.end_of_word = False


class Trie:
    """Implements prefix tree.

    Since the "Search Term" always contains a single word we don't necessarily
    need to implement prefix tree data structure.
    But in case, there are more than a single word to store, a prefix tree can be more efficient than
    just using a dictionary.

    Attributes:
        root : A root node.
    """

    def __init__(self):
        """Inits a root node with TrieNode."""
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Inserts a string into the tree.

        Input string should be only with "a - z" (total, 26) lowercase characters.

        Args:
            word: A string you want to store in the tree.

        Returns:
            None

        """

        current = self.root
        
        for character in word:
            if character not in current.children:
                current.children[character] = TrieNode()

            current = current.children[character]

        current.end_of_word = True

        return None

    def search_substring(self, word: str) -> bool:
        """Searchs the input string if it's in the tree.

        Input string should be only with "a - z" (total, 26) lowercase characters.

        Args:
            word: A string you want to search in the tree.

        Returns:
            A boolean that is True if input string in the tree, False otherwise

            If the input string exists in the tree as a substring, it will return
            False.

        """

        current = self.root
        
        for character in word:
            if character in current.children:
                current = current.children[character]

        return current.end_of_word
