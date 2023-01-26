import logging
from typing import Optional

from the_spymaster_util.http_client import BaseHttpClient
from the_spymaster_util.logger import wrap
from urllib3 import Retry

from .structs import (
    GenerateGuessRequest,
    GenerateGuessResponse,
    GenerateHintRequest,
    GenerateHintResponse,
    LoadModelsRequest,
    LoadModelsResponse,
)

log = logging.getLogger(__name__)
DEFAULT_BASE_URL = "http://localhost:5000"
DEFAULT_RETRY_STRATEGY = Retry(
    raise_on_status=False,
    total=5,
    backoff_factor=0.3,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "OPTIONS", "GET", "POST", "PUT", "DELETE"],
)


class TheSpymasterSolversClient(BaseHttpClient):
    def __init__(self, base_url: str = None, retry_strategy: Optional[Retry] = DEFAULT_RETRY_STRATEGY):
        if not base_url:
            base_url = DEFAULT_BASE_URL
        super().__init__(base_url=base_url, retry_strategy=retry_strategy)
        log.debug(f"Solvers client is using backend: {wrap(self.base_url)}")

    def generate_hint(self, request: GenerateHintRequest) -> GenerateHintResponse:
        data = self._post("generate-hint", data=request.dict())
        return GenerateHintResponse(**data)

    def generate_guess(self, request: GenerateGuessRequest) -> GenerateGuessResponse:
        data = self._post("generate-guess", data=request.dict())
        return GenerateGuessResponse(**data)

    def load_models(self, request: LoadModelsRequest) -> LoadModelsResponse:
        data = self._post("load-models", data=request.dict())
        return LoadModelsResponse(**data)
