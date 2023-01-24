from typing import Optional, Tuple

from django.conf import settings
from shopcloud_django_instrumenting import tracing

from monitoring import models


class Plugin:
    NAME = "NOT_SUCCESS_V1"

    def proceed(self, span: tracing.Span, metric: models.Metric, **kwargs) -> Tuple[bool, Optional[int]]:
        if settings.TEST_MODE:
            return False, 5

        return False, 0
