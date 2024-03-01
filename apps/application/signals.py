from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
from .models import ApplicationForm, ApplicationLogs


@receiver(pre_save, sender=ApplicationForm)
def track_application_changes(sender, instance, **kwargs):
    if instance.pk is not None:
        obj = sender.objects.get(id=instance.id)
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
                message += f"'{field.verbose_name}' изменено с '{old_value}' на '{new_value}'\n "
            expiration_time = timezone.now() + timedelta(days=1)
            ApplicationLogs.objects.create(text=message, expiration_time=expiration_time,
                                           task_number=instance.task_number, form_id=instance.id)
    expired_messages = ApplicationLogs.objects.filter(expiration_time__lt=timezone.now())
    expired_messages.delete()




