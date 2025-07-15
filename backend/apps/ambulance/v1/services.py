from typing import Dict
from apps.ambulance.models import Ambulance, AmbulanceLocation


def create_ambulance_with_location(validated_data: Dict) -> Ambulance:
    location_data = validated_data.pop("location")
    ambulance = Ambulance.objects.create(**validated_data)
    AmbulanceLocation.objects.create(ambulance=ambulance, **location_data)
    return ambulance


def update_ambulance_with_location(instance: Ambulance, validated_data: Dict) -> Ambulance:
    location_data = validated_data.pop("location", None)

    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    instance.save()

    if location_data:
        AmbulanceLocation.objects.update_or_create(
            ambulance=instance, defaults=location_data
        )

    return instance
