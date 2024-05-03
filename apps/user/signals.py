from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import CustomUser
from django.core.exceptions import PermissionDenied


@receiver(pre_delete, sender=CustomUser)
def prevent_delete_first_user(sender, instance, **kwargs):
    first_user = CustomUser.objects.first()
    if instance.id == first_user.id:
        raise PermissionDenied("Нельзя удалить первого пользователя!")

