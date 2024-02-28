from django.db import models
from apps.user.models import CustomUser


class Checklist(models.Model):
    class Meta:
        verbose_name = 'Подзадача'
        verbose_name_plural = 'Подзадачи'

    text = models.CharField(max_length=255, verbose_name='Текст подзадачи')
    completed = models.BooleanField(default=False)
    application = models.ManyToManyField('ApplicationForm', verbose_name='Заявки', related_name='checklists')
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
    # manager = models.ForeignKey(CustomUser, related_name='manager_comments', on_delete=models.CASCADE, blank=True,null=True, verbose_name='Менеджер')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    application = models.ForeignKey('ApplicationForm', on_delete=models.CASCADE, related_name='comments', verbose_name='Заявка')

    def __str__(self):
        return f"Комментарий от {self.user} по заявке {self.application.title}"


class ApplicationForm(models.Model):
    class Meta:
        verbose_name = 'Заявка'
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
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, null=True, verbose_name='Компания')
    main_client = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, null=True, related_name='client_application',
                                    verbose_name='Заявитель', limit_choices_to={'is_client': True})
    main_manager = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, null=True, blank=True, related_name='manager_application',
                                     verbose_name='Менеджер', limit_choices_to={'is_manager': True})
    application_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата подачи заявки')
    confirm_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата утверждения заявки')
    offer_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата отправки КП')
    payment_state = models.CharField(max_length=100, choices=PAYMENT_STATE, null=True, verbose_name='Статус оплаты')
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата начала')
    finish_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата окончания')
    description = models.CharField(blank=True, null=True, max_length=200, verbose_name='Описание')
    files = models.ImageField(upload_to='', null=True, blank=True, verbose_name='Файлы')
    checklist = models.ManyToManyField(Checklist, verbose_name='Чек-листы', blank=True, related_name='checklists')
    comment = models.ManyToManyField(Comments,  verbose_name='Комментарии', blank=True, related_name='comments')

    def __str__(self):
        return f'{self.title}'
