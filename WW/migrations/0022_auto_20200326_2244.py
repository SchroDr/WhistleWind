# Generated by Django 2.1.7 on 2020-03-26 14:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('WW', '0021_auto_20200326_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followship',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='开始关注的日期'),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='成为好友的日期'),
        ),
    ]
