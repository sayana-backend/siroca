from . import views
from django.urls import path



urlpatterns = [
    path('logs/', views.ApplicationLogsListCreateAPIView.as_view()),
    path('logs/<int:id>/', views.ApplicationLogsRetrieveUpdateDestroyAPIView.as_view()),
    path('create/', views.ApplicationFormCreateAPIView.as_view()),
    path('form/', views.ApplicationFormListAPIView.as_view()),
    path('form/<int:id>/', views.ApplicationFormRetrieveUpdateDestroyAPIView.as_view()),
    path('checklist/', views.ChecklistAPIView.as_view()),
    path('checklist/<int:id>/', views.CheckListDetailAPIView.as_view()),
    path('comments/', views.CommentsAPIView.as_view()),
    path('comments/<int:id>/', views.CommentsDetailAPIView.as_view()),
]
