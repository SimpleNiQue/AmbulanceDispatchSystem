from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound 
from django.core.exceptions import ValidationError
from apps.hospital.models import Hospital
from apps.hospital.v1.serializers import HospitalSerializer
from apps.hospital.v1.services import create_hospital, update_hospital
from utils.permissions import IsAdmin
from utils.responses import api_response


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdmin()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        message = "No Hospital record" if not queryset else "Hospitals retrieved successfully."
        return api_response(
            status=status.HTTP_200_OK,
            message=message,
            data=serializer.data,
        )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Hospital.DoesNotExist:
            raise NotFound("Hospital not found.")

        serializer = self.get_serializer(instance)
        return api_response(
            status=status.HTTP_200_OK,
            message="Hospital retrieved successfully.",
            data=serializer.data,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            hospital = create_hospital(serializer.validated_data, created_by=request.user)
        except ValidationError as e:
            return api_response(
                status=status.HTTP_400_BAD_REQUEST,
                message=str(e)
            )

        output_serializer = self.get_serializer(hospital)
        return api_response(
            status=status.HTTP_201_CREATED,
            message="Hospital created successfully.",
            data=output_serializer.data,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        updated_instance = update_hospital(instance, serializer.validated_data)
        output_serializer = self.get_serializer(updated_instance)

        return api_response(
            status=status.HTTP_200_OK,
            message="Hospital updated successfully.",
            data=output_serializer.data,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_response(
            status=status.HTTP_204_NO_CONTENT,
            message="Hospital deleted successfully.",
            data=None,
        )
