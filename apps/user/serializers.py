from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import (UserProfile, ManagerProfile,
                     AdminProfile, AdminProfileManager)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username_validator first_name last_name '
                  'username password job_title company groups user_permissions').split()


class UserProfileValidateSerializers(serializers.Serializer):
    username_validate = serializers.CharField()
    first_name = serializers.CharField(max_length=150, min_length=1, required=True)
    last_name = serializers.CharField(max_length=150, min_length=1, required=True)
    username = serializers.CharField(max_length=150, min_length=1, required=True)
    password = serializers.CharField(max_length=150, min_length=8, required=True)
    job_title_id = serializers.CharField(max_length=150, min_length=1)
    company_id = serializers.CharField(max_length=150, min_length=1, required=True)
    groups_id = serializers.CharField(max_length=150, min_length=1, required=True)
    user_permissions_id = serializers.CharField()

    def validate_job_title_id(self, job_title_id):
        try:
            UserProfile.objects.get(id=job_title_id)
        except UserProfile.DoesNotExist:
            raise ValidationError('Job title not found')
        return job_title_id

    def validate_company_id(self, company_id):
        try:
            UserProfile.objects.get(id=company_id)
        except UserProfile.DoesNotExist:
            raise ValidationError('Company not found')
        return company_id

    def validate_group_id(self, group_id):
        try:
            UserProfile.objects.get(id=group_id)
        except UserProfile.DoesNotExist:
            raise ValidationError('Group not found')
        return group_id

    def validate_user_permission(self, user_permission_id):
        try:
            UserProfile.objects.get(id=user_permission_id)
        except UserProfile.DoesNotExist:
            raise ValidationError('User permission not found')
        return user_permission_id


class ManagerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerProfile
        fields = 'username_validator first_name last_name username password groups user_permissions'.split()


class ManagerProfileValidateSerializers(serializers.Serializer):
    username_validate = serializers.CharField()
    first_name = serializers.CharField(max_length=150, min_length=1, required=True)
    last_name = serializers.CharField(max_length=150, min_length=1, required=True)
    username = serializers.CharField(max_length=150, min_length=1, required=True)
    password = serializers.CharField(max_length=150, min_length=8, required=True)
    job_title_id = serializers.CharField(max_length=150, min_length=1)
    company_id = serializers.CharField(max_length=150, min_length=1, required=True)
    groups_id = serializers.CharField(max_length=150, min_length=1, required=True)
    user_permissions_id = serializers.CharField()

    def validate_job_title_id(self, job_title_id):
        try:
            UserProfile.objects.get(id=job_title_id)
        except UserProfile.DoesNotExist:
            raise ValidationError('Job title not found')
        return job_title_id

    def validate_company_id(self, company_id):
        try:
            UserProfile.objects.get(id=company_id)
        except UserProfile.DoesNotExist:
            raise ValidationError('Company not found')
        return company_id

    def validate_group_id(self, group_id):
        try:
            UserProfile.objects.get(id=group_id)
        except UserProfile.DoesNotExist:
            raise ValidationError('Group not found')
        return group_id

    def validate_user_permission(self, user_permission_id):
        try:
            UserProfile.objects.get(id=user_permission_id)
        except UserProfile.DoesNotExist:
            raise ValidationError('User permission not found')
        return user_permission_id


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = 'username_validator first_name last_name username password groups user_permissions'.split()


class AdminProfileValidateSerializer(serializers.Serializer):
    username_validate = serializers.CharField()
    first_name = serializers.CharField(max_length=150, min_length=1, required=True)
    last_name = serializers.CharField(max_length=150, min_length=1, required=True)
    username = serializers.CharField(max_length=150, min_length=1, required=True)
    password = serializers.CharField(max_length=150, min_length=8, required=True)
    job_title_id = serializers.CharField(max_length=150, min_length=1)
    company_id = serializers.CharField(max_length=150, min_length=1, required=True)
    groups_id = serializers.CharField(max_length=150, min_length=1, required=True)
    user_permissions_id = serializers.CharField()


def validate_job_title_id(self, job_title_id):
    try:
        UserProfile.objects.get(id=job_title_id)
    except UserProfile.DoesNotExist:
        raise ValidationError('Job title not found')
    return job_title_id


def validate_company_id(self, company_id):
    try:
        UserProfile.objects.get(id=company_id)
    except UserProfile.DoesNotExist:
        raise ValidationError('Company not found')
    return company_id


def validate_group_id(self, group_id):
    try:
        UserProfile.objects.get(id=group_id)
    except UserProfile.DoesNotExist:
        raise ValidationError('Group not found')
    return group_id


def validate_user_permission(self, user_permission_id):
    try:
        UserProfile.objects.get(id=user_permission_id)
    except UserProfile.DoesNotExist:
        raise ValidationError('User permission not found')
    return user_permission_id
