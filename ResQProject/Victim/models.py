from django.db import models

# Create your models here.
from Utilities.base import BaseModel

# ------------------------------------------------------
# Victim Model
# ------------------------------------------------------
class Victim(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    injury_details = models.TextField()
    is_recovered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ------------------------------------------------------
# Victim Real-Time Location (Dynamic)
# ------------------------------------------------------
class VictimLocation(BaseModel):
    victim = models.OneToOneField(Victim, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.victim} Location"