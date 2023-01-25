"""
JsonRPC sub module for JWT authentication
"""
import logging
from typing import Dict
from typing import Union

from drakaina.config import rpc_config
from drakaina.contrib.jwt.exceptions import InvalidToken
from drakaina.contrib.jwt.exceptions import JwtTokenError
from drakaina.contrib.jwt.exceptions import TokenBackendError
from drakaina.contrib.jwt.tokens import _check_exp
from drakaina.contrib.jwt.tokens import _set_exp
from drakaina.contrib.jwt.tokens import _set_iat
from drakaina.contrib.jwt.tokens import _set_jti
from drakaina.contrib.jwt.tokens import AccessToken
from drakaina.contrib.jwt.tokens import decode
from drakaina.contrib.jwt.tokens import RefreshToken
from drakaina.contrib.jwt.tokens import utc_now_aware

log = logging.getLogger(__name__)


def get_user_id(token: str) -> int:
    validated_token = AccessToken(token)
    try:
        return validated_token[rpc_config.USER_ID_CLAIM]
    except KeyError:
        raise InvalidToken("Token contained no recognizable user identification")


def get_tokens_by(refresh, rotate_refresh: bool = False) -> Dict[str, str]:
    refresh = RefreshToken(refresh)

    result = {"access": str(refresh.access_token)}

    if rotate_refresh:
        _set_jti(refresh.payload)
        _set_exp(refresh.payload, utc_now_aware(), rpc_config.REFRESH_TOKEN_LIFETIME)
        _set_iat(refresh.payload, utc_now_aware())

        result["refresh"] = str(refresh)

    return result


def get_tokens_for(user_id: Union[int, str]) -> Dict[str, str]:
    refresh = RefreshToken.for_user(user_id)

    result = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return result


def verify_tk(token: str):
    """

    :param token: Token for verification
    :except JwtTokenError: raised when the token is not valid
    """
    """
    !!!! IMPORTANT !!!! MUST raise a TokenError with a user-facing error
    message if the given token is invalid, expired, or otherwise not safe
    to use.
    """
    current_time = utc_now_aware()

    # Decode token
    try:
        payload = decode(token, verify=True)
    except TokenBackendError:
        raise JwtTokenError("Token is invalid or expired")

    """
    Performs additional validation steps which were not performed when this
    token was decoded. This method is part of the "public" API to indicate
    the intention that it may be overridden in subclasses.
    """
    # According to RFC 7519, the "exp" claim is OPTIONAL
    # (https://tools.ietf.org/html/rfc7519#section-4.1.4).  As a more
    # correct behavior for authorization tokens, we require an "exp"
    # claim.  We don't want any zombie tokens walking around.
    _check_exp(payload, current_time)

    # Ensure token id is present
    if rpc_config.JTI_CLAIM not in payload:
        raise JwtTokenError("Token has no id")
