from rest_framework import serializers
from apps.ambulance.models import Ambulance, AmbulanceLocation
from apps.hospital.models import Hospital
from apps.hospital.v1.serializers import HospitalSerializer
from apps.ambulance.v1.services import (
    create_ambulance_with_location,
    update_ambulance_with_location,
)


class AmbulanceLocationSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField()
    latitude = serializers.CharField()

    class Meta:
        model = AmbulanceLocation
        fields = ["longitude", "latitude"]


class AmbulanceSerializer(serializers.ModelSerializer):
    location = AmbulanceLocationSerializer()
    hospital = HospitalSerializer(read_only=True)
    hospitalId = serializers.PrimaryKeyRelatedField(
        queryset=Hospital.objects.all(),
        write_only=True,
        source="hospital"
    )
    createdBy = serializers.StringRelatedField(read_only=True, source="created_by")

    class Meta:
        model = Ambulance
        fields = [
            "id",
            "status",
            "ambulance_type",
            "last_assigned",
            "hospital",
            "hospitalId",
            "createdBy",
            "location",
        ]

    def create(self, validated_data):
        return create_ambulance_with_location(validated_data)

    def update(self, instance, validated_data):
        return update_ambulance_with_location(instance, validated_data)
