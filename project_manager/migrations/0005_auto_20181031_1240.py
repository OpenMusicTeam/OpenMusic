# Generated by Django 2.1.1 on 2018-10-31 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0004_auto_20181025_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
