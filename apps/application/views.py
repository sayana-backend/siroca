from apps.application.signals import BaseLoggingCreateDestroy, BaseLoggingUpdate
from django.db.models import Count, Q, Case, When, Value, CharField
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ApplicationFormFilter, CustomPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import Coalesce
from rest_framework.response import Response
from rest_framework import generics, filters
from django.db.models import Prefetch
from django.core.cache import cache
from django.db import transaction
from apps.user.permissions import *
from rest_framework import status
from .serializers import *
from .models import *


class ApplicationFormCreateAPIView(generics.CreateAPIView):
    '''Create new application'''
    queryset = ApplicationForm.objects.all().select_related('main_client', 'main_manager', 'company')
    serializer_class = ApplicationFormCreateSerializer
    permission_classes = [IsClientCanCreateApplicationOrIsAdminAndManagerUser]

    @transaction.atomic
    def perform_create(self, serializer):
        '''Tracking the creation of an application for notifications'''
        instance = serializer.save()

        admin_notification = CustomUser.objects.filter(is_superuser=True)
        user = self.request.user

        notifications = [
            Notification(
                task_number=instance.task_number,
                text='Создана новая заявка', title=instance.title,
                made_change=f"{user.full_name} создал(а) заявку", is_admin=True, admin_id=admin.id
            )
            for admin in admin_notification
        ]

        Notification.objects.bulk_create(notifications)


class ApplicationFormListAPIView(generics.ListAPIView):
    serializer_class = ApplicationFormListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
    filterset_class = ApplicationFormFilter
    pagination_class = CustomPagination
    search_fields = ['task_number', 'title', 'company__name', 'short_description',
                     'main_client__full_name', 'main_manager__full_name',
                     'start_date', 'finish_date', 'priority', 'payment_state', 'comments__text']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            queryset = ApplicationForm.objects.all()
        elif user.is_client:
            queryset = ApplicationForm.objects.filter(Q(main_client=user) |
                                                      Q(company=user.main_company))
        elif user.is_manager:
            queryset = ApplicationForm.objects.filter(Q(main_manager=user) |
                                                      Q(checklists__subtasks__manager=user)|
                                                      Q(company=user.main_company)).distinct()

        queryset = queryset.select_related('main_client', 'main_manager', 'company').annotate(
            priority_order=Case(
                When(priority='Самый высокий', then=Value(1)),
                When(priority='Высокий', then=Value(2)),
                When(priority='Средний', then=Value(3)),
                When(priority='Низкий', then=Value(4)),
                When(priority='Самый низкий', then=Value(5)),
                default=Value(6),
                output_field=CharField(),
            )
        ).order_by('priority_order', '-application_date')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count_queryset = queryset.annotate(
            status_count=Count('id', distinct=True)
        )
        created_count = count_queryset.aggregate(created_count=Count('id'))
        in_progress_count = count_queryset.filter(status='В работе').aggregate(in_progress_count=Coalesce(Count('id', distinct=True), 0))
        closed_count = count_queryset.filter(status='Проверено').aggregate(closed_count=Coalesce(Count('id', distinct=True), 0))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = {
                'created_count': created_count['created_count'],
                'in_progress_count': in_progress_count['in_progress_count'],
                'closed_count': closed_count['closed_count'],
                'results': serializer.data
            }

            return self.get_paginated_response(data)
        return Response({'detail': 'Not found'}, status=404)


class ApplicationFormRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    '''  update API '''
    queryset = ApplicationForm.objects.all().select_related('main_client', 'main_manager', 'company')
    serializer_class = ApplicationFormUpdateSerializer
    lookup_field = 'id'
    permission_classes = [IsClientCanEditApplicationAndIsManagerUser]
    checklist_prefetch = Prefetch('checklists', queryset=Checklist.objects.all())
    file_prefetch = Prefetch('files', queryset=ApplicationFile.objects.all())
    queryset = queryset.prefetch_related(checklist_prefetch, file_prefetch)

    def update(self, request, *args, **kwargs):
        '''Change tracking for logs and notifications'''
        instance = self.get_object()
        old_instance = ApplicationForm.objects.get(id=instance.id)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        instance = self.get_object()
        user = request.user
        user_id = user.id
        user_image = user.image
        for field in instance._meta.fields:
            old_value = getattr(old_instance, field.name)
            new_value = getattr(instance, field.name)
            if old_value != new_value:
                ApplicationLogs.objects.create(field=field.verbose_name,
                                               initially=old_value, new=new_value,
                                               form=instance, user=user.full_name,
                                               user_id=user_id, user_image=user_image)

        changes = []
        if old_instance.status != instance.status:
            changes.append(
                f"Статус изменен с '{old_instance.get_status_display()}' на '{instance.get_status_display()}'")
        if old_instance.priority != instance.priority:
            changes.append(
                f"Приоритет изменен с '{old_instance.get_priority_display()}' на '{instance.get_priority_display()}'")

        if changes:
            manager_name = f"{user.full_name} изменил(а)"
            for change in changes:
                Notification.objects.create(task_number=instance.task_number, title=instance.title,
                                            text=change, made_change=manager_name, form_id=instance.id,
                                            is_manager_notic=True)
                Notification.objects.create(task_number=instance.task_number, title=instance.title, text=change,
                                            made_change=manager_name, form_id=instance.id,
                                            is_client_notic=True)

        admin_notification = CustomUser.objects.filter(is_superuser=True)
        user = request.user
        manager_name = user.full_name
        for admin in admin_notification:
            if instance.status == 'Проверено':
                Notification.objects.create(task_number=instance.task_number,
                                            text=f"Заявка закрыта",
                                            title=instance.title, made_change=manager_name, is_admin=True,
                                            admin_id=admin.id)

        return Response(serializer.data)


class ApplicationFormRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = ApplicationForm.objects.all().select_related('main_client', 'main_manager', 'company')
    serializer_class = ApplicationFormDetailViewSerializer
    lookup_field = 'id'
    permission_classes = [IsManagerCanDeleteApplicationOrIsAdminUser]


class ApplicationLogsListCreateAPIView(generics.ListCreateAPIView):
    queryset = ApplicationLogs.objects.all()
    serializer_class = LogsSerializer
    lookup_field = 'id'
    # permission_classes = [IsClientCanViewLogsOrIsAdminAndManagerUser]



class FileListCreateAPIView(generics.ListCreateAPIView):
    queryset = ApplicationFile.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsClientCanAddFilesOrIsAdminAndManagerUser]

    def perform_create(self, serializer):
        instance = serializer.save()

        user = self.request.user
        user_id = user.id
        user_name = f"{user.first_name} {user.surname}"
        file_name = instance.file.name
        ApplicationLogs.objects.create(
            user=user_name, field="Описание", new=f"добавлен файл {file_name}", file_logs=instance.file,
            form=instance.application, user_id=user_id)


class FileDeleteAPIView(generics.DestroyAPIView, BaseLoggingCreateDestroy):
    queryset = ApplicationFile.objects.all()
    serializer_class = FileSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUserAndManagerUser]

    def perform_destroy(self, instance):
        file_name = instance.file.name
        self.log_destroy(instance, "Описание", f"Файл удалён {file_name}")


class ApplicationsOnlyDescriptionAPIView(generics.RetrieveUpdateAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationsOnlyDescriptionSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


class ChecklistListCreateAPIView(generics.ListCreateAPIView, BaseLoggingCreateDestroy):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    lookup_field = 'id'
    permission_classes = [IsClientCanAddChecklistOrIsAdminAndManagerUser]

    def perform_create(self, serializer):
        instans = serializer.save()
        self.log_create(serializer, "Чеклист", f"Чеклист создан {instans.name}")


class CheckListDetailAPIView(generics.RetrieveUpdateDestroyAPIView, BaseLoggingUpdate, BaseLoggingCreateDestroy):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    lookup_field = 'id'
    permission_classes = [IsClientCanAddChecklistOrIsAdminAndManagerUser]

    def update(self, request, *args, **kwargs):
        '''
        Change tracking for logs and notifications
        '''
        instance = self.get_object()
        old_instance = Checklist.objects.get(id=instance.id)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        instance = self.get_object()
        self.log_changes(old_instance, instance)

        return Response(serializer.data)

    def perform_destroy(self, instance):
        checklist_name = instance.name
        self.log_destroy(instance, "Чеклист", f"Чеклист {checklist_name} удалён")


class SubTaskCreateAPIView(generics.ListCreateAPIView, BaseLoggingCreateDestroy):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    lookup_field = 'id'
    permission_classes = [IsClientCanAddChecklistOrIsAdminAndManagerUser]

    def perform_create(self, serializer):
        instans = serializer.save()

        user = self.request.user
        user_id = user.id
        user_name = f"{user.first_name} {user.surname}"
        ApplicationLogs.objects.create(
            user=user_name, field="Подзадача", new=instans.text,
            check_list_id=instans.checklist, user_id=user_id)


class SubTaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    lookup_field = 'id'
    permission_classes = [IsClientCanAddChecklistOrIsAdminAndManagerUser]

    def update(self, request, *args, **kwargs):
        '''Change tracking for logs and notifications'''
        instance = self.get_object()
        old_instance = SubTask.objects.get(id=instance.id)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        instance = self.get_object()

        user = request.user
        user_id = user.id
        user_image = user.image

        for field in instance._meta.fields:
            old_value = getattr(old_instance, field.name)
            new_value = getattr(instance, field.name)
            if old_value != new_value:
                ApplicationLogs.objects.create(field=field.verbose_name,
                                               initially=old_value, new=new_value,
                                               check_list_id=instance.checklist, user=user.full_name,
                                               user_id=user_id, user_image=user_image)

        return Response(serializer.data)


class CommentsAPIView(generics.ListCreateAPIView, BaseLoggingCreateDestroy):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsClientCanCreateCommentsOrIsAdminAndManagerUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        instans = serializer.save()
        self.log_create(serializer, "Комментарии", f"{instans.text}")


class CommentsDetailAPIView(generics.RetrieveUpdateDestroyAPIView, BaseLoggingUpdate, BaseLoggingCreateDestroy):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminOrManagerOrClientUsersCanEditComments]

    def update(self, request, *args, **kwargs):
        '''Change tracking for logs and notifications'''
        instance = self.get_object()
        old_instance = Comments.objects.get(id=instance.id)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        instance = self.get_object()
        self.log_changes(old_instance, instance)

        return Response(serializer.data)

    def perform_destroy(self, instance):
        self.log_destroy(instance, "Комментарий", "Комментарий удалён")


class NotificationAPIView(generics.ListAPIView):
    '''Sending notifications'''
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request):
        if request.user.is_superuser:
            admin_id_n = request.user.id
            admin_notifications = Notification.objects.filter(is_admin=True, admin_id=admin_id_n)

            for notification in admin_notifications:
                cache.set(f'notification_sent_{notification.id}', True)

            serializer = NotificationSerializer(admin_notifications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user_application = ApplicationForm.objects.filter(
                Q(main_client=request.user) | Q(main_manager=request.user))
            notification_user_application = Notification.objects.filter(form__in=user_application)
            if request.user.is_manager:
                notification_user_application = notification_user_application.filter(is_manager_notic=True)
            elif request.user.is_client:
                notification_user_application = notification_user_application.filter(is_client_notic=True)

            for notification in notification_user_application:
                cache.set(f'notification_sent_{notification.id}', True)

            serializer = NotificationSerializer(notification_user_application, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationDeleteViewAPI(generics.DestroyAPIView):
    '''Deleting notifications'''

    def delete(self, request, id=None):
        admin_id = request.user.id
        if id is None or id == 'all':
            for notification in Notification.objects.all():
                if cache.get(f'notification_sent_{notification.id}'):
                    cache.delete(f'notification_sent_{notification.id}')
                    notification.delete()
                elif admin_id == notification.admin_id:
                    notification.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            try:
                notification = Notification.objects.get(id=id)
                if cache.get(f'notification_sent_{notification.id}'):
                    cache.delete(f'notification_sent_{notification.id}')
                notification.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Notification.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)


class NotificationTrueAPIView(generics.ListAPIView):
    '''API for separating notifications into read and unread'''
    queryset = Notification.objects.all().select_related('form')
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            admin_id_get = request.user.id
            admin_notifications = Notification.objects.filter(is_admin=True, admin_id=admin_id_get)
            serializer = NotificationSerializer(admin_notifications, many=True)
            admin_notifications.update(is_read=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user_application = ApplicationForm.objects.filter(
                Q(main_client=request.user) | Q(main_manager=request.user))
            notification_user_application = Notification.objects.filter(form__in=user_application)
            serializer = NotificationSerializer(notification_user_application, many=True)
            notification_user_application.update(is_read=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
