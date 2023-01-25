import boto3
import requests
import uuid
from boto3 import Session
from botocore.credentials import RefreshableCredentials
from botocore.session import get_session
from functools import lru_cache
from spackle import log

from spackle.exceptions import SpackleException


class DynamoDB:
    adapter_config = None

    def __init__(self):
        self.client = self._bootstrap_client()

    def get_item(self, key):
        if not self.adapter_config:
            raise SpackleException("Adapter not configured")

        return self.client.get_item(
            TableName=self.adapter_config["table_name"],
            Key={
                "AccountId": {"S": self.adapter_config["identity_id"]},
                **key,
            },
        )

    def query(self, KeyConditionExpression, ExpressionAttributeValues, **kwargs):
        if not self.adapter_config:
            raise SpackleException("Adapter not configured")

        return self.client.query(
            TableName=self.adapter_config["table_name"],
            KeyConditionExpression=f"AccountId = :account_id AND {KeyConditionExpression}",
            ExpressionAttributeValues={
                ":account_id": {"S": self.adapter_config["identity_id"]},
                **ExpressionAttributeValues,
            },
            **kwargs,
        )

    def _bootstrap_client(self):
        log.log_debug("Bootstrapping DynamoDB client...")

        session_credentials = RefreshableCredentials.create_from_metadata(
            metadata=self._refresh_credentials(),
            refresh_using=self._refresh_credentials,
            method="sts-assume-role-with-web-identity",
        )
        session = get_session()
        session._credentials = session_credentials
        autorefresh_session = Session(botocore_session=session)
        return autorefresh_session.client(
            "dynamodb", region_name=self.adapter_config["region"]
        )

    def _refresh_credentials(self):
        log.log_debug("Refreshing credentials...")
        self._configure()
        return self._fetch_credentials()

    def _configure(self):
        from spackle import api_key, api_base

        session = requests.post(
            f"{api_base}/sessions",
            headers={"Authorization": f"Bearer {api_key}"},
        ).json()

        self.adapter_config = session["adapter"]
        log.log_debug("Configured adapter: %s" % session)

        return session

    def _fetch_credentials(self):
        if not self.adapter_config:
            raise SpackleException("Adapter not configured")

        log.log_debug("Assuming aws role %s..." % self.adapter_config["role_arn"])
        sts_client = boto3.client("sts")
        response = sts_client.assume_role_with_web_identity(
            RoleArn=self.adapter_config["role_arn"],
            RoleSessionName=str(uuid.uuid4()),
            WebIdentityToken=self.adapter_config["token"],
        )

        return {
            "access_key": response["Credentials"]["AccessKeyId"],
            "secret_key": response["Credentials"]["SecretAccessKey"],
            "token": response["Credentials"]["SessionToken"],
            "expiry_time": response["Credentials"]["Expiration"].isoformat(),
        }


@lru_cache(maxsize=1)
def get_client():
    log.log_debug("Creating DynamoDB client...")
    return DynamoDB()
