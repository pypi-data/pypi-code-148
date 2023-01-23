# clients
from src.flask_request_data_normalizer import RequestDataNormalizer
from flask import Flask
import unittest

# utils
from tests.utils import call_wrapper
from flask import request

class TestBasicOperations(unittest.TestCase):
    """
        Regression tests for common Flask functionality that
        should be preserved by this extenstion.
    """

    app = Flask(__name__)
    my_extension = RequestDataNormalizer(app)
    app.testing = True

    def test_handle_request_no_params(self):
        """
        Test simple requests with no query or form params.
        Ensure request args, values, and json are empty
        """

        # Validations to run on each call
        def validator(_, __):
            assert request.args is None
            assert not request.values
            assert request.json is None
            assert request.get_json() is None

        # Make calls to specified URL with specified methods with optional body
        call_wrapper(self.app, validator)

    def test_handle_request_body(self):
        """
        Test simple requests with a single body param
        """

        body = {"test": "val"}

        # Validations to run on each call
        def validator(_, __):
            assert request.args is None
            assert not request.values 
            assert request.json == body
            assert request.get_json() == body

        # Make calls to specified URL with specified methods with optional body
        call_wrapper(self.app, validator, body=body)

    def test_handle_complex_request_body(self):
        """
        Test simple requests with a comples body params
        """

        body = {
            "test": "val",
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
            assert request.args is None
            assert not request.values 
            assert request.json == body
            assert request.get_json() == body

        # Make calls to specified URL with specified methods with optional body
        call_wrapper(self.app, validator, body=body)
