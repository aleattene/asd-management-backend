from rest_framework.routers import DefaultRouter

from .views import TrainerViewSet, SportDoctorViewSet

router: DefaultRouter = DefaultRouter()
router.register("trainers", TrainerViewSet, basename="trainer")
router.register("doctors", SportDoctorViewSet, basename="doctor")

urlpatterns: list = router.urls
