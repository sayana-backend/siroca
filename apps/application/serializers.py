from rest_framework import serializers
from .models import *


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


