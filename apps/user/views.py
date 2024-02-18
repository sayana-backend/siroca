from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet
from django.urls import reverse_lazy
from .models import UserProfile, ManagerProfile, AdminProfile
from django.contrib.auth.mixins import PermissionRequiredMixin
from .serializers import UserProfileSerializer, AdminProfileSerializer, ManagerProfileSerializer


class AddUserProfileView(PermissionRequiredMixin, ModelViewSet):
    model = UserProfile
    serializer_class = UserProfileSerializer
    template_name = ''
    success_url = reverse_lazy('')  
    permission_required = 'user.add_user_userprofile'


class AddManagerProfileView(PermissionRequiredMixin, ModelViewSet):
    model = ManagerProfile
    serializer_class = ManagerProfileSerializer
    template_name = ''
    success_url = reverse_lazy('') 
    permission_required = 'user.add_user_managerprofile'


class AddAdminProfileView(PermissionRequiredMixin, ModelViewSet):
    model = AdminProfile
    serializer_class = AdminProfileSerializer
    template_name = ''
    success_url = reverse_lazy('') 
    permission_required = 'user.add_user_managerprofile'
    

