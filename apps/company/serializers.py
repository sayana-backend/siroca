from rest_framework import serializers
from .models import Company, JobTitle
from ..user.models import CustomUser


class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = ['id', 'title']


class CompanyListSerializer(serializers.ModelSerializer):
    main_manager = serializers.CharField(source='main_manager_username', read_only=True)
    count_users = serializers.SerializerMethodField()
    count_applications = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'country', 'count_users', 'count_applications', 
                  'main_manager', 'created_at', 'last_updated_at']

    def get_count_users(self, obj):
        return obj.get_count_users()

    def get_count_applications(self, obj):
        return obj.get_count_applications()
    

class CompanyDetailSerializer(serializers.ModelSerializer):
    count_users = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    count_applications = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'company_code', 'country', 'domain', 'main_manager',
                  'managers', 'count_users', 'users', 'count_applications', 'created_at', 'last_updated_at']

    def get_count_users(self, obj):
        return obj.get_count_users()
    
    def get_users(self, obj):
        return obj.get_users()

    def get_count_applications(self, obj):
        return obj.get_count_applications()


class CompanyCreateSerializer(serializers.ModelSerializer):  # не правильно но сначала нужна оптимизация
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
