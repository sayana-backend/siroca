from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .usermanager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    RoleType = {
        'Клиент': 'Клиент',
        'Менеджер': 'Менеджер',
    }
    image = models.ImageField()
    name = models.CharField(max_length=30)
    role_type = models.CharField(max_length=20, choices=RoleType.items())
    username = models.CharField(max_length=30, verbose_name="Имя", unique=True)
    surname = models.CharField(max_length=30, verbose_name="Фамилия", null=True, blank=True)
    password = models.CharField("password", max_length=128)
    job_title = models.CharField(max_length=30)
    company = models.CharField(max_length=30)
    created_at = models.DateField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False, verbose_name="Менеджер")

    # manager = models.ForeignKey('self',
    #                             on_delete=models.SET_NULL,
    #                             blank=True,
    #                             null=True,
    #                             related_name='Clients',
    #                             limit_choices_to={'is_manager': True})

    objects = CustomUserManager()

    def str(self) -> str:
        return f"{self.username}"


    def save(self, *args, **kwargs):
        if self.role_type == 'Менеджер':
            self.is_manager = True
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = verbose_name


    USERNAME_FIELD = 'username'


