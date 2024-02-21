from rest_framework.routers import DefaultRouter
from apps.application.views import ApplicationFormAPIView,ChecklistAPIView

router = DefaultRouter()
router.register('', ApplicationFormAPIView, "api_application")
router.register('', ChecklistAPIView, "api_checklist")



urlpatterns =router.urls

