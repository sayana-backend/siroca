from rest_framework import serializers
from .models import CustomUser,AdminContact
from apps.company.models import Company



class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['surname', ]


class UserProfileRegisterSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'role_type', 'surname', 'first_name', 'image', 'created_at', 'job_title', 'company_relation']

    # def get_username(self, obj):
    #     return f"{obj.username}@{obj.company_relation.domain}.com" if obj.company_relation else obj.username

    # def create(self, validated_data):
    #     company_id = self.context['request'].data.get('company_id')
    #     if not company_id:
    #         raise serializers.ValidationError("Не указан идентификатор компании")
    #     company = Company.objects.get(pk=company_id)
    #     validated_data['company_relation'] = company
        
    #     # Создание пользователя без company_domain в username
    #     user = CustomUser.objects.create(**validated_data)

    #     # Обновление username с company_domain после сохранения пользователя
    #     if company:
    #         company_domain = company.domain
    #         user.username = f"{user.username}@{company_domain}.com"
    #         user.save()

    #     return user


class AdminContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminContact
        fields = ['email', 'phone_number', 'whatsapp_number']



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        new_password1 = data.get('new_password1')
        new_password2 = data.get('new_password2')

        if new_password1 != new_password2:
            raise serializers.ValidationError("Новые пароли не совпадают")

        return data