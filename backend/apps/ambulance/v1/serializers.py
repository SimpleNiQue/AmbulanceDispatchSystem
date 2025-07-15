from rest_framework import serializers
from apps.ambulance.models import Ambulance, AmbulanceLocation
from apps.hospital.models import Hospital
from apps.ambulance.utils import StatusEnum, AmbulanceTypeEnum
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
    lastAssigned = serializers.DateTimeField(source="last_assigned", required=False)
    ambulanceType = serializers.ChoiceField(choices=AmbulanceTypeEnum.options_list(), source="ambulance_type")
    status = serializers.ChoiceField(choices=StatusEnum.options_list())
    busyUntil = serializers.DateTimeField(source="busy_until", required=False)
    createdBy = serializers.StringRelatedField(read_only=True, source="created_by")

    class Meta:
        model = Ambulance
        fields = [
            "id",
            "status",
            "ambulanceType",
            "lastAssigned",
            "hospitalId",
            "location",
            "busyUntil",
            "createdBy",
            "hospital",
        ]

    def create(self, validated_data):
        return create_ambulance_with_location(validated_data)

    def update(self, instance, validated_data):
        return update_ambulance_with_location(instance, validated_data)
