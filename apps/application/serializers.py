from .models import ApplicationForm, Checklist, Comments, ApplicationLogs, Notification, SubTask, ApplicationFile
from rest_framework import serializers
from ..company.models import Company
from ..user.models import CustomUser


class SubTaskSerializer(serializers.ModelSerializer):
    manager = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all(), required=False)

    class Meta:
        model = SubTask
        fields = '__all__'


class ChecklistSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Checklist
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_image = serializers.ImageField(source='user.image', read_only=True)
    formatted_date_added = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = '__all__'

    def get_formatted_date_added(self, instance):
        return instance.date_added.strftime('%Y.%m.%d / %H:%M')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationFile
        fields = '__all__'


class LogsSerializer(serializers.ModelSerializer):
    formatted_created_at = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationLogs
        fields = ('id', 'user', 'formatted_created_at', 'field', 'initially', 'new', 'user_id')

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
    company = serializers.CharField(source='company.name', read_only=True)
    main_client = serializers.SlugRelatedField(slug_field='username', read_only=True)
    main_manager = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = ApplicationForm
        fields = ('id', 'task_number', 'title', 'short_description', 'status',
                  'priority', 'company', 'main_client', 'main_manager', 'application_date',
                  'start_date', 'finish_date')


class ApplicationFormUpdateSerializer(serializers.ModelSerializer):
    '''Application ypdate'''
    company = serializers.CharField(source='company.name', read_only=True)
    main_client = serializers.SlugRelatedField(slug_field='username', source='get_full_name', queryset=CustomUser.objects.all(), required=False)
    main_manager = serializers.SlugRelatedField(slug_field='username', source='get_full_name', queryset=CustomUser.objects.all(), required=False)
    checklists = ChecklistSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = ApplicationForm
        fields = '__all__'


class ApplicationFormDetailViewSerializer(serializers.ModelSerializer):
    '''Application detail view'''
    logs = LogsSerializer(many=True, read_only=True)
    company = serializers.CharField(source='company.name', read_only=True)
    main_client = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())
    main_manager = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())
    checklists = ChecklistSerializer(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = ApplicationForm
        fields = '__all__'


class ApplicationsOnlyDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForm
        fields = ['description']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'task_number', 'title', 'text', 'created_at', 'made_change',
                  'form_id', 'is_read', 'is_manager_notic', 'is_client_notic', 'admin_id')
