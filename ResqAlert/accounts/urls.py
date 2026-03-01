# to save user fcm_token and device type for push notifications
from django.urls import path
from .views import save_device

urlpatterns = [
    path("save-device/", save_device, name="save_device"),
]