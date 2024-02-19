from django.db import models

class Checklist(models.Model):
    text = models.CharField(max_length=255, verbose_name='Текст подзадачи')
    completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Чек-лист'
        verbose_name_plural = 'Чек-листы'
