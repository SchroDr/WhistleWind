# Generated by Django 2.1.7 on 2019-03-06 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WW', '0005_auto_20190305_2239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='who_dislike',
        ),
        migrations.AddField(
            model_name='comment',
            name='who_like',
            field=models.TextField(default='[]', verbose_name='点赞用户'),
        ),
        migrations.AddField(
            model_name='user',
            name='comments',
            field=models.TextField(default='[]', verbose_name='所发评论'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='img',
            field=models.ImageField(null=True, upload_to='command_img', verbose_name='评论图片'),
        ),
    ]
