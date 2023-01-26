import boto3
import hmac
import hashlib
import base64

from botocore.exceptions import ClientError

from ..base import UserManager


def new_instance(**kwargs):
    return CognitoUserMgr(**kwargs)


class CognitoUserMgr(UserManager):

    def __init__(self, user_pool_id, client_id, client_secret, **kwargs):
        self.idp = boto3.client('cognito-idp')
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self.client_secret = client_secret

    def close(self):
        self.idp.close()

    def _make_hash(self, username):
        return base64.b64encode(hmac.new(
            bytes(self.client_secret, 'utf-8'),
            bytes(username + self.client_id, 'utf-8'),
            digestmod=hashlib.sha256).digest()).decode()

    def add_user(self, username, password, email, **kwargs):
        # TODO ユーザ属性をどのように設定するか？
        response = self.idp.admin_create_user(
            UserPoolId=self.user_pool_id,
            Username=username,
            TemporaryPassword=password,
            UserAttributes=[
                {
                    "Name": "email",
                    "Value": email
                },
                {
                    "Name": "email_verified",
                    "Value": "true"
                }
            ],
            MessageAction="SUPPRESS"
        )
        print(response)

        response = self.idp.admin_initiate_auth(
            UserPoolId=self.user_pool_id,
            ClientId=self.client_id,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
                'SECRET_HASH': self._make_hash(username)
            }
        )

        print(response)

        session = response['Session']

        response = self.idp.admin_respond_to_auth_challenge(
            UserPoolId=self.user_pool_id,
            ClientId=self.client_id,
            ChallengeName='NEW_PASSWORD_REQUIRED',
            ChallengeResponses={
                'USERNAME': username,
                'NEW_PASSWORD': password,
                'SECRET_HASH': self._make_hash(username)
            },
            Session=session
        )
        print(response)

    def delete_user(self, username):
        response = self.idp.admin_delete_user(
            UserPoolId=self.user_pool_id,
            Username=username
        )
        print(response)

    def is_exist_user(self, username):
        try:
            response = self.idp.admin_get_user(
                UserPoolId=self.user_pool_id,
                Username=username
            )
            print(response)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'UserNotFoundException':
                return False
            raise

    def add_user_to_group(self, username, groupname):
        self.idp.admin_add_user_to_group(
            UserPoolId=self.user_pool_id,
            Username=username,
            GroupName=groupname
        )

    def add_group(self, groupname, description=''):
        self.idp.create_group(
            UserPoolId=self.user_pool_id,
            GroupName=groupname,
            Description=description
        )

    def delete_group(self, groupname):
        self.idp.delete_group(
            UserPoolId=self.user_pool_id,
            GroupName=groupname
        )

    def list_users(self, groupname, limit=60, nexttoken=''):
        # TODO Paging対応する。
        return self.idp.list_users_in_group(
            UserPoolId=self.user_pool_id,
            GroupName=groupname,
            Limit=limit,
            # NextToken=nexttoken
        )
