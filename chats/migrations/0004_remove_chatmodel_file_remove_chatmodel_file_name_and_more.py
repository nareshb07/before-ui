# Generated by Django 4.2.1 on 2023-06-07 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0003_alter_chatmodel_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmodel',
            name='file',
        ),
        migrations.RemoveField(
            model_name='chatmodel',
            name='file_name',
        ),
        migrations.AddField(
            model_name='chatmodel',
            name='media_file',
            field=models.FileField(blank=True, null=True, upload_to='media_files/'),
        ),
    ]