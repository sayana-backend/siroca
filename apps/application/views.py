from ..application.serializers import ApplicationLogsSerializer, ApplicationFormLogsDetailSerializer
from apps.application.serializers import ApplicationFormSerializer
from ..application.models import ApplicationForm, ApplicationLogs
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from ..company.views import BaseViewSet
from rest_framework import generics


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
