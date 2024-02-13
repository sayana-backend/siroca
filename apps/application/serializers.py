from rest_framework import serializers
from .models import *


class ApplicationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForm
        fields = "__all__"
        read_only_fields = ("id","task_number", "title", "company", "username", "manager", "application_date")


