
from rest_framework import serializers
from .models import ApplicationForm, Checklist, Comments


class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class ApplicationFormSerializer(serializers.ModelSerializer):
    checklist = ChecklistSerializer(many=True)
    comments = CommentsSerializer(many=True)

    class Meta:
        model = ApplicationForm
        fields = 'id task_number title checklist comments ' \
                 'company main_client main_manager' \
                 ' application_date'.split() \



class ApplicationFormDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForm
        fields = "__all__"
        





















