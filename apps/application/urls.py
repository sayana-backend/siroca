from django.urls import path
from . import views


urlpatterns = [
    path('', views.ApplicationFormListCreateAPIView.as_view()),
    path('<int:id>/', views.ApplicationFormRetrieveUpdateDestroyAPIView.as_view()),
]