from django.core.exceptions import PermissionDenied
from functools import wraps
from .service import AlastriaAuthService
import waffle
from .enums import AlastriaAuthSwitches


def requires_alastria_auth(view):
    @wraps(view)
    def _view(request, *args, **kwargs):
        if not waffle.switch_is_active(AlastriaAuthSwitches.auth.value):
            return view(request, *args, **kwargs)
        if "HTTP_ALASTRIA_TOKEN" not in request.request.META.keys():  # Alastria-Token
            raise PermissionDenied
        else:
            AlastriaAuthService.validate_permission(
                request.request.META["HTTP_ALASTRIA_TOKEN"]
            )
        return view(request, *args, **kwargs)

    return _view
