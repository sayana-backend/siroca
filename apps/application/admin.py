from django.contrib import admin
from .models import Checklist, Comments, ApplicationFile
from .models import ApplicationForm, ApplicationLogs, SubTask, Checklist



@admin.register(ApplicationForm)
class ApplicationFormAdmin(admin.ModelAdmin):
    list_display = ['task_number', 'company', 'title',
                    'description', 'main_client', 'main_manager',
                    'start_date', 'finish_date', 'priority',
                    'status']
    search_fields = ['task_number', 'title', 'main_manager',
                     'main_client', 'company']
    # fields = ['title', 'main_client', 'main_manager', 'company']
    # fields = ['task_number', 'company', 'title',
    #           'description', 'main_client', 'main_manager',
    #           'start_date', 'finish_date', 'priority',
    #           'status']


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['text',  'application']
    search_fields = ['text',  'application', 'date_added']
    


admin.site.register(ApplicationLogs)
admin.site.register(Checklist)
admin.site.register(SubTask)
# admin.site.register(Comments)
admin.site.register(ApplicationFile)


