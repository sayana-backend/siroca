from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from ..application.models import ApplicationForm, ApplicationLogs
from ..application.serializers import ApplicationLogsSerializer, ApplicationFormLogsDetailSerializer
from rest_framework import filters
from .models import ApplicationForm, Checklist,Comments
from .serializers import ApplicationFormDetailSerializer, ChecklistSerializer,CommentsSerializer
from rest_framework import generics
from apps.user.permissions import *
from rest_framework import permissions



class ApplicationFormListCreateAPIView(generics.ListCreateAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormLogsDetailSerializer
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # search_fields = '__all__'
    # filterset_fields = ['task_number', 'title', 'description', 'main_client', 'main_manager', 'start_date', 'priority', 'status', 'checklist', 'comments' ]

class ApplicationFormRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormLogsDetailSerializer
    lookup_field = 'id'

class ApplicationLogsListCreateAPIView(generics.ListCreateAPIView):
    queryset = ApplicationLogs.objects.all()
    serializer_class = ApplicationLogsSerializer
    # permission_classes = [IsClientCanViewLogs,]
    permission_classes = [IsAuthenticated]
    
class ApplicationLogsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationLogs.objects.all()
    serializer_class = ApplicationLogsSerializer
    lookup_field = 'id'





class ChecklistAPIView(generics.ListCreateAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    permission_classes = [IsClientCanAddChecklist, ]
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # search_fields = '__all__'
    # filterset_fields = ['completed', 'text', 'manager']

class CheckListDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    lookup_field = 'id'





class CommentsAPIView(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsManagerCanEdit, IsClientCanPutComments]

class CommentsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    lookup_field = 'id'
    permission_classes = [IsManagerCanEdit, IsClientCanPutComments, IsClientCanDeleteComments, ]







