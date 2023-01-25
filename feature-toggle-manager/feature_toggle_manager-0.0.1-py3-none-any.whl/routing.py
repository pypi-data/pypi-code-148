from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/features/updates", consumers.FeatureToggleConsumer.as_asgi()),
]
