# Generated by Django 4.1.4 on 2023-06-10 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UploadFiles', '0012_serverdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='serverdata',
            name='status',
            field=models.CharField(default='Enabled', max_length=10),
        ),
    ]
