from datetime import datetime, timedelta, date
import django_filters
from django.http import Http404
from apps.application.models import ApplicationForm


class ApplicationFormFilter(django_filters.FilterSet):
    company_name = django_filters.CharFilter(field_name='company__name', lookup_expr='icontains')
    manager_first_name = django_filters.CharFilter(field_name='manager__first_name', lookup_expr='icontains')
    week = django_filters.BooleanFilter(method='filter_by_week')
    month = django_filters.BooleanFilter(method='filter_by_month')
    all_time = django_filters.BooleanFilter(method='filter_by_all_time')
    start_date = django_filters.DateFilter(field_name='application_date', method='filter_by_start_date')
    finish_date = django_filters.DateFilter(field_name='finish_date', method='filter_by_finish_date')

    class Mete:
        model = ApplicationForm
        fields = ['start_date', 'finish_date', 'week', 'month', 'all_time']

    def filter_by_week(self, queryset, value, name):
        if value:
            week_date = date.today() - timedelta(days=7)
            return queryset.filter(application_date__gte=week_date)
        # return queryset

    def filter_by_month(self, queryset, value, name):
        if value:
            month_date = datetime.now() - timedelta(days=30)
            return queryset.filter(application_date__gte=month_date)
        # return queryset

    def filter_by_all_time(self, queryset, value, name):
        if value:
            return queryset
        return queryset.none()

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

