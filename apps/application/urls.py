from rest_framework.routers import DefaultRouter
from ..application.views import ApplicationFormAPIView

router = DefaultRouter()
router.register('', ApplicationFormAPIView, "api_application")


urlpatterns = router.urls

