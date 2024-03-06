<<<<<<< HEAD
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


=======
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
>>>>>>> origin/user_register

