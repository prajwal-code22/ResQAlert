import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close()
            return

        self.group_name = f"user_{self.user.id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def emergency_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": "emergency_notification",
            "emergency_id": event["emergency_id"],
            "latitude": event["latitude"],
            "longitude": event["longitude"],
            "category": event["category"],
        }))