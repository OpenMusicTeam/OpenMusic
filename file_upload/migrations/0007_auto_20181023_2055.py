# Generated by Django 2.1.1 on 2018-10-23 17:55

from django.db import migrations, models
import file_upload.upload_validator


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0006_auto_20181023_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemodel',
            name='data',
            field=models.FileField(upload_to='user_projects/', validators=[file_upload.upload_validator.FileValidator(allowed_extensions=('mp3', 'jpg'), max_size=25165824)]),
        ),
    ]
