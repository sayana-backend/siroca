from django.urls import path
from . import views


urlpatterns = [
    path('', views.UserListAPIView.as_view()),
    path('<int:id>/', views.UserDetailAPIView.as_view()),
    path('', views.ManagerListAPIView.as_view()),
    path('<int:id>/', views.ManagerDetailAPIView.as_view()),
    path('', views.AdminListAPIView.as_view()),
    path('<int:id>/', views.AdminDetailAPIView.as_view()),
]

