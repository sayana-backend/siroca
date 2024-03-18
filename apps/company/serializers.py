from rest_framework import serializers
from ..company.models import Company, JobTitle

class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = ['id', 'title']

class CompanySerializer(serializers.ModelSerializer):
    # responsible_manager = serializers.StringRelatedField()
    # users = serializers.StringRelatedField()
    # jobtitle = JobTitleSerializer(many=True)
    count_users = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()


    class Meta:
        model = Company
        fields = '__all__'

    def get_count_users(self, obj):
        return obj.get_count_users()
    
    def get_users(self, obj):
        return obj.get_users()

class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = ['id', 'title']
