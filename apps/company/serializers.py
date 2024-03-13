from rest_framework import serializers
from ..company.models import Company, JobTitle

class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitle
        fields = ['id', 'title']

class CompanySerializer(serializers.ModelSerializer):
    responsible_manager = serializers.StringRelatedField()
    users = serializers.StringRelatedField()
    jobtitle = JobTitleSerializer(many=True)

    class Meta:
        model = Company
        fields = '__all__'

