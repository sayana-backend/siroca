from rest_framework.routers import DefaultRouter
from ..application.views import ApplicationFormAPIView, ApplicationLogsAPIView

router = DefaultRouter()
router.register(r'', ApplicationFormAPIView, "api_application")
router.register(r'logs', ApplicationLogsAPIView, "api_application_logs")



urlpatterns = router.urls

