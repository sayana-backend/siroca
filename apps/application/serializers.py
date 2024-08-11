from .models import (ApplicationForm, Checklist, Comments, ApplicationLogs,
                     Notification, SubTask, ApplicationFile)
from rest_framework import serializers
from ..company.models import Company
from ..user.models import CustomUser
from django.utils import timezone


class SubTaskSerializer(serializers.ModelSerializer):
    manager = serializers.SlugRelatedField(slug_field='full_name',
                                           queryset=CustomUser.objects.filter(role_type='manager'),
                                           required=False)

    class Meta:
        model = SubTask
        fields = '__all__'


class ChecklistSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Checklist
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.full_name', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_image = serializers.ImageField(source='user.image', read_only=True)
    formatted_date_added = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = '__all__'

    def get_formatted_date_added(self, instance):
        return instance.date_added.strftime('%Y.%m.%d / %H:%M')


class FileSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField()

    def get_file_name(self, obj):
        return obj.file.name

    class Meta:
        model = ApplicationFile
        fields = ('id', 'file', 'application', 'file_name')


class LogsSerializer(serializers.ModelSerializer):
    formatted_created_at = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationLogs
        fields = ('id', 'user', 'formatted_created_at', 'field', 'initially',
                  'new', 'user_id', 'file_logs', 'user_image')

    def get_formatted_created_at(self, instance):
        return instance.created_at.strftime('%Y.%m.%d / %H:%M')


class ApplicationFormCreateSerializer(serializers.ModelSerializer):
    '''Application create'''
    company = serializers.SlugRelatedField(slug_field='name', queryset=Company.objects.all())

    class Meta:
        model = ApplicationForm
        fields = ('id', 'title', 'company', 'task_number')


class ApplicationFormListSerializer(serializers.ModelSerializer):
    '''Application list'''
    company = serializers.SlugRelatedField(slug_field='name', read_only=True)
    main_client = serializers.SlugRelatedField(slug_field='full_name', read_only=True)
    main_manager = serializers.SlugRelatedField(slug_field='full_name', read_only=True)

    class Meta:
        model = ApplicationForm
        fields = ('id', 'task_number', 'title', 'short_description', 'status',
                  'priority', 'company', 'main_client', 'main_manager', 'application_date',
                  'start_date', 'finish_date')


class ApplicationFormUpdateSerializer(serializers.ModelSerializer):
    '''Application update'''
    company = serializers.SlugRelatedField(slug_field='name', read_only=True, required=False)
    main_client = serializers.SlugRelatedField(slug_field='full_name',
                                               queryset=CustomUser.objects.filter(role_type='client'),
                                               required=False)
    main_manager = serializers.SlugRelatedField(slug_field='full_name',
                                                queryset=CustomUser.objects.filter(role_type='manager'),
                                                required=False)
    checklists = ChecklistSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = ApplicationForm
        fields = '__all__'


class ApplicationFormDetailViewSerializer(serializers.ModelSerializer):
    '''Application detail view'''
    logs = LogsSerializer(many=True, read_only=True)
    company = serializers.SlugRelatedField(slug_field='name', read_only=True)
    main_client = serializers.SlugRelatedField(slug_field='full_name', read_only=True)
    main_manager = serializers.SlugRelatedField(slug_field='full_name', read_only=True)
    checklists = ChecklistSerializer(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = ApplicationForm
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['logs'] = LogsSerializer(instance.logs.order_by('-created_at'), many=True).data
        return data


class ApplicationsOnlyDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForm
        fields = ['description']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'task_number', 'title', 'made_change', 'text', 'created_at', 'form_id')