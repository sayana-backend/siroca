from rest_framework.routers import DefaultRouter
from apps.application.views import ApplicationFormAPIView,ChecklistAPIView,CommentsSerializer

router = DefaultRouter()
router.register('', ApplicationFormAPIView, "api_application")
router.register('', ChecklistAPIView, "api_checklist")
router.register('', ChecklistAPIView, "api_comments")



urlpatterns =router.urls

