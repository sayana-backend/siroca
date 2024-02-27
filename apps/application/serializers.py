
from rest_framework import serializers
from .models import *


class ApplicationFormSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name', read_only=True)
    username = serializers.CharField(source='username.first_name', read_only=True)
    manager = serializers.CharField(source='manager.first_name', read_only=True)
    class Meta:
        model = ApplicationForm
        # fields = 'id task_number title ' \
        #          'company username manager status priority payment_state' \
        #          ' application_date'.split()
        fields = "__all__"
        # read_only_fields = ("id","task_number", "title", "company", "username", "manager", "application_date")

# class ApplicationFormDetailSerializer(serializers.ModelSerializer):
#     company = serializers.CharField(source='company.name', read_only=True)
#     username = serializers.CharField(source='username.first_name', read_only=True)
#     manager = serializers.CharField(source='manager.first_name', read_only=True)
#     class Meta:
#         model = ApplicationForm
#         fields = "__all__"




class ApplicationLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationLogs
        fields = '__all__'
        depth = 1

class ApplicationLogsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationLogs
        fields = '__all__'




