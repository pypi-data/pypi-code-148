from typing import Dict, List, Literal, Optional
from django.conf import settings
from django.db.models import Model
from rest_framework.serializers import Serializer
from rudra.settings import RudraBaseSettings
from django.http import HttpRequest
from rudra.paginator import PaginatorService


METHODS = Literal['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
rudrasettings: RudraBaseSettings = settings.RUDRASETTINGS

def get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)            
    return m

def get_success_response(data: dict = None, paginator: PaginatorService = None):
    success_path = rudrasettings.success_path
    success = get_class(success_path)
    if paginator:
        return success(data, paginator.has_next(), paginator.pages(), paginator.get_query_set_count())
    return success(data)

def get_error_response(message: str):
    error_path = rudrasettings.error_path
    error = get_class(error_path)
    return error(Exception(message))

def get_models() -> List[type[Model]]:
    return [get_class(meta_settings.model_path) for meta_settings in rudrasettings.meta_settings]

def get_model(model_name: str) -> Optional[type[Model]]:
    for meta_settings in rudrasettings.meta_settings:
        if model_name.lower() == meta_settings.model_path.split('.')[-1].lower():
            return get_class(meta_settings.model_path)
    return None

def get_serializer(model: Model, method: METHODS = None) -> Optional[type[Serializer]]:
    for meta_settings in rudrasettings.meta_settings:
        if meta_settings.model_path.split('.')[-1].lower() == model.__name__.lower():
            if meta_settings.serializer_settings.serializer_path:
                return get_class(meta_settings.serializer_settings.serializer_path)
            else:
                if method:
                    return get_class(meta_settings.serializer_settings.map_serializer.get(method))

def get_user_serializer() -> Optional[type[Serializer]]:
    if rudrasettings.user_serializer_path:
        return get_class(rudrasettings.user_serializer_path)
    return None

def check_method_allowed(model: Model, method: METHODS) -> bool:
    for meta_settings in rudrasettings.meta_settings:
        if meta_settings.model_path.split('.')[-1].lower() == model.__name__.lower():
            return method in meta_settings.methods_allowed
    return False

def get_serializer_context(request: HttpRequest) -> Dict:
    for meta_settings in rudrasettings.meta_settings:
        if meta_settings.serializer_settings.serializer_context:
            return meta_settings.serializer_settings.serializer_context(request)
    return {}