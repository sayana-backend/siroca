
from rest_framework.routers import DefaultRouter
from apps.user.views import AddAdminProfileView, AddManagerProfileView, AddUserProfileView

router = DefaultRouter()
router.register('client', AddUserProfileView, "api_user")
router.register('manager', AddManagerProfileView, "api_manager")
router.register('admin', AddAdminProfileView, "api_admin")

urlpatterns = router.urls

