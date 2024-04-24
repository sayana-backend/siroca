from rest_framework import serializers
from .models import ApplicationForm, Checklist, Comments, ApplicationLogs, Notification
from ..company.models import Company
from ..user.models import CustomUser


class ChecklistSerializer(serializers.ModelSerializer):
    manager = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())
    class Meta:
        model = Checklist
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_image = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = '__all__'

    def get_user_image(self, obj):
        user = obj.user
        if hasattr(user, 'image')and user.image:
            return user.image.url
        return None  


class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationLogs
        fields = ('id', 'username', 'task_number', 'text', 'created_at')


class ApplicationFormCreateSerializer(serializers.ModelSerializer):
    '''Для страницы создания заявки'''
    company = serializers.SlugRelatedField(slug_field='name', queryset=Company.objects.all())
    checklist = ChecklistSerializer(many=True)
    comments = CommentsSerializer(many=True)

    class Meta:
        model = ApplicationForm
        fields = ('id', 'title', 'company', 'task_number')


class ApplicationFormListSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name', read_only=True)
    main_client = serializers.SlugRelatedField(slug_field='username', read_only=True)
    main_manager = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = ApplicationForm
        fields = ('id', 'task_number', 'title', 'short_description', 'status',
                  'priority', 'company', 'main_client', 'main_manager', 'application_date',
                  'start_date', 'finish_date')


class ApplicationLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationLogs
        fields = ('id', 'task_number', 'text', 'username')


class ApplicationFormDetailSerializer(serializers.ModelSerializer):
    logs = LogsSerializer(many=True, read_only=True)
    company = serializers.CharField(source='company.name', read_only=True)
    main_client = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())
    main_manager = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())
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
        fields = ('id', 'task_number', 'title', 'text', 'created_at', 'made_change',
                  'form_id', 'is_read', 'is_manager_notic', 'is_client_notic', 'admin_id')
