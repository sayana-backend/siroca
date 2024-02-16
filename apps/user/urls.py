from django.urls import path
from . import views


urlpatterns = [
    path('userprofile/', views.user_view)
]
