from django.db import models
import django.utils.timezone as timezone


class User(models.Model):
    id = models.AutoField("用户唯一标识符", primary_key=True)
    email = models.EmailField("邮箱")
    phonenumber = models.CharField("电话号码", max_length=11)
    username = models.CharField(
        "用户名", max_length=62, null=False, default="WWer")
    password = models.CharField("密码", max_length=32, null=False)
    avatar = models.ImageField(
        "头像", upload_to="avatars", null=False, default="rua.jpg")
    follows = models.ManyToManyField(
        "self", verbose_name="关注用户", through="Followship", symmetrical=False, related_name='follow_set')
    friends = models.ManyToManyField(
        "self", verbose_name="好友", through="Friendship", symmetrical=False, related_name='friend_set')
    introduction = models.TextField("简介", default="Hello，World")
    deleted = models.IntegerField("是否被删除", default=0)

    class Meta:
        verbose_name = ("User")
        verbose_name_plural = ("Users")

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        # return reverse("User_detail", kwargs={"pk": self.pk})
        pass


class Message(models.Model):
    id = models.AutoField("信息唯一标识符", primary_key=True)
    pos_x = models.FloatField("信息位置经度", default=0)
    pos_y = models.FloatField("信息位置纬度", default=0)
    title = models.CharField("信息标题", max_length=62)
    content = models.TextField("信息内容")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name="该信息作者", related_name='message_author_set')
    like = models.IntegerField("点赞数", default=0)
    dislike = models.IntegerField("点踩数", default=0)
    who_like = models.ManyToManyField(
        User, verbose_name="点赞该信息的用户", related_name='message_who_like_set', blank=True)
    who_dislike = models.ManyToManyField(
        User, verbose_name="点踩该信息的用户", related_name='message_who_dislike_set', blank=True)
    add_date = models.DateField("发布日期", default=timezone.now)
    mod_date = models.DateField("最后修改日期", auto_now=True)
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
    id = models.AutoField("评论唯一标识符", primary_key=True)
    msg = models.ForeignKey(Message, on_delete=models.CASCADE,
                            verbose_name="该评论所属信息", default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name="该评论所属用户", related_name='comment_author_set', default='')
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
        return reverse("Comment_detail", kwargs={"pk": self.pk})


class MessageImage(models.Model):
    id = models.AutoField("信息图片唯一标识符", primary_key=True)
    img = models.ImageField("存储图片", upload_to="pic", null=False)
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


class CommentImage(models.Model):
    id = models.AutoField("评论图片唯一标识符", primary_key=True)
    img = models.ImageField("存储图片", upload_to="pic", null=False)
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
    date = models.DateField("成为好友的日期", default=timezone.now)
    deleted = models.IntegerField("是否被删除", default=0)


class Followship(models.Model):
    followed_user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="被关注者", related_name='followed_user_set')
    fan = models.ForeignKey(User, on_delete=models.CASCADE,
                            verbose_name="粉丝", related_name='fan_set')
    date = models.DateField("开始关注的日期", default=timezone.now)
    deleted = models.IntegerField("是否被删除", default=0)
