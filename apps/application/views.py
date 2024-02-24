from django.shortcuts import render

from report.filter import ApplicationFilter
from .models import ApplicationForm
from .serializers import ApplicationFormSerializer, ApplicationFormDetailSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend


class ApplicationFormListCreateAPIView(ListCreateAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormSerializer


class ApplicationFormRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer

    lookup_field = 'id'
