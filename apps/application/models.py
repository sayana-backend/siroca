from django.contrib.auth.models import Group
from ..user.models import CustomUser
from django.db import models


class Checklist(models.Model):
    class Meta:
        verbose_name = 'Подзадача'
        verbose_name_plural = 'Подзадачи'

    text = models.CharField(max_length=255, verbose_name='Текст подзадачи')
    completed = models.BooleanField(default=False)
    application = models.ForeignKey('ApplicationForm', verbose_name='Заявки', on_delete=models.CASCADE,
                                    related_name='checklists')
    deadline = models.DateField(verbose_name='Дедлайн', blank=True, null=True)
    manager = models.ForeignKey(CustomUser,
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
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    application = models.ForeignKey('ApplicationForm', on_delete=models.CASCADE, related_name='comments',
                                    verbose_name='Заявка')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='user_comments',null=True, blank=True)


    
    def __str__(self):
        return self.text


class ApplicationForm(models.Model):
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    STATUS = (
        ('К выполнению', 'К выполнению'),
        ('В работе', 'В работе'),
        ('В тестировании', 'В тестировании'),
        ('Выполнено', 'Выполнено'),
        ('Проверено', 'Проверено'),
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
    title = models.CharField(max_length=100, verbose_name='Название заявки', blank=False, null=True)
    description = models.TextField( verbose_name='Описание', blank=True, null=True)
    short_description = models.CharField(max_length=60, verbose_name='Краткое описание', blank=True, null=True)
    files = models.ImageField(upload_to='', null=True, verbose_name='Файлы', blank=True)
    jira = models.URLField(null=True, verbose_name='ссылка JIRA', blank=True)
    status = models.CharField(max_length=100, choices=STATUS, default='К выполнению',
                              verbose_name='Статус заявки', blank=True, null=True)
    payment_state = models.CharField(max_length=100, choices=PAYMENT_STATE,
                                     verbose_name='Статус оплаты', blank=True, null=True)
    priority = models.CharField(max_length=100, choices=PRIORITY, verbose_name='Приоритет заявки', blank=True,
                                null=True)

    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, verbose_name='Компания', blank=False,
                                null=True)
    main_client = models.ForeignKey('user.CustomUser',
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True,
                                    related_name='client_application',
                                    verbose_name='Заявитель',
                                    limit_choices_to={'is_manager': False})
    main_manager = models.ForeignKey('user.CustomUser',
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     blank=True,
                                     related_name='manager_application',
                                     verbose_name='Менеджер',
                                     limit_choices_to={'is_manager': True})

    application_date = models.DateField(auto_now_add=True, verbose_name='Дата подачи заявки', blank=True)
    confirm_date = models.DateField(null=True, verbose_name='Дата утверждения заявки', blank=True)
    offer_date = models.DateField(null=True, verbose_name='Дата отправки КП', blank=True)
    start_date = models.DateField(null=True, verbose_name='Дата начала', blank=True)
    finish_date = models.DateField(null=True, verbose_name='Дата окончания', blank=True)
    deadline_date = models.DateField(null=True, verbose_name='Срок выполнения', blank=True)

    def __str__(self):
        return f'{self.title}'


class TrackingStatus(models.Model):
    status = models.CharField(max_length=100, null=True, blank=True)
    date_status = models.DateField(auto_now_add=True, null=True, blank=True)
    expiration_time = models.DateTimeField()
    form = models.ForeignKey(ApplicationForm, on_delete=models.CASCADE, null=True, blank=True)


class TrackingPriority(models.Model):
    priority = models.CharField(max_length=100, null=True, blank=True)
    date_priority = models.DateField(auto_now_add=True, null=True, blank=True)
    expiration_time = models.DateTimeField()
    form = models.ForeignKey(ApplicationForm, on_delete=models.CASCADE, null=True, blank=True)


class ApplicationLogs(models.Model):
    username = models.CharField(max_length=100, null=True, blank=True)
    task_number = models.CharField(max_length=50, null=True, blank=True)
    text = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    expiration_time = models.DateTimeField(null=True)
    form = models.ForeignKey(ApplicationForm, on_delete=models.CASCADE, null=True, related_name='logs')

    objects = models.Manager()

    def __str__(self):
        return self.text


class Notification(models.Model):
    task_number = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    text = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    made_change = models.CharField(max_length=70, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False, null=True, blank=True)
    form = models.ForeignKey(ApplicationForm, on_delete=models.CASCADE, null=True, blank=True)
    expiration_time = models.DateTimeField(null=True)
