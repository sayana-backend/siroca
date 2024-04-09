from django.urls import path
from .views import *



urlpatterns = [
    path('create/', CompanyCreateAPIView.as_view()),
    path('list/', CompanyListAPIView.as_view()),
    path('list/<int:id>/', CompanyListDetailAPIView.as_view()),
    path('<int:id>/', CompanyRetrieveUpdateDestroyAPIView.as_view()),
    path('list_job-title/', JobTitleListAPIView.as_view()),
    path('create_job-title/', JobTitleCreateAPIView.as_view()),
    path('destroy_job-title/<int:id>/', JobTitleDestroyAPIView.as_view()),
    path('code/', generate_codes_view),
    path('logo/', LogoAPIView.as_view())
]


