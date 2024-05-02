from collections import OrderedDict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, filters
from .filters import ApplicationFormFilter
from apps.user.permissions import *
from django.core.cache import cache
from rest_framework import status
from django.db.models import Q
from .serializers import *
from .signals import *
from .models import *


class CustomPagination(PageNumberPagination):
    page_size = 2

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('data', data)
        ]))


class ApplicationFormCreateAPIView(generics.CreateAPIView):
    '''Create new application'''
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormCreateSerializer
    permission_classes = [IsClientCanCreateApplicationOrIsAdminAndManagerUser]

    def perform_create(self, serializer):
        '''Tracking the creation of an application for notifications'''
        instance = serializer.save()

        # Создание уведомления для администраторов при создании новой заявки
        admin_notification = CustomUser.objects.filter(is_superuser=True)
        user = self.request.user
        user_name = f"{user.first_name}. {user.surname}"
        for admin in admin_notification:
            Notification.objects.create(
                task_number=f'Номер заявки: {instance.task_number}',
                text=f'Создана новая заявка', title=instance.title,
                made_change=user_name, is_admin=True, admin_id=admin.id
            )


class ApplicationFormListAPIView(generics.ListAPIView):
    serializer_class = ApplicationFormListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
    filterset_class = ApplicationFormFilter
    pagination_class = CustomPagination
    search_fields = ['task_number', 'title', 'company__name', 'short_description',
                     'main_client__first_name', 'main_manager__first_name',
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
                                                      Q(checklists__manager=user) |
                                                      Q(company=user.main_company))

        queryset = queryset.order_by('-application_date')
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            created_count = queryset.count()
            in_progress_count = queryset.filter(status='В работе').count()
            closed_count = queryset.filter(status='Проверено').count()
            data = {
                'created_count': created_count,
                'in_progress_count': in_progress_count,
                'closed_count': closed_count,
                'results': serializer.data
            }
            return self.get_paginated_response(data)
        return Response({'detail': 'Not found'}, status=404)


class ApplicationFormRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    '''  update API '''
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormUpdateSerializer
    lookup_field = 'id'
    permission_classes = [IsClientCanEditApplicationAndIsManagerUser]

    def update(self, request, *args, **kwargs):
        '''Change tracking for logs and notifications'''
        instance = self.get_object()
        old_instance = ApplicationForm.objects.get(id=instance.id)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        instance = self.get_object()

        user = request.user
        user_name = f"{user.first_name}. {user.surname}"
        for field in instance._meta.fields:
            old_value = getattr(old_instance, field.name)
            new_value = getattr(instance, field.name)
            if old_value != new_value:
                change_message = f"{field.verbose_name} изменено с {old_value} на {new_value}"
                ApplicationLogs.objects.create(text=f"{change_message}",
                                               form=instance, user=user_name)

        changes = []
        if old_instance.status != instance.status:
            changes.append(
                f"Статус изменен с '{old_instance.get_status_display()}' на '{instance.get_status_display()}'")
        if old_instance.priority != instance.priority:
            changes.append(
                f"Приоритет изменен с '{old_instance.get_priority_display()}' на '{instance.get_priority_display()}'")

        if changes:
            manager_name = f"{user_name}"
            for change in changes:
                Notification.objects.create(task_number=instance.task_number, title=instance.title,
                                            text=change, made_change=manager_name, form_id=instance.id,
                                            is_manager_notic=True)
                Notification.objects.create(task_number=instance.task_number, title=instance.title, text=change,
                                            made_change=manager_name, form_id=instance.id,
                                            is_client_notic=True)

        admin_notification = CustomUser.objects.filter(is_superuser=True)

        for admin in admin_notification:
            if instance.status == 'Проверено':
                Notification.objects.create(task_number=f'Номер заявки: {instance.task_number}',
                                            text=f"Заявка закрыто",
                                            title=instance.title, made_change=manager_name, is_admin=True,
                                            admin_id=admin.id)

        return Response(serializer.data)


class ApplicationFormRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailViewSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUserAndManagerUser]


class ApplicationLogsListCreateAPIView(generics.ListCreateAPIView):
    queryset = ApplicationLogs.objects.all()
    serializer_class = LogsSerializer
    lookup_field = 'id'
    permission_classes = [IsClientCanViewLogsOrIsAdminAndManagerUser]


class ApplicationLogsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationLogs.objects.all()
    serializer_class = LogsSerializer
    lookup_field = 'id'


class ChecklistListCreateAPIView(generics.ListCreateAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    lookup_field = 'id'
    permission_classes = [IsClientCanAddChecklistOrIsAdminAndManagerUser]


class CheckListDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    lookup_field = 'id'
    # permission_classes = [IsAdminUser,
    #                       IsManagerUser]


class CommentsAPIView(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsClientCanCreateCommentsOrIsAdminAndManagerUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminOrManagerOrClientUsersCanEditComments]


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

        return Response(status=status.HTTP_400_BAD_REQUEST)


class NotificationTrueAPIView(generics.ListAPIView):
    '''API for separating notifications into read and unread'''
    queryset = Notification.objects.all()
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
