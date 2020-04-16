import django.utils.timezone as timezone
from django.db import models
from datetime import datetime
from django.db.backends.mysql.base import DatabaseFeatures # 关键设置
DatabaseFeatures.supports_microsecond_precision = False # 关键设置


class Image(models.Model):
    image_type = {
        ('avatar', 'Avatar'),
        ('universal', 'Universal'),
        ('unknown', 'Unknown')
    }
    id = models.AutoField("图片唯一标识符", primary_key=True)
    img = models.ImageField("存储图片", upload_to="pic", null=False)
    type = models.CharField("图片类型", choices=image_type,
                            default="universal", max_length=31)
    upload_date = models.DateTimeField('保存日期', default=timezone.now)
    size = models.FloatField("图片大小，单位为Mb", null=True)

class Video(models.Model):
    id = models.AutoField("图片唯一标识符", primary_key=True)
    video = models.FileField("存储视频", upload_to="video", null=False)
    upload_date = models.DateTimeField('保存日期', default=timezone.now)
    size = models.FloatField("图片大小，单位为Mb", null=True)


class Device(models.Model):
    id = models.AutoField("设备信息唯一标识符", primary_key=True)
    phone_model = models.CharField("手机型号", max_length=63)
    imei = models.CharField("IMEI", max_length=31)

class User(models.Model):
    gender_type = {
        ('male', 'Male'),
        ('female', 'Female')
    }
    id = models.AutoField("用户唯一标识符", primary_key=True)
    email = models.EmailField("邮箱")
    phonenumber = models.CharField("电话号码", max_length=11)
    username = models.CharField(
        "用户名", max_length=62, null=False, default="WWer")
    password = models.CharField("密码", max_length=32, null=False)
    avatar = models.CharField("存储头像地址", null=False,
                              max_length=500, default="media/pic/rua.jpg")
    follows = models.ManyToManyField(
        "self", verbose_name="关注用户", through="Followship", symmetrical=False, related_name='follow_set')
    friends = models.ManyToManyField(
        "self", verbose_name="好友", through="Friendship", symmetrical=False, related_name='friend_set')
    devices = models.ManyToManyField(
        Device, verbose_name="使用过的设备", through="UserDevice", related_name='device_set')
    introduction = models.TextField("简介", default="Hello, World")
    deleted = models.IntegerField("是否被删除", default=0)
    birth_date = models.DateField("出生日期", default=datetime(1980, 1, 1, 0, 0))
    gender = models.CharField("性别", choices = gender_type, default = 'unknown', max_length = 31)
    registration_date = models.DateTimeField("注册时间", default=timezone.now)

    class Meta:
        verbose_name = ("User")
        verbose_name_plural = ("Users")

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        # return reverse("User_detail", kwargs={"pk": self.pk})
        pass

class Tag(models.Model):
    id = models.AutoField("标签唯一标识符", primary_key=True)
    tag = models.TextField("标签", max_length=62)

    class Meta:
        verbose_name = ("Message")
        verbose_name_plural = ("Messages")


class Message(models.Model):
    id = models.AutoField("信息唯一标识符", primary_key=True)
    pos_x = models.FloatField("信息位置经度", default=0)
    pos_y = models.FloatField("信息位置纬度", default=0)
    title = models.CharField("信息标题", max_length=62, null=True)
    content = models.TextField("信息内容")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name="该信息作者", related_name='message_set')
    like = models.IntegerField("点赞数", default=0)
    dislike = models.IntegerField("点踩数", default=0)
    who_like = models.ManyToManyField(
        User, verbose_name="点赞该信息的用户", related_name='message_who_like_set', blank=True)
    who_dislike = models.ManyToManyField(
        User, verbose_name="点踩该信息的用户", related_name='message_who_dislike_set', blank=True)
    tag = models.ManyToManyField(
        Tag, verbose_name="该信息的tag", related_name='message_tag_set', blank=True
    )
    mention = models.ManyToManyField(
        User, verbose_name="被该信息@的用户", related_name='message_mention_user', blank=True
    )
    device = models.TextField("设备信息", blank=True)
    add_date = models.DateTimeField("发布日期", default=timezone.now)
    mod_date = models.DateTimeField("最后修改日期", auto_now=True)
    deleted = models.IntegerField("是否被删除", default=0)

    class Meta:
        verbose_name = ("Message")
        verbose_name_plural = ("Messages")

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        # return reverse("Message_detail", kwargs={"pk": self.pk})
        pass


class Comment(models.Model):
    comment_type = {
        ('child', 'Child'),
        ('parent', 'Parent')
    }
    id = models.AutoField("评论唯一标识符", primary_key=True)
    msg = models.ForeignKey(Message, on_delete=models.CASCADE,
                            verbose_name="该评论所属信息", default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name="该评论所属用户", related_name='comment_set', default='')
    #当该评论为父评论时，设为parent，为子评论时，设为child
    type = models.CharField("类型", choices = comment_type, default = 'parent', max_length = 31)
    #当该评论为子评论时，则使用reply_to参数，其为该评论所回复的用户
    #当该评论非子评论时，则该参数为空
    reply_to = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="该评论所回复的用户", 
        related_name='comment_reply_to_set', blank=True, null=True
    )
    #当该评论为子评论时，则使用parent_comment参数，其为该评论所属的父评论
    #当该评论非子评论时，则该参数为空
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, verbose_name="该评论属的父评论", 
        related_name='comment_parent_comment_set', blank=True, null=True
    )
    content = models.TextField("评论内容", default="Hello")
    like = models.IntegerField("点赞数", default=0)
    who_like = models.ManyToManyField(
        User, verbose_name="点赞该评论的用户", related_name='comment_who_like_set', blank=True)
    add_date = models.DateTimeField('保存日期', default=timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now=True)
    deleted = models.IntegerField("是否被删除", default=0)

    class Meta:
        verbose_name = ("Comment")
        verbose_name_plural = ("Comments")

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        # return reverse("Comment_detail", kwargs={"pk": self.pk})
        pass


class MessageImage(models.Model):
    id = models.AutoField("信息图片唯一标识符", primary_key=True)
    img = models.CharField("存储图片地址", null=False, max_length=500)
    thumbnail = models.CharField("存储缩略图片地址", null=False, max_length=500)
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="该图片所属信息")
    deleted = models.IntegerField("是否被删除", default=0)

    class Meta:
        verbose_name = ("MessageImage")
        verbose_name_plural = ("MessageImages")

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        # return reverse("Image_detail", kwargs={"pk": self.pk})
        pass

class MessageVideo(models.Model):
    id = models.AutoField("信息视频唯一标识符", primary_key=True)
    video = models.CharField("存储视频地址", null=False, max_length=500)
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="该图片所属信息")
    deleted = models.IntegerField("是否被删除", default=0)

    class Meta:
        verbose_name = ("MessageVideo")
        verbose_name_plural = ("MessageVideos")

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        # return reverse("Image_detail", kwargs={"pk": self.pk})
        pass


class CommentImage(models.Model):
    id = models.AutoField("评论图片唯一标识符", primary_key=True)
    img = models.CharField("存储图片地址", null=False, max_length=500)
    thumbnail = models.CharField("存储缩略图片地址", null=False, max_length=500)
    message = models.ForeignKey(
        Comment, on_delete=models.CASCADE, verbose_name="该图片所属评论")
    deleted = models.IntegerField("是否被删除", default=0)

    class Meta:
        verbose_name = ("CommentImage")
        verbose_name_plural = ("CommentImages")

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        # return reverse("CommentImage_detail", kwargs={"pk": self.pk})
        pass


class Friendship(models.Model):
    initiator = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="发起申请的用户", related_name='initiator_set')
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="接受申请的用户", related_name='recipient_set')
    date = models.DateTimeField("成为好友的日期", default=timezone.now)
    deleted = models.IntegerField("是否被删除", default=0)


class Followship(models.Model):
    followed_user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="被关注者", related_name='followed_user_set')
    fan = models.ForeignKey(User, on_delete=models.CASCADE,
                            verbose_name="粉丝", related_name='fan_set')
    date = models.DateTimeField("开始关注的日期", default=timezone.now)
    deleted = models.IntegerField("是否被删除", default=0)

class UserDevice(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="用户", related_name="userdevice_user_set"
    )
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, verbose_name="用户", related_name="userdevice_device_set"
    )

