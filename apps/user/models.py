from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .usermanager import CustomUserManager


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
    is_client = models.BooleanField(default=False, verbose_name="Клиент")

    main_company = models.ForeignKey('company.Company', verbose_name="Компания", related_name='company_users', null=True, on_delete=models.CASCADE)
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
        if self.role_type == 'manager':
            self.is_manager = True
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = verbose_name



# class ClientPermissions(models.Model):
#     logs_view = models.BooleanField(default=False, verbose_name='Просмотр логов')
#     put_comments = models.BooleanField(default=False, verbose_name='Добавление комментариев')
#     delete_comments = models.BooleanField(default=False,  verbose_name='Удаление комментариев')
#     add_checklist = models.BooleanField(default=False,  verbose_name='Добавление чеклиста')
#     get_report = models.BooleanField(default=False,  verbose_name='Получение отчета по своим заявкам')
#
#     class Meta:
#         verbose_name_plural = 'Права пользователей'
#
#
#
# class ManagerPermissions(models.Model):
#     manage_comments = models.BooleanField(default=False, verbose_name='Управлять комментариями')
#     get_all_reports = models.BooleanField(default=False, verbose_name='Получение отчетов по всем своим заявкам')
#
#     class Meta:
#         verbose_name_plural = 'Права менеджеров'




