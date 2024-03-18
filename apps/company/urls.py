from django.urls import path
from .views import *



urlpatterns = [
    path('create/', CompanyCreateAPIView.as_view()),
    path('list/', CompanyListAPIView.as_view()),
    path('<int:id>/', CompanyRetrieveUpdateDestroyAPIView.as_view()),
    path('job-title/', JobTitleListCreateAPIView.as_view()),
    path('code/', generate_codes_view)
]


