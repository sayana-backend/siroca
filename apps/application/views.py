from django.shortcuts import render
from .models import ApplicationForm
from .serializers import ApplicationFormSerializer, ApplicationFormDetailSerializer
from rest_framework.generics import ListCreateAPIView,  RetrieveUpdateDestroyAPIView
from ..user.models import UserProfile, UserManager, AdminProfile


class ApplicationFormListCreateAPIView(ListCreateAPIView):

    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormSerializer
    permission_classes = (UserManager, UserProfile,  AdminProfile,)

class ApplicationFormRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer
    permission_classes = (UserManager, AdminProfile,)
    lookup_field = 'id'