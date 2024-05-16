from rest_framework import serializers
from .models import Company, JobTitle
from ..user.models import CustomUser


class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = ['id', 'title']


class CompanyListSerializer(serializers.ModelSerializer):
    count_users = serializers.IntegerField()
    count_applications = serializers.IntegerField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'country', 'count_users', 'count_applications',
                  'main_manager', 'created_at', 'last_updated_at']
    

class CompanyDetailSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    count_users = serializers.IntegerField()
    count_applications = serializers.IntegerField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'company_code', 'country', 'domain', 'main_manager',
                  'managers', 'count_users', 'users', 'count_applications', 'created_at', 'last_updated_at']

    def get_users(self, obj):
        return obj.get_users()


class CompanyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'country', 'company_code', 'domain', 'main_manager', 'managers']


class CompanyRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'country', 'company_code', 'domain', 'main_manager', 'managers']


class CompanyOnlyNameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']
