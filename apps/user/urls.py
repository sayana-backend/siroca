from django.urls import path
from .views import *



urlpatterns = [
    path('create/', CreateUserView.as_view()),
    path('profiles/', ListUserProfileView.as_view()),
    path('<int:id>/', DetailUserProfileView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('managerpermissions/', ManagerPermissionsView.as_view()),
    path('clientpermissions/', ClientPermissionsView.as_view())
]