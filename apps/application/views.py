
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


from .models import ApplicationForm
from rest_framework import mixins
from apps.application.models import ApplicationForm
from apps.application.serializers import ApplicationFormSerializer
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
    serializer_class = ApplicationFormSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = '__all__'
    filterset_fields = ['task_number', 'title', 'description', 'username', 'manager', 'start_date', 'priority', 'status'] 



