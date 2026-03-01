from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import UserDevice
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_device(request):

    token = request.data.get("fcm_token")
    device_type = request.data.get("device_type")

    if not token:
        return Response({"message": "Token required"}, status=400)

    # Create or update device
    UserDevice.objects.update_or_create(
        fcm_token=token,
        defaults={
            "user": request.user,
            "device_type": device_type,
            "is_active": True
        }
    )

    return Response({"message": "Device saved"}) 