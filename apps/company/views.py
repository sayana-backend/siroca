from rest_framework import generics
from .models import Company, JobTitle
from .serializers import CompanySerializer, JobTitleSerializer


class CompanyListAPIView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyCreateAPIView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'id'


class JobTitleListCreateAPIView(generics.ListCreateAPIView):
    queryset = JobTitle.objects.all()
    serializer_class = JobTitleSerializer

