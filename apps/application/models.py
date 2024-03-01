from django.db import models
from django.contrib.auth.models import Group
from ..user.models import CustomUser


class ApplicationForm(models.Model):
    class Meta:
        verbose_name = 'Заявка',
        verbose_name_plural = 'Заявки'
    STATUS = (
        ('Сделать', 'Сделать'),
        ('В работе', 'В работе'),
        ('Тестируется', 'Тестируется'),
        ('Перекрыто', 'Перекрыто'),
        ('На обновлении', 'На обновлении'),
        ('Закрыто', 'Закрыто'),
    )

    PRIORITY = (
        ('Низкий', 'Низкий'),
        ('Средний', 'Средний'),
        ('Высокий', 'Высокий'),
    )

    PAYMENT_STATE = (
        ('Оплачено', 'Оплачено'),
        ('Ожидание оплаты', 'Ожидание оплаты'),
        ('Не оплачено', 'Не оплачено'),
    )

    task_number = models.PositiveIntegerField(verbose_name='Номер заявки', null=True)
    title = models.CharField(max_length=100, verbose_name='Название заявки')
    status = models.CharField(max_length=100, choices=STATUS, null=True, verbose_name='Статус заявки')
    priority = models.CharField(max_length=100, choices=PRIORITY, null=True, verbose_name='Приоритет заявки')
    jira = models.URLField(null=True, verbose_name='ссылка JIRA')
    company = models.ForeignKey('company.Company',  on_delete=models.CASCADE, null=True, verbose_name='Компания')
    username = models.ForeignKey('user.UserProfile', on_delete=models.CASCADE, null=True, verbose_name='Заявитель')
    manager = models.ForeignKey('user.ManagerProfile', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Менеджер')
    application_date = models.DateField(auto_now_add=True, verbose_name='Дата подачи заявки')
    confirm_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата утверждения заявки')
    offer_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата отправки КП')
    payment_state = models.CharField(max_length=100, choices=PAYMENT_STATE, null=True, verbose_name='Статус оплаты')
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата начала')
    finish_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата окончания')
    description = models.CharField(blank=True, null=True, max_length=200, verbose_name='Описание')
    files = models.ImageField(upload_to='', null=True, blank=True, verbose_name='Файлы')
    comments = models.CharField(max_length=200, blank=True, null=True, verbose_name='Комментарии')
    comments_date = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.title}'


class ApplicationLogs(models.Model):
    task_number = models.CharField(max_length=50, null=True, blank=True)
    username = models.ForeignKey('user.UserProfile', on_delete=models.CASCADE, null=True, related_name='user')
    text = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    expiration_time = models.DateTimeField(null=True)
    form = models.ForeignKey(ApplicationForm, on_delete=models.CASCADE, null=True, related_name='logs')

    objects = models.Manager()

    def __str__(self):
        return self.text

