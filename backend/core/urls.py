from django.urls import path, include

urlpatterns = [
    path("v1/users/", include("apps.user.v1.urls")),
    path("v1/", include("apps.hospital.v1.urls")),
    path("v1/", include("apps.ambulance.v1.urls")),
]
