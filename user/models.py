from django.db import models

USER_ROLE_CHOICES = [
    ('manager', 'Менеджер'),
    ('client', 'Клиент'),
]


class Users(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    login = models.CharField(max_length=100, unique=True, verbose_name='Логин')
    password = models.CharField(max_length=500, verbose_name='Пароль')
    company = models.OneToOneField(max_length=100, verbose_name='Компания')
    position_company = models.OneToOneField(max_length=100, blank=True, verbose_name='Должность в компании')
    user_role = models.CharField(max_length=50, choices=USER_ROLE_CHOICES, verbose_name='Роль')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

# >>>>>>> a151017e203b00847846fced4a64669a1fd2acf2
