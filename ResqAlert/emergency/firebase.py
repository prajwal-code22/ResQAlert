import firebase_admin
from firebase_admin import credentials, messaging
import os

KEY_PATH = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')

cred = credentials.Certificate("KEY_PATH")
firebase_admin.initialize_app(cred)

def send_push_notification(device_token, title, body, data=None):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data or {},
        token=device_token,
    )

    messaging.send(message)