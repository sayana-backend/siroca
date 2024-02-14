from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import Permission, Group


class UserProfile(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
        verbose_name='Логин'
    )
    password = models.CharField(max_length=128, verbose_name='Пароль')
    job_title = models.ForeignKey('company.JobTitle', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Должность в компании')
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, null=True, verbose_name='Компания')
    groups = models.ManyToManyField(Group, related_name='user_profiles_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_profiles_permissions')


    def __str__(self):
        return self.first_name
    
    class Meta:
        verbose_name='Клиент'
        verbose_name_plural='Клиенты'




class ManagerProfile(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
        verbose_name='Логин'
    )
    password = models.CharField(max_length=128, verbose_name='Пароль')
    groups = models.ManyToManyField(Group, related_name='manager_profiles_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='manager_profiles_permissions')
    

    def __str__(self):
        return self.first_name
    
    class Meta:
        verbose_name='Менеджер'
        verbose_name_plural='Менеджеры'






class AdminProfileManager(UserManager):
    def create_admin(self, username, password=None, **extra_fields):

        return self.create_superuser(username, password, **extra_fields)

class AdminProfile(AbstractUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
        verbose_name='Логин'
    )
    password = models.CharField(max_length=128, verbose_name='Пароль')
    groups = models.ManyToManyField(Group, related_name='admin_profiles_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='admin_profiles_permissions')

    objects = AdminProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name
    
    class Meta:
        verbose_name='Администратор'
        verbose_name_plural='Администраторы'