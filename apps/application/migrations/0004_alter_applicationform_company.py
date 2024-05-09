# Generated by Django 4.2 on 2024-05-09 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_initial'),
        ('application', '0003_alter_applicationform_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationform',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='applications_count', to='company.company', verbose_name='Компания'),
        ),
    ]
