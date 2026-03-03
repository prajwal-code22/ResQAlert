from django.db import models
from accounts.models import User
class EmergencyRequest(models.Model):
    victim = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_requests')
    responder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')
    latitude = models.FloatField()
    longitude = models.FloatField()
    category = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Emergency by {self.victim.username}"

class EmergencyResponder(models.Model):
    request=models.ForeignKey(EmergencyRequest, on_delete=models.CASCADE, related_name='responders')
    responder=models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_responses')
    status=models.CharField(max_length=20, default='notified')
    notified_at=models.DateTimeField(auto_now_add=True)