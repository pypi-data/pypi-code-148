"""Tests http_interaction module"""

import unittest
from webinteractions import http_request, get_file_data

class HttpTestMethods(unittest.TestCase):
    """Contains test cases for testing http_interaction module"""
    def setUp(self):
        """Initializing different urls used in testing"""
        self.invalid_url = "test.com"
        self.authentication_required_url = "https://officerakuten.sharepoint.com/sites/GlobalPortal/Pages/top.aspx"
        self.open_api_url = "https://catfact.ninja/fact"
        self.file_url = "https://raw.githubusercontent.com/Vinesh0299/python-learning/main/web_interactions_python/test/setup.py"

    def test_empty_url(self):
        """Function tests to check if ValueError is being raised on empty url"""
        with self.assertRaises(ValueError):
            http_request()

    def test_invalid_url(self):
        """Functions tests for invalid urls"""
        with self.assertRaises(ValueError):
            http_request(url=self.invalid_url)

    def test_invalid_request(self):
        """Function tests for invalid requests"""
        self.assertEqual(http_request(url=self.open_api_url, data={"method": "POST"}), {"message": "Invalid request", "status": 405})

    def test_open_api(self):
        """Function tests the result from an open api url"""
        self.assertEqual(http_request(url=self.open_api_url)['status'], 200)

    def test_invalid_data(self):
        """Function tests for invalid data type"""
        with self.assertRaises(TypeError):
            http_request(url=self.open_api_url, data="TEST")

    def test_file_data(self):
        """Function tests the output of a file url"""
        self.assertEqual(get_file_data(url=self.file_url), ["from setuptools import setup, find_packages\n", '\n', 'setup(name="webinteractions", packages=find_packages())'])


if __name__ == "__main__":
    unittest.main()
