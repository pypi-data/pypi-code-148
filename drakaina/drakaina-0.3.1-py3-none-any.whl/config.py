from datetime import timedelta


parameters = (
    "ACCESS_TOKEN_LIFETIME",
    "REFRESH_TOKEN_LIFETIME",
    "ROTATE_REFRESH_TOKENS",
    "UPDATE_LAST_LOGIN",
    "AUTH_HEADER_NAME",
    "AUTH_HEADER_TYPES",
    "TOKEN_TYPE_CLAIM",
    "USER_ID_CLAIM",
    "JTI_CLAIM",
    "ALGORITHM",
    "SIGNING_KEY",
    "VERIFYING_KEY",
    "AUDIENCE",
    "ISSUER",
    "JWK_URL",
    "LEEWAY",
)


class Config:
    ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)
    REFRESH_TOKEN_LIFETIME = timedelta(minutes=60 * 24)
    ROTATE_REFRESH_TOKENS = False
    UPDATE_LAST_LOGIN = False

    AUTH_HEADER_NAME = "Authorization"
    AUTH_HEADER_TYPES = ("Bearer",)
    TOKEN_TYPE_CLAIM = "token_type"
    USER_ID_CLAIM = "user_id"
    JTI_CLAIM = "jti"

    ALGORITHM = "HS256"
    SIGNING_KEY = None
    VERIFYING_KEY = None
    AUDIENCE = None
    ISSUER = None
    JWK_URL = None
    LEEWAY = 0


rpc_config = Config()


def parse_settings(settings_object: object, prefix: str = ""):
    for parameter_name in parameters:
        attr_name = parameter_name if not prefix else f"{prefix}_{parameter_name}"
        value = getattr(settings_object, attr_name, None)
        if value:
            if "LIFETIME" in parameter_name:
                assert isinstance(value, int)
                value = timedelta(minutes=value)
            setattr(rpc_config, parameter_name, value)
