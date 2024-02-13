from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email адрес')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    is_staff = models.BooleanField(default=False, verbose_name='Администратор')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        swappable = 'AUTH_USER_MODEL'
        app_label = 'auth'


class UserGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def add_user(self, user):
        user.groups.add(self)

    def remove_user(self, user):
        user.groups.remove(self)

    def get_users(self):
        return self.user_set.all()

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        app_label = 'auth'


class UserPermission(models.Model):
    name = models.CharField(max_length=100, unique=True)

    code = models.CharField(max_length=50, unique=True)

    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def assign_to_group(self, group):
        group.permissions.add(self)

    def remove_from_group(self, group):
        group.permissions.remove(self)

    def is_assigned_to_group(self, group):
        return self in group.permissions.all()

    class Meta:
        verbose_name = 'Разрешение'
        verbose_name_plural = 'Разрешения'
        app_label = 'auth'
