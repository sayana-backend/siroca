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


class ApplicationLogsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationLogs.objects.all()
    serializer_class = ApplicationLogsSerializer
    lookup_field = 'id'





class ChecklistAPIView(generics.CreateAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # search_fields = '__all__'
    # filterset_fields = ['completed', 'text', 'manager']


class CheckListDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    lookup_field = 'id'


class CommentsAPIView(generics.CreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class CommentsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    lookup_field = 'id'







