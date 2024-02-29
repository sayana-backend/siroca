from django.contrib import admin
from .models import ApplicationForm, ApplicationLogs


@admin.register(ApplicationForm)
class ApplicationFormAdmin(admin.ModelAdmin):
    list_display = ['task_number', 'company', 'title',
                    'description', 'username', 'manager',
                    'start_date', 'finish_date', 'priority',
                    'status']
    search_fields = ['task_number', 'title', 'manager',
                     'username', 'company']

admin.site.register(ApplicationLogs)