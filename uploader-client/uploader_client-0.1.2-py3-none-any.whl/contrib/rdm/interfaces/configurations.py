from typing import (
    TYPE_CHECKING,
)

from pydantic.fields import (
    Field,
)
from uploader_client.configurations import (
    AbstractConfig,
)
from uploader_client.const import (
    DEFAULT_REQUEST_RETRIES,
    DEFAULT_REQUEST_TIMEOUT,
    DEFAULT_RETRY_FACTOR,
)


if TYPE_CHECKING:
    from dataclasses import (
        dataclass,
    )
else:
    from pydantic.dataclasses import (
        dataclass,
    )


@dataclass
class RegionalDataMartUploaderConfig(AbstractConfig):
    """Объект конфигурации загрузчика в витрину данных."""

    url: str = Field(
        title='Адрес витрины данных (schema://host:post)',
        default='http://localhost:8090',
        min_length=1,
    )

    datamart_name: str = Field(
        title='Мнемоника витрины',
        min_length=1,
    )

    request_retries: int = Field(
        title='Количество повторных попыток',
        default=DEFAULT_REQUEST_RETRIES,
    )

    retry_factor: int = Field(
        title='Шаг увеличения задержки м.д. запросами',
        default=DEFAULT_RETRY_FACTOR,
    )

    timeout: int = Field(
        title='Таймаут запроса, сек',
        default=DEFAULT_REQUEST_TIMEOUT,
    )

    interface: str = 'uploader_client.interfaces.rest.OpenAPIInterface'

    logger: str = 'uploader_client.logging.db.Logger'
