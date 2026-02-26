from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import timedelta
from accounts.models import EmergencyRequest, EmergencyResponder
from find_responder import find_nearby_responders
from .tasks import process_emergency_request


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def emergency_request(request):

    user = request.user

    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')
    category = request.data.get('category')

    if not latitude or not longitude or not category:
        return Response(
            {"message": "Latitude, longitude and category are required"},
            status=400
        )

    
    emergency = EmergencyRequest.objects.create(
        victim=user,
        latitude=latitude,
        longitude=longitude,
        category=category,
        status="searching"
    )

    process_emergency_request.delay(emergency.id)


