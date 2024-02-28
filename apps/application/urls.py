from rest_framework.routers import DefaultRouter
from apps.application.views import ApplicationFormAPIView,ChecklistAPIView, CommentsAPIView

router = DefaultRouter()
router.register('', ApplicationFormAPIView, "api_application")
router.register('checklist/', ChecklistAPIView, "api_checklist")
router.register('comments/', CommentsAPIView, "api_comments")



urlpatterns =router.urls

