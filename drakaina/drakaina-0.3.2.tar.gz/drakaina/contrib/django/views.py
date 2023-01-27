import logging
from typing import Callable
from typing import Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.http import HttpResponse
from django.utils.module_loading import autodiscover_modules
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from drakaina.rpc_protocols import BaseRPCProtocol
from drakaina.rpc_protocols import JsonRPCv2

log = logging.getLogger(__name__)
UserModel = get_user_model()


def parse_settings(settings_object: object, prefix: str = ""):
    # for parameter_name in parameters:
    #     attr_name = parameter_name
    #       if not prefix else f"{prefix}_{parameter_name}"
    #     value = getattr(settings_object, attr_name, None)
    #     if value:
    #         if "LIFETIME" in parameter_name:
    #             assert isinstance(value, int)
    #             value = timedelta(minutes=value)
    #         setattr(rpc_config, parameter_name, value)
    ...


class RPCView(View):
    """Django class based view implements JSON-RPC"""

    http_method_names = ["post", "options"]
    content_type = "application/json"
    handler: BaseRPCProtocol

    @classmethod
    def as_view(
        cls,
        autodiscover: str = "rpc_methods",
        settings_prefix: str = "JSONRPC",
        handler: Optional[BaseRPCProtocol] = None,
        **initkwargs,
    ) -> Callable:
        """

        :param autodiscover: submodule name(s) where defined RPC methods
        :type autodiscover: str
        :param settings_prefix: prefix to search for JsonRPC module settings in
                                django config file
        :type settings_prefix: str
        :param handler:
        :type handler: BaseRPCProtocol
        :param initkwargs:
        :return: Instance of this class
        """
        # Configure drakaina module
        parse_settings(settings_object=settings, prefix=settings_prefix)

        view = cls.as_view(handler=handler or JsonRPCv2(), **initkwargs)
        view.cls = cls

        # Scan specified sub-modules
        autodiscover_modules(autodiscover)

        return csrf_exempt(view)

    def http_method_not_allowed(
        self,
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> HttpResponse:
        msg = f"HTTP Method Not Allowed ({request.method}): {request.path}"
        content = self.handler.get_raw_error(self.handler.BadRequestError(msg))

        return HttpResponse(content=content, content_type=self.content_type)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.content_type != self.content_type or len(request.body) == 0:
            msg = f"HTTP Method Not Allowed ({request.method}): {request.path}"
            content = self.handler.get_raw_error(
                self.handler.BadRequestError(msg),
            )
        else:
            content = self.handler.handle_raw_request(
                request.body,
                request=request,
            )

        return HttpResponse(content=content, content_type=self.content_type)
