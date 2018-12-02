# Generated by Django 2.1.1 on 2018-11-26 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0007_project_contributors'),
        ('file_upload', '0028_auto_20181124_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='filemodel',
            name='project_publish_resource',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_publish_resource', to='project_manager.Project'),
        ),
    ]