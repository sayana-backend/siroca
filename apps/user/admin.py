from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser,Contact


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


admin.site.register(CustomUser)
admin.site.register(Contact)
