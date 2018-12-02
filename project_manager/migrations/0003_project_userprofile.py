# Generated by Django 2.1.1 on 2018-10-25 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20181025_0028'),
        ('project_manager', '0002_remove_project_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='userProfile',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.UserProfile'),
            preserve_default=False,
        ),
    ]
