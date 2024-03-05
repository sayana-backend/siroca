from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# @@admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {"fields": ("username", "password")}),
#         (("Personal info"), {"fields": ("first_name", "last_name", "email")}),
#         (
#             ("Permissions"),
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     "groups",
#                     "user_permissions",
#                 ),
#             },
#         ),
#         (("Important dates"), {"fields": ("last_login", "date_joined")}),
#     )
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("username", "password1", "password2"),
#             },
#         ),
#     )


@admin.register(CustomUser)
class AdminUser(admin.ModelAdmin):
    list_display = ['username', 'role_type', 'is_manager', 'is_client', 'manager_can_edit',
                    'manager_can_get_reports', 'client_can_put_comments',
                    'client_can_get_reports', 'client_can_view_logs',
                    'client_can_delete_comments', 'client_can_add_checklist']
    list_filter = ['role_type']


# class ClientPermissionsAdmin(admin.ModelAdmin):
#     def has_add_permission(self, request):
#         if ClientPermissions.objects.exists():
#             return False
#         return True
#     list_display = ('logs_view', 'put_comments', 'delete_comments', 'add_checklist', 'get_report')
#
# admin.site.register(ClientPermissions, ClientPermissionsAdmin)
#
#
# class ManagerPermissionsAdmin(admin.ModelAdmin):
#     def has_add_permission(self, request):
#         if ManagerPermissions.objects.exists():
#             return False
#         return True
#     list_display = ('manage_comments', 'get_all_reports')
#
# admin.site.register(ManagerPermissions, ManagerPermissionsAdmin)