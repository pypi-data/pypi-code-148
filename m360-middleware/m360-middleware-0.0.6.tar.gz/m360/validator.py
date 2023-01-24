"""
Copyright (C) 2022 Corsair M360, Inc - All Rights Reserved.
Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
"""

import os
import logging
from jsonschema import RefResolver, Draft7Validator
from jsonschema.exceptions import ValidationError

from m360 import utils

DIR_NAME = os.path.dirname(__file__)
API_SCHEMA_PATH = "schemas/api.json"
CONTRACT_SCHEMA_PATH = "schemas/contract.json"
MIDDLEWARE_SCHEMA_PATH = "schemas/middleware.json"

_logger = logging.getLogger(__name__)

class Validator(object):
    """Offers validator related helper methods"""

    # singleton
    _instance = None

    def __init__(self):
        _logger.debug("Validator created")
        self.schemas = {
            "api": utils.json_file_to_dict(os.path.join(DIR_NAME, API_SCHEMA_PATH)),
            "contract": utils.json_file_to_dict(os.path.join(DIR_NAME, CONTRACT_SCHEMA_PATH)),
            "middleware": utils.json_file_to_dict(os.path.join(DIR_NAME, MIDDLEWARE_SCHEMA_PATH))
        }
        self.schema_store = {
            self.schemas["api"]["$id"]: self.schemas["api"],
            self.schemas["contract"]["$id"]: self.schemas["contract"],
            self.schemas["middleware"]["$id"]: self.schemas["middleware"]
        }
        self.ValidationError = ValidationError

    @staticmethod
    def validator_singleton():
        """Access the singleton receiver"""

        if Validator._instance:
            return Validator._instance

        if not Validator._instance:
            _logger.debug("Creating validator instance")
            Validator._instance = Validator()

        return Validator._instance

    def validate(self, data, schema_name):
        resolver = RefResolver.from_schema(self.schemas.get("api"), store=self.schema_store)
        validator = Draft7Validator(self.schemas.get(schema_name), resolver=resolver)
        return validator.validate(data)


def instance():
    """Get the singleton instance of the validator"""
    _logger.debug("calling instance, os.pid=%d", os.getpid())
    return Validator.validator_singleton()
