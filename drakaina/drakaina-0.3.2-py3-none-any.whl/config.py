from datetime import timedelta


class Config:
    MAX_CONTENT_SIZE = 1024 * 4
    """The maximum request content size allowed. Should
    be set to a sane value to prevent DoS-Attacks.
    """
    CORS_ALLOW_ORIGIN = "*"
    """The "Access-Control-Allow-Origin" header.
    """
    CORS_ALLOW_HEADERS = "Accept, Content-Type, Origin"
    """The "Access-Control-Allow-Headers" header.
    """


rpc_config = Config()
