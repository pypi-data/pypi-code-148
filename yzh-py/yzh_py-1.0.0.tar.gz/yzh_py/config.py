class Config(object):
    def __init__(self, host, dealer_id, sign_type, app_key, des3key, private_key: str, public_key: str):
        self.host = host
        self.dealer_id = dealer_id
        self.sign_type = sign_type
        self.app_key = app_key
        self.des3key = des3key
        self.private_key = private_key
        self.public_key = public_key
        self.check_config()

    def check_config(self):
        if self.private_key is not None:
            self.private_key = self.private_key.strip()
        if self.public_key is not None:
            self.public_key = self.public_key.strip()
        if self.sign_type != "sha256" and self.sign_type != "rsa":
            raise ValueError('wrong encrypt type')
        if self.host is None:
            self.host = "https://api-service.yunzhanghu.com"
