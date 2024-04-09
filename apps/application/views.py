from functools import reduce
from .serializers import *
from .models import *
from rest_framework import generics, filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ApplicationFormFilter
from datetime import timedelta
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from apps.user.permissions import *
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import generics
from .models import Comments
from .serializers import CommentsSerializer
from django.http import HttpRequest
from django.shortcuts import render


class CustomSearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'search_fields', [])
        search_term = request.query_params.get(self.search_param, '').strip()

        if search_term:
            or_condition = Q()
            for field_name in search_fields:
                or_condition |= Q(**{f'{field_name}__iregex': f'.*{search_term}.*'})
            queryset = queryset.filter(or_condition)
        return queryset


class ApplicationFormCreateAPIView(generics.CreateAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormCreateSerializer

    def perform_create(self, serializer):
        serializer.save(main_manager=self.request.user)


class ApplicationFormListAPIView(generics.ListAPIView):
    serializer_class = ApplicationFormDetailSerializer
    filter_backends = [CustomSearchFilter, DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
    filterset_class = ApplicationFormFilter
    pagination_class = PageNumberPagination
    search_fields = ['task_number', 'title', 'short_description',
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


class ApplicationFormRetrieveAPIView(generics.RetrieveAPIView):
    ''' Second create API '''
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormListSerializer
    # permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class ApplicationFormRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer
    lookup_field = 'id'
    # permission_classes = [IsManagerCanDeleteComments,
    #                       IsManagerCanDeleteApplication,
    #                       IsAdminUser]


class ApplicationLogsListCreateAPIView(generics.ListCreateAPIView):
    queryset = ApplicationLogs.objects.all()
    serializer_class = ApplicationLogsSerializer
    lookup_field = 'id'
    # permission_classes = [IsClientCanViewLogs,
    #                       IsAdminUser,
    #                       IsManagerUser]


# class ApplicationLogsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):   #### убрать DELETE - запрос
#     queryset = ApplicationLogs.objects.all()
#     serializer_class = ApplicationLogsSerializer
#     lookup_field = 'id'


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
    # permission_classes = [IsManagerCanDeleteComments,
    #                       IsClientCanEditComments,
    #                       IsAdminUser]


# class NotificationAPIView(generics.ListCreateAPIView):

class NotificationAPIView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

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

    def finalize_response(self, request, response, *args, **kwargs):
        if request.method == 'GET' and response.status_code == status.HTTP_200_OK:
            if request.user.is_superuser:
                admin_notifications = Notification.objects.filter(is_admin=True)
                admin_notifications.update(is_read=True)
            else:
                user_application = ApplicationForm.objects.filter(
                    Q(main_client=request.user) | Q(main_manager=request.user))
                notification_user_application = Notification.objects.filter(form__in=user_application)
                notification_user_application.update(is_read=True)
        return super().finalize_response(request, response, *args, **kwargs)


# class FinalizeNotifiactionAPIView(generics.ListAPIView):
#     # queryset = Notification.objects.all()
#     serializer_class = NotificationSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_serializer_class(self):
#         if self.request.user.is_superuser:
#             return NotificationSerializer
#         else:
#             return NotificationSerializer
#
#     def get_queryset(self):
#         if self.request.user.is_superuser:
#             admin_notifications = Notification.objects.filter(is_admin=True)
#             admin_notifications.update(is_read=True)
#             return admin_notifications
#         else:
#             user_application = ApplicationForm.objects.filter(
#                 Q(main_client=self.request.user) | Q(main_manager=self.request.user))
#             notification_user_application = Notification.objects.filter(form__in=user_application)
#             notification_user_application.update(is_read=True)
#             return notification_user_application
