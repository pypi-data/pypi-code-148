from abc import abstractmethod, ABC
from .validators import (
    OperatorOnboardingValidator
)


class AClient(ABC):
    @abstractmethod
    def get_operators_onboarding_template_rendered(self, body: OperatorOnboardingValidator) -> str:
        ...
