from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .usermanager import CustomUserManager
from .permissions import UsersPermissions


class CustomUser(AbstractBaseUser, PermissionsMixin, UsersPermissions):
    RoleType = {
        'client': 'Клиент',
        'manager': 'Менеджер',
    }
    role_type = models.CharField(max_length=20, choices=RoleType.items(), default="", verbose_name='Тип роли')
    username = models.CharField(max_length=100, verbose_name="Логин", unique=True)
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    surname = models.CharField(max_length=30, verbose_name="Фамилия")
    full_name = models.CharField(max_length=61, verbose_name="Полное имя")
    image = models.FileField(verbose_name="Изображение", upload_to='', null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False, verbose_name="Менеджер")
    is_client = models.BooleanField(default=False, verbose_name="Клиент")

    main_company = models.ForeignKey('company.Company', verbose_name="Компания", related_name='company_users',
                                     on_delete=models.CASCADE, default=1)
    managers_company = models.ManyToManyField('company.Company', verbose_name="Компании менеджеров",
                                              related_name='managers_company')
    job_title = models.ForeignKey('company.JobTitle',
                                  verbose_name="Должность",
                                  null=True,
                                  related_name='user_job_titles',
                                  on_delete=models.SET_NULL)

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.surname}"

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

    USERNAME_FIELD = "username"


class AdminContact(models.Model):
    email = models.EmailField(verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=20, verbose_name='Телефонный номер')
    whatsapp_number = models.CharField(max_length=20, verbose_name='Номер WhatsApp')

    def __str__(self):
        return f"Контакт для админа"

    class Meta:
        verbose_name = 'Контакт для админа'
        verbose_name_plural = "Контакты для админа"
