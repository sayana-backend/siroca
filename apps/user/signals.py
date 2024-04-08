from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import CustomUser
from .permissions import *




# def jls_extract_def():
#     return


# @receiver(post_save, sender=CustomUser)
# def update_username(sender, instance, created, **kwargs):
#     if created:
#         username = instance.surname.lower() + instance.first_name.lower()
#         company_domain = instance.main_company.domain = jls_extract_def()
#         full_username = f"{username}@{company_domain}.com"
#         instance.username = full_username
#         instance.save()


@receiver(post_save, sender=CustomUser)
def set_manager_permissions(sender, instance, created, **kwargs):
    if created and instance.role_type == 'manager':
        instance.refresh_from_db()
        manager_permissions = {
            "manager_can_delete_comments": instance.manager_can_delete_comments,
            "manager_can_get_reports": instance.manager_can_get_reports,
            "manager_can_view_profiles": instance.manager_can_view_profiles,
            "manager_can_delete_application": instance.manager_can_delete_application
        }
        instance.manager_can_delete_comments = manager_permissions['manager_can_delete_comments']
        instance.manager_can_get_reports = manager_permissions['manager_can_get_reports']
        instance.manager_can_view_profiles = manager_permissions['manager_can_view_profiles']
        instance.manager_can_delete_application = manager_permissions['manager_can_delete_application']
        instance.save()
        print(manager_permissions)

