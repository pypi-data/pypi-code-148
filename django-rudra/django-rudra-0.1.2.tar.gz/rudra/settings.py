from typing import Callable, Dict, List, Optional
from django.http import HttpRequest

 
class SerializerSettings:
    serializer_path: str
    map_serializer: Dict[str, str]
    serializer_context: Callable[[HttpRequest], dict]

    def __init__(self, serializer_path: str = None, map_serializer: Dict[str, str] = None, serializer_context: Callable[[HttpRequest], dict] = None,):
        self.serializer_path = serializer_path
        self.map_serializer = map_serializer
        self.serializer_context = serializer_context

class RudraMetaSettings:
    methods_allowed: List[str]
    serializer_path: str
    model_path: str
    serializer_settings: SerializerSettings

    def __init__(self, methods_allowed: List[str], model_path: str, serializer_settings: SerializerSettings = None):
        self.methods_allowed = methods_allowed
        self.model_path = model_path 
        self.serializer_settings = serializer_settings

class RudraBaseSettings:
    success_path: str
    error_path: str
    user_serializer_path: str
    fixed_page_number: Optional[int] # for pagination page number
    meta_settings: List[RudraMetaSettings]