from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from ..application.models import ApplicationLogs
from ..application.serializers import ApplicationLogsSerializer, ApplicationFormLogsDetailSerializer, \
    ApplicationFormSerializer
from .models import ApplicationForm, Checklist, Comments
from .serializers import ChecklistSerializer, CommentsSerializer
from rest_framework import generics

from ..company.views import BaseViewSet


class ApplicationFormAPIView(BaseViewSet):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = '__all__'
    filterset_fields = ['task_number', 'title', 'description', 'username', 'manager', 'start_date', 'priority',
                        'status']


class ApplicationFormListCreateAPIView(generics.ListCreateAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormLogsDetailSerializer


class ApplicationFormRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormLogsDetailSerializer
    lookup_field = 'id'


class ApplicationLogsListCreateAPIView(generics.ListCreateAPIView):
    queryset = ApplicationLogs.objects.all()
    serializer_class = ApplicationLogsSerializer


class ApplicationLogsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationLogs.objects.all()
    serializer_class = ApplicationLogsSerializer
    lookup_field = 'id'


class ChecklistAPIView(generics.ListCreateAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer


class CheckListDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    lookup_field = 'id'


class CommentsAPIView(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class CommentsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    lookup_field = 'id'
