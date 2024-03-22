from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model, authenticate


User = get_user_model()


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "role_type image first_name surname username password main_company job_title".split()

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user



class ManagerPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['manager_can_edit', 'manager_can_get_reports']




class ClientPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['client_can_put_comments', 'client_can_get_reports', 'client_can_view_logs', 'client_can_delete_comments', 'client_can_add_checklist']


