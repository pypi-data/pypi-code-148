"""
Copyright (C) 2022 Corsair M360, Inc - All Rights Reserved.
Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
"""

import logging
from django.http import JsonResponse

from ..helper import helper_instance

_logger = logging.getLogger(__name__)

class DjangoMiddleware:
    """
    Django M360 Middleware
    """

    def __init__(self, get_response):
        from django.conf import settings
        from .settings import CONFIG

        self.get_response = get_response
        self.helper = helper_instance("django", CONFIG, getattr(settings, "M360", None))

    def __call__(self, request):
        # handle reserved routes
        data = self.helper.handle_request(request)
        if data:
            if data.get("name"):
                return JsonResponse(data, status=200)
            else:
                return JsonResponse(data, status=500)

        # everything above this line happens before the app's request handler execution
        response = self.get_response(request)  # handler execution
        # everything below here happens after the app's request handler execution

        return response
