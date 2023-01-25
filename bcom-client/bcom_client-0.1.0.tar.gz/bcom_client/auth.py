from collections.abc import Generator

import httpx
from pydantic.types import SecretStr


class TokenAuth(httpx.Auth):
    def __init__(self, token: SecretStr) -> None:
        self.token = token

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers["Authorization"] = f"Token {self.token.get_secret_value()}"
        yield request
