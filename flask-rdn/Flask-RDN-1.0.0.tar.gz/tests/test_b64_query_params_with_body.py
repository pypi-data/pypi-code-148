# clients
from src.flask_request_data_normalizer import RequestDataNormalizer
from flask import Flask
import unittest

# utils
from tests.utils import QueryURLtoResultMapping, call_wrapper
from flask import request

# typing
from decimal import Decimal

class TestBase64QueryParamsWithBody(unittest.TestCase):
    """
        Tests for Flask's ability to parse base64 encoded query strings in incoming
        requests to dictionaries with an additional request body:
            - New functionality for reading parsed base64 query strings from Request.args,
              Request.value, Request.get_json() and Request.json with a request body
            - Overlap handling with request bodies, request body takes precedence
    """

    app = Flask(__name__)
    my_extension = RequestDataNormalizer(app)
    app.testing = True

    def test_handle_request_with_basic_b64_query_string_and_body(self):
        """
        Test requests with one base64 encoded key/value pair in the query string and
        a key/value pair in the request body
        """

        validate = QueryURLtoResultMapping("q=IkhlbGxvIg==", {"q": "Hello"})
        body = {"body": "val"}

        # Validations to run on each call
        def validator(_, __):
            assert request.args == validate.result
            assert request.values.to_dict() == validate.result
            assert request.json == {**body, **validate.result}
            assert request.get_json() == {**body, **validate.result}

        # Make calls to specified URL with specified methods with optional body
        call_wrapper(self.app, validator, validate.url, body)

    def test_handle_request_with_complex_b64_query_string_and_body(self):
        """
        Test requests with complex base64 encoded key/value pairs in the query string
        and complex key/value pairs in the request body
        """

        validate = QueryURLtoResultMapping("data=eyJuZXN0ZWQiOnsiYSI6ImEiLCJiIjoiYiJ9LCJsaXN0IjpbMSx7ImluIjoibGlzdCJ9LHRydWVdfQ==", {
            'data': {
                'nested': {
                    'a': 'a', 'b': 'b'
                }, 
                'list': [1, {'in': 'list'}, True]
            }
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

        # Validations to run on each call
        def validator(_, __):
            assert request.args == validate.result
            assert request.values.to_dict() == validate.result
            assert request.json == {**body, **validate.result}
            assert request.get_json() == {**body, **validate.result}

        # Make calls to specified URL with specified methods with optional body
        call_wrapper(self.app, validator, validate.url, body)

    def test_handle_request_with_mixed_b64_query_string_and_overlapping_body(self):
        """
        Test requests with mixed base64 encoded and regular key/value pairs in the query string
        and a body that overlaps on a key.
        The body takes precedence
        """

        validate = QueryURLtoResultMapping("hello%20world=eyJ0ZXN0IjogeyJuZXN0ZWQiOiAxfSwgInRlc3QyIjogW3siaGkiOiAiVGhlcmUifV0sICJ0ZXN0MyI6IDMuMTR9", {
            "hello world": {
                "test": {
                    "nested": 1
                }, 
                "test2": [{"hi": "There"}], "test3": Decimal("3.14")
            }
        })

        body = {
            "hello world": {
                "test": {
                    "nested": Decimal("0.3")
                },
                "list": False
            }
        }

        final = {
            "hello world": {
                "test": {
                    "nested":"0.3"
                },
                "list": False,
                "test2": [{"hi": "There"}], "test3": Decimal("3.14")
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
