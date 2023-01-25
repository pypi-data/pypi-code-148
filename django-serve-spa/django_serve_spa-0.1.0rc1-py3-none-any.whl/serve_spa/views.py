from django.conf import settings
from django.shortcuts import redirect
from django.views.static import serve

from . import settings as app_settings


def serve_file(request, filename, **kwargs):
    """
    Serves a file from the SPA root using Django static serve
    """
    return serve(request, path=filename, document_root=app_settings.SPA_ROOT)


def redirect_static(request, resource):
    """
    Redirect a request for a SPA static resource to be served using Django staticfiles
    """
    return redirect(settings.STATIC_URL + resource)


__all__ = [
    'serve_file',
    'redirect_static',
]
