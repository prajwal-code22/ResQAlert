from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import UserDevice
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer



#resgister the user
@api_view(['POST'])
def register(request):
    serializer= UserSerializer(data=request.data)
    if serializer.is_valid():
        user=serializer.save()
        return Response({"message":"User registered successfully"}, status=201)
    return Response(serializer.errors, status=400)


    
    



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