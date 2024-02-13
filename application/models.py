from django.db import models


class ApplicationForm(models.Model):
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

    STATE = (
        ('Оплачено', 'Оплачено'),
        ('Ожидание оплаты', 'Ожидание оплаты'),
        ('Не оплачено', 'Не оплачено'),
    )

    task_number = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS, null=True)
    priority = models.CharField(max_length=100, choices=PRIORITY, null=True)
    jira = models.URLField(null=True)
    company = models.ForeignKey()
    username = models.ForeignKey()
    manager = models.ForeignKey()
    application_date = models.DateTimeField(auto_now_add=True)
    confirm_date = models.PositiveIntegerField(null=True)
    offer_date = models.PositiveIntegerField(null=True)
    payment_state = models.CharField(max_length=100, choices=STATE, null=True)
    start_date = models.PositiveIntegerField(null=True)
    finish_date = models.PositiveIntegerField(null=True)
    description = models.CharField(blank=True, null=True, max_length=200)
    files = models.ImageField(upload_to='', null=True)
    comments = models.CharField(max_length=200, blank=True, null=True)
    comments_date = models.DateTimeField(auto_now_add=True)
    # check_list = models.CharField(max_length=100, null=True)
    # logs = models.CharField(max_length=100, null=True)
