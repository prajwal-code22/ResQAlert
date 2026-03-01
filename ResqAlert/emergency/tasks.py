from accounts.models import EmergencyRequest, EmergencyResponder
from find_responder import find_nearby_responders
from celery import shared_task
from .notifications import send_notification


@shared_task
def process_emergency_request(emergency_id, radius=10):

    try:
        emergency = EmergencyRequest.objects.get(id=emergency_id)

        if emergency.status != "searching":
            return

        responders = find_nearby_responders(
            emergency.latitude,
            emergency.longitude,
            emergency.category,
            radius_km=radius
        )

        if responders:
            responders = responders[:3]

            for res in responders:

                if not EmergencyResponder.objects.filter(
                    emergency=emergency,
                    responder=res['user']
                ).exists():

                    EmergencyResponder.objects.create(
                        emergency=emergency,
                        responder=res['user'],
                        status='notified',
                    )

                    send_notification(res['user'], emergency)

        # Schedule next check after 60 seconds
        check_emergency_status.apply_async(
            args=[emergency_id, radius],
            countdown=60
        )

    except EmergencyRequest.DoesNotExist:
        return


@shared_task
def check_emergency_status(emergency_id, radius):
    try:
        emergency = EmergencyRequest.objects.get(id=emergency_id)

        if emergency.status == 'accepted':
            return

        radius += 10

        if radius > 50:
            emergency.status = 'no_responders'
            emergency.save()
            return

        process_emergency_request.delay(emergency_id, radius)

    except EmergencyRequest.DoesNotExist:
        return