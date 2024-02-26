from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
from .models import ApplicationForm, ApplicationLogs


@receiver(pre_save, sender=ApplicationForm)
def track_application_changes(sender, instance, **kwargs):
    if instance.pk is not None:
        obj = sender.objects.get(pk=instance.pk)
        changes = {}
        # data = ApplicationForm.objects.all()
        for field in instance._meta.fields:
            old_value = getattr(obj, field.name)
            new_value = getattr(instance, field.name)
            if old_value != new_value:
                changes[field] = (old_value, new_value)
        if changes:
            message = ""
            for field, (old_value, new_value) in changes.items():
                message += f"'{field.name}' changed from '{old_value}' to '{new_value}'. "
            expiration_time = timezone.now() + timedelta(days=1)
            ApplicationLogs.objects.create(text=message, expiration_time=expiration_time,
                                           changed_app_name=instance.task_number)
    expired_messages = ApplicationLogs.objects.filter(expiration_time__lt=timezone.now())
    expired_messages.delete()




