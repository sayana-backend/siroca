from django.contrib import admin
from .models import Checklist, Comments
from .models import ApplicationForm, ApplicationLogs



@admin.register(ApplicationForm)
class ApplicationFormAdmin(admin.ModelAdmin):
    list_display = ['task_number', 'company', 'title',
                    'description', 'main_client', 'main_manager',
                    'start_date', 'finish_date', 'priority',
                    'status']
    search_fields = ['task_number', 'title', 'main_manager',
                     'main_client', 'company']


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ['text','completed']  
    search_fields = ['text']  


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['text', 'user', 'application']  
    search_fields = ['text', 'user', 'application', 'date_added']
    # search_fields = ['task_number', 'title', 'manager',
    #                  'username', 'company']

# admin.site.register(ApplicationLogs)

