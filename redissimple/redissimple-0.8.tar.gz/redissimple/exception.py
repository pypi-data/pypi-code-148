class RedisSimpleException(Exception):

    def __init__(self, error_code, exp=""):
        self.error_code = error_code
        self.root_exception = exp

