from django.db import models
from django.conf import settings
from utils.mixins import Audit
from apps.ambulance.utils import AmbulanceTypeEnum, StatusEnum
from apps.hospital.models import Hospital

class Ambulance(Audit):
    status = models.CharField(
        choices=StatusEnum.options(), default=StatusEnum.AVAILABLE, max_length=255
    )
    ambulance_type = models.CharField(
        choices=AmbulanceTypeEnum.options(),
        default=AmbulanceTypeEnum.BLS,
        max_length=255,
    )
    last_assigned = models.DateTimeField(null=True, blank=True)
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="ambulance"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ambulances_created"
    )
    busy_until = models.DateTimeField(null=True, blank=True)
    

class AmbulanceLocation(Audit):
    ambulance = models.OneToOneField(
        Ambulance, on_delete=models.CASCADE, related_name="location"
    )
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
