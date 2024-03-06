from django.urls import path
from report.export import (ApplicationFormFilterAPIView, ExportToExcelView)
from ..application.views import *


urlpatterns = [
    path('filter/export-to-excel/', ExportToExcelView.as_view(), name='export_to_excel_view'),
    path('filter/', ApplicationFormFilterAPIView.as_view({'get': 'list'})),
    path('logs/', ApplicationLogsListCreateAPIView.as_view()),
    path('create/', ApplicationFormCreateAPIView.as_view()),
    path('form/', ApplicationFormListAPIView.as_view()),
    path('form/<int:id>/', ApplicationFormRetrieveUpdateDestroyAPIView.as_view()),
    path('checklist/', ChecklistAPIView.as_view()),
    path('comments/', CommentsAPIView.as_view()),
    path('logs/<int:id>/', ApplicationLogsRetrieveUpdateDestroyAPIView.as_view()),
    path('comments/<int:id>/', CommentsDetailAPIView.as_view()),
    path('checklist/<int:id>/', CheckListDetailAPIView.as_view()),
]

