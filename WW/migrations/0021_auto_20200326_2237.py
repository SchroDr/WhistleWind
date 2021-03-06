# Generated by Django 2.1.7 on 2020-03-26 14:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('WW', '0020_auto_20200326_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='add_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布日期'),
        ),
        migrations.AlterField(
            model_name='message',
            name='mod_date',
            field=models.DateTimeField(auto_now=True, verbose_name='最后修改日期'),
        ),
    ]
