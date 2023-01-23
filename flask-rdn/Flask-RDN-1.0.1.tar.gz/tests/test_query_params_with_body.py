# clients
from src.flask_request_data_normalizer import RequestDataNormalizer
from flask import Flask
import unittest

# utils
from tests.utils import QueryURLtoResultMapping, call_wrapper
from flask import request

# typing
from decimal import Decimal

class TestQueryParamsWithBody(unittest.TestCase):
    """
        Tests for Flask's ability to parse query strings and request bodies to dictionaries:
            - Combining both dictionaries with no overlaps
            - Combining both dictionaries with overlaps
    """

    app = Flask(__name__)
    my_extension = RequestDataNormalizer(app)
    app.testing = True

    def test_handle_request_with_query_param_and_body(self):
        """
        Test requests with one key/value in query params and the same in body params
        """

        validate = QueryURLtoResultMapping("test=val", {"test": "val"})
        body = {"body": "val"}

        # Validations to run on each call
        def validator(_, __):
            assert request.args == validate.result
            assert request.values.to_dict() == validate.result
            assert request.json == {**validate.result,  **body}
            assert request.get_json() ==  {**validate.result,  **body}

        # Make calls to specified URL with specified methods with optional body
        call_wrapper(self.app, validator, validate.url, body)
    
    def test_handle_request_with_complex_query_params_and_complex_body(self):
        """
        Test requests with mutiple keys/values in query params and body
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
        
        body = {
            "test6": "val",
            "sub": {
                "list": [
                    1,2,3, {
                        "deep_obj": None
                    }
                ]
            },
            "1": False
        }

        # Validations to run on each call
        def validator(_, __):
            assert request.args == validate.result
            assert request.values.to_dict() == validate.result
            assert request.json == {**body, **validate.result}
            assert request.get_json() == {**body, **validate.result}

        # Make calls to specified URL with specified methods with optional body
        call_wrapper(self.app, validator, validate.url, body)

    def test_handle_request_with_overlapping_query_params_body_params(self):
        """
        Test requests with mutiple keys/values in query params and body that overlap
        Body params take precedence
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
        
        body = {
            "test3": "val",
            "sub": {
                "list": [
                    1,2,3, {
                        "deep_obj": None
                    }
                ]
            },
            "test2": False
        }

        final = {
            "test": Decimal("0.3"),
            "test2": False,
            "test3": "val",
            "test4": -1,
            "test5": "-1a",
            "sub": {
                "list": [
                    1,2,3, {
                        "deep_obj": None
                    }
                ]
            }
        }

        # Validations to run on each call
        def validator(_, __):
            assert request.args == validate.result
            assert request.values.to_dict() == validate.result
            assert request.json == final
            assert request.get_json() == final

        # Make calls to specified URL with specified methods with optional body
        call_wrapper(self.app, validator, validate.url, body)