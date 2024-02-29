
from rest_framework import serializers
from .models import *
from ..user.models import CustomUser, UserProfile


class ApplicationFormDetailSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name', read_only=True)
    username = serializers.CharField(source='username.first_name', read_only=True)
    manager = serializers.CharField(source='manager.first_name', read_only=True)
    class Meta:
        model = ApplicationForm
        fields = "__all__"


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ('id', 'first_name', 'last_name')


class ApplicationLogsSerializer(serializers.ModelSerializer):
    # user = UserProfileSerializer(many=False, read_only=True)
    class Meta:
        model = ApplicationLogs
        fields = ('id', 'task_number', 'text')




class ApplicationFormLogsDetailSerializer(serializers.ModelSerializer):
    logs = ApplicationLogsSerializer(many=True, read_only=True)
    company = serializers.CharField(source='company.name', read_only=True)
    username = serializers.CharField(source='username.first_name', read_only=True)
    manager = serializers.CharField(source='manager.first_name', read_only=True)

    class Meta:
        model = ApplicationForm
        fields = ('id', 'task_number', 'title', 'company', 'username', 'manager', 'status', 'priority', 'payment_state', 'application_date', 'logs')







