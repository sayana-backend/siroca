from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
from .models import ApplicationForm, ApplicationLogs
from datetime import datetime

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


    

@receiver(post_save, sender=ApplicationForm)
def fill_task_number(sender, instance, created, **kwargs):
    if created and not instance.task_number:
        current_date = timezone.now()
        num_applications = ApplicationForm.objects.filter(company=instance.company).count()
        application_count_formatted = str(num_applications).zfill(2)
        month = str(current_date.month).zfill(2)
        year = str(current_date.year)[-2:]
        company_code = instance.company.company_code
        instance.task_number = f"{company_code}-{application_count_formatted}{month}{year}"
        instance.save()