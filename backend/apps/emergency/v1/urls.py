# apps/emergency/urls.py

# from django.urls import path
# from apps.emergency.v1.views import EmergencyRequestCreateView
# # from apps.ambulance.v1.services import get_ambulance_location  # Optional, if tracking

# urlpatterns = [
#     path('emergency-requests/', EmergencyRequestCreateView.as_view(), name='create-emergency-request'),
    
#     # Optional real-time tracking endpoint
#     # path('ambulances/<int:ambulance_id>/location/', get_ambulance_location, name='ambulance-location'),
# ]


# apps/emergency/urls.py

from django.urls import path
from apps.emergency.v1.views import EmergencyRequestView

urlpatterns = [
    path("emergency-requests/", EmergencyRequestView.as_view(), name="emergency-request-list-create"),
    path("emergency-requests/<int:pk>/", EmergencyRequestView.as_view(), name="emergency-request-detail"),
]
