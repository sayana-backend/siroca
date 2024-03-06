from django.urls import path
from ..company.views import (CompanyListAPIView,
                             CompanyCreateAPIView,
                             CompanyRetrieveUpdateDestroyAPIView,
                             JobTitleListCreateAPIView)


urlpatterns = [
    path('create/', CompanyCreateAPIView.as_view()),
    path('list/', CompanyListAPIView.as_view()),
    path('<int:id>/', CompanyRetrieveUpdateDestroyAPIView.as_view()),
    path('job-title/', JobTitleListCreateAPIView.as_view()),
]