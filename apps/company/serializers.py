from rest_framework import serializers
from apps.company.models import Company, JobTitle

class CompanySerializer(serializers.ModelSerializer):
    responsible_manager = serializers.StringRelatedField()
    users = serializers.StringRelatedField(many=True)

    class Meta:
        model = Company
        fields = '__all__'

class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = ['id', 'title']