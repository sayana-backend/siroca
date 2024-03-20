from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .usermanager import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class Contact(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='contact')
    email = models.EmailField(verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=20, verbose_name='Телефонный номер')
    whatsapp_number = models.CharField(max_length=20, verbose_name='Номер WhatsApp')

    def __str__(self):
        return f"Contact for {self.user.username}"

    class  Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = "Контакты"


class CustomUser(AbstractBaseUser, PermissionsMixin):
    RoleType = {
        'client': 'Клиент',
        'manager': 'Менеджер',
    }
    role_type = models.CharField(max_length=20, choices=RoleType.items(), verbose_name='Тип роли')
    username = models.CharField(max_length=30, verbose_name="Логин", unique=True)
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    surname = models.CharField(max_length=30, verbose_name="фамилия")
    image = models.ImageField(verbose_name="Изображение", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False, verbose_name="Менеджер")
    is_client = models.BooleanField(default=False, verbose_name="Клиент")

    company_relation = models.ForeignKey('company.Company', null=True, blank=True, on_delete=models.SET_NULL,
                                         related_name='users')
    main_company = models.ForeignKey('company.Company', verbose_name="Компания", related_name='company_users', on_delete=models.CASCADE, null=True)
    managers_company = models.ManyToManyField('company.Company', verbose_name="Компании менеджеров", related_name='managers_company', blank=True)
    job_title = models.ForeignKey('company.JobTitle',
                                  verbose_name="Должность",
                                  related_name='user_job_titles',
                                  null=True,
                                  blank=True,
                                  on_delete=models.SET_NULL)

    manager_can_edit = models.BooleanField(default=False, verbose_name='Редактирование комментариев')
    manager_can_get_reports = models.BooleanField(default=False, verbose_name='Отчет по заявкам(Менеджер)')

    client_can_put_comments = models.BooleanField(default=False, verbose_name='Комментарий к заявке')
    client_can_get_reports = models.BooleanField(default=False, verbose_name='Отчет по заявкам(Клиент)')
    client_can_view_logs = models.BooleanField(default=False, verbose_name='Просмотр логов')
    client_can_delete_comments = models.BooleanField(default=False, verbose_name='Удаление комментариев')
    client_can_add_checklist = models.BooleanField(default=False, verbose_name='Добавление чеклиста')


    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.company_relation:
            company_domain = self.company_relation.domain
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








