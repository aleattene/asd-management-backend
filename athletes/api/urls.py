from rest_framework.routers import DefaultRouter

from .views import AthleteViewSet, CategoryViewSet

router: DefaultRouter = DefaultRouter()
router.register("athletes", AthleteViewSet, basename="athlete")
router.register("categories", CategoryViewSet, basename="category")

urlpatterns: list = router.urls
