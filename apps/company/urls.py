from rest_framework.routers import DefaultRouter
from django.urls import path
from ..company.views import CompanyAPIView,JobTitleAPIView

router = DefaultRouter()
router.register('', CompanyAPIView, "api_company")
router.register('', JobTitleAPIView, "api_jobtitle")


urlpatterns =router.urls


