from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = (
        ('victim', 'Victim'),
        ('responder', 'Responder'),
    )

    RESPONDER_CATEGORY = (
        ('police', 'Police'),
        ('fire', 'Fire Brigade'),
        ('ambulance', 'Ambulance'),
        ('volunteer', 'Volunteer'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    responder_category = models.CharField(
        max_length=20,
        choices=RESPONDER_CATEGORY,
        null=True,
        blank=True
    )
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.username
    
class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='location')
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.user.username}'s Location"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

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
    status=models.CharField(max_length=20, defalut='notified')
    notified_at=models.DateTimeField(auto_now_add=True)
    
class DeviceToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='device_token')
    token = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s Device Token"