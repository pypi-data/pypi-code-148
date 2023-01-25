from eolymp.cognito import cognito_pb2
from eolymp.cognito.cognito_http import CognitoClient
from eolymp.wellknown import expression_pb2

from peolymp.abstract import AbstractAPI


class CognitoAPI(AbstractAPI):

    def __init__(self, **kwargs):
        super(CognitoAPI, self).__init__(**kwargs)
        self.client = CognitoClient(self.http_client)

    def find_user_by_nickname(self, nickname):
        s = expression_pb2.ExpressionString(value=nickname)
        setattr(s, 'is', 1)
        f = cognito_pb2.ListUsersInput.Filter(username=[s])
        users_input = cognito_pb2.ListUsersInput(filters=f)
        o = self.client.ListUsers(users_input)
        if len(o.items) == 0:
            return None
        return o.items[0]

    def find_user_by_id(self, user_id):
        return self.client.DescribeUser(cognito_pb2.DescribeUserInput(user_id=user_id)).user
