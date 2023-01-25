from datetime import datetime
from typing import Any
from typing import Dict
from typing import Union
from uuid import uuid4

try:
    from zoneinfo import ZoneInfo

    UTC = ZoneInfo("UTC")
except (ImportError, KeyError):
    try:
        from pytz import utc as UTC
    except ImportError:
        from datetime import timezone

        UTC = timezone.utc

import jwt
from jwt import algorithms
from jwt import InvalidAlgorithmError
from jwt import InvalidTokenError
from jwt import PyJWKClient

from drakaina.config import rpc_config
from drakaina.contrib.jwt.exceptions import JwtTokenError
from drakaina.contrib.jwt.exceptions import TokenBackendError

ALLOWED_ALGORITHMS = (
    "HS256",
    "HS384",
    "HS512",
    "RS256",
    "RS384",
    "RS512",
)

jwks_client = PyJWKClient(rpc_config.JWK_URL) if rpc_config.JWK_URL else None


def utc_now_aware():
    return datetime.now(tz=UTC)


def datetime_to_timestamp(dt):
    return int(dt.timestamp())


def datetime_from_timestamp(ts):
    return datetime.fromtimestamp(ts, UTC)


def _set_exp(payload: Dict[str, Any], current_time, lifetime, claim="exp"):
    """
    Updates the expiration time of a token.
    See here:
    https://tools.ietf.org/html/rfc7519#section-4.1.4
    """
    payload[claim] = datetime_to_timestamp(current_time + lifetime)


def _check_exp(payload: Dict[str, Any], current_time, claim="exp"):
    """
    Checks whether a timestamp value in the given claim has passed (since
    the given datetime value in `current_time`). Raises a TokenError with
    a user-facing error message if so.
    """
    try:
        claim_value = payload[claim]
    except KeyError:
        raise JwtTokenError(f"Token has no '{claim}' claim")

    claim_time = datetime_from_timestamp(claim_value)
    if claim_time <= current_time:
        raise JwtTokenError(f"Token '{claim}' claim has expired")


def _set_iat(payload: Dict[str, Any], current_time, claim="iat"):
    """
    Updates the time at which the token was issued.
    See here:
    https://tools.ietf.org/html/rfc7519#section-4.1.6
    """
    payload[claim] = datetime_to_timestamp(current_time)


def _set_jti(payload: Dict[str, Any]):
    """
    Populates the configured jti claim of a token with a string where there
    is a negligible probability that the same string will be chosen at a
    later time.
    See here:
    https://tools.ietf.org/html/rfc7519#section-4.1.7
    """
    payload[rpc_config.JTI_CLAIM] = uuid4().hex


def _validate_algorithm(algorithm):
    """
    Ensure that the nominated algorithm is recognized, and that cryptography is installed for those
    algorithms that require it
    """
    if algorithm not in ALLOWED_ALGORITHMS:
        raise TokenBackendError(f"Unrecognized algorithm type '{algorithm}'")

    if algorithm in algorithms.requires_cryptography and not algorithms.has_crypto:
        raise TokenBackendError(f"You must have cryptography installed to use {algorithm}.")


def _verifying_key():
    if rpc_config.ALGORITHM.startswith("HS"):
        return rpc_config.SIGNING_KEY
    return rpc_config.VERIFYING_KEY


def get_verifying_key(token):
    if rpc_config.ALGORITHM.startswith("HS"):
        return rpc_config.SIGNING_KEY

    if jwks_client:
        return jwks_client.get_signing_key_from_jwt(token).key

    return rpc_config.VERIFYING_KEY


def encode(payload: Dict[str, Any]):
    """
    Returns an encoded token for the given payload dictionary.
    """
    jwt_payload = payload.copy()
    if rpc_config.AUDIENCE is not None:
        jwt_payload["aud"] = rpc_config.AUDIENCE
    if rpc_config.ISSUER is not None:
        jwt_payload["iss"] = rpc_config.ISSUER

    token = jwt.encode(jwt_payload, rpc_config.SIGNING_KEY, algorithm=rpc_config.ALGORITHM)
    if isinstance(token, bytes):
        # For PyJWT <= 1.7.1
        return token.decode("utf-8")
    # For PyJWT >= 2.0.0a1
    return token


def decode(token, verify=True):
    """
    Performs a validation of the given token and returns its payload
    dictionary.
    Raises a `TokenBackendError` if the token is malformed, if its
    signature check fails, or if its 'exp' claim indicates it has expired.
    """
    try:
        return jwt.decode(
            token,
            get_verifying_key(token),
            algorithms=[rpc_config.ALGORITHM],
            audience=rpc_config.AUDIENCE,
            issuer=rpc_config.ISSUER,
            leeway=rpc_config.LEEWAY,
            options={
                "verify_aud": rpc_config.AUDIENCE is not None,
                "verify_signature": verify,
            },
        )
    except InvalidAlgorithmError as error:
        raise TokenBackendError("Invalid algorithm specified") from error
    except InvalidTokenError:
        raise TokenBackendError("Token is invalid or expired")


_validate_algorithm(rpc_config.ALGORITHM)


class Token:
    """
    A class which validates and wraps an existing JWT or can be used to build a
    new JWT.
    """

    token_type = None
    lifetime = None

    def __init__(self, token=None, verify=True):
        """
        !!!! IMPORTANT !!!! MUST raise a TokenError with a user-facing error
        message if the given token is invalid, expired, or otherwise not safe
        to use.
        """
        if self.token_type is None or self.lifetime is None:
            raise JwtTokenError("Cannot create token with no type or lifetime")

        self.token = token
        self.current_time = utc_now_aware()

        # Set up token
        if token is not None:
            # An encoded token was provided

            # Decode token
            try:
                self.payload = decode(token, verify=verify)
            except TokenBackendError:
                raise JwtTokenError("Token is invalid or expired")

            if verify:
                self.verify()
        else:
            # New token.  Skip all the verification steps.
            self.payload = {rpc_config.TOKEN_TYPE_CLAIM: self.token_type}

            # Set "exp" and "iat" claims with default value
            _set_exp(self.payload, self.current_time, self.lifetime)
            _set_iat(self.payload, self.current_time)

            # Set "jti" claim
            _set_jti(self.payload)

    def __repr__(self):
        return repr(self.payload)

    def __getitem__(self, key):
        return self.payload[key]

    def __setitem__(self, key, value):
        self.payload[key] = value

    def __delitem__(self, key):
        del self.payload[key]

    def __contains__(self, key):
        return key in self.payload

    def get(self, key, default=None):
        return self.payload.get(key, default)

    def __str__(self):
        """
        Signs and returns a token as a base64 encoded string.
        """
        return encode(self.payload)

    def verify(self):
        """
        Performs additional validation steps which were not performed when this
        token was decoded.  This method is part of the "public" API to indicate
        the intention that it may be overridden in subclasses.
        """
        # According to RFC 7519, the "exp" claim is OPTIONAL
        # (https://tools.ietf.org/html/rfc7519#section-4.1.4). As a more
        # correct behavior for authorization tokens, we require an "exp"
        # claim. We don't want any zombie tokens walking around.
        _check_exp(self.payload, self.current_time)

        # Ensure token id is present
        if rpc_config.JTI_CLAIM not in self.payload:
            raise JwtTokenError("Token has no id")

        """
        Ensures that the token type claim is present and has the correct value.
        """
        try:
            token_type = self.payload[rpc_config.TOKEN_TYPE_CLAIM]
        except KeyError:
            raise JwtTokenError("Token has no type")

        if self.token_type != token_type:
            raise JwtTokenError("Token has wrong type")

    @classmethod
    def for_user(cls, user_id: Union[str, int]):
        """
        Returns an authorization token for the given user that will be provided
        after authenticating the user's credentials.
        """
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            user_id = str(user_id)

        token = cls()
        token[rpc_config.USER_ID_CLAIM] = user_id

        return token


class RefreshToken(Token):
    no_copy_claims = (
        rpc_config.TOKEN_TYPE_CLAIM,
        "exp",
        # Both of these claims are included even though they may be the same.
        # It seems possible that a third party token might have a custom or
        # namespaced JTI claim as well as a default "jti" claim.  In that case,
        # we wouldn't want to copy either one.
        rpc_config.JTI_CLAIM,
        "jti",
    )

    def __init__(self, token=None, verify=True):
        self.token_type = "refresh"
        self.lifetime = rpc_config.REFRESH_TOKEN_LIFETIME
        super().__init__(token, verify)

    @property
    def access_token(self):
        """
        Returns an access token created from this refresh token.  Copies all
        claims present in this refresh token to the new access token except
        those claims listed in the `no_copy_claims` attribute.
        """
        access = AccessToken()

        # Use instantiation time of refresh token as relative timestamp for
        # access token "exp" claim.  This ensures that both a refresh and
        # access token expire relative to the same time if they are created as
        # a pair.
        _set_exp(access.payload, self.current_time, access.lifetime)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value

        return access


class AccessToken(Token):
    def __init__(self, token=None, verify=True):
        self.token_type = "access"
        self.lifetime = rpc_config.ACCESS_TOKEN_LIFETIME
        super().__init__(token, verify)
