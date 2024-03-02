from report.export import ApplicationFormFilterAPIView, ExportToExcelView
from apps.application.views import (ApplicationFormAPIView)
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.application.views import ChecklistAPIView, CommentsAPIView, CheckListDetailAPIView, CommentsDetailAPIView
from ..application.views import (ApplicationFormListCreateAPIView,
                                 ApplicationLogsListCreateAPIView,
                                 ApplicationLogsRetrieveUpdateDestroyAPIView,
                                 ApplicationFormRetrieveUpdateDestroyAPIView,)


router = DefaultRouter()
router.register('crud', ApplicationFormAPIView, "api_application_crud")

urlpatterns = [
    path('', include(router.urls)),
    path('filter/export-to-excel/', ExportToExcelView.as_view(), name='export_to_excel_view'),
    path('filter/', ApplicationFormFilterAPIView.as_view({'get': 'list'})),
    path('logs/', ApplicationLogsListCreateAPIView.as_view()),
    path('logs/<int:id>/', ApplicationLogsRetrieveUpdateDestroyAPIView.as_view()),
    path('form/', ApplicationFormListCreateAPIView.as_view()),
    path('form/<int:id>/', ApplicationFormRetrieveUpdateDestroyAPIView.as_view()),
    path('checklist/', ChecklistAPIView.as_view()),
    path('checklist/<int:id>/', CheckListDetailAPIView.as_view()),
    path('comments/', CommentsAPIView.as_view()),
    path('comments/<int:id>/', CommentsDetailAPIView.as_view()),
]

