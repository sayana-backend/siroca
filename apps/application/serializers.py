from rest_framework import serializers
from .models import ApplicationForm, Checklist, Comments, ApplicationLogs, Notification


class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Comments
        fields = '__all__'


class LogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationLogs
        fields = ('id', 'username', 'task_number', 'text')


class ApplicationFormCreateSerializer(serializers.ModelSerializer):
    '''Для первой страницы создания заявки'''
    company = serializers.StringRelatedField()
    class Meta:
        model = ApplicationForm
        fields = ('id', 'title', 'company')


class ApplicationFormListSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.name', read_only=True)
    main_client = serializers.CharField(source='main_client.name', read_only=True)
    main_manager = serializers.CharField(source='main_manager.name', read_only=True)
    class Meta:
        model = ApplicationForm
        fields = ('id', 'task_number', 'title', 'short_description', 'status',
                  'priority', 'company', 'main_client', 'main_manager', 'application_date',
                  'start_date', 'finish_date')


# class ApplicationSerializer(serializers.ModelSerializer):
#     company = serializers.CharField(source='company.name', read_only=True)
#     main_client = serializers.CharField(source='main_client.name', read_only=True)
#     main_manager = serializers.CharField(source='main_manager.name', read_only=True)
#     checklists = ChecklistSerializer(many=True, required=False)
#     comments = CommentsSerializer(many=True, read_only=True)
#     logs = LogsSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = ApplicationForm
#         fields = '__all__'
#
#     def update(self, instance, validated_data):
#         # Ваш текущий код
#         instance.save()
#
#         # Обновление вложенных полей checklists
#         checklists_data = validated_data.pop('checklists', [])  # Убираем checklists из validated_data
#         for checklist_data in checklists_data:
#             checklist_id = checklist_data.get('id', None)
#             if checklist_id:
#                 checklist = Checklist.objects.get(id=checklist_id)
#                 ChecklistSerializer().update(checklist, checklist_data)
#             else:
#                 checklist_data['application'] = instance  # Указываем application для нового объекта
#                 Checklist.objects.create(**checklist_data)
#
#         # Обновление вложенных полей comments
#         comments_data = validated_data.pop('comments', [])  # Убираем comments из validated_data
#         for comment_data in comments_data:
#             comment_id = comment_data.get('id', None)
#             if comment_id:
#                 comment = Comments.objects.get(id=comment_id)
#                 CommentsSerializer().update(comment, comment_data)
#             else:
#                 comment_data['application'] = instance  # Указываем application для нового объекта
#                 comment_data['user'] = self.context['request'].user
#                 Comments.objects.create(**comment_data)
#
#         return instance


# class ApplicationFormDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ApplicationForm
#         fields = '__all__'
#
#     def create(self, validated_data):
#         checklists_data = validated_data.pop('checklists', [])
#         application_form = ApplicationForm.objects.create(**validated_data)
#         for checklist_data in checklists_data:
#             Checklist.objects.create(application=application_form, **checklist_data)
#         return application_form


class ApplicationFormDetailSerializer(serializers.ModelSerializer):
    logs = LogsSerializer(many=True, read_only=True)
    company = serializers.CharField(source='company.name', read_only=True)
    main_client = serializers.CharField(source='main_client.name', read_only=True)
    main_manager = serializers.CharField(source='main_manager.name', read_only=True)

    class Meta:
        model = ApplicationForm
        fields = '__all__'






class ApplicationFormLogsDetailSerializer(serializers.ModelSerializer):
    logs = LogsSerializer(many=True, read_only=True)
    company = serializers.CharField(source='company.name', read_only=True)
    main_client = serializers.CharField(source='main_client.name', read_only=True)
    main_manager = serializers.CharField(source='main_manager.name', read_only=True)
    checklist = ChecklistSerializer(many=True)
    comments = CommentsSerializer(many=True)

    class Meta:
        model = ApplicationForm
        fields = ('id', 'task_number', 'title', 'company', 'main_client', 'main_manager',
                  'status', 'priority', 'comments', 'checklist', 'payment_state',
                  'application_date', 'logs')



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('task_number', 'title', 'text', 'created_at', 'made_change', 'form_id', 'is_read')


