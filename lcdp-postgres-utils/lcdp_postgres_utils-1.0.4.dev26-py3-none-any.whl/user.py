from .utils import fetch_password_from_ssm


class User:
    name = None
    password = None

    def __init__(self, credentials):
        self.name = credentials['user_name']
        self.password = fetch_password_from_ssm(credentials["user_password"])

    def get_name(self):
        return self.name

    def get_password(self):
        return self.password
