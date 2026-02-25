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