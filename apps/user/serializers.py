from rest_framework import serializers
from .models import CustomUser


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', ]


class UserProfileRegisterSerializer(serializers.ModelSerializer):
    # manager = serializers.SerializerMethodField()
    # manager = ManagerSerializer(many =True)
    class Meta:
        model = CustomUser
        fields = "username role_type surname name password image created_at job_title company".split()

    # def get_manager(self, obj):
    #     if obj.manager:
    #         return obj.manager.name if obj.manager else None
    #     return None

    # def create(self, validated_data):
    #     user = CustomUser.objects.create_user(**validated_data)
    #     return user


class AllUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "all"