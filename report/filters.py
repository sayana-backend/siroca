from apps.application.models import ApplicationForm
from datetime import datetime, timedelta, date
from django.http import Http404
from django.db.models import Q
import django_filters


class ApplicationFormFilter(django_filters.FilterSet):
    '''Filter for report'''
    company_name = django_filters.CharFilter(field_name='company__name', lookup_expr='icontains', method='filter_by_company_name')
    manager_name = django_filters.CharFilter(method='filter_by_manager')
    start_date = django_filters.DateFilter(field_name='application_date', method='filter_by_start_date')
    finish_date = django_filters.DateFilter(field_name='finish_date', method='filter_by_finish_date')

    class Meta:
        model = ApplicationForm
        fields = ['company_name', 'manager_name', 'start_date', 'finish_date']

    def filter_by_company_name(self, queryset, name, value):
        if not value:
            return queryset
        companies = [company.strip() for company in value.split(',')]
        return queryset.filter(company__name__in=companies)

    def filter_by_manager(self, queryset, name, value):
        if not value:
            return queryset
        managers = [manager.strip() for manager in value.split(',')]
        q_filter = Q()
        for manager in managers:
            q_filter |= (Q(main_manager__first_name__icontains=manager) |
                         Q(main_manager__surname__icontains=manager) |
                         Q(main_manager__full_name__icontains=manager))
        return queryset.filter(q_filter)

    def filter_by_start_date(self, queryset, name, value):
        filter_start_date = queryset.filter(application_date__gte=value)
        if not filter_start_date.exists():
            raise Http404()
        return filter_start_date

    def filter_by_finish_date(self, queryset, name, value):
        filter_finish_date = queryset.filter(application_date__lte=value)
        if not filter_finish_date.exists():
            raise Http404()
        return filter_finish_date
