from report.export import (ApplicationFormFilterAPIView, ExportToExcelView)
from .views import *
from django.urls import path
urlpatterns = [

    path('filter/export-to-excel/', ExportToExcelView.as_view(), name='export_to_excel_view'),
    path('filter/', ApplicationFormFilterAPIView.as_view({'get': 'list'})),
    path('logs/', ApplicationLogsListCreateAPIView.as_view()),
    path('file/', FileListCreateAPIView.as_view()),
    path('delete_file/<int:id>/', FileDeleteAPIView.as_view()),
    path('description/<int:id>/', ApplicationsOnlyDescriptionAPIView.as_view()),


    path('create/', ApplicationFormCreateAPIView.as_view()),   # POST
    path('form_edit/<int:id>/', ApplicationFormRetrieveUpdateAPIView.as_view()), # GET PUT (id)
    path('form_view/<int:id>/', ApplicationFormRetrieveAPIView.as_view()), # GET (id)
    path('form_delete/<int:id>/', ApplicationFormDestroyAPIView.as_view()), # DELETE (id)
    path('form/', ApplicationFormListAPIView.as_view()), # GET

    path('checklist/', ChecklistListCreateAPIView.as_view()),
    path('checklist/<int:id>/', CheckListDetailAPIView.as_view()),
    path('subtask/', SubTaskCreateAPIView.as_view()),
    path('subtask/<int:id>/', SubTaskDetailAPIView.as_view()),
    path('comments/', CommentsAPIView.as_view()),
    path('comments/<int:id>/', CommentsDetailAPIView.as_view()),

    path('notifications/', NotificationListAPIView.as_view()),
    path('notifications/delete/<int:id>/', NotificationDeleteViewAPI.as_view()),
    path('notifications/delete/all/', NotificationDeleteViewAPI.as_view()),
    path('notifications/has_new/', NewNotificationAPIView.as_view()),
]




