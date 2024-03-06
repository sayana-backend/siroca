from django.db.models.signals import post_save, pre_save

from django.dispatch import receiver
from datetime import timedelta
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from requests import post
from django.utils import timezone
from .models import ApplicationForm, ApplicationLogs, TrackingStatus, TrackingPriority


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
# def notification_applications(sender, instance, **kwargs):
#     if instance.pk is not None:
#         obj = sender.objects.get(id=instance.id)
#         changes = {}
#         # data = ApplicationForm.objects.all()
#         for field in instance._meta.fields:
#             old_value = getattr(obj, field.name)
#             new_value = getattr(instance, field.name)
#             if old_value != new_value:
#                 changes[field] = (old_value, new_value)
#         if changes:
#             message = ""
#             for field, (old_value, new_value) in changes.items():
#                 message += f"'{field.verbose_name}' изменено с '{old_value}' на '{new_value}'\n "
#                 ApplicationLogs.objects.create(text=message, expiration_time=expiration_time,
#                                                task_number=instance.task_number, form_id=instance.id)
#     expired_messages = ApplicationLogs.objects.filter(expiration_time__lt=timezone.now())
#     expired_messages.delete()
#
#             user = instance.user
#
#             channel_layer = get_channel_layer()
#             async_to_sync(channel_layer.send)(
#                 user.websocket_channel_name,
#                 {
#                     'type': 'send_notification',
#                     'message': message
#                 }
#             )
