from rest_framework import serializers
from .models import ApplicationForm, Checklist, Comments, ApplicationLogs, Notification
from ..company.models import Company


class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    '''айди и аватарка'''

    class Meta:
        model = Comments
        fields = '__all__'


class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationLogs
        fields = ('id', 'username', 'task_number', 'text')


class ApplicationFormCreateSerializer(serializers.ModelSerializer):
    '''Для первой страницы создания заявки'''
    company = serializers.SlugRelatedField(slug_field='name', queryset=Company.objects.all())

    class Meta:
        model = ApplicationForm
        fields = ('id', 'title', 'company', 'task_number')


class ApplicationFormListSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name', read_only=True)
    main_client = serializers.CharField(source='main_client.name', read_only=True)
    main_manager = serializers.CharField(source='main_manager.name', read_only=True)

    class Meta:
        model = ApplicationForm
        fields = ('id', 'task_number', 'title', 'short_description', 'status',
                  'priority', 'company', 'main_client', 'main_manager', 'application_date',
                  'start_date', 'finish_date')




class ApplicationFormDetailSerializer(serializers.ModelSerializer):
    logs = LogsSerializer(many=True, read_only=True)
    company = serializers.CharField(source='company.name', read_only=True)
    main_client = serializers.CharField(source='main_client.name', read_only=True)
    main_manager = serializers.CharField(source='main_manager.name', read_only=True)
    checklists = ChecklistSerializer(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = ApplicationForm
        fields = '__all__'


class ApplicationFormLogsDetailSerializer(serializers.ModelSerializer):
    logs = LogsSerializer(many=True, read_only=True)
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
        fields = ('id', 'title', 'text', 'created_at', 'made_change', 'form_id', 'is_read')
