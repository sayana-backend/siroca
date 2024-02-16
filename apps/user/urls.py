from django.urls import path
from . import views


urlpatterns = [
    path('userprofile/<int:id>/', views.userprofile_view)
]
