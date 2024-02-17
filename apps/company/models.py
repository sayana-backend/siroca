from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    country = models.CharField(max_length=255, verbose_name='Страна')
    manager = models.ForeignKey(
        'user.ManagerProfile',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Менеджер компании',
        related_name='managed_companies',
        blank=True
    )
    users = models.OneToOneField(
        'user.UserProfile',
        verbose_name='Пользователи',
        related_name='companies',
        on_delete=models.SET_NULL,
        blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    # job_titles = models.ManyToManyField(
    #     'JobTitle',
    #     verbose_name='Должности',
    #     related_name='companies',
    #     null=True,
    #     blank=True
    # )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def get_users(self):
        return self.users.all()


class JobTitle(models.Model):
    title = models.CharField(max_length=255, verbose_name='Должность')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    @classmethod
    def create_job_title(cls, title):
        job_title = cls.objects.create(title=title)
        return job_title
