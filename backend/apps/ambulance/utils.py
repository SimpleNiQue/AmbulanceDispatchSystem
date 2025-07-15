from utils.main import BaseStrEnum


class StatusEnum(BaseStrEnum):
    AVAILABLE = "Available"
    BUSY = "Busy"
    OFFLINE = "Offline"

    
class AmbulanceTypeEnum(BaseStrEnum):
    BLS = "Basic Life Support"
    ALS = "Advanced Life Support"
    ICU = "Intensive Care Unit"
    PTA = "Patient Transport Ambulance"
    AIR = "Air Ambulance"
    WATER = "Water Ambulance"
    