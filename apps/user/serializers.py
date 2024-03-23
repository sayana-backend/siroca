from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model, authenticate


User = get_user_model()


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class UserProfileRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "id role_type image first_name surname username password main_company job_title".split()

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    main_company = serializers.StringRelatedField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role_type', 'surname', 'first_name', 'image', 'created_at', 'job_title', 'main_company']


class AdminContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminContact
        fields = ['email', 'phone_number', 'whatsapp_number']


class ManagerPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['manager_can_edit', 'manager_can_get_reports']


class ClientPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['client_can_put_comments', 'client_can_get_reports', 'client_can_view_logs', 'client_can_delete_comments', 'client_can_add_checklist']


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

