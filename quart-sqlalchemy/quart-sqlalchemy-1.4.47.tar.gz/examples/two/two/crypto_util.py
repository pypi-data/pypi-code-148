import base64

import boto3
from mypy_boto3_kms.client import KMSClient


def get_kms_client() -> KMSClient:
    """
    Returns a KMS client
    """
    return boto3.client("kms")


def encrypt(key_id: str, value: str, kms: KMSClient) -> str:
    """
    Takes a KMS key id, encrypts the value using it and
    returns the encrypted value
    """
    response = kms.encrypt(KeyId=key_id, Plaintext=value.encode())
    return base64.b64encode(response["CiphertextBlob"]).decode()


def decrypt(key_id: str, value: str, kms: KMSClient) -> str:
    """
    Takes a KMS key id, decrypts the value using it and
    returns the decrypted value
    """
    response = kms.decrypt(
        KeyId=key_id,
        CiphertextBlob=bytes(base64.b64decode(value)),
    )
    return response["Plaintext"].decode()
