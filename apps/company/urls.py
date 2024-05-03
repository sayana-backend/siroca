from django.urls import path
from .views import *


urlpatterns = [
    path('create/', CompanyCreateAPIView.as_view()),
    path('list/', CompanyListAPIView.as_view()),
    path('detail/<int:id>/', CompanyDetailAPIView.as_view()),  # GET
    path('edit/<int:id>/', CompanyRetrieveUpdateDestroyAPIView.as_view()), # GET PUT DELETE

    path('list_job-title/', JobTitleListAPIView.as_view()),
    path('create_job-title/', JobTitleCreateAPIView.as_view()),
    path('delete_job-title/<int:id>/', JobTitleDestroyAPIView.as_view()),

    path('code/', generate_codes_view),
    path('logo/', LogoAPIView.as_view()),
    path('name_list/', CompanyOnlyNameListAPIView.as_view()),

]


