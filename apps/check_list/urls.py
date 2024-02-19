from rest_framework.routers import DefaultRouter

from apps.check_list.views import ChecklistAPIView

router = DefaultRouter()
router.register('', ChecklistAPIView, "api_checklist")


urlpatterns =router.urls