from rest_framework import serializers
from .models import ApplicationForm, Checklist, Comments, ApplicationLogs


class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class ApplicationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForm
        fields = 'id task_number title ' \
                 'company username manager' \
                 ' application_date'.split()


class ApplicationFormDetailSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name', read_only=True)
    main_client = serializers.CharField(source='main_client.name', read_only=True)
    main_manager = serializers.CharField(source='main_manager.name', read_only=True)
    checklist = ChecklistSerializer(many=True)
    comments = CommentsSerializer(many=True)

    class Meta:
        model = ApplicationForm

        fields = 'id task_number title checklist comments ' \
                 'company main_client main_manager' \
                 ' application_date'.split()


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
        return obj.main_client.username if obj.main_client else None

    def get_manager(self, obj):
        return obj.main_manager.username if obj.main_manager else None


class ApplicationLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationLogs
        fields = ('id', 'task_number', 'text')


class ApplicationFormLogsDetailSerializer(serializers.ModelSerializer):
    logs = ApplicationLogsSerializer(many=True, read_only=True)
    company = serializers.CharField(source='company.name', read_only=True)
    main_client = serializers.CharField(source='main_client.name', read_only=True)
    main_manager = serializers.CharField(source='main_manager.name', read_only=True)
    checklist = ChecklistSerializer(many=True)
    comments = CommentsSerializer(many=True)

    class Meta:
        model = ApplicationForm
        fields = ('id', 'task_number', 'title', 'company','main_client', 'main_manager',
                  'status','priority', 'comments', 'checklist', 'payment_state',
                  'application_date', 'logs')
