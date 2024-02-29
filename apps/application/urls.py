from rest_framework.routers import DefaultRouter
from ..application.views import ApplicationFormListCreateAPIView, \
    ApplicationLogsListCreateAPIView, ApplicationLogsRetrieveUpdateDestroyAPIView, ApplicationFormRetrieveUpdateDestroyAPIView

from django.urls import include, path


# router = DefaultRouter()
# router.register(r'', ApplicationFormAPIView, "api_application")
# router.register(r'logs', ApplicationLogsAPIView, "api_application_logs")



# urlpatterns = router.urls

urlpatterns = [
    path('logs/', ApplicationLogsListCreateAPIView.as_view()),
    path('logs/<int:id>/', ApplicationLogsRetrieveUpdateDestroyAPIView.as_view()),
    path('form/', ApplicationFormListCreateAPIView.as_view()),
    path('form/<int:id>/', ApplicationFormRetrieveUpdateDestroyAPIView.as_view()),
]
