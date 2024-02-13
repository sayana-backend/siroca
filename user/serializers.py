from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Users
from datetime import datetime


# серизализатор User
class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = 'name surname login password user_role company position_company create_at'.split()


# загатовка пользователя
class UsersValidateSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=30, min_length=2, required=True)
    surname = serializers.CharField(max_length=30, min_length=2, required=True)
    login = serializers.CharField(max_length=30, min_length=2, required=True)
    password = serializers.CharField(max_length=50, min_length=8, required=True)
    user_role = serializers.CharField(required=True)
    position_company_id = serializers.CharField(max_length=30, min_length=5, required=False)
    created_at = serializers.DateTimeField(read_only=True)

    # проверка должность компании
    def validate_position_company_id(self, position_company_id,):
        try:
            Users.objects.get(id=position_company_id,)
        except Users.DoesNotExist:
            raise ValidationError('position company not found')

