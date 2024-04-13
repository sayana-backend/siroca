from rest_framework import serializers
from .models import Company, JobTitle
from ..user.models import CustomUser



class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = ['id', 'title']


class CompanyListSerializer(serializers.ModelSerializer):
    count_users = serializers.SerializerMethodField()
    manager = serializers.SerializerMethodField()
    count_applications = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'country', 'count_users', 'count_applications', 
                  'manager', 'created_at', 'last_updated_at']

    def get_manager(self, obj):
        if obj.main_manager:
            return f"{obj.main_manager.first_name} {obj.main_manager.surname}"
        return None

    def get_count_users(self, obj):
        return obj.get_count_users()

    def get_count_applications(self, obj):
        return obj.get_count_applications()
    

class CompanyListDetailSerializer(serializers.ModelSerializer):
    count_users = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    responsible_manager = serializers.SerializerMethodField()
    managers = serializers.SerializerMethodField()
    count_applications = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'company_code', 'country', 'domain', 'responsible_manager',
                  'managers', 'count_users', 'users', 'count_applications', 'created_at', 'last_updated_at']

    def get_responsible_manager(self, obj):
        if obj.main_manager:
            return f"{obj.main_manager.first_name} {obj.main_manager.surname}"
        return None
    
    def get_managers(self, obj):
        managers = obj.managers.all()
        return [f"{manager.first_name} {manager.surname}" for manager in managers]

    def get_count_users(self, obj):
        return obj.get_count_users()
    
    def get_users(self, obj):
        return obj.get_users()

    def get_count_applications(self, obj):
        return obj.get_count_applications()
    


class CompanyCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'name', 'country', 'company_code', 'domain', 'main_manager', 'managers']

    

class CompanyRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'name', 'country', 'company_code', 'domain', 'main_manager', 'managers']
