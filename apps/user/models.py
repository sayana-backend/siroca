from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .usermanager import CustomUserManager
# from apps.application.models import ApplicationForm


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


    main_company = models.ForeignKey('company.Company', verbose_name="Компания", related_name='company_users', on_delete=models.CASCADE, null=True)
    managers_company = models.ManyToManyField('company.Company', verbose_name="Компании менеджеров", related_name='managers_company', blank=True)
    job_title = models.ForeignKey('company.JobTitle',
                                  verbose_name="Должность",
                                  related_name='user_job_titles',
                                  null=True,
                                  blank=True,
                                  on_delete=models.SET_NULL)

    manager_can_delete_comments = models.BooleanField(default=False, verbose_name='Удаление комментариев')
    manager_can_get_reports = models.BooleanField(default=False, verbose_name='Отчет по заявкам(Менеджер)')
    manager_can_view_profiles = models.BooleanField(default=False, verbose_name='Просмотр профиля пользователей(Менеджер)')
    manager_can_delete_application = models.BooleanField(default=False, verbose_name='Удаление заявки')


    client_can_edit_comments = models.BooleanField(default=False, verbose_name='Добавление/удаление комментария')
    client_can_get_reports = models.BooleanField(default=False, verbose_name='Отчет по заявкам(Клиент)')
    client_can_view_logs = models.BooleanField(default=False, verbose_name='Просмотр логов')
    client_can_add_checklist = models.BooleanField(default=False, verbose_name='Добавление чеклиста')
    client_can_add_files = models.BooleanField(default=False, verbose_name='Добавление файла')
    client_can_view_profiles = models.BooleanField(default=False, verbose_name='Просмотр профиля пользователей(Клиент)')


    objects = CustomUserManager()
    USERNAME_FIELD = 'username'

    def __str__(self) -> str:
        return f"{self.username}"

    def save(self, *args, **kwargs):
        if self.role_type == 'manager':
            self.is_manager = True
        else:
            self.role_type == 'client'
            self.is_client = True
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

