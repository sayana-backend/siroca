from report.export import (ApplicationFormFilterAPIView, ExportToExcelView)
from .views import *
from django.urls import path


urlpatterns = [

    path('filter/export-to-excel/', ExportToExcelView.as_view(), name='export_to_excel_view'),
    path('filter/', ApplicationFormFilterAPIView.as_view({'get': 'list'})),
    path('logs/', ApplicationLogsListCreateAPIView.as_view()),
    path('notifications/', NotificationAPIView.as_view()),

    path('create/', ApplicationFormCreateAPIView.as_view()),   # POST
    path('form_redact/<int:id>/', ApplicationFormRetrieveUpdateAPIView.as_view()), # GET PUT (id)
    path('form_view/<int:id>/', ApplicationFormRetrieveUpdateDestroyAPIView.as_view()), # GET DELETE (id)
    path('form/', ApplicationFormListAPIView.as_view()), # GET

    path('checklist/', ChecklistAPIView.as_view()),
    path('comments/', CommentsAPIView.as_view()),
    # path('logs/<int:id>/', ApplicationLogsRetrieveUpdateDestroyAPIView.as_view()),
    path('notifications/', NotificationAPIView.as_view()),
    # path('notifications/delete/<int:id>/', NotificationDestroyAPIView.as_view()),
    # path('notifications/delete-all/', NotificationDestroyAPIView.as_view()),
    path('notifications/true/', NotificationTrueAPIView.as_view()),
    path('comments/<int:id>/', CommentsDetailAPIView.as_view()),
    path('checklist/<int:id>/', CheckListDetailAPIView.as_view()),

]


