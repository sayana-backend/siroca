from django.db import models
from apps.user.models import CustomUser
from django.contrib.auth.models import Group
from ..user.models import CustomUser



class Checklist(models.Model):
    class Meta:
        verbose_name = 'Подзадача'
        verbose_name_plural = 'Подзадачи'

    text = models.CharField(max_length=255, verbose_name='Текст подзадачи')
    completed = models.BooleanField(default=False)
    application = models.ForeignKey('ApplicationForm', verbose_name='Заявки', on_delete=models.CASCADE, related_name='checklists')
    deadline = models.DateField(verbose_name='Дедлайн', blank=True, null=True)
    manager = models.OneToOneField(CustomUser,
                                   on_delete=models.CASCADE,
                                   verbose_name='Отмеченный менеджер',
                                   blank=True,
                                   null=True,
                                   limit_choices_to={'is_manager': True})

    def __str__(self):
        return self.text


class Comments(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    text = models.TextField(verbose_name='Текст комментария')
    user = models.ForeignKey(CustomUser, related_name='user_comments', on_delete=models.CASCADE, verbose_name='Пользователь')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    application = models.ForeignKey('ApplicationForm', on_delete=models.CASCADE, related_name='comments', verbose_name='Заявка')

    def __str__(self):
        return f"Комментарий от {self.user} по заявке {self.application.title}"


class ApplicationForm(models.Model):
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    STATUS = (
        ('К выполнению', 'К выполнению'),
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

    task_number = models.CharField(max_length=10, verbose_name='Номер заявки', blank=True, null=True)
    title = models.CharField(max_length=100, verbose_name='Название заявки')
    description = models.CharField(null=True, max_length=200, verbose_name='Описание')
    files = models.ImageField(upload_to='', null=True, verbose_name='Файлы')
    jira = models.URLField(null=True, verbose_name='ссылка JIRA')
    status = models.CharField(max_length=100, choices=STATUS, default='К выполнению', verbose_name='Статус заявки')
    payment_state = models.CharField(max_length=100, choices=PAYMENT_STATE, null=True, verbose_name='Статус оплаты')
    priority = models.CharField(max_length=100, choices=PRIORITY, verbose_name='Приоритет заявки')

    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, verbose_name='Компания')
    main_client = models.ForeignKey('user.CustomUser',
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    related_name='client_application',
                                    verbose_name='Заявитель',
                                    limit_choices_to={'is_manager': False})
    main_manager = models.ForeignKey('user.CustomUser',
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     related_name='manager_application',
                                     verbose_name='Менеджер',
                                     limit_choices_to={'is_manager': True})

    application_date = models.DateField(auto_now_add=True, verbose_name='Дата подачи заявки')
    confirm_date = models.DateField(null=True, verbose_name='Дата утверждения заявки')
    offer_date = models.DateField(null=True, verbose_name='Дата отправки КП')
    start_date = models.DateField(null=True, verbose_name='Дата начала')
    finish_date = models.DateField(null=True, verbose_name='Дата окончания')

    objects = models.Manager()

    def __str__(self):
        return f'{self.title}'




class ApplicationLogs(models.Model):
    task_number = models.CharField(max_length=50, null=True, blank=True)
    # username = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, null=True, related_name='user')
    text = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    expiration_time = models.DateTimeField(null=True)
    form = models.ForeignKey(ApplicationForm, on_delete=models.CASCADE, null=True, related_name='logs')

    objects = models.Manager()

    def __str__(self):
        return self.text


