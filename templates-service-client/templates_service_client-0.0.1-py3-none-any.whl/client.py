import requests
from .validators import (
    OperatorOnboardingValidator,
)
import json
from .abstractions import AClient
import os
from typing import Any, Dict
from requests.models import Request


class Client(AClient):
    def __init__(
        self, service_host: str, secret: str = os.environ.get("TEMPLATES_SERVICE_SECRET", "")
    ):

        self.host: str = service_host
        self.secret: str = secret

    def get_operators_onboarding_template_rendered(self, body: OperatorOnboardingValidator) -> Request:
        headers: Dict[str, Any] = {}
        r: Request = requests.post(
            f"{self.host}/get-operators-onboarding-template-rendered",
            json=json.loads(body.json()),
            headers=headers,
            timeout=5,
        )
        return r
