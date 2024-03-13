from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.CompanyListCreateAPIView.as_view()),
    path('list/<int:id>/', views.CompanyRetrieveUpdateDestroyAPIView.as_view()),

    path('jobtitles/', views.JobTitleListCreateAPIView.as_view()),
]
