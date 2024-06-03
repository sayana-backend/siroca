from collections import OrderedDict
import django_filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import ApplicationForm
from django.utils import timezone
from datetime import timedelta


class ApplicationFormFilter(django_filters.FilterSet):
    interval = django_filters.CharFilter(method='filter_by_interval')
    task_number = django_filters.CharFilter(method='filter_by_multiple_values', field_name='task_number')
    company = django_filters.CharFilter(method='filter_by_multiple_values', field_name='company__name')
    title = django_filters.CharFilter(method='filter_by_multiple_values', field_name='title')
    short_description = django_filters.CharFilter(method='filter_by_multiple_values', field_name='short_description')
    main_client = django_filters.CharFilter(method='filter_by_multiple_values', field_name='main_client__full_name')
    main_manager = django_filters.CharFilter(method='filter_by_multiple_values', field_name='main_manager__full_name')
    start_date = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    finish_date = django_filters.DateFilter(field_name='finish_date', lookup_expr='lte')
    priority = django_filters.NumberFilter(method='filter_by_multiple_values', field_name='priority')
    payment_state = django_filters.CharFilter(method='filter_by_multiple_values', field_name='payment_state')

    def filter_by_interval(self, queryset, name, value):
        if value == 'week':
            start_date = timezone.now() - timedelta(days=7)
            queryset = queryset.filter(application_date__gte=start_date)
        elif value == 'month':
            start_date = timezone.now() - timedelta(days=30)
            queryset = queryset.filter(application_date__gte=start_date)
        return queryset

    def filter_by_multiple_values(self, queryset, name, value):
        values = value.split(',')
        filtered_queryset = queryset.none()
        for val in values:
            filtered_queryset |= queryset.filter(**{f"{name}__icontains": val.strip()})
        return filtered_queryset.distinct()

    class Meta:
        model = ApplicationForm
        fields = ['interval', 'task_number', 'company', 'title', 'short_description', 'main_client', 
                  'main_manager', 'start_date', 'finish_date', 'priority', 'payment_state']


class CustomPagination(PageNumberPagination):
    page_size = 50

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('data', data)
        ]))
