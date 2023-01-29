import logging
from enum import Enum
from typing import Any

from scrapy import Request, Spider
from seleniumwire.webdriver import Firefox

logger = logging.getLogger(__name__)

ignore_http_methods = [
    "OPTIONS",
    "POST",
    "GET",
    "PUT",
    "DELETE",
    "CONNECT",
    "TRACE",
    "PATCH",
]


class RequestMetaKeys(Enum):
    """Not changed
    """    
    return_value_browser_interaction = (
        "__SELENIUM_MIDDLEWARE_BROWSER_INTERACTION_RETURN_VALUE__"
    )
    use_middleware = "__SELENIUM_MIDDLEWARE_USE_FOR_THIS_REQUEST__"


class SeleniumSpider(Spider):
    def parse(self, response, **kwargs):
        """Not changed
        """
        pass

    def browser_interaction_before_get(self, driver: Firefox, request: Request) -> None:
        """
        Override this method to interact with the browser before driver.get(request.url)
        was called in middleware
        """
        pass

    def browser_interaction_after_get(self, driver: Firefox, request: Request) -> Any:
        """
        Override this method to interact with the browser after driver.get(request.url)
        was called in middleware
        :return any value returned from this method will be added to the response meta dict
        with the key "__SELENIUM_MIDDLEWARE_BROWSER_INTERACTION_VALUE__"
        """
        pass