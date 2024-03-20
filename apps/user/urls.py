from django.urls import path
from .views import *
from apps.application.views import NotificationListAPIView


urlpatterns = [
    path('create/', CreateUserView.as_view()),
    path('profiles/', ListUserProfileView.as_view()),
    path('<int:id>/', DetailUserProfileView.as_view()),
    path('<int:id>/notifications/', NotificationListAPIView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('admin-contacts/', ContactDetailView.as_view()),
    path('contacts/', ContactListView.as_view()),
    path('managerpermissions/', ManagerPermissionsView.as_view()),
    path('clientpermissions/', ClientPermissionsView.as_view()),
    # path('clientpermissions/get',ClientPermissionsListView.as_view())
]

