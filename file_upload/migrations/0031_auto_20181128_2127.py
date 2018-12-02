# Generated by Django 2.1.1 on 2018-11-28 19:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0030_auto_20181128_0341'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='filemodel',
            name='comments',
        ),
        migrations.AddField(
            model_name='commentmodel',
            name='comments',
            field=models.ManyToManyField(to='file_upload.FileModel'),
        ),
    ]