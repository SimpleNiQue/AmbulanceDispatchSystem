from apps.hospital.models import Hospital, HospitalLocation
from typing import Dict
from django.db import transaction
from django.core.exceptions import ValidationError


@transaction.atomic
def create_hospital(validated_data: Dict, created_by=None) -> Hospital:
    location_data = validated_data.pop("location")

    exists = Hospital.objects.filter(
        name__iexact=validated_data["name"].strip(),
        address__iexact=validated_data["address"].strip(),
        location__latitude__iexact=location_data["latitude"].strip(),
        location__longitude__iexact=location_data["longitude"].strip(),
    ).exists()

    if exists:
        raise ValidationError("A hospital with the same name, address, and location already exists.")

    hospital = Hospital.objects.create(created_by=created_by, **validated_data)
    HospitalLocation.objects.create(hospital=hospital, **location_data)
    return hospital


@transaction.atomic
def update_hospital(instance: Hospital, validated_data: Dict) -> Hospital:
    location_data = validated_data.pop("location", None)

    # Only run duplicate check if location is being updated
    if location_data:
        latitude = location_data.get("latitude", "").strip()
        longitude = location_data.get("longitude", "").strip()
        name = validated_data.get("name", instance.name).strip()
        address = validated_data.get("address", instance.address).strip()

        exists = Hospital.objects.exclude(id=instance.id).filter(
            name__iexact=name,
            address__iexact=address,
            location__latitude__iexact=latitude,
            location__longitude__iexact=longitude,
        ).exists()

        if exists:
            raise ValidationError("Another hospital with the same name, address, and location already exists.")

    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    instance.save()

    if location_data:
        HospitalLocation.objects.update_or_create(
            hospital=instance, defaults=location_data
        )

    return instance
