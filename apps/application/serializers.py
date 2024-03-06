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


class ApplicationFormDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationForm
        fields = '__all__'


class ApplicationLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationLogs
        fields = ('id', 'task_number', 'text')






