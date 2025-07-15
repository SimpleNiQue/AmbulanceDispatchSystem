from rest_framework.routers import DefaultRouter
from apps.hospital.v1.views import HospitalViewSet

router = DefaultRouter()
router.register(r"hospitals", HospitalViewSet, basename="hospital")

urlpatterns = router.urls
