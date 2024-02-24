from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, ManagerProfile, AdminProfile


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    list_display = ["username", "photo", "first_name", "last_name", "username", "job_title", "company"]
    filter_horizontal = ("user_permissions",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("photo", "first_name", "last_name", "email", "job_title", "company")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("photo", "first_name", "last_name", "username", "company", "job_title",  "password1", "password2"),
            },
        ),
    )


@admin.register(ManagerProfile)
class ManagerProfileAdmin(UserAdmin):
    list_display = ["username", "photo", "first_name", "last_name"]
    filter_horizontal = ("user_permissions",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("photo", "first_name", "last_name", "email", "phone")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("photo", "first_name", "last_name", "username", "email", "phone", "password1", "password2"),
            },
        ),
    )



@admin.register(AdminProfile)
class AdminProfileAdmin(UserAdmin):
    list_display = ["username", "photo", "first_name", "last_name"]
    filter_horizontal = ("user_permissions",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("photo", "first_name", "last_name", "email", "phone")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    search_fields = ["first_name"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("photo", "first_name", "last_name", "username", "email", "phone", "password1", "password2"),
            },
        ),
    )