from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, ManagerProfile, AdminProfile



@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    model = UserProfile

    list_display=["first_name", "last_name","username","job_title", "company"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
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
                "fields": ("first_name", "last_name","username", "password1", "password2", "job_title", "company"),
            },
        ),
    )





@admin.register(ManagerProfile)
class ManagerProfileAdmin(UserAdmin):
    model = ManagerProfile

    list_display=["first_name", "last_name","username"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
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
                "fields": ("first_name", "last_name","username", "password1", "password2"),
            },
        ),
    )


@admin.register(AdminProfile)
class ProfileAdmin(UserAdmin):
    model = AdminProfile

    list_display=["first_name", "last_name","username"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
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
                "fields": ("first_name", "last_name","username", "password1", "password2"),
            },
        ),
    )