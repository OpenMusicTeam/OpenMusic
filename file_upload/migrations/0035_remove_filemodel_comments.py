# Generated by Django 2.1.1 on 2018-11-30 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0034_auto_20181130_1828'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filemodel',
            name='comments',
        ),
    ]
