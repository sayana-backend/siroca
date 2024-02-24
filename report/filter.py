import django_filters
from apps.application.models import ApplicationForm


class ApplicationFilter(django_filters.Filter):
    company_name = django_filters.CharFilter(field_name='company__name', lookup_expr='icontains')
    manager_name = django_filters.CharFilter(field_name='manager__name', lookup_expr='icontains')

    start_date = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='end_date', lookup_expr='lte')

    class Meta:
        model = ApplicationForm
        fields = ['company_name', 'manager_name', 'start_date', 'end_date']

    def filter_by_week(self, queryset, value):
        week_number = int(value)
        return queryset.filter(start_date__week=week_number)

    def filter_by_month(self, queryset, value):
        month_number = int(value)
        return queryset.filter(end_date__month=month_number)



# class ApplicationFilter