from functools import reduce
from .serializers import *
from .models import *
from rest_framework import generics, filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ApplicationFormFilter
from datetime import datetime
from apps.user.permissions import *
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.db.models import Count
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination


class ApplicationFormCreateAPIView(generics.CreateAPIView):
    queryset = ApplicationForm.objects.all()
    serializer_class = ApplicationFormCreateSerializer
    # permission_classes = [IsAdminUser, IsManagerUser]



class CaseInsensitiveSearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_fields = getattr(view, 'search_fields', [])
        search_term = request.query_params.get(self.search_param, '').strip()

        if search_term:
            or_condition = Q()
            for field_name in search_fields:
                or_condition |= Q(**{f'{field_name}__iregex': f'.*{search_term}.*'})
            queryset = queryset.filter(or_condition)
        return queryset


class ApplicationFormListAPIView(generics.ListAPIView):
    serializer_class = ApplicationFormDetailSerializer
    filter_backends = [CaseInsensitiveSearchFilter, DjangoFilterBackend]
    # permission_classes = [IsAuthenticated]
    queryset = ApplicationForm.objects.all()
    filterset_class = ApplicationFormFilter
    # pagination_class = PageNumberPagination
    search_fields = ['task_number', 'title', 'description', 
                 'main_client__first_name', 'main_manager__first_name', 
                 'start_date', 'finish_date', 'priority', 'payment_state']
    def get_queryset(self):
        user = self.request.user
        if user.is_client:
            queryset = ApplicationForm.objects.filter(Q(main_client=user) | 
                                                        Q(company=user.main_company))
        elif user.is_manager:
            queryset = ApplicationForm.objects.filter(Q(main_manager=user) | 
                                                        Q(checklists__manager=user) | 
                                                        Q(company=user.main_company))
        elif user.is_superuser:
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






