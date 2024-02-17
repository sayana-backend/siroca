from django.shortcuts import render
from rest_framework.generics import (ListAPIView,
                                     ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from .models import UserProfile, ManagerProfile, AdminProfile
from .serializetors import UserProfileSerializer, ManagerProfileSerializer, AdminProfileSerializer


class UserProfileLISTView(ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'id'


class ManagerProfileLISTView(ListCreateAPIView):
    queryset = ManagerProfile.objects.all()
    serializer_class = ManagerProfileSerializer


class ManagerProfileDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ManagerProfile.objects.all()
    serializer_class = ManagerProfileSerializer
    lookup_field = 'id'


class AdminProfileLISTView(ListCreateAPIView):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer


class AdminProfileDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer
    lookup_field = 'id'
