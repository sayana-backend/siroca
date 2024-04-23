from .serializers import *
from .models import *
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ApplicationFormFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from apps.user.permissions import *
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Comments
from .serializers import CommentsSerializer
from .signals import *



class ApplicationFormCreateAPIView(generics.CreateAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormCreateSerializer

    def perform_create(self, serializer):
        serializer.save(main_manager=self.request.user)

class CustomPagination(PageNumberPagination):
    page_size = 50
    def get_paginated_response(self, data):
        return Response(data)



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
            closed_count = queryset.filter(status='Закрыто').count()
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
    lookup_field = 'id'
    serializer_class = ApplicationFormDetailSerializer

    # permission_classes = [IsManagerCanCreateAndEditCompany]


class ApplicationFormRetrieveUpdateDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer
    lookup_field = 'id'


class ApplicationLogsListCreateAPIView(generics.ListCreateAPIView):
    queryset = ApplicationLogs.objects.all()
    lookup_field = 'id'
    serializer_class = LogsSerializer
    permission_classes = [IsAdminUserOrIsManagerCanDeleteComments]


class ApplicationLogsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):  #### убрать DELETE - запрос
    queryset = ApplicationLogs.objects.all()
    serializer_class = LogsSerializer
    lookup_field = 'id'


class ChecklistAPIView(generics.CreateAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    # permission_classes = [IsClientCanAddChecklist,
    #                       IsAdminUser,
    #                       IsManagerUser]


class CheckListDetailAPIView(generics.RetrieveUpdateDestroyAPIView):  ### посмотреть внимательно
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    lookup_field = 'id'
    # permission_classes = [IsAdminUser,
    #                       IsManagerUser]


class CommentsAPIView(generics.CreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    lookup_field = 'id'
    # permission_classes = [IsManagerCanDeleteComments,]


class NotificationAPIView(generics.ListAPIView, generics.DestroyAPIView, generics.CreateAPIView, generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request):
        if request.user.is_superuser:
            admin_notifications = Notification.objects.filter(is_admin=True)
            serializer = NotificationSerializer(admin_notifications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user_application = ApplicationForm.objects.filter(
                Q(main_client=request.user) | Q(main_manager=request.user))
            notification_user_application = Notification.objects.filter(form__in=user_application)
            serializer = NotificationSerializer(notification_user_application, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # def perform_create(self, serializer):
    #     serializer.save(made_change=self.request.user)
    # def delete(self, request, *args, **kwargs):
    #     if 'id' in kwargs:  # Если указан конкретный идентификатор уведомления
    #         return self.destroy(request, *args, **kwargs)
    #     else:  # Если не указан идентификатор, то удаляем все уведомления
    #         notifications = self.get_queryset()
    #         notifications.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationTrueAPIView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            admin_notifications = Notification.objects.filter(is_admin=True)
            serializer = NotificationSerializer(admin_notifications, many=True)
            admin_notifications.update(is_read=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user_application = ApplicationForm.objects.filter(
                Q(main_client=request.user) | Q(made_change=request.user))
            notification_user_application = Notification.objects.filter(form__in=user_application)
            serializer = NotificationSerializer(notification_user_application, many=True)
            notification_user_application.update(is_read=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # def delete(self, request, *args, **kwargs):
    #     if 'id' in kwargs:  # Если указан конкретный идентификатор уведомления
    #         return self.destroy(request, *args, **kwargs)
    #     else:  # Если не указан идентификатор, то удаляем все уведомления
    #         notifications = self.get_queryset()
    #         notifications.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    # return self.destroy_all(request, *args, **kwargs)

    # def destroy_all(self, request, *args, **kwargs):
    #     notifications = self.get_queryset()
    #     notifications.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # def get(self, request):
    #     if request.user.is_superuser:
    #         admin_notifications = Notification.objects.filter(is_admin=True)
    #         serializer = NotificationSerializer(admin_notifications, many=True)
    #         cache.set('notifications', admin_notifications)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         user_application = ApplicationForm.objects.filter(
    #             Q(main_client=request.user) | Q(main_manager=request.user))
    #         notification_user_application = Notification.objects.filter(form__in=user_application)
    #         serializer = NotificationSerializer(notification_user_application, many=True)
    #         cache.set('notifications', notification_user_application)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # def delete(self, request, *args, **kwargs):
    #     notifications = cache.get('notifications')
    #     if 'id' in kwargs and notifications.filter(id=kwargs['id']).exists():
    #         notification = notifications.get(id=kwargs['id'])
    #         notification.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     elif 'id' not in kwargs:
    #         notifications.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     else:
    #         return Response(status=status.HTTP_404_NOT_FOUND)


# class NotificationDestroyAPIView(generics.DestroyAPIView):
#     queryset = Notification.objects.all()
#     serializer_class = NotificationSerializer
#     permission_classes = [IsAuthenticated]
#     lookup_field = 'id'

    # def delete(self, request, id):
    #     if id:
    #         try:
    #             notification = Notification.objects.get(id=id)
    #             notification.delete()
    #             return Response(status=status.HTTP_204_NO_CONTENT)
    #         except Notification.DoesNotExist:
    #             return Response(status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         notifications = Notification.objects.all()
    #         notifications.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
