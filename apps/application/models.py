from django.contrib.auth.models import Group
from ..user.models import CustomUser
from django.db import models
from django.utils import timezone
import datetime
import pytz


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
        ('Самый низкий', 'Самый низкий'),
        ('Низкий', 'Низкий'),
        ('Средний', 'Средний'),
        ('Высокий', 'Высокий'),
        ('Самый высокий', 'Самый высокий'),
    )

    PAYMENT_STATE = (
        ('Оплачено', 'Оплачено'),
        ('Ожидание оплаты', 'Ожидание оплаты'),
        ('Не оплачено', 'Не оплачено'),
    )

    task_number = models.CharField(max_length=10, verbose_name='Номер заявки', blank=True, null=True)
    title = models.CharField(max_length=100, verbose_name='Название заявки', blank=False, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    short_description = models.CharField(max_length=60, verbose_name='Краткое описание', blank=True, null=True)
    jira = models.URLField(null=True, verbose_name='ссылка JIRA', blank=True)
    status = models.CharField(max_length=100, choices=STATUS, default='К выполнению',
                              verbose_name='Статус заявки', blank=True, null=True)
    payment_state = models.CharField(max_length=100, choices=PAYMENT_STATE, default='Ожидание оплаты',
                                     verbose_name='Статус оплаты', blank=True, null=True)
    priority = models.CharField(max_length=100, choices=PRIORITY, verbose_name='Приоритет заявки',
                                blank=True, default='Средний')

    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='company_application', verbose_name='Компания')
    main_client = models.ForeignKey('user.CustomUser',
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True,
                                    related_name='client_application',
                                    verbose_name='Заявитель',
                                    limit_choices_to={'is_client': True})
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
        return self.title


class ApplicationFile(models.Model):
    file = models.FileField(upload_to='', verbose_name='Файл', blank=True)
    application = models.ForeignKey('ApplicationForm',
                                    on_delete=models.CASCADE,
                                    verbose_name='Заяка',
                                    related_name='files')

    def __str__(self):
        return self.file.name


class Checklist(models.Model):
    application = models.ForeignKey('ApplicationForm',
                                    verbose_name='Заявка',
                                    on_delete=models.CASCADE,
                                    related_name='checklists')
    completed = models.BooleanField(default=False)
    name = models.CharField(max_length=100, verbose_name='Название чеклиста')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Чеклист'
        verbose_name_plural = 'Чеклисты'


class SubTask(models.Model):
    checklist = models.ForeignKey('Checklist', verbose_name='Чеклист', on_delete=models.CASCADE,
                                  related_name='subtasks')
    text = models.CharField(max_length=255, verbose_name='Текст подзадачи')
    completed = models.BooleanField(default=False)
    deadline = models.DateField(verbose_name='Дедлайн', blank=True, null=True)
    manager = models.ForeignKey('user.CustomUser', on_delete=models.SET_NULL, verbose_name='Отмеченный менеджер',
                                related_name='sabtasks', blank=True, null=True, limit_choices_to={'is_manager': True})

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Подзадача'
        verbose_name_plural = 'Подзадачи'


class Comments(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    text = models.TextField(verbose_name='Текст комментария')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    application = models.ForeignKey('ApplicationForm', on_delete=models.CASCADE, related_name='comments',
                                    verbose_name='Заявка')
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='user_comments', null=True, blank=True)

    def __str__(self):
        return self.text


class ApplicationLogs(models.Model):
    user = models.CharField(max_length=100, null=True, blank=True, verbose_name="Пользователь")
    field = models.CharField(max_length=500, null=True, blank=True, verbose_name="Название поля")
    initially = models.CharField(max_length=500, null=True, blank=True, verbose_name="Старое значение")
    new = models.CharField(max_length=500, null=True, blank=True, verbose_name="Новое значение")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Дата и время создания")
    file_logs = models.FileField(upload_to='', blank=True, null=True, verbose_name="Файл картинки")
    user_image = models.FileField(upload_to='', blank=True, null=True, verbose_name="Аватар пользователя")

    form = models.ForeignKey(ApplicationForm, on_delete=models.CASCADE, null=True, related_name='logs', verbose_name="Заявка")
    user_id = models.IntegerField(null=True, blank=True, verbose_name="id пользователя")
    check_list_id = models.ForeignKey(Checklist, on_delete=models.CASCADE, null=True, blank=True, verbose_name="id чеклиста")
    objects = models.Manager()

    def __str__(self):
        return self.new


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


class Notification(models.Model):
    task_number = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    text = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    made_change = models.CharField(max_length=70, null=True, blank=True)
    form = models.ForeignKey(ApplicationForm, on_delete=models.CASCADE, null=True, blank=True)

    is_read = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False, null=True, blank=True)
    is_manager_notic = models.BooleanField(default=False, null=True, blank=True)
    is_client_notic = models.BooleanField(default=False, null=True, blank=True)
    admin_id = models.IntegerField(null=True, blank=True)
