from .models import ApplicationForm, Checklist, Comments, ApplicationLogs
from .serializers import (ApplicationFormDetailSerializer,
                          ChecklistSerializer,
                          CommentsSerializer,
                          ApplicationLogsSerializer)
from rest_framework import generics


class ApplicationFormCreateAPIView(generics.CreateAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer


class ApplicationFormListAPIView(generics.ListAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer



class ApplicationFormRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer
    lookup_field = 'id'


class ApplicationLogsListCreateAPIView(generics.ListCreateAPIView):
    queryset = ApplicationLogs.objects.all()
    serializer_class = ApplicationLogsSerializer


class ChecklistAPIView(generics.ListCreateAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer


class CommentsAPIView(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class ApplicationLogsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationLogs.objects.all()
    serializer_class = ApplicationLogsSerializer
    lookup_field = 'id'


class CheckListDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    lookup_field = 'id'


class CommentsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    lookup_field = 'id'

