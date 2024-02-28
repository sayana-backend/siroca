from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework import filters
from .models import ApplicationForm, Checklist,Comments
from .serializers import ApplicationFormSerializer, ChecklistSerializer,CommentsSerializer






class BaseViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    pass

class ApplicationFormAPIView(BaseViewSet):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = '__all__'
    filterset_fields = ['task_number', 'title', 'description', 'main_client', 'main_manager', 'start_date', 'priority', 'status', 'checklist', 'comments' ]

class ChecklistAPIView(BaseViewSet):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = '__all__'
    filterset_fields = ['completed', 'text', 'manager']


class CommentsAPIView(BaseViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = '__all__'
    filterset_fields = '__all__'