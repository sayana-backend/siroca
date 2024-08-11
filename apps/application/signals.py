from .models import (ApplicationForm, ApplicationLogs, TrackingStatus,
                     TrackingPriority, Notification, Checklist)
from django.db.models.signals import post_save, pre_save
from apps.user.models import CustomUser
from apps.company.models import Company
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta


class NotificationService:
    TEXT_CHOICE = (
        ("create", "создал(а) заявку"),  #есть
        ("delete", "удалил(а) заявку"), #есть
        ("close", "закрыл(а) заявку"),  #есть
        ("checklist", "добавил(а) чек-лист"),  #есть
        ("status", "изменил(а) статус"),  #есть
        ("priority", "изменил(а) приоритет"),  #есть
        ("manager", "назначил(а) Вас менеджером по заявке")  #есть
    )

    @staticmethod
    def get_text_for_action(action):
        for choice in NotificationService.TEXT_CHOICE:
            if choice[0] == action:
                return choice[1]
        return None

    def notification_read(self, instances, user):
        for instance in instances:
            try:
                notic = Notification.objects.get(id=instance['id'])
                notic.readed.add(user)
                notic.save()
                print(f"User {user} added to readed for notification {notic.id}")
            except Notification.DoesNotExist:
                print(f"Notification with id {instance['id']} does not exist.")

    def create_notification(self, application, action):
        user = self.request.user
        text = self.get_text_for_action(action)
        managers = CustomUser.objects.filter(companies__company_application=application)
        # print("КОМПАНИЯ", application.company)
        # print("ОТВЕТСТВЕННЫЙ МЕНЕДЖЕР", application.company.main_manager)
        # print("МЕНЕДЖЕРЫ КОМПАНИИ", managers)
        # print("ПОЛЬЗОВТЕЛИ КОМПАНИИ", application.company.get_users())
        users = []
        if action in ['create', 'delete', 'close']:
            for admin in CustomUser.objects.filter(is_superuser=True):
                users.append(admin)
        main_manager = application.company.main_manager
        if main_manager:
            users.append(CustomUser.objects.get(username=main_manager))
        company_users = application.company.get_users()
        if company_users:
            for c_user in company_users:
                users.append(CustomUser.objects.get(id=c_user.get("id")))
        if managers:
            for i in managers:
                users.append(i)
        # print('====================================================')
        # print(users)
        users = set(users)
        # print(users)
        if text:
            notification = Notification.objects.create(
                task_number=application.task_number,
                text=text,
                title=application.title,
                made_change=user.full_name,
                form_id=application.id
            )
            notification.users.set(users)
            notification.save()

        else:
            raise ValueError(f"Action '{action}' not recognized.")


class BaseLoggingCreateDestroy:
    def log_application_create(self, instance):
        user = self.request.user
        user_id = user.id
        user_name = f"{user.first_name} {user.surname}"
        user_image = user.image
        ApplicationLogs.objects.create(
            user=user_name, user_id=user_id, user_image=user_image,
            field=f'Создал заявку "{instance.task_number}"', form=instance)

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

