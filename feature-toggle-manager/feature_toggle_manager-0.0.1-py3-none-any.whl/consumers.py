import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.conf import settings


class FeatureToggleConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "feature_toggle_update"
        self.room_group_name = "feature_toggle_update_group"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        secret = text_data_json.get("secret")
        if secret and secret == settings.BACKEND_NOTIFICATIONS_SECRET:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "feature_toggle_update", "message": message}
            )

    def feature_toggle_update(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))
