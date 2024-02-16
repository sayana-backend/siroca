# Generated by Django 4.2 on 2024-02-16 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('application', '0002_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationform',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.managerprofile', verbose_name='Менеджер'),
        ),
        migrations.AddField(
            model_name='applicationform',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.userprofile', verbose_name='Заявитель'),
        ),
    ]
