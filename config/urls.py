from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/company/', include('apps.company.urls')),
    path('api/v1/applications/', include('apps.application.urls')),
    path('api/v1/users/', include('apps.user.urls')),

]

