from django.db import models
from django.contrib.auth.models import User  

class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название  компании')
    country = models.CharField(max_length=255, verbose_name='Страна')
    manager = models.ForeignKey(
        User,  
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Менеджер компании',
        related_name='managed_companies'
    )
    users = models.ManyToManyField(
        'auth.User',
        verbose_name='Пользователи',
        related_name='companies'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    job_titles = models.ManyToManyField(
        'JobTitle',
        verbose_name='Должности',
        related_name='companies'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    
    def get_users(self):
        return self.users.all()


class JobTitle(models.Model):
    title = models.CharField(max_length=255, verbose_name='Должность')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    @classmethod
    def create_job_title(cls, title):
        job_title = cls.objects.create(title=title)
        return job_title
