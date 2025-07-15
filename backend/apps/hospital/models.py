from django.db import models
from utils.mixins import Audit
from django.conf import settings

class Hospital(Audit):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hospitals_created"
    )
    
    
class HospitalLocation(Audit):
    hospital = models.OneToOneField(
        Hospital, on_delete=models.CASCADE, related_name="location"
    )
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)