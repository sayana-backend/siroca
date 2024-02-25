
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet
from django.urls import reverse_lazy
from .models import UserProfile, ManagerProfile, AdminProfile
from django.contrib.auth.mixins import PermissionRequiredMixin
from .serializers import UserProfileSerializer, AdminProfileSerializer, ManagerProfileSerializer


class AddUserProfileView(PermissionRequiredMixin, ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    template_name = ''
    success_url = reverse_lazy('')
    permission_required = 'user.add_userprofile'
    # lookup_field = 'id'


class AddManagerProfileView(PermissionRequiredMixin, ModelViewSet):
    queryset = ManagerProfile.objects.all()
    serializer_class = ManagerProfileSerializer
    template_name = ''
    success_url = reverse_lazy('')
    permission_required = 'user.add_managerprofile'
    lookup_field = 'id'


class AddAdminProfileView(PermissionRequiredMixin, ModelViewSet):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer
    template_name = ''
    success_url = reverse_lazy('')
    permission_required = 'user.add_adminprofile'
    lookup_field = 'id'

