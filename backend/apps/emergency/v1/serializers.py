# apps/emergency/serializers.py

from rest_framework import serializers
from apps.emergency.models import EmergencyRequest, EmergencyRequestLocation
from apps.ambulance.models import Ambulance
from apps.hospital.models import Hospital
from apps.emergency.utils import SeverityLevel


class EmergencyRequestLocationSerializer(serializers.ModelSerializer):
    latitude = serializers.CharField()
    longitude = serializers.CharField()

    class Meta:
        model = EmergencyRequestLocation
        fields = ['latitude', 'longitude']


class EmergencyRequestSerializer(serializers.ModelSerializer):
    location = EmergencyRequestLocationSerializer(write_only=True)
    ambulance = serializers.PrimaryKeyRelatedField(read_only=True)
    severity = serializers.ChoiceField(choices=SeverityLevel.options_list())
    isResolved = serializers.BooleanField(required=False, source="is_resolved")
    responseTimeSeconds = serializers.DateTimeField(required=False, source="response_time_seconds")
    

    class Meta:
        model = EmergencyRequest
        fields = ['id', 'severity', 'ambulance', 'location', 'isResolved', 'responseTimeSeconds']
        read_only_fields = ['ambulance', 'isResolved', 'responseTimeSeconds']
