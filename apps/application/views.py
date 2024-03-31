from .serializers import *
from .models import *
from datetime import timedelta
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from apps.user.permissions import *
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


class ApplicationFormCreateAPIView(generics.CreateAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormCreateSerializer
    # permission_classes = [IsAdminUser, IsManagerUser]



class ApplicationFormListAPIView(generics.ListAPIView):
    serializer_class = ApplicationFormDetailSerializer
    # permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = ApplicationForm.objects.all()

        all_count = queryset.count()  

        interval = self.request.query_params.get('interval')
        status = self.request.query_params.get('status')

        if interval:
            if interval == 'week':
                start_date = timezone.now() - timedelta(days=7)
                if status:
                    queryset = queryset.filter(
                        Q(application_date__gte=start_date) & Q(status=status)
                    )
                else:
                    queryset = queryset.filter(application_date__gte=start_date)
            elif interval == 'month':
                start_date = timezone.now() - timedelta(days=30)
                if status:
                    queryset = queryset.filter(
                        Q(application_date__gte=start_date) & Q(status=status)
                    )
                else:
                    queryset = queryset.filter(application_date__gte=start_date)

        in_progress_week_count = queryset.filter(status='В работе').count()
        closed_week_count = queryset.exclude(status='В работе').count()

        if status:
            queryset = queryset.filter(status=status)

        in_progress_month_count = queryset.filter(status='В работе').count()
        closed_month_count = queryset.exclude(status='В работе').count()

        
        response_data = {
            'all_count': all_count ,
            'in_progress_week_count': in_progress_week_count,
            'closed_week_count': closed_week_count,
            'in_progress_month_count': in_progress_month_count,
            'closed_month_count': closed_month_count,
        }

        return queryset, response_data

    def list(self, request, *args, **kwargs):
        queryset, response_data = self.get_queryset()

    
        response_data['results'] = self.get_serializer(queryset, many=True).data
        paginated_queryset = self.paginate_queryset(queryset)

        if paginated_queryset is not None:
            response_data['results'] = self.get_serializer(paginated_queryset, many=True).data

        return self.get_paginated_response(response_data)


class ApplicationFormRetrieveAPIView(generics.RetrieveAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer
    # permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class ApplicationFormRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer
    # permission_classes = [IsManagerCanDeleteComments,
    #                       IsManagerCanDeleteApplication,
    #                       IsAdminUser]
    lookup_field = 'id'



class ApplicationLogsListCreateAPIView(generics.ListCreateAPIView):  ### внимательно посмотреть нужен ли CREATE - запрос
    queryset = ApplicationLogs.objects.all()
    serializer_class = ApplicationLogsSerializer
    # permission_classes = [IsClientCanViewLogs,
    #                       IsAdminUser,
    #                       IsManagerUser]


# class ApplicationLogsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):   #### убрать DELETE - запрос
#     queryset = ApplicationLogs.objects.all()
#     serializer_class = ApplicationLogsSerializer
#     lookup_field = 'id'


class ChecklistAPIView(generics.ListCreateAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    # permission_classes = [IsClientCanAddChecklist,
    #                       IsAdminUser,
    #                       IsManagerUser]


class CheckListDetailAPIView(generics.RetrieveUpdateDestroyAPIView):   ### посмотреть внимательно
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    lookup_field = 'id'
    # permission_classes = [IsAdminUser,
    #                       IsManagerUser]


class CommentsAPIView(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    # permission_classes = [IsClientCanEditComments,
    #                       IsAdminUser,
    #                       IsManagerUser]


class CommentsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    lookup_field = 'id'
    # permission_classes = [IsManagerCanDeleteComments,
    #                       IsClientCanEditComments,
    #                       IsAdminUser]





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
            user_application = ApplicationForm.objects.filter(Q(main_client=request.user) | Q(main_manager=request.user))
            notification_user_application = Notification.objects.filter(form__in=user_application)
            serializer = NotificationSerializer(notification_user_application, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
