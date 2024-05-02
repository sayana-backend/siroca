from django.urls import path
from .views import *


urlpatterns = [
    path('create/', CreateUserView.as_view()),            # POST
    path('profiles/', ListUserProfileView.as_view()),     # GET
    path('<int:id>/', DetailUserProfileView.as_view()),   # GET id
    path('destroy/<int:id>/', DeleteUserView.as_view()),  # DELETE
    path('edit/<int:id>/', UserUpdateView.as_view()),     # PUT

    path('login/', UserLoginView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('admin_reset_password/<int:id>/', AdminResetPasswordView.as_view()),
    path('admin_contacts/', AdminContactDetailView.as_view()),
    path('admin_contacts_list/', AdminContactListView.as_view()),

    path('managerpermissions/general/', ManagerPermissionsGeneralView.as_view()),
    path('clientpermissions/general/', ClientPermissionsGeneralView.as_view()),
    path('clientpermissions/detail/', ClientPermissionsDetailAPIView.as_view()),
    path('managerpermissions/detail/', ManagerPermissionsDetailAPIView.as_view()),
    path('userpermissions/<int:id>/', UserPermissionsDetailAPIView.as_view()),



]

