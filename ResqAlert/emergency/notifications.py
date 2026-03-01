from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from firebase_admin import messaging
from .firebase import send_push_notification

def send_notification(user, emergency):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",
        {
            "type": "emergency_notification",
            "emergency_id": emergency.id,
            "latitude": emergency.latitude,
            "longitude": emergency.longitude,
            "category": emergency.category,
            "message": "New Emergency Alert"
        }
    )

    send_push_notification(
        user.fcm_token,
        title="New Emergency Alert",
        body=f"Emergency in {emergency.category} category. Tap to view details.",
        data={
            "emergency_id": str(emergency.id),
            "latitude": str(emergency.latitude),
            "longitude": str(emergency.longitude),
            "category": emergency.category,
        }
    )