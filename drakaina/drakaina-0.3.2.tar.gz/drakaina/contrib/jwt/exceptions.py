from drakaina.exceptions import JsonRPCError


class AuthenticationFailed(JsonRPCError):
    """Authentication failed"""

    code = -32001
    default_message = "Authentication failed"


class JwtTokenError(JsonRPCError):
    """"""

    code = -32001
    default_message = "JWT Token Error"


class TokenBackendError(JsonRPCError):
    """"""

    code = -32001
    default_message = "Token Backend Error"


class InvalidToken(AuthenticationFailed):
    """"""

    code = -32001
    default_message = "Invalid Token"
