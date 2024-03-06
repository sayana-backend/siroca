<<<<<<< HEAD
=======
from django.contrib.auth.models import AbstractUser
>>>>>>> origin/user_register
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .usermanager import CustomUserManager


<<<<<<< HEAD
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
=======
class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Фото')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    phone = models.CharField(max_length=150, blank=True, null=True, verbose_name='Номер телефона')
    job_title = models.ForeignKey('company.JobTitle', on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name='Должность в компании')
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, null=True, verbose_name='Компания')
>>>>>>> origin/user_register

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False, verbose_name="Менеджер")

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
        if self.role_type == 'manager':
            self.is_manager = True
        super().save(*args, **kwargs)


<<<<<<< HEAD
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = verbose_name



=======
class UserProfile(CustomUser):
    groups = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='user_profiles', default=3)
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='user_profiles')

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class ManagerProfile(CustomUser):
    groups = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='manager_profiles', default=2)
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='manager_profiles')

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'


class AdminProfile(CustomUser):
    is_staff = models.BooleanField(default=True)
    groups = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='admin_profiles', default=1)
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='admin_profiles')

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'
>>>>>>> origin/user_register
