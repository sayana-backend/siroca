
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ApplicationFormDetailSerializer, ApplicationFormSerializer
from ..user.models import UserProfile, ManagerProfile, AdminProfile
from rest_framework import mixins
from ..application.models import ApplicationForm
from ..application.serializers import ApplicationFormSerializer
from rest_framework.viewsets import GenericViewSet




class BaseViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    pass

class ApplicationFormAPIView(BaseViewSet):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer, ApplicationFormSerializer
    permission_classes = (ManagerProfile, UserProfile,  AdminProfile,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = '__all__'
    filterset_fields = ['task_number', 'title', 'description', 'username', 'manager', 'start_date', 'priority', 'status'] 



