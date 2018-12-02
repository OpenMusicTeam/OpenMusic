# Generated by Django 2.1.1 on 2018-11-21 22:50

from django.db import migrations, models
import file_upload.upload_validator


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0026_auto_20181030_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemodel',
            name='data',
            field=models.FileField(upload_to='', validators=[file_upload.upload_validator.FileValidator(allowed_extensions=('mp3', 'jpg', 'wav'), max_size=25165824)]),
        ),
    ]
