from django.contrib import admin
from .models import Company, JobTitle

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'created_at']  
    search_fields = ['name']  

@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ['title']  
    search_fields = ['title']  
