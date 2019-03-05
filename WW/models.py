from django.db import models
import django.utils.timezone as timezone

class User(models.Model):
    unique_ID = models.AutoField("用户唯一标识符", primary_key = True)
    email = models.CharField("email", max_length = 32, null = False, default = "")
    user_name = models.CharField("用户名", max_length = 32, null = False, default = "user")
    password = models.CharField("密码", max_length = 32, null = False, default = "000000")
    avatar_name = models.ImageField("头像存储名", upload_to = "avatars", null = False, default = "rua.jpg")
    follows = models.TextField("关注用户", default = '[]')
    fans = models.TextField("粉丝", default = '[]')
    msgs = models.TextField("所发推文", default = '[]')
    friends = models.TextField("好友", default = '[]')
    introductino = models.TextField("简介", default = 'Hello, World')

class Message(models.Model):
    msg_ID = models.AutoField("信息唯一标识符", primary_key = True)
    pos_x = models.FloatField(default = 0)
    pox_y = models.FloatField(default = 0)
    title = models.CharField("标题", max_length = 64, null = False, default = "Title")
    content = models.TextField("内容", default = "Content")
    img = models.TextField("照片名", default = "Pic")
    author = models.IntegerField("作者", default = 0)
    like = models.IntegerField("点赞数", default = 0)
    dislike = models.IntegerField("点踩数", default = 0)
    who_like = models.TextField("点赞用户", default = '[]')
    who_dislike = models.TextField("点踩用户", default = '[]')
    add_date = models.DateTimeField('保存日期',default = timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now = True)
    comments = models.TextField("评论", default = '[]')

class Comment(models.Model):
    comment_ID = models.AutoField("评论唯一标识符", primary_key = True)
    msg_ID = models.IntegerField("所评论信息唯一标识符", default = 0)
    user_ID = models.IntegerField("评论用户唯一标识符", default = 0)
    content = models.TextField("评论内容", default = 'Content')
    img = models.ImageField("评论图片", upload_to = "command_img")
    like = models.IntegerField("点赞数", default = 0)
    who_dislike = models.TextField("点踩用户", default = '[]')
    add_date = models.DateTimeField('保存日期',default = timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now = True)


