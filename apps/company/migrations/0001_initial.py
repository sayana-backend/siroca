# Generated by Django 4.2 on 2024-05-19 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название  компании')),
                ('company_code', models.CharField(max_length=3, unique=True, verbose_name='Краткий код')),
                ('country', models.CharField(max_length=255, verbose_name='Страна')),
                ('domain', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('last_updated_at', models.DateField(auto_now=True, verbose_name='Дата последнего редактирования')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
            },
        ),
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
            },
        ),
    ]
