from rest_framework.routers import DefaultRouter
from django.urls import path
from ..company.views import CompanyAPIView,JobTitleAPIView, UsersInfoAPIView, generate_codes_view

router = DefaultRouter()
router.register('', CompanyAPIView, "api_company")
router.register('', JobTitleAPIView, "api_jobtitle")


urlpatterns =router.urls


