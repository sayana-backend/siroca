from django.urls import path
from ..application.views import (ApplicationFormListAPIView,
                                 ApplicationFormCreateAPIView,
                                 ApplicationLogsListCreateAPIView,
                                 ApplicationFormRetrieveUpdateDestroyAPIView,
                                 ChecklistAPIView,
                                 CommentsAPIView)


urlpatterns = [
    path('logs/', ApplicationLogsListCreateAPIView.as_view()),
    path('create/', ApplicationFormCreateAPIView.as_view()),
    path('form/', ApplicationFormListAPIView.as_view()),
    path('form/<int:id>/', ApplicationFormRetrieveUpdateDestroyAPIView.as_view()),
    path('checklist/', ChecklistAPIView.as_view()),
    path('comments/', CommentsAPIView.as_view()),
    # path('logs/<int:id>/', ApplicationLogsRetrieveUpdateDestroyAPIView.as_view()),
    # path('comments/<int:id>/', CommentsDetailAPIView.as_view()),
    # path('checklist/<int:id>/', CheckListDetailAPIView.as_view()),
]



