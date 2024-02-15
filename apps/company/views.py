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

class JobTitleAPIView(BaseViewSet):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer
