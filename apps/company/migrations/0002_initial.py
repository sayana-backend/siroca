# Generated by Django 4.2 on 2024-03-12 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='main_manager',
            field=models.ForeignKey(blank=True, limit_choices_to={'role_type': 'manager'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_companies', to=settings.AUTH_USER_MODEL, verbose_name='Менеджер компании'),
        ),
        migrations.AddField(
            model_name='company',
            name='managers',
            field=models.ManyToManyField(blank=True, limit_choices_to={'is_manager': True}, related_name='companies', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи'),
        ),
    ]
