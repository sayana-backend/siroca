from django.urls import path
from .views import *



urlpatterns = [
    path('create/', CompanyCreateAPIView.as_view()),
    path('list/', CompanyListAPIView.as_view()),
    path('<int:id>/', CompanyRetrieveUpdateDestroyAPIView.as_view()),
    path('list_job-title/', JobTitleListAPIView.as_view()),
    path('create_job-title/', JobTitleListAPIView.as_view()),
    path('code/', generate_codes_view),
    path('logo/', LogoAPIView.as_view())
]


