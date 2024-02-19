from django.contrib import admin
from .models import Checklist


@admin.register(Checklist)
class ChecklistFormAdmin(admin.ModelAdmin):
    list_display = ['text', 'completed']
    search_fields = ['text']
