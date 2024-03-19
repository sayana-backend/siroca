from django.urls import path
from .views import (CreateUserView, ListUserProfileView,
                    DetailUserProfileView, UserLoginView,AdminContactDetailView)
from apps.application.views import NotificationListAPIView

urlpatterns = [
    path('create/', CreateUserView.as_view()),
    path('profiles/', ListUserProfileView.as_view()),
    path('<int:id>/', DetailUserProfileView.as_view()),
    path('<int:id>/notifications/', NotificationListAPIView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('admin_contacts/', AdminContactDetailView.as_view()),
]

