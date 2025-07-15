from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from django.db import transaction

from apps.ambulance.models import Ambulance
from apps.ambulance.v1.serializers import AmbulanceSerializer
from utils.permissions import IsAdmin
from utils.responses import api_response


class AmbulanceViewSet(viewsets.ModelViewSet):
    queryset = Ambulance.objects.select_related("hospital", "created_by").all()
    serializer_class = AmbulanceSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdmin()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        message = "No Ambulance found" if len(queryset) < 1 else "Ambulances retrieved successfully."
        return api_response(
            status=status.HTTP_200_OK,
            message=message,
            data=serializer.data or None,
        )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Ambulance.DoesNotExist:
            raise NotFound("Ambulance not found.")
        serializer = self.get_serializer(instance)
        return api_response(
            status=status.HTTP_200_OK,
            message="Ambulance retrieved successfully.",
            data=serializer.data,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            self.perform_create(serializer)
        return api_response(
            status=status.HTTP_201_CREATED,
            message="Ambulance created successfully.",
            data=serializer.data,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            self.perform_update(serializer)
        return api_response(
            status=status.HTTP_200_OK,
            message="Ambulance updated successfully.",
            data=serializer.data,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        with transaction.atomic():
            self.perform_destroy(instance)
        return api_response(
            status=status.HTTP_204_NO_CONTENT,
            message="Ambulance deleted successfully.",
            data=None,
        )
