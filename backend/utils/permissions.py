from rest_framework import permissions

from apps.user.utils import UserTypesEnum


class IsAdmin(permissions.BasePermission):
    """
    Safety check for Admins
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.role == UserTypesEnum.ADMIN)
        )
        

class IsPatient(permissions.BasePermission):
    """
    Safety check for Patients
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.role == UserTypesEnum.PATIENT)
        )