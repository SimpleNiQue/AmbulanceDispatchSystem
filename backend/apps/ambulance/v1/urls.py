from rest_framework.routers import DefaultRouter
from apps.ambulance.v1.views import AmbulanceViewSet

router = DefaultRouter()
router.register(r"ambulance", AmbulanceViewSet, basename="hospital")

urlpatterns = router.urls
