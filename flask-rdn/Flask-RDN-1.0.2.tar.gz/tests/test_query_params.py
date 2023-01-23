# clients
from src.flask_request_data_normalizer import RequestDataNormalizer
from flask import Flask
import unittest

# utils
from tests.utils import QueryURLtoResultMapping, call_wrapper
from flask import request

# typing
from decimal import Decimal

class TestQueryParams(unittest.TestCase):
    """
        Tests for Flask's ability to parse query strings in incoming
        requests to dictionaries:
            - Regressions for parsing standard query strings and 
                reading them from Request.args and Request.values. 
            - New functionality for reading parsed query strings from Request.get_json()
                and Request.json
    """

    app = Flask(__name__)
    my_extension = RequestDataNormalizer(app)
    app.testing = True

    def test_handle_basic_request(self):
        """
        Test simple requests with one key/value in query params
        """

        validate = QueryURLtoResultMapping("test=val", {"test": "val"})

        # Validations to run on each call
        def validator(_, __):
            assert request.args == validate.result
            assert request.values.to_dict() == validate.result
            assert request.json == validate.result
            assert request.get_json() == validate.result

        # Make calls to specified URL with specified methods with optional body
        call_wrapper(self.app, validator, validate.url)

    def test_handle_basic_multiple_args(self):
        """
        Test simple requests with mutiple keys/values in query params
        """

        validate = QueryURLtoResultMapping(
            "test=0.3&test2=True&test3=1&test4=-1&test5=-1a", 
            {
                "test": Decimal("0.3"),
                "test2": True,
                "test3": 1,
                "test4": -1,
                "test5": "-1a"
            })

        # Validations to run on each call
        def validator(_, __):
            assert request.args == validate.result
            assert request.values.to_dict() == validate.result
            assert request.json == validate.result
            assert request.get_json() == validate.result

        # Make calls to specified URL with specified methods with optional body
        call_wrapper(self.app, validator, validate.url)
