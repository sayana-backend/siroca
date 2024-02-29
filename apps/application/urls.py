from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.application.views import (ApplicationFormAPIView,
                                    # ApplicationFormFilterAPIView,
                                    # ExportToExcelView
    )
from report.export import ApplicationFormFilterAPIView, ExportToExcelView

router = DefaultRouter()
router.register('crud', ApplicationFormAPIView, "api_application_crud")

urlpatterns = [
    path('', include(router.urls)),
    path('filter/export-to-excel/', ExportToExcelView.as_view(), name='export_to_excel_view'),
    path('filter/', ApplicationFormFilterAPIView.as_view({'get': 'list'}))
]

