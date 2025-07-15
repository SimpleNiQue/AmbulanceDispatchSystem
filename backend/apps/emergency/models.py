from django.db import models
from django.conf import settings
from utils.mixins import Audit
from apps.ambulance.models import Ambulance
from apps.hospital.models import Hospital
from apps.emergency.utils import SeverityLevel

class EmergencyRequest(Audit):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="emergency_requests"
    )
    ambulance = models.ForeignKey(Ambulance, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')
    severity = models.CharField(max_length=10, choices=SeverityLevel.options(), default=SeverityLevel.MEDIUM)

    is_resolved = models.BooleanField(default=False)
    response_time_seconds = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Request by {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class EmergencyRequestLocation(Audit):
    emergency = models.OneToOneField(
        EmergencyRequest, on_delete=models.CASCADE, related_name="location"
    )
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
