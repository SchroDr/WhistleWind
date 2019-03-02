from django.db import models
import django.utils.timezone as timezone

class User(models.Model):
    unique_ID = models.AutoField("用户唯一标识符", primary_key = True)
    user_ID = models.CharField("用户ID", max_length = 32, null = False)
    user_name = models.CharField("用户名", max_length = 32, null = False)
    password = models.CharField("密码", max_length = 32, null = False)
    avatar_name = models.ImageField("头像存储名", upload_to = "avatars", null = False)
    follows = models.TextField("关注用户", default = '[]')
    fans = models.TextField("粉丝", default = '[]')
    msgs = models.TextField("所发推文", default = '[]')
    friends = models.TextField("好友", default = '[]')
    introductino = models.TextField("简介", default = 'Hello, World')

class Message(models.Model):
    msg_ID = models.AutoField("信息唯一标识符", primary_key = True)
    pos_x = models.IntegerField()
    pox_y = models.IntegerField()
    title = models.CharField("标题", max_length = 64, null = False)
    content = models.TextField("内容")
    img = models.TextField("照片名")
    author = models.IntegerField("作者")
    like = models.IntegerField("点赞数")
    dislike = models.IntegerField("点踩数")
    add_date = models.DateTimeField('保存日期',default = timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now = True)
    comments = models.TextField("评论")

class Comment(models.Model):
    comment_ID = models.AutoField("评论唯一标识符", primary_key = True)
    msg_ID = models.IntegerField("所评论信息唯一标识符")
    user_ID = models.IntegerField("评论用户唯一标识符")
    content = models.TextField("评论内容")
    img = models.ImageField("评论图片", upload_to = "command_img")


