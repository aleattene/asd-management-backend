from rest_framework.routers import SimpleRouter

from .views import SportDoctorViewSet

router: SimpleRouter = SimpleRouter()
router.register("doctors", SportDoctorViewSet, basename="doctor")

urlpatterns: list = router.urls
