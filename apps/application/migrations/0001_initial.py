# Generated by Django 4.2 on 2024-05-09 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to='', verbose_name='Файл')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_number', models.CharField(blank=True, max_length=10, null=True, verbose_name='Номер заявки')),
                ('title', models.CharField(max_length=100, null=True, verbose_name='Название заявки')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('short_description', models.CharField(blank=True, max_length=60, null=True, verbose_name='Краткое описание')),
                ('jira', models.URLField(blank=True, null=True, verbose_name='ссылка JIRA')),
                ('status', models.CharField(blank=True, choices=[('К выполнению', 'К выполнению'), ('В работе', 'В работе'), ('В тестировании', 'В тестировании'), ('Выполнено', 'Выполнено'), ('Проверено', 'Проверено')], default='К выполнению', max_length=100, null=True, verbose_name='Статус заявки')),
                ('payment_state', models.CharField(blank=True, choices=[('Оплачено', 'Оплачено'), ('Ожидание оплаты', 'Ожидание оплаты'), ('Не оплачено', 'Не оплачено')], default='Ожидание оплаты', max_length=100, null=True, verbose_name='Статус оплаты')),
                ('priority', models.CharField(blank=True, choices=[('Самый низкий', 'Самый низкий'), ('Низкий', 'Низкий'), ('Средний', 'Средний'), ('Высокий', 'Высокий'), ('Самый высокий', 'Самый высокий')], default='Средний', max_length=100, verbose_name='Приоритет заявки')),
                ('application_date', models.DateField(auto_now_add=True, verbose_name='Дата подачи заявки')),
                ('confirm_date', models.DateField(blank=True, null=True, verbose_name='Дата утверждения заявки')),
                ('offer_date', models.DateField(blank=True, null=True, verbose_name='Дата отправки КП')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Дата начала')),
                ('finish_date', models.DateField(blank=True, null=True, verbose_name='Дата окончания')),
                ('deadline_date', models.DateField(blank=True, null=True, verbose_name='Срок выполнения')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
        migrations.CreateModel(
            name='ApplicationLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=100, null=True)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('field', models.CharField(blank=True, max_length=500, null=True)),
                ('initially', models.CharField(blank=True, max_length=500, null=True)),
                ('new', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100, verbose_name='Название чеклиста')),
            ],
            options={
                'verbose_name': 'Чеклист',
                'verbose_name_plural': 'Чеклисты',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_number', models.CharField(blank=True, max_length=50, null=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('text', models.CharField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('made_change', models.CharField(blank=True, max_length=70, null=True)),
                ('is_read', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(blank=True, default=False, null=True)),
                ('is_manager_notic', models.BooleanField(blank=True, default=False, null=True)),
                ('is_client_notic', models.BooleanField(blank=True, default=False, null=True)),
                ('admin_id', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrackingStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('date_status', models.DateField(auto_now_add=True, null=True)),
                ('expiration_time', models.DateTimeField()),
                ('form', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.applicationform')),
            ],
        ),
        migrations.CreateModel(
            name='TrackingPriority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.CharField(blank=True, max_length=100, null=True)),
                ('date_priority', models.DateField(auto_now_add=True, null=True)),
                ('expiration_time', models.DateTimeField()),
                ('form', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.applicationform')),
            ],
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Текст подзадачи')),
                ('completed', models.BooleanField(default=False)),
                ('deadline', models.DateField(blank=True, null=True, verbose_name='Дедлайн')),
                ('checklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtasks', to='application.checklist', verbose_name='Чеклист')),
            ],
            options={
                'verbose_name': 'Подзадача',
                'verbose_name_plural': 'Подзадачи',
            },
        ),
    ]
