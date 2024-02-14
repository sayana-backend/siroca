# Generated by Django 4.2 on 2024-02-14 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('company', '0003_alter_company_users'),
        ('application', '0002_applicationform_company_applicationform_manager_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationform',
            name='application_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата подачи заявки'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='comments',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Комментарии'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='Компания'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='confirm_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата утверждения заявки'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='files',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Файлы'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='finish_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='jira',
            field=models.URLField(null=True, verbose_name='ссылка JIRA'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.managerprofile', verbose_name='Менеджер'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='offer_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата отправки КП'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='payment_state',
            field=models.CharField(choices=[('Оплачено', 'Оплачено'), ('Ожидание оплаты', 'Ожидание оплаты'), ('Не оплачено', 'Не оплачено')], max_length=100, null=True, verbose_name='Статус оплаты'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='priority',
            field=models.CharField(choices=[('Низкий', 'Низкий'), ('Средний', 'Средний'), ('Высокий', 'Высокий')], max_length=100, null=True, verbose_name='Приоритет заявки'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата начала'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='status',
            field=models.CharField(choices=[('Сделать', 'Сделать'), ('В работе', 'В работе'), ('Тестируется', 'Тестируется'), ('Перекрыто', 'Перекрыто'), ('На обновлении', 'На обновлении'), ('Закрыто', 'Закрыто')], max_length=100, null=True, verbose_name='Статус заявки'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Название заявки'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.userprofile', verbose_name='Заявитель'),
        ),
    ]
