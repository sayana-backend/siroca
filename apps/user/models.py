from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from .usermanager import CustomUserManager
# from apps.application.models import ApplicationForm
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class CustomUser(AbstractBaseUser, PermissionsMixin):
    RoleType = {
        'client': 'Клиент',
        'manager': 'Менеджер',
    }
    role_type = models.CharField(max_length=20, choices=RoleType.items())
    username = models.CharField(max_length=30, verbose_name="Логин", unique=True)
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    surname = models.CharField(max_length=30, verbose_name="фамилия")
    image = models.ImageField(verbose_name="Изображение", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False, verbose_name="Менеджер")
    is_client = models.BooleanField(default=True, verbose_name="Клиент")

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

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'

    def __str__(self) -> str:
        return f"{self.username}"

    def save(self, *args, **kwargs):
        if not self.username:
            if self.surname and self.name:
                self.username = f"{slugify(self.surname)}{slugify(self.name)}"
            elif self.surname:
                self.username = f"{slugify(self.surname)}"
            elif self.name:
                self.username = f"{slugify(self.name)}"
            else:
                raise ValueError("Surname and name cannot be both empty")

            if self.role_type == 'Клиент':
                self.is_client = True
            elif self.role_type == 'Менеджер':
                self.is_manager = True

            if self.company_relation:
                company_domain = self.company_relation.domain
                self.username += f"@{company_domain}.com"

            super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.role_type == 'manager':
            self.is_manager = True
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = verbose_name


# class Notification(models.Model):
#     task_number = models.CharField(max_length=50,null=True,blank=True)
#     text = models.CharField(max_length=300, null=True, blank=True)
#     created_at = models.DateField(auto_now_add=True, null=True, blank=True)
#     expiration_time = models.DateTimeField(null=True)
#     user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
#     application_id = models.ForeignKey(ApplicationForm, on_delete=models.CASCADE, null=True)



