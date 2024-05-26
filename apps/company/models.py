from django.db import models
from transliterate import translit
import random
from ..user.models import CustomUser
from ..application.models import ApplicationForm


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название  компании', unique=True)
    company_code = models.CharField(max_length=3, unique=True, verbose_name='Краткий код')
    country = models.CharField(max_length=255, verbose_name='Страна')
    domain = models.CharField(max_length=100, unique=True)
    main_manager = models.ForeignKey(
        'user.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Ответственный Менеджер',
        related_name='managed_companies',
        blank=True,
        limit_choices_to={'role_type': 'manager'}
    )

    managers = models.ManyToManyField(
        'user.CustomUser',
        verbose_name='Менеджеры',
        related_name='companies',
        blank=True,
        limit_choices_to={'is_manager': True}
    )

    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    last_updated_at = models.DateField(auto_now=True, verbose_name='Дата последнего редактирования')

    def generate_codes(self, company_name):
        company_name = translit(company_name.replace(' ', ''), 'ru', reversed=True).upper()
        middle_chars = [char for char in company_name[1:-1]]

        middle_char = random.choice(middle_chars)
        code = company_name[0] + middle_char + company_name[-1]
        if not Company.objects.filter(company_code=code).exists():
            return code

    def get_users(self):
        users = CustomUser.objects.filter(main_company=self).values('id', 'first_name', 'surname')
        return list(users)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class JobTitle(models.Model):
    title = models.CharField(max_length=255, verbose_name='Должность')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
