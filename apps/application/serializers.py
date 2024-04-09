from rest_framework import serializers
from .models import ApplicationForm, Checklist, Comments, ApplicationLogs, Notification
from django.core.serializers.json import DjangoJSONEncoder
import json


class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Comments
        fields = '__all__'

    



class ApplicationFormCreateSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name', read_only=True)
    main_client = serializers.CharField(source='main_client.name', read_only=True)
    main_manager = serializers.CharField(source='main_manager.name', read_only=True)
    checklist = ChecklistSerializer(many=True)
    comments = CommentsSerializer(many=True)
    class Meta:
        model = ApplicationForm
        fields = ['id', 'title', 'company', 'priority', 'status', 'jira',  'main_manager', 'main_client',
                  'start_date', 'deadline_date', 'offer_date', 'finish_date', 'application_date', 'confirm_date',
                  'payment_state', 'description', 'files', 'short_description']



class ApplicationLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationLogs
        fields = ('id', 'task_number', 'text')


class ApplicationFormCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForm
        fields = ('title', 'company')

    '''Для создания заявки '''


class ApplicationFormDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForm
        fields = '__all__'


class ApplicationFormListSerializer(serializers.ModelSerializer):
    checklist = ChecklistSerializer(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)
    company = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationForm
        fields = ('task_number', 'title', 'description', 'short_description', 'files', 'jira', 'status',
                  'payment_state', 'priority', 'company', 'main_client', 'main_manager', 'application_date',
                  'confirm_date', 'offer_date', 'start_date', 'finish_date', 'deadline_date', 'checklist', 'comments')

    def get_company(self, obj):
        return obj.company.name if obj.company else None


class ApplicationFormLogsDetailSerializer(serializers.ModelSerializer):
    logs = ApplicationLogsSerializer(many=True, read_only=True)
    company = serializers.CharField(source='company.name', read_only=True)
    main_client = serializers.CharField(source='main_client.name', read_only=True)
    main_manager = serializers.CharField(source='main_manager.name', read_only=True)
    checklist = ChecklistSerializer(many=True)
    comments = CommentsSerializer(many=True)

    class Meta:
        model = ApplicationForm
        fields = ('id', 'task_number', 'title', 'company', 'main_client', 'main_manager',
                  'status', 'priority', 'comments', 'checklist', 'payment_state',
                  'application_date', 'logs')


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('task_number', 'title', 'text', 'created_at', 'made_change', 'form_id', 'is_read')
