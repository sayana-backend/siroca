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

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ApplicationLogsSerializer(serializers.ModelSerializer):
    # user = UserProfileSerializer(many=False, read_only=True)
    class Meta:
        model = ApplicationLogs
        fields = ('id', 'task_number', 'text')


class ApplicationFormDetailSerializer(serializers.ModelSerializer):
    # company = serializers.CharField(source='company.name', read_only=True)
    # main_client = serializers.CharField(source='main_client.name', read_only=True)
    # main_manager = serializers.CharField(source='main_manager.name', read_only=True)
    # checklist = ChecklistSerializer(many=True)
    # comments = CommentsSerializer(many=True)
    # logs = ApplicationLogsSerializer(many=True)

    class Meta:
        model = ApplicationForm
        fields = '__all__'




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
