from accounts.models import EmergencyRequest, EmergencyResponder
from find_responder import find_nearby_responders
from celery import shared_task

@shared_task
def process_emergency_request(emergency_id, radius=10):

    try:
        emergency = EmergencyRequest.objects.get(id=emergency_id)

        if emergency.status != "searching":
            return

        max_radius = 50

        responders = find_nearby_responders(
            emergency.latitude,
            emergency.longitude,
            emergency.category,
            radius_km=radius
        )

        if responders:
            responders = responders[:3]

            for res in responders:
                EmergencyResponder.objects.create(
                    emergency=emergency,
                    responder=res['user'],
                    status='notified',
                )

                send_notification(res['user'], emergency)

        # 🔥 Schedule check after 60 seconds
        check_emergency_status.apply_async(
            args=[emergency_id, radius],
            countdown=60
        )

    except EmergencyRequest.DoesNotExist:
        return
    
    try:
        emergency=EmergencyRequest.objects.get(id=emergency_id)
        radius=10
        max_radius=50
        wait_time=60
        responder=find_nearby_responders(
            emergency.latitude,
            emergency.longitude,
            emergency.category,
            radius_km=radius
        )
        while not responder and radius<=max_radius:
            radius+=10
            responder=find_nearby_responders(
                emergency.latitude,
                emergency.longitude,
                emergency.category,
                radius_km=radius
            )
        if responder:
            responder=responder[:3]
            for res in responder:
                EmergencyResponder.objects.create(
                    request=emergency,
                    responder=res['user'],
                    status='notified',
                )
                # here to send notification to responder with position according to category(like fire emergency than to fire fighter)
                # here to check whether responder accepted or not and update status accordingly
                # if accepted then assign request to responder and update request status to accepted
                # if not accepted then after wait_time seconds check for next responder and repeat the process until max_radius is reached or responders are available
                import time
                time.sleep(wait_time)
                # check if request is accepted
                emergency.refresh_from_db()
                if emergency.status == 'accepted':


                    
                else:
                    continue


    except EmergencyRequest.DoesNotExist:
        return