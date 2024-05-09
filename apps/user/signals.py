from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import CustomUser
from .permissions import UsersPermissions
from django.core.exceptions import PermissionDenied


@receiver(pre_delete, sender=CustomUser)
def prevent_delete_first_user(sender, instance, **kwargs):
    first_user = CustomUser.objects.first()
    if instance.id == first_user.id:
        raise PermissionDenied("Нельзя удалить первого пользователя!")
    

@receiver(post_save, sender=CustomUser)
def set_superuser_for_manager(sender, instance, **kwargs):
    if instance.is_superuser:
        return True
    elif instance.is_manager:
        manager_permissions = [
            instance.manager_can_delete_comments_extra,
            instance.manager_can_get_reports_extra,
            instance.manager_can_delete_application_extra,
            instance.manager_can_create_and_edit_company_extra,
            instance.manager_can_create_and_edit_user_extra,
            instance.manager_can_create_and_delete_job_title_extra
        ]
        if all(manager_permissions):
            CustomUser.objects.filter(id=instance.id).update(is_manager=False, is_superuser=True)


@receiver(post_save, sender=CustomUser)
def remove_superuser_for_manager(sender, instance, **kwargs):
    if not instance.is_superuser:
        return False
    elif instance.is_manager:
        manager_permissions = [
            instance.manager_can_delete_comments_extra,
            instance.manager_can_get_reports_extra,
            instance.manager_can_delete_application_extra,
            instance.manager_can_create_and_edit_company_extra,
            instance.manager_can_create_and_edit_user_extra,
            instance.manager_can_create_and_delete_job_title_extra
        ]
        if not all(manager_permissions):
            CustomUser.objects.filter(id=instance.id).update(is_manager=True, is_superuser=False)

