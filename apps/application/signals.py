from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
from .models import ApplicationForm, ApplicationLogs


@receiver(pre_save, sender=ApplicationForm)
def track_application_changes(sender, instance, **kwargs):
    if instance.pk is not None:
        obj = ApplicationForm.objects.get(pk=instance.pk)
        changes = {}
        queryset = ApplicationForm.objects.all().iterator()
        for obj in queryset:
            if obj.task_number != instance.task_number:
                changes['task_number'] = (obj.task_number, instance.task_number)
            if obj.title != instance.title:
                changes['title'] = (obj.title, instance.title)
            if obj.company != instance.company:
                changes['company'] = (obj.company, instance.company)
            if obj.status != instance.status:
                changes['status'] = (obj.status, instance.status)
            if obj.priority != instance.priority:
                changes['priority'] = (obj.priority, instance.priority)
            if obj.jira != instance.jira:
                changes['jira'] = (obj.jira, instance.jira)
            if obj.username != instance.username:
                changes['username'] = (obj.username, instance.username)
            if obj.manager != instance.manager:
                changes['manager'] = (obj.manager, instance.manager)
            if obj.confirm_date != instance.confirm_date:
                changes['confirm_date'] = (obj.confirm_date, instance.confirm_date)
            if obj.offer_date != instance.offer_date:
                changes['offer_date'] = (obj.offer_date, instance.offer_date)
            if obj.payment_state != instance.payment_state:
                changes['payment_state'] = (obj.payment_state, instance.payment_state)
            if obj.start_date != instance.start_date:
                changes['start_date'] = (obj.start_date, instance.start_date)
            if obj.finish_date != instance.finish_date:
                changes['finish_date'] = (obj.finish_date, instance.finish_date)
            if obj.description != instance.description:
                changes['description'] = (obj.description, instance.description)
            if obj.files != instance.files:
                changes['files'] = (obj.files, instance.files)
            if obj.comments != instance.comments:
                changes['comments'] = (obj.comments, instance.comments)
        if changes:
            message = ""
            changed_app_name = ""
            for field, (old_value, new_value) in changes.items():
                message += f"'{field}' changed from '{old_value}' to '{new_value}'. "
                if field == 'task_number':
                    changed_app_name = new_value
            expiration_time = timezone.now() + timedelta(days=7)
            ApplicationLogs.objects.create(text=message, expiration_time=expiration_time,
                                           changed_app_name=instance.task_number)
    expired_messages = ApplicationLogs.objects.filter(expiration_time__lt=timezone.now())
    expired_messages.delete()

# @receiver(post_save, sender=ApplicationForm):
# def handle_model_save(sender, instance, created, **kwargs):
#     data = {'id': instance.id, 'task_number': instance.task_number,
#             'title': instance.title, 'company': instance.company,}
#     requests.post()




