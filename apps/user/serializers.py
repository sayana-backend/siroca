from rest_framework import serializers
from .models import CustomUser, Contact
from apps.company.models import Company



class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "role_type image first_name surname username password main_company job_title".split()

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


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


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['email', 'phone_number', 'whatsapp_number']




class ManagerPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['manager_can_edit', 'manager_can_get_reports']




class ClientPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['client_can_put_comments', 'client_can_get_reports', 'client_can_view_logs', 'client_can_delete_comments', 'client_can_add_checklist']