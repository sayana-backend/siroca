from rest_framework import filters
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from apps.company.models import Company, JobTitle
from apps.company.serializers import CompanySerializer, JobTitleSerializer

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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country']  
    ordering_fields = '__all__'  

class JobTitleAPIView(BaseViewSet):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
