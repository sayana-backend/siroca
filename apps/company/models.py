import random

from django.db import models
from transliterate import translit



class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название  компании')
    country = models.CharField(max_length=255, verbose_name='Страна')
    # code =
    # domen =
    main_manager = models.ForeignKey(
        'user.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Менеджер компании',
        related_name='managed_companies',
        blank=True,
        limit_choices_to={'role_type': 'manager'}
    )
    managers = models.ManyToManyField(
        'user.CustomUser',
        verbose_name='Пользователи',
        related_name='companies',
        blank=True,
        limit_choices_to={'is_manager': True}
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def get_users(self):
        return self.company_users.all()


class JobTitle(models.Model):
    title = models.CharField(max_length=255, verbose_name='Должность')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    
