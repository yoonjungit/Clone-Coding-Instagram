# Generated by Django 4.1.3 on 2022-12-12 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0003_bookmark_like_reply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='like_count',
        ),
    ]
