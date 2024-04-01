from django.urls import path
from .views import *
from apps.application.views import NotificationListAPIView


urlpatterns = [
    path('create/', CreateUserView.as_view()),
    path('profiles/', ListUserProfileView.as_view()),
    path('<int:id>/', DetailUserProfileView.as_view()),
    path('<int:id>/notifications/', NotificationListAPIView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('managerpermissions/general/', ManagerPermissionsGeneralView.as_view()),
    path('clientpermissions/general/', ClientPermissionsGeneralView.as_view()),
    path('clientpermissions/detail/', ClientPermissionsDetailAPIView.as_view()),
    path('managerpermissions/detail/', ManagerPermissionsDetailAPIView.as_view()),
]

