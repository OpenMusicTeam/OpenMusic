# Generated by Django 2.1.1 on 2019-04-08 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0039_filemodel_isaneditedsong'),
    ]

    operations = [
        migrations.AddField(
            model_name='filemodel',
            name='version',
            field=models.FloatField(null=True),
        ),
    ]
