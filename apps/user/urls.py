from django.urls import path
from .views import CreateUserView,ListUserProfileView,DetailUserProfileView,UserLoginView
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('create/', CreateUserView.as_view()),
    path('profiles/', ListUserProfileView.as_view()),
    path('<int:id>/', DetailUserProfileView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
]