from utils.main import BaseStrEnum

class UserTypesEnum(BaseStrEnum):
    ADMIN = "admin"
    PATIENT = "patient"
    
class DB_NAMES(BaseStrEnum):
    User = "User"
    Profile = "Profile"
    
class GenderEnum(BaseStrEnum):
    MALE = "male"
    FEMALE = "female"
    