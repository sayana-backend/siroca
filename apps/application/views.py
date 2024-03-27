from .models import ApplicationForm, Checklist, Comments, ApplicationLogs, Notification
from .serializers import (ApplicationFormDetailSerializer,
                          ChecklistSerializer,
                          CommentsSerializer,
                          ApplicationLogsSerializer,
                          NotificationSerializer)
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q
from django.db.models import Count
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination


class ApplicationFormCreateAPIView(generics.CreateAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer


class ApplicationFormListAPIView(generics.ListAPIView):
    serializer_class = ApplicationFormDetailSerializer
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


class ApplicationFormRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormDetailSerializer
    lookup_field = 'id'


class ApplicationLogsListCreateAPIView(generics.ListCreateAPIView):
    queryset = ApplicationLogs.objects.all()
    serializer_class = ApplicationLogsSerializer


class ChecklistAPIView(generics.ListCreateAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer


class CommentsAPIView(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class ApplicationLogsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApplicationLogs.objects.all()
    serializer_class = ApplicationLogsSerializer
    lookup_field = 'id'


class CheckListDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer
    lookup_field = 'id'


class CommentsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    lookup_field = 'id'


class NotificationListAPIView(generics.ListAPIView):
    # queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user_id = self.kwargs['id']
        return Notification.objects.filter(user_id=user_id)




