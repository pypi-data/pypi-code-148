import unittest

import pandas

from kodra import Kodra, share


# TODO: Add an integration test with a mock HTTP Server
class KodraTest(unittest.TestCase):
    def test_share_invalid_data(self):
        # pylint: disable=no-member
        """Pass a regular dict instead of a Pandas DataFrame to share().
        The method should throw an exception.
        """
        df = {"key1": "Value1", "key2": "Value2"}
        self.assertRaises(AssertionError, Kodra().share, data=df)

    def test_share_empty_data(self):
        # pylint: disable=no-member
        """Pass an empty DataFrame to share().
        The method should throw an exception.
        """
        df = pandas.DataFrame()
        self.assertRaises(ValueError, share, data=df)


if __name__ == "__main__":
    unittest.main()
