# Generated by Django 4.1.4 on 2023-06-11 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UploadFiles', '0014_serverdata_assignedid'),
    ]

    operations = [
        migrations.AddField(
            model_name='myfileupload',
            name='mode',
            field=models.CharField(default='Non-Encrypted', max_length=10),
        ),
    ]
