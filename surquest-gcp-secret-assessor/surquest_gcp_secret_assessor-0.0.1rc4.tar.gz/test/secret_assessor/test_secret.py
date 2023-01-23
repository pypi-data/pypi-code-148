# import external modules
import os
import sys
from google.oauth2 import service_account
from unittest import TestCase

sys.path.append(os.getenv("SRC_DIR"))

# import internal modules
from surquest.GCP.secrets_assessor import Secret, exceptions


class TestSecret(TestCase):

    def test__get_secret__from_env_var(self):
        """Method tests the get method of the Secret class

        Scenario: get secret from environment variable
        """

        secret_value = "This is a secret"
        os.environ["MY_SECRET"] = secret_value
        assert secret_value == Secret.get("MY_SECRET")

    def test__get_secret__from_GCP__success(self):
        """Method tests the get method of the Secret class

        Scenario: get secret from GCP Secret Manager
        """

        secret_name = "dev--credentials--app-store"
        key_file = "/opt/project/credentials/keyfile.json"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_file

        secret_value = Secret.get(secret_name)
        assert str == type(secret_value)

    def test__get_secret__from_GCP__error(self):
        """Method tests the get method of the Secret class

        Scenario: get secret from GCP Secret Manager
        """

        secret_name = "unknown-secret"
        key_file = "/opt/project/credentials/keyfile.json"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_file

        try:
            Secret.get(secret_name)
        except Exception as e:
            assert True is isinstance(e, exceptions.SecretsAssessorError)

    def test__get_credentials(self):
        """Method tests the get_credentials method of the Secret class

        Scenario: get secret from GCP Secret Manager
        """

        key_file = "/opt/project/credentials/keyfile.json"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_file

        credentials = Secret.get_credentials()

        assert True is isinstance(
            credentials,
            service_account.Credentials
        )



