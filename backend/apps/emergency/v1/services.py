from math import radians, cos, sin, asin, sqrt
from apps.ambulance.models import Ambulance, AmbulanceLocation
from apps.ambulance.utils import StatusEnum
from apps.emergency.models import EmergencyRequest, EmergencyRequestLocation
from django.utils import timezone
from datetime import timedelta


def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(float, (lat1, lon1, lat2, lon2))

    # Earth radius in km
    R = 6371.0

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return R * c



def assign_nearest_ambulance(emergency: EmergencyRequest) -> Ambulance:
    # Get patient coordinates
    patient_location = emergency.location
    patient_lat = patient_location.latitude
    patient_lon = patient_location.longitude

    # Step 1: Refresh all busy ambulances (expire if 30 mins passed)
    for ambulance in Ambulance.objects.filter(status="busy", busy_until__isnull=False):
        if timezone.now() > ambulance.busy_until:
            ambulance.status = StatusEnum.AVAILABLE
            ambulance.busy_until = None
            ambulance.save()

    # Step 2: Get available ambulances with valid locations
    ambulances = Ambulance.objects.filter(status=StatusEnum.AVAILABLE, location__isnull=False)

    if not ambulances.exists():
        raise Exception("No available ambulances") # TODO: RETURN A BETTER ERROR HERE

    # Step 3: Calculate distance to each available ambulance
    distances = []
    for amb in ambulances:
        amb_loc = amb.location
        distance = haversine_distance(
            patient_lat, patient_lon, amb_loc.latitude, amb_loc.longitude
        )
        distances.append((distance, amb))

    # Step 4: Select closest ambulance
    distances.sort(key=lambda x: x[0])
    selected_amb = distances[0][1]

    # Step 5: Assign & update ambulance status
    selected_amb.status = StatusEnum.BUSY
    selected_amb.busy_until = timezone.now() + timedelta(minutes=30)
    selected_amb.last_assigned = timezone.now()
    selected_amb.save()

    # Step 6: Attach ambulance to emergency
    emergency.ambulance = selected_amb
    emergency.response_time_seconds = 0 
    emergency.save()

    return selected_amb
