from .models import ApplicationForm, ApplicationLogs, TrackingStatus, TrackingPriority, Notification
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.signals import post_save, pre_save
from apps.user.models import CustomUser
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
import json


@receiver(pre_save, sender=ApplicationForm)
def track_application_changes(sender, instance, **kwargs):
    if instance.pk is not None:
        obj = sender.objects.get(id=instance.id)
        changes = {}
        for field in instance._meta.fields:
            old_value = getattr(obj, field.name)
            new_value = getattr(instance, field.name)
            if old_value != new_value:
                changes[field] = (old_value, new_value)
        if changes:
            message = ""
            for field, (old_value, new_value) in changes.items():
                message += f"{field.verbose_name} изменено с {old_value} на {new_value}\n "
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


@receiver(post_save, sender=ApplicationForm)
def record_status(sender, instance, *args, **kwargs):
    if instance.pk is not None:
        try:
            old_status = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return
        if old_status != instance.status:
            existing_record = TrackingStatus.objects.filter(form=instance, status=instance.status).exists()
            if not existing_record:
                expiration_time = timezone.now() + timedelta(weeks=13)
                TrackingStatus.objects.create(status=instance.status, form_id=instance.id,
                                              expiration_time=expiration_time)
    expired_messages = TrackingStatus.objects.filter(expiration_time__lt=timezone.now())
    expired_messages.delete()


@receiver(post_save, sender=ApplicationForm)
def record_priority(sender, instance, *args, **kwargs):
    if instance.pk is not None:
        try:
            old_priority = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return
        if old_priority != instance.priority:
            existing_record = TrackingPriority.objects.filter(form=instance, priority=instance.priority).exists()
            if not existing_record:
                expiration_time = timezone.now() + timedelta(weeks=13)
                TrackingPriority.objects.create(priority=instance.priority, form_id=instance.id,
                                                expiration_time=expiration_time)
    expired_messages = TrackingPriority.objects.filter(expiration_time__lt=timezone.now())
    expired_messages.delete()


# @receiver(pre_save, sender=ApplicationForm)
# def track_application_send_notification(sender, instance, **kwargs):
#     if instance.pk is not None:
#         obj = sender.objects.get(id=instance.id)
#         for field in instance._meta.fields:
#             old_value = getattr(obj, field.name)
#             new_value = getattr(instance, field.name)
#             if old_value != new_value:
#                 message = f"{field.verbose_name} изменено с {old_value} на {new_value}"
#                 manager_name = f"{instance.main_manager.first_name} {instance.main_manager.surname}"
#                 Notification.objects.create(task_number=instance.task_number, title=instance.title,
#                                             text=message, made_change=manager_name, form_id=instance.id)

@receiver(pre_save, sender=ApplicationForm)
def track_application_send_notification(sender, instance, **kwargs):
    if instance.pk is not None:
        obj = sender.objects.get(id=instance.id)
        changes = []
        if obj.status != instance.status:
            changes.append(f"Статус изменен с '{obj.get_status_display()}' на '{instance.get_status_display()}'")
        if obj.priority != instance.priority:
            changes.append(f"Приоритет изменен с '{obj.get_priority_display()}' на '{instance.get_priority_display()}'")
        if changes:
            message = ', '.join(changes)
            manager_name = f"{instance.main_manager.first_name} {instance.main_manager.surname}"
            Notification.objects.create(
                task_number=instance.task_number,
                title=instance.title,
                text=message,
                made_change=manager_name,
                form_id=instance.id
            )


@receiver(post_save, sender=ApplicationForm)
def send_notification_on_create_close(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            task_number=f'Номер заявки: {instance.task_number}',
            text=f'Создана новая заявка',
            title=instance.title,
            made_change=f"{instance.main_manager.first_name} {instance.main_manager.surname}",
            form_id=instance.id,
        )

    elif instance.status == 'Закрыто':
        Notification.objects.create(
            task_number=f'Номер заявки: {instance.task_number}',
            text=f"Заявка закрыто",
            title=instance.title,
            made_change=f"{instance.main_manager.first_name} {instance.main_manager.surname}",
            form_id=instance.id,
        )
