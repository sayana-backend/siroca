from rest_framework import serializers
from .models import *


class ApplicationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForm
        fields = 'id task_number title ' \
                 'company username manager' \
                 ' application_date'.split()


class ApplicationFormDetailSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name', read_only=True)
    username = serializers.CharField(source='username.first_name', read_only=True)
    manager = serializers.CharField(source='manager.first_name', read_only=True)
    class Meta:
        model = ApplicationForm

        fields = "__all__"


class ApplicationFormFilterSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    manager = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationForm
        fields = 'id task_number title ' \
                 'company username manager' \
                 ' application_date'.split()

    def get_company(self, obj):
        return obj.company.name if obj.company else None

    def get_username(self, obj):
        return obj.username.first_name if obj.username else None

    def get_manager(self, obj):
        return obj.manager.first_name if obj.manager else None


class ApplicationLogsSerializer(serializers.ModelSerializer):
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
        fields = ('id', 'task_number', 'title', 'company', 'username',
                  'manager', 'status', 'priority', 'payment_state',
                  'application_date', 'logs')
