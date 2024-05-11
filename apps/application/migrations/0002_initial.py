# Generated by Django 4.2 on 2024-05-11 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('application', '0001_initial'),
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='subtask',
            name='manager',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_manager': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Отмеченный менеджер'),
        ),
        migrations.AddField(
            model_name='notification',
            name='form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.applicationform'),
        ),
        migrations.AddField(
            model_name='comments',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='application.applicationform', verbose_name='Заявка'),
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='checklist',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checklists', to='application.applicationform', verbose_name='Заявка'),
        ),
        migrations.AddField(
            model_name='applicationlogs',
            name='check_list_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.checklist', verbose_name='id чеклиста'),
        ),
        migrations.AddField(
            model_name='applicationlogs',
            name='form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='application.applicationform', verbose_name='Заявка'),
        ),
        migrations.AddField(
            model_name='applicationform',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='Компания'),
        ),
        migrations.AddField(
            model_name='applicationform',
            name='main_client',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_client': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client_application', to=settings.AUTH_USER_MODEL, verbose_name='Заявитель'),
        ),
        migrations.AddField(
            model_name='applicationform',
            name='main_manager',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_manager': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manager_application', to=settings.AUTH_USER_MODEL, verbose_name='Менеджер'),
        ),
        migrations.AddField(
            model_name='applicationfile',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='application.applicationform', verbose_name='Заяка'),
        ),
    ]
