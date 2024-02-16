from .models import *
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import datetime


class ApplicationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForm
        fields = "__all__"
        read_only_fields = ("id","task_number", "title", "company", "username", "manager", "application_date")


