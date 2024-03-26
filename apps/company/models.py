from django.db import models
from transliterate import translit
import random
from ..user.models import CustomUser



class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название  компании', unique=True)
    company_code = models.CharField(max_length=255, unique=True, verbose_name='Краткий код')
    country = models.CharField(max_length=255, verbose_name='Страна')
    domain = models.CharField(max_length=100, unique=True)
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
        null=True,
        blank=True,
        limit_choices_to={'is_manager': True}
    )

    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')

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
    
    def get_count_users(self):
        count_users = CustomUser.objects.filter(main_company=self).count()
        return count_users
    
    def get_users(self):
        users = CustomUser.objects.filter(main_company=self)
        user_names = [user.first_name for user in users]
        return user_names
    


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
