from apps.application.signals import BaseLoggingCreateDestroy, BaseLoggingUpdate, NotificationService
from django.db.models import Count, Q, Case, When, Value, CharField
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ApplicationFormFilter, CustomPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import Coalesce
from rest_framework.response import Response
from rest_framework import generics, filters
from .signals import NotificationService
from django.db.models import Prefetch
from django.core.cache import cache
from django.db import transaction
from apps.user.permissions import *
from rest_framework import status
from .serializers import *
from .models import *


class ApplicationFormCreateAPIView(generics.CreateAPIView, BaseLoggingCreateDestroy, NotificationService):
    '''Create new application'''
    queryset = ApplicationForm.objects.all().select_related('main_client', 'main_manager', 'company')
    serializer_class = ApplicationFormCreateSerializer
    permission_classes = [IsClientCanCreateApplicationOrIsAdminAndManagerUser]

    @transaction.atomic
    def perform_create(self, serializer):
        '''Tracking the creation of an application for notifications'''
        instance = serializer.save()
        self.log_application_create(instance)

        self.create_notification(instance, 'create')


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
            ),
            status_order=Case(
                When(status='Проверено', then=Value(2)),
                default=Value(1),
                output_field=CharField(),
            )
        ).order_by('status_order', 'priority_order', '-application_date')

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


class ApplicationFormRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView, NotificationService):
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

        if old_instance.main_manager != instance.main_manager:
            self.create_notification(instance, 'manager')
        if old_instance.status != instance.status:
            if instance.status == 'Проверено':
                self.create_notification(instance, 'close')
            else:
                self.create_notification(instance, 'status')
        if old_instance.priority != instance.priority:
            self.create_notification(instance, 'priority')

        return Response(serializer.data)


class ApplicationFormRetrieveAPIView(generics.RetrieveAPIView):
    queryset = ApplicationForm.objects.all().select_related('main_client', 'main_manager', 'company')
    serializer_class = ApplicationFormDetailViewSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]


class ApplicationFormDestroyAPIView(generics.DestroyAPIView, NotificationService):
    queryset = ApplicationForm.objects.all().select_related('main_client', 'main_manager', 'company')
    serializer_class = ApplicationFormDetailViewSerializer
    lookup_field = 'id'
    permission_classes = [IsManagerCanDeleteApplicationOrIsAdminUser]

    def perform_destroy(self, instance):
        self.create_notification(instance, 'delete')


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


class ChecklistListCreateAPIView(generics.ListCreateAPIView, BaseLoggingCreateDestroy, NotificationService):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    lookup_field = 'id'
    permission_classes = [IsClientCanAddChecklistOrIsAdminAndManagerUser]

    def perform_create(self, serializer):
        instans = serializer.save()
        self.log_create(serializer, "Чеклист", f"Чеклист создан {instans.name}")
        self.create_notification(instans.application, 'checklist')


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


class NotificationListAPIView(generics.ListAPIView, NotificationService):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def list(self, request):
        user = request.user
        print(user)
        new = self.queryset.filter(users=user).exclude(Q(readed=user) | Q(cleared=user)).order_by('-id')
        old = self.queryset.filter(users=user, readed=user).exclude(cleared=user).order_by('-id')
        new_ser = self.serializer_class(new, many=True).data
        old_ser = self.serializer_class(old, many=True).data
        self.notification_read(new_ser, user)
        return Response({"new": new_ser, "read": old_ser})


class NotificationDeleteViewAPI(generics.DestroyAPIView):
    '''Deleting notifications'''

    def delete(self, request, id=None):
        user = request.user.id
        if id is None or id == 'all':
            for notification in Notification.objects.filter(users=user):
                notification.cleared.add(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            try:
                notification = Notification.objects.get(id=id)
                notification.cleared.add(user)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Notification.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)


class NewNotificationAPIView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def list(self, request):
        user = request.user
        print(user)
        new = self.queryset.filter(users=user).exclude(Q(readed=user) | Q(cleared=user))
        if new:
            return Response(True)
        else:
            return Response(False)
