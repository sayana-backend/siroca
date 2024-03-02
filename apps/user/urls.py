from django.urls import path
from .views import CreateUserView,ListUserProfileView,AllUsersView,UserLoginView


urlpatterns = [
    path('create/',CreateUserView.as_view()),
    path('profiles/',ListUserProfileView.as_view()),
    path('<int:id>/',AllUsersView.as_view()),
    path('login/',UserLoginView.as_view()),
]