# Generated by Django 4.1.4 on 2023-05-04 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UploadFiles', '0002_myfileupload_user_alter_myfileupload_my_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myfileupload',
            name='my_file',
        ),
    ]
