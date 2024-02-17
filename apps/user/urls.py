from django.urls import path
from . import views


urlpatterns = [
    path('', views.UserProfileLISTView.as_view()),
    path('<int:id>/', views.UserProfileDetailAPIView.as_view()),
    path('manager/', views.ManagerProfileLISTView.as_view()),
    path('manager/<int:id>/', views.ManagerProfileDetailAPIView.as_view()),
    path('admin-siroco/', views.AdminProfileLISTView.as_view()),
    path('admin-siroco/<int:id>/', views.AdminProfileDetailAPIView.as_view()),
]
