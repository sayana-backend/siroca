from django.db import models
# from apps.user.models import CustomUser

class JobTitle(models.Model):
    title = models.CharField(max_length=255, verbose_name='Должность')
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name='jobtitles',
        verbose_name='Компания'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

 # Импортируем CustomUser из вашего приложения users


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название компании')
    country = models.CharField(max_length=255, verbose_name='Страна')
    manager = models.ForeignKey('apps.CustomUser', 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Менеджер компании',
        related_name='managed_companies',
        limit_choices_to={'is_manager': True}
    )
    users = models.ManyToManyField('apps.CustomUser',
        blank=True,
        verbose_name='Пользователи',
        related_name='companies',
        limit_choices_to={'is_client': True}
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    jobtitle = models.ManyToManyField('JobTitle', verbose_name='Должности', blank=True, related_name='jobtitles')
    domain = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name