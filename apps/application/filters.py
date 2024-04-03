import django_filters
from .models import ApplicationForm
from django.utils import timezone
from datetime import timedelta


class ApplicationFormFilter(django_filters.FilterSet):
    interval = django_filters.CharFilter(method='filter_by_interval')
    task_number = django_filters.CharFilter(field_name='task_number', lookup_expr='iregex')
    title = django_filters.CharFilter(field_name='title', lookup_expr='iregex')
    description = django_filters.CharFilter(field_name='short_description', lookup_expr='iregex')
    main_client = django_filters.CharFilter(field_name='main_client__first_name', lookup_expr='iregex')
    main_manager = django_filters.CharFilter(field_name='main_manager__first_name', lookup_expr='iregex')
    start_date = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    finish_date = django_filters.DateFilter(field_name='finish_date', lookup_expr='lte')
    priority = django_filters.NumberFilter(field_name='priority', lookup_expr='iregex')
    payment_state = django_filters.CharFilter(field_name='payment_state', lookup_expr='iregex')

    def filter_by_interval(self, queryset, name, value):
        if value == 'week':
            start_date = timezone.now() - timedelta(days=7)
            queryset = queryset.filter(application_date__gte=start_date)
        elif value == 'month':
            start_date = timezone.now() - timedelta(days=30)
            queryset = queryset.filter(application_date__gte=start_date)
        return queryset

    class Meta:
        model = ApplicationForm
        fields = ['task_number', 'title', 'description', 'main_client', 'main_manager', 'start_date', 'finish_date', 'priority', 'payment_state']