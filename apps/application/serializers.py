from .models import *
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import datetime


class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        # model = Users
        fields = 'name surname login password user_role company position_company create_at'.split()


class ApplicationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationForm
        fields = "__all__"
        read_only_fields = ("id","task_number", "title", "company", "username", "manager", "application_date")


