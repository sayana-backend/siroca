
from rest_framework import serializers
from .models import *
from apps.application.models import Checklist

class ApplicationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForm
        fields = 'id task_number title ' \
                 'company username manager' \
                 ' application_date'.split()
        # read_only_fields = ("id","task_number", "title", "company", "username", "manager", "application_date")

class ApplicationFormDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForm
        fields = "__all__"

class ChecklistSerializers(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = "__all__"


