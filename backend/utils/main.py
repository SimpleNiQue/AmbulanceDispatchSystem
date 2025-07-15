from enum import StrEnum


class BaseStrEnum(StrEnum):
    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def options(cls):
        return [(member.value, member.value) for member in cls]

    @classmethod
    def options_list(cls):
        return [member.value for member in cls]


class DB_NAMES(BaseStrEnum):
    AuditBaseModel = "AuditBaseModel"
