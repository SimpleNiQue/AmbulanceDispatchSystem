from rest_framework.views import APIView
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from apps.emergency.models import EmergencyRequest, EmergencyRequestLocation
from apps.emergency.v1.serializers import EmergencyRequestSerializer
from apps.emergency.v1.services import assign_nearest_ambulance
from utils.responses import api_response
from utils.permissions import IsAdmin, IsPatient


class EmergencyRequestView(APIView):
    """
    Handles:
    - POST for users to create emergency requests
    - GET (list & detail), PUT, PATCH for admins
    """
    def get_permissions(self):
        if self.request.method in ["GET", "PUT", "PATCH"]:
            return [IsAdmin()]
        return [IsPatient()]

    def post(self, request):
        serializer = EmergencyRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            location_data = serializer.validated_data.pop('location')

            # Step 1: Create emergency request without ambulance
            emergency = EmergencyRequest.objects.create(user=user, **serializer.validated_data)

            # Step 2: Save patient location
            EmergencyRequestLocation.objects.create(
                emergency=emergency,
                latitude=location_data['latitude'],
                longitude=location_data['longitude']
            )

            # Step 3: Assign nearest ambulance
            try:
                assign_nearest_ambulance(emergency)
            except Exception as e:
                return api_response(
                    status=status.HTTP_400_BAD_REQUEST,
                    message=str(e)
                )

            # Step 4: Serialize and return
            response_serializer = EmergencyRequestSerializer(emergency)
            return api_response(
                status=status.HTTP_201_CREATED,
                message="Emergency request submitted and ambulance assigned successfully.",
                data=response_serializer.data
            )

        return api_response(
            status=status.HTTP_400_BAD_REQUEST,
            message="Validation error",
            data=serializer.errors
        )

    def get(self, request, pk=None):
        if pk:
            emergency = get_object_or_404(EmergencyRequest, pk=pk)
            serializer = EmergencyRequestSerializer(emergency)
            return api_response(
                status=status.HTTP_200_OK,
                message="Emergency request retrieved successfully.",
                data=serializer.data
            )
        queryset = EmergencyRequest.objects.all().order_by('-date_created')
        serializer = EmergencyRequestSerializer(queryset, many=True) 
        
        message = "No emergency request" if len(queryset) < 1 else "All emergency requests retrieved successfully."
        return api_response(
            status=status.HTTP_200_OK,
            message=message,
            data=serializer.data or None,
        )
        

    def put(self, request, pk):
        emergency = get_object_or_404(EmergencyRequest, pk=pk)
        serializer = EmergencyRequestSerializer(emergency, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                status=status.HTTP_200_OK,
                message="Emergency request updated successfully.",
                data=serializer.data
            )
        return api_response(
            status=status.HTTP_400_BAD_REQUEST,
            message="Validation error",
            data=serializer.errors
        )

    def patch(self, request, pk):
        emergency = get_object_or_404(EmergencyRequest, pk=pk)
        serializer = EmergencyRequestSerializer(emergency, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                status=status.HTTP_200_OK,
                message="Emergency request partially updated successfully.",
                data=serializer.data
            )
        return api_response(
            status=status.HTTP_400_BAD_REQUEST,
            message="Validation error",
            data=serializer.errors
        )
