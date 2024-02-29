
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..user.models import UserProfile, ManagerProfile, AdminProfile
from rest_framework import mixins
from ..application.models import ApplicationForm, ApplicationLogs
from ..application.serializers import ApplicationLogsSerializer, ApplicationFormLogsDetailSerializer
from rest_framework.viewsets import GenericViewSet

from rest_framework.viewsets import ModelViewSet
from django.urls import reverse_lazy
from rest_framework import generics


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


#####  НЕ ИСПОЛЬЗОВАТЬ #####

# class BaseViewSet(GenericViewSet,
#                   mixins.ListModelMixin,
#                   mixins.RetrieveModelMixin,
#                   mixins.CreateModelMixin,
#                   mixins.UpdateModelMixin,
#                   mixins.DestroyModelMixin):
#     pass

# class ApplicationFormAPIView(BaseViewSet):
#     queryset = ApplicationForm.objects.all()
    # permission_classes = (ManagerProfile, UserProfile,  AdminProfile,)
    # filter_backends = (DjangoFilterBackend, SearchFilter)
    # search_fields = '__all__'
    # filterset_fields = ['task_number', 'title', 'description', 'username', 'manager', 'start_date', 'priority', 'status']

    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return ApplicationFormDetailSerializer
    #     return ApplicationFormSerializer



# class ApplicationLogsAPIView(BaseViewSet):
#     queryset = ApplicationLogs.objects.all()
    # permission_classes = (ManagerProfile, UserProfile, AdminProfile,)
    # filter_backends = (DjangoFilterBackend, SearchFilter)
    # search_fields = '__all__'

    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return ApplicationLogsDetailSerializer
    #     return ApplicationLogsSerializer


