# apps/hospital/serializers.py

from rest_framework import serializers
from apps.hospital.models import Hospital, HospitalLocation
from apps.hospital.v1.services import (
    create_hospital,
    update_hospital,
)


class HospitalLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalLocation
        fields = ["longitude", "latitude"]

class HospitalSerializer(serializers.ModelSerializer):
    contactNumber = serializers.CharField(source="contact_number")
    location = HospitalLocationSerializer()
    createdBy = serializers.StringRelatedField(read_only=True, source="created_by")

    class Meta:
        model = Hospital
        fields = ["id", "createdBy", "name", "contactNumber", "address", "location"]

    def create(self, validated_data):
        created_by = validated_data.pop("created_by", None)
        return create_hospital(validated_data, created_by=created_by)

    def update(self, instance, validated_data):
        return update_hospital(instance, validated_data)
