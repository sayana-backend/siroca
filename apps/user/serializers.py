from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from ..company.models import Company, JobTitle

User = get_user_model()


class UserAuthSerializer(serializers.ModelSerializer):
    '''Log in'''
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class UserProfileRegisterSerializer(serializers.ModelSerializer):
    '''Create user'''
    main_company = serializers.SlugRelatedField(slug_field='name', queryset=Company.objects.all())
    job_title = serializers.SlugRelatedField(slug_field='title', queryset=JobTitle.objects.all())

    class Meta:
        model = CustomUser
        fields = "id role_type image first_name surname username password main_company job_title".split()


class UserProfileSerializer(serializers.ModelSerializer):
    '''User only view'''
    main_company = serializers.CharField(source='main_company.name', read_only=True)
    job_title = serializers.CharField(source='job_title.title', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role_type',  'surname',
                  'first_name', 'image', 'created_at', 'job_title', 'main_company']


class UserUpdateSerializer(serializers.ModelSerializer):
    '''Update user'''
    main_company = serializers.SlugRelatedField(slug_field='name', queryset=Company.objects.all())
    job_title = serializers.SlugRelatedField(slug_field='title', queryset=JobTitle.objects.all())

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role_type',  'surname', 'first_name', 'image', 'created_at', 'job_title', 'main_company']


class UserDeleteSerializer(serializers.ModelSerializer):
    '''Delete user'''
    class Meta:
        model = CustomUser
        fields = ['id', 'username']


'''Serializers for admin contact and password change and reset'''


class AdminContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminContact
        fields = ['email', 'phone_number', 'whatsapp_number']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        new_password1 = data.get('new_password1')
        new_password2 = data.get('new_password2')

        if new_password1 != new_password2:
            raise serializers.ValidationError("Новые пароли не совпадают")
        return data


class AdminResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)


'''Permission serializer'''


class ManagerPermissionsGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id',
                  'username',
                  'role_type',
                  'manager_can_delete_comments',
                  'manager_can_get_reports',
                  'manager_can_delete_application']


class ManagerPermissionsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id',
                  'username',
                  'role_type',
                  'manager_can_delete_comments_extra',
                  'manager_can_get_reports_extra',
                  'manager_can_delete_application_extra',
                  'manager_can_create_and_edit_company_extra',
                  'manager_can_create_and_edit_user_extra',
                  'manager_can_create_and_delete_job_title_extra']

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        return instance


class ClientPermissionsGeneralSerializer(serializers.ModelSerializer):
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
                  'client_can_add_checklist']

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        return instance


class ClientPermissionsDetailSerializer(serializers.ModelSerializer):
    # role_type = serializers.CharField(source='role_type', read_only=True)

    # company = serializers.CharField(source='company.name', read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id',
                  'username',
                  'role_type',
                  'client_can_edit_comments_extra',
                  'client_can_get_reports_extra',
                  'client_can_view_logs_extra',
                  'client_can_add_files_extra',
                  'client_can_add_checklist_extra',
                  'client_can_create_application_extra',
                  'client_can_edit_application_extra']

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        return instance






