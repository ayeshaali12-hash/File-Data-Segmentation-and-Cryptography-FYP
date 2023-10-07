# Generated by Django 4.1.4 on 2023-07-30 17:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UploadFiles', '0015_myfileupload_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='myfileupload',
            name='del_end_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='myfileupload',
            name='del_start_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='myfileupload',
            name='download_end_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='myfileupload',
            name='download_start_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
