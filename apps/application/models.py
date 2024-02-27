from django.db import models
from apps.user.models import ManagerProfile
# from apps.application.models import Checklist
# from apps.application.models import ApplicationForm



class Checklist(models.Model):

    class Meta:
        verbose_name = 'Подзадача'
        verbose_name_plural = 'Подзадач'

    text = models.CharField(max_length=255, verbose_name='Текст подзадачи')
    completed = models.BooleanField(default=False)
    application = models.ManyToManyField('application.ApplicationForm',  verbose_name='Заявки', related_name='checklists')    
    deadline = models.DateField(verbose_name='Дедлайн', blank=True, null=True)
    manager = models.OneToOneField(ManagerProfile, on_delete=models.CASCADE, verbose_name='Отмеченный менеджер', blank=True, null=True)

    def __str__(self):
        return self.text

    


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
    application_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата подачи заявки')
    confirm_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата утверждения заявки')
    offer_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата отправки КП')
    payment_state = models.CharField(max_length=100, choices=PAYMENT_STATE, null=True, verbose_name='Статус оплаты')
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата начала')
    finish_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата окончания')
    description = models.CharField(blank=True, null=True, max_length=200, verbose_name='Описание')
    files = models.ImageField(upload_to='', null=True, blank=True, verbose_name='Файлы')
    comments = models.CharField(max_length=200, blank=True, null=True, verbose_name='Комментарии')
    comments_date = models.DateTimeField(auto_now_add=True)
    checklist = models.ForeignKey('application.Checklist',on_delete=models.CASCADE, max_length=500, verbose_name='Чек-листы', blank=True, related_name='checklists')
    # check_list = models.CharField(max_length=100, null=True)
    # logs = models.OneToOneField('ApplicationLogs', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'



# class ApplicationLogs(models.Model):
#     username = models.ForeignKey('user.UserProfile', on_delete=models.CASCADE, null=True, verbose_name='Заявитель')
#     changed_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
#     description = models.CharField(max_length=200, verbose_name='Описание')
#
#     def __str__(self):
#         return f'{self.username} {self.description} {self.changed_date}'


    