from report.export import (ApplicationFormFilterAPIView, ExportToExcelView)
from .views import *
from django.urls import path


urlpatterns = [

    path('filter/export-to-excel/', ExportToExcelView.as_view(), name='export_to_excel_view'),
    path('filter/', ApplicationFormFilterAPIView.as_view({'get': 'list'})),
    path('logs/', ApplicationLogsListCreateAPIView.as_view()),
    path('create/', ApplicationFormCreateAPIView.as_view()),
    path('form/', ApplicationFormListAPIView.as_view()),
    path('form_redact/<int:id>/', ApplicationFormRetrieveUpdateDestroyAPIView.as_view()),
    path('form_view/<int:id>/', ApplicationFormRetrieveAPIView.as_view()),
    path('checklist/', ChecklistAPIView.as_view()),
    path('comments/', CommentsAPIView.as_view()),
    # path('logs/<int:id>/', ApplicationLogsRetrieveUpdateDestroyAPIView.as_view()),
    path('notifications/', NotificationAPIView.as_view()),
    path('comments/<int:id>/', CommentsDetailAPIView.as_view()),
    path('checklist/<int:id>/', CheckListDetailAPIView.as_view()),
]
