from django.urls import path
from .views import emergency_request, accept_emergency

urlpatterns = [
    path("emergency/", emergency_request, name="emergency_request"),
    path("emergency/<int:emergency_id>/accept/", accept_emergency, name="accept_emergency"),
]