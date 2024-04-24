# Generated by Django 4.2 on 2024-04-23 13:15

import apps.user.usermanager
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('role_type', models.CharField(choices=[('client', 'Клиент'), ('manager', 'Менеджер')], max_length=20, verbose_name='Тип роли')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Логин')),
                ('first_name', models.CharField(max_length=30, verbose_name='Имя')),
                ('surname', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('image', models.FileField(blank=True, null=True, upload_to='', verbose_name='Изображение')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_manager', models.BooleanField(default=False, verbose_name='Менеджер')),
                ('is_client', models.BooleanField(default=False, verbose_name='Клиент')),
                ('manager_can_delete_comments', models.BooleanField(default=False, verbose_name='Удаление комментариев')),
                ('manager_can_delete_comments_extra', models.BooleanField(null=True, verbose_name='Удаление комментариев')),
                ('manager_can_get_reports', models.BooleanField(default=False, verbose_name='Отчет по заявкам(Менеджер)')),
                ('manager_can_get_reports_extra', models.BooleanField(null=True, verbose_name='Отчет по заявкам(Менеджер)')),
                ('manager_can_view_profiles', models.BooleanField(default=False, verbose_name='Просмотр профиля пользователей(Менеджер)')),
                ('manager_can_view_profiles_extra', models.BooleanField(null=True, verbose_name='Просмотр профиля пользователей(Менеджер)')),
                ('manager_can_delete_application', models.BooleanField(default=False, verbose_name='Удаление заявки')),
                ('manager_can_delete_application_extra', models.BooleanField(null=True, verbose_name='Удаление заявки')),
                ('manager_can_create_and_edit_company_extra', models.BooleanField(null=True, verbose_name='Создание/Редактирование заявки')),
                ('manager_can_create_and_edit_user_extra', models.BooleanField(null=True, verbose_name='Создание/Редактирование пользователя')),
                ('manager_can_create_and_delete_job_title_extra', models.BooleanField(null=True, verbose_name='Просмотр списка по компаниям/пользователям/должностям')),
                ('client_can_edit_comments', models.BooleanField(default=False, verbose_name='Добавление/удаление комментария')),
                ('client_can_edit_comments_extra', models.BooleanField(null=True, verbose_name='Добавление/удаление комментария')),
                ('client_can_get_reports', models.BooleanField(default=False, verbose_name='Отчет по заявкам(Клиент)')),
                ('client_can_get_reports_extra', models.BooleanField(null=True, verbose_name='Отчет по заявкам(Клиент)')),
                ('client_can_view_logs', models.BooleanField(default=False, verbose_name='Просмотр логов')),
                ('client_can_view_logs_extra', models.BooleanField(null=True, verbose_name='Просмотр логов')),
                ('client_can_add_checklist', models.BooleanField(default=False, verbose_name='Добавление чеклиста')),
                ('client_can_add_checklist_extra', models.BooleanField(null=True, verbose_name='Добавление чеклиста')),
                ('client_can_add_files', models.BooleanField(default=False, verbose_name='Добавление файла')),
                ('client_can_add_files_extra', models.BooleanField(null=True, verbose_name='Добавление файла')),
                ('client_can_view_profiles', models.BooleanField(default=False, verbose_name='Просмотр профиля пользователей(Клиент)')),
                ('client_can_view_profiles_extra', models.BooleanField(null=True, verbose_name='Просмотр профиля пользователей(Клиент)')),
                ('client_can_create_application_extra', models.BooleanField(default=False, verbose_name='Создание заявки')),
                ('client_can_edit_application_extra', models.BooleanField(null=True, verbose_name='Редактирование заявки')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('job_title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_job_titles', to='company.jobtitle', verbose_name='Должность')),
                ('main_company', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='company_users', to='company.company', verbose_name='Компания')),
                ('managers_company', models.ManyToManyField(blank=True, related_name='managers_company', to='company.company', verbose_name='Компании менеджеров')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', apps.user.usermanager.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AdminContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Телефонный номер')),
                ('whatsapp_number', models.CharField(max_length=20, verbose_name='Номер WhatsApp')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contact', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Контакт для админа',
                'verbose_name_plural': 'Контакты для админа',
            },
        ),
    ]
