from accounts.models import User, UserLocation
from .utils import calculate_distance

def find_nearby_responders(lat, lon, category, radius_km=10):

    responders = User.objects.filter(
        role='responder',
        responder_category=category,
        is_available=True
    ).select_related('location')

    nearby = []

    for responder in responders:
        if hasattr(responder, 'location'):

            distance = calculate_distance(
                lat,
                lon,
                responder.location.latitude,
                responder.location.longitude
            )

            if distance <= radius_km:
                nearby.append({
                    "user": responder,
                    "distance": round(distance, 2)
                })

    # sort by nearest
    nearby.sort(key=lambda x: x["distance"])

    return nearby