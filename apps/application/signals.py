from .models import (ApplicationForm, ApplicationLogs, TrackingStatus,
                     TrackingPriority, Notification, Checklist)
from django.db.models.signals import post_save, pre_save
from apps.user.models import CustomUser
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta


class BaseLoggingCreateDestroy:
    def log_create(self, serializer, log_field_name, new_value):
        instance = serializer.save()
        user = self.request.user
        user_id = user.id
        user_name = f"{user.first_name} {user.surname}"
        user_image = user.image
        ApplicationLogs.objects.create(
            user=user_name, field=log_field_name, new=new_value,
            form=instance.application, user_id=user_id, user_image=user_image)

    def log_destroy(self, instance, log_field_name, delete_value):
        user = self.request.user
        user_id = user.id
        user_name = f"{user.first_name} {user.surname}"
        user_image = user.image
        ApplicationLogs.objects.create(
            user=user_name, field=log_field_name, new=delete_value,
            form=instance.application, user_id=user_id, user_image=user_image)
        instance.delete()


class BaseLoggingUpdate:
    def log_changes(self, old_instance, new_instance):
        user = self.request.user
        user_id = user.id
        user_name = f"{user.first_name} {user.surname}"
        user_image = user.image
        for field in new_instance._meta.fields:
            old_value = getattr(old_instance, field.name)
            new_value = getattr(new_instance, field.name)
            if old_value != new_value:
                ApplicationLogs.objects.create(field=field.verbose_name,
                                               initially=old_value, new=new_value,
                                               form=new_instance.application,
                                               user=user_name, user_id=user_id, user_image=user_image)


# @receiver(post_save, sender=Checklist)
# def update_subtasks_on_checklist_completion(sender, instance, **kwargs):
#     if instance.completed:
#         instance.subtasks.update(completed=True)

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

