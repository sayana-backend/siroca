
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Permission, Group


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Фото')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    phone = models.CharField(max_length=150, blank=True, null=True, verbose_name='Номер телефона')
    job_title = models.ForeignKey('company.JobTitle', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Должность в компании')
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, null=True, verbose_name='Компания')

    USERNAME_FIELD = 'username'

    class Meta:
        abstract = True


class ExampleSuperUser(AbstractUser):
    pass


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




