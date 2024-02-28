from django.contrib import admin
from .models import ApplicationForm,Checklist,Comments


@admin.register(ApplicationForm)
class ApplicationFormAdmin(admin.ModelAdmin):
    list_display = ['task_number', 'company', 'title',
                    'description', 'username', 'manager',
                    'start_date', 'finish_date', 'priority',
                    'status']
    search_fields = ['task_number', 'title', 'manager',
                     'username', 'company']


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ['text','completed']  
    search_fields = ['text']  

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['text', 'user', 'application']  
    search_fields = ['text', 'user','manager', 'application', 'date_added']
