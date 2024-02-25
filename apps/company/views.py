from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from ..company.models import Company, JobTitle
from ..company.serializers import CompanySerializer, JobTitleSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend



class BaseViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    pass

class CompanyAPIView(BaseViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['name', 'country']  
    filterset_fields = '__all__'

class JobTitleAPIView(BaseViewSet):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
