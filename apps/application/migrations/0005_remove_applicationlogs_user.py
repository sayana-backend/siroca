# Generated by Django 4.2 on 2024-04-30 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_applicationlogs_user_alter_applicationform_files_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationlogs',
            name='user',
        ),
    ]
