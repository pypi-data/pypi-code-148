from django.dispatch import receiver
from django.db.models.signals import post_save
from waffle.models import Switch
from websocket import create_connection
import json
from django.conf import settings


@receiver(post_save, sender=Switch)
def post_save_switch(sender, instance, **kwargs):
    ws = create_connection(settings.WS_FEATURE_TOGGLE_PATH)
    data = json.dumps(
        {
            "message": {"name": instance.name, "active": instance.active},
            "secret": settings.BACKEND_NOTIFICATIONS_SECRET,
        }
    )
    ws.send(data)
