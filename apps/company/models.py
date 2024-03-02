from django.db import models
from transliterate import translit
import random


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название  компании')
    company_code = models.CharField(max_length=255, unique=True, verbose_name='Краткий код')
    country = models.CharField(max_length=255, verbose_name='Страна')
    manager = models.ForeignKey(
        'user.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Менеджер компании',
        related_name='managed_companies',
        blank=True,
        limit_choices_to={'is_manager': True}
    )
    users = models.OneToOneField(
        'user.CustomUser',
        verbose_name='Пользователи',
        related_name='companies',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        limit_choices_to={'is_client': True}
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def generate_codes(self, company_name):
        company_name = translit(company_name.replace(' ', ''), 'ru', reversed=True).upper()
        middle_chars = [char for char in company_name[1:-1]]

        codes = set() 
        for _ in range(15):
            middle_char = random.choice(middle_chars)
            code = company_name[0] + middle_char + company_name[-1]
            if not Company.objects.filter(company_code=code).exists():
                codes.add(code)
        return list(codes)
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def get_users(self):
        return self.users.all()
    
    



class JobTitle(models.Model):
    title = models.CharField(max_length=255, verbose_name='Должность')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    

