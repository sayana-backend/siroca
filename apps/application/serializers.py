from rest_framework import serializers
from .models import ApplicationForm, Checklist, Comments, ApplicationLogs, Notification


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


class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationLogs
        fields = ('id', 'task_number', 'text')


class ApplicationSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name', read_only=True)
    main_client = serializers.CharField(source='main_client.name', read_only=True)
    main_manager = serializers.CharField(source='main_manager.name', read_only=True)
    checklists = ChecklistSerializer(many=True, required=False)
    comments = CommentsSerializer(many=True)
    logs = LogsSerializer(many=True)

    class Meta:
        model = ApplicationForm
        fields = '__all__'

    def create(self, validated_data):
        checklists_data = validated_data.pop('checklists', [])
        application_form = ApplicationForm.objects.create(**validated_data)
        for checklist_data in checklists_data:
            Checklist.objects.create(application=application_form, **checklist_data)
        return application_form



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'task_number', 'text', 'created_at')



# class ApplicationFormLogsDetailSerializer(serializers.ModelSerializer):
    #     logs = ApplicationLogsSerializer(many=True, read_only=True)
    #     company = serializers.CharField(source='company.name', read_only=True)
    #     main_client = serializers.CharField(source='main_client.name', read_only=True)
    #     main_manager = serializers.CharField(source='main_manager.name', read_only=True)
    #     checklist = ChecklistSerializer(many=True)
    #     comments = CommentsSerializer(many=True)

    # class Meta:
    #     model = ApplicationForm
    #     fields = ('id', 'task_number', 'title', 'company', 'main_client', 'main_manager',
    #               'status', 'priority', 'comments', 'checklist', 'payment_state',
    #               'application_date', 'logs')

