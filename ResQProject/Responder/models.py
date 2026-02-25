from django.db import models
from Utilities.base import BaseModel
from Victim.models import Victim

#


# ------------------------------------------------------
# Static Location (Only for Organizations)
# ------------------------------------------------------
class Location(BaseModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


# ------------------------------------------------------
# Organization Model
# ------------------------------------------------------
class Organization(BaseModel):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    description = models.TextField()
    established_date = models.DateField()
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='organization_logos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# ------------------------------------------------------
# Responder Model
# ------------------------------------------------------
class Responder(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    role = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    joined_date = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ------------------------------------------------------
# Responder Real-Time Location (Dynamic)
# ------------------------------------------------------
class ResponderLocation(BaseModel):
    responder = models.OneToOneField(Responder, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.responder} Location"





# ------------------------------------------------------
# Rescue Type Model
# ------------------------------------------------------
class RescueType(BaseModel):

    RESCUE_CHOICES = [
        ("FIR", "FIR Case"),
        ("RWR", "Raped Women Risk"),
        ("DV", "Domestic Violence"),
        ("CHILD", "Child Abuse"),
        ("ACCIDENT", "Accident Rescue"),
        ("DISASTER", "Disaster Rescue"),
    ]

    name = models.CharField(max_length=50, choices=RESCUE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


# ------------------------------------------------------
# Rescue Model
# ------------------------------------------------------
class Rescue(BaseModel):
    responder = models.ForeignKey(Responder, on_delete=models.CASCADE)
    victim = models.ForeignKey(Victim, on_delete=models.CASCADE)
    rescue_type = models.ForeignKey(RescueType, on_delete=models.SET_NULL, null=True)
    rescue_date = models.DateTimeField()
    description = models.TextField()
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"Rescue by {self.responder} for {self.victim}"
