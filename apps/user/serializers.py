from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model, authenticate


User = get_user_model()


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(read_only=True)
    main_company = serializers.CharField(read_only=True)


    class Meta:
        model = CustomUser
        fields = "role_type image first_name surname username password image main_company job_title".split()

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user



class ManagerPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id',

                  'role_type',
                  'manager_can_delete_comments',
                  'manager_can_get_reports',
                  'manager_can_view_profiles',
                  'manager_can_delete_application']




class ClientPermissionsSerializer(serializers.ModelSerializer):
    # role_type = serializers.CharField(source='role_type', read_only=True)

    # company = serializers.CharField(source='company.name', read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id',
                  'username',
                  'role_type',
                  'client_can_edit_comments',
                  'client_can_get_reports',
                  'client_can_view_logs',
                  'client_can_add_files',
                  'client_can_add_checklist',
                  'client_can_view_profiles']

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.save()
        return instance


