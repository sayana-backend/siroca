from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .usermanager import CustomUserManager


class AdminContact(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='contact')
    email = models.EmailField(verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=20, verbose_name='Телефонный номер')
    whatsapp_number = models.CharField(max_length=20, verbose_name='Номер WhatsApp')

    def __str__(self):
        return f"Контакт для админа {self.user}"

    class Meta:
        verbose_name = 'Контакт для админа'
        verbose_name_plural = "Контакты для админа"


class CustomUser(AbstractBaseUser, PermissionsMixin):
    RoleType = {
        'client': 'Клиент',
        'manager': 'Менеджер',
    }
    role_type = models.CharField(max_length=20, choices=RoleType.items(), verbose_name='Тип роли')
    username = models.CharField(max_length=30, verbose_name="Логин", unique=True)
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    surname = models.CharField(max_length=30, verbose_name="Фамилия")
    image = models.FileField(verbose_name="Изображение", upload_to='', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False, verbose_name="Менеджер")
    is_client = models.BooleanField(default=False, verbose_name="Клиент")

    main_company = models.ForeignKey('company.Company', verbose_name="Компания", related_name='company_users',
                                     on_delete=models.CASCADE, default=1)
    managers_company = models.ManyToManyField('company.Company', verbose_name="Компании менеджеров",
                                              related_name='managers_company', blank=True)
    job_title = models.ForeignKey('company.JobTitle',
                                  verbose_name="Должность",
                                  null=True,
                                  related_name='user_job_titles',
                                  on_delete=models.SET_NULL)

    manager_can_delete_comments = models.BooleanField(default=False, verbose_name='Удаление комментариев')
    manager_can_delete_comments_extra = models.BooleanField(null=True, verbose_name='Удаление комментариев')
    manager_can_get_reports = models.BooleanField(default=False, verbose_name='Отчет по заявкам(Менеджер)')
    manager_can_get_reports_extra = models.BooleanField(null=True, verbose_name='Отчет по заявкам(Менеджер)')
    manager_can_view_profiles = models.BooleanField(default=False, verbose_name='Просмотр профиля пользователей(Менеджер)')
    manager_can_view_profiles_extra = models.BooleanField(null=True, verbose_name='Просмотр профиля пользователей(Менеджер)')
    manager_can_delete_application = models.BooleanField(default=False, verbose_name='Удаление заявки')
    manager_can_delete_application_extra = models.BooleanField(null=True, verbose_name='Удаление заявки')
    manager_can_create_and_edit_company_extra = models.BooleanField(null=True, verbose_name='Создание/Редактирование заявки')
    manager_can_create_and_edit_user_extra = models.BooleanField(null=True, verbose_name='Создание/Редактирование пользователя')
    manager_can_create_and_delete_job_title_extra = models.BooleanField(null=True,
                                                                  verbose_name='Просмотр списка по компаниям/пользователям/должностям')
    client_can_edit_comments = models.BooleanField(default=False, verbose_name='Добавление/удаление комментария')
    client_can_edit_comments_extra = models.BooleanField(null=True, verbose_name='Добавление/удаление комментария')
    client_can_get_reports = models.BooleanField(default=False, verbose_name='Отчет по заявкам(Клиент)')
    client_can_get_reports_extra = models.BooleanField(null=True, verbose_name='Отчет по заявкам(Клиент)')
    client_can_view_logs = models.BooleanField(default=False, verbose_name='Просмотр логов')
    client_can_view_logs_extra = models.BooleanField(null=True, verbose_name='Просмотр логов')
    client_can_add_checklist = models.BooleanField(default=False, verbose_name='Добавление чеклиста')
    client_can_add_checklist_extra = models.BooleanField(null=True, verbose_name='Добавление чеклиста')
    client_can_add_files = models.BooleanField(default=False, verbose_name='Добавление файла')
    client_can_add_files_extra = models.BooleanField(default=False, verbose_name='Добавление файла')
    client_can_view_profiles = models.BooleanField(default=False, verbose_name='Просмотр профиля пользователей(Клиент)')
    client_can_view_profiles_extra = models.BooleanField(default=False, verbose_name='Просмотр профиля пользователей(Клиент)')
    client_can_create_application_extra = models.BooleanField(default=False, verbose_name='Создание заявки')
    client_can_edit_application_extra = models.BooleanField(default=False, verbose_name='Редактирование заявки')



    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.main_company:
            company_domain = self.main_company.domain
            if not self.username.endswith(f"@{company_domain}.com"):
                self.username += f"@{company_domain}.com"

        if self.role_type == 'client':
            self.is_client = True
        elif self.role_type == 'manager':
            self.is_manager = True

        super().save(*args, **kwargs)


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    USERNAME_FIELD = 'username'



