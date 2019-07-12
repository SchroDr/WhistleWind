from django.db import models
import django.utils.timezone as timezone

"""
class User(models.Model):
    unique_ID = models.AutoField("用户唯一标识符", primary_key = True)
    email = models.CharField("email", max_length = 32, null = False, default = "")
    user_name = models.CharField("用户名", max_length = 32, null = False, default = "user")
    password = models.CharField("密码", max_length = 32, null = False, default = "000000")
    avatar_name = models.ImageField("头像存储名", upload_to = "avatars", null = False, default = "rua.jpg")
    follows = models.TextField("关注用户", default = '[]')
    fans = models.TextField("粉丝", default = '[]')
    msgs = models.TextField("所发推文", default = '[]')
    comments = models.TextField("所发评论", default = '[]')
    friends = models.TextField("好友", default = '[]')
    introductino = models.TextField("简介", default = 'Hello, World')

    def __str__(self):
        return str(self.unique_ID)
"""

class User(models.Model):
    id = models.AutoField("用户唯一标识符", primary_key = True)
    email = models.EmailField("邮箱")
    username = models.CharField("用户名", max_length = 62, null = False, default = "WWer")
    password = models.CharField("密码", max_length = 32, null = False)
    avatar = models.ImageField("头像", upload_to = "avatars", null = False, default = "rua.jpg")
    follows = models.ManyToManyField("关注用户", User)
    fans = models.ManyToManyField("粉丝", User)
    friends = models.ManyToManyField("好友", User)
    introduction = models.TextField("简介", default = "Hello，World")

    class Meta:
        verbose_name = ("User")
        verbose_name_plural = ("Users")

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        #return reverse("User_detail", kwargs={"pk": self.pk})
        pass

"""
class Message(models.Model):
    msg_ID = models.AutoField("信息唯一标识符", primary_key = True)
    pos_x = models.FloatField(default = 0)
    pos_y = models.FloatField(default = 0)
    title = models.CharField("标题", max_length = 64, null = False, default = "Title")
    content = models.TextField("内容", default = "Content")
    img = models.TextField("照片名", default = "Pic")
    author = models.IntegerField("作者", default = 0)
    like = models.IntegerField("点赞数", default = 0)
    dislike = models.IntegerField("点踩数", default = 0)
    who_like = models.TextField("点赞用户", default = '[]')
    who_dislike = models.TextField("点踩用户", default = '[]')
    add_date = models.DateTimeField('保存日期', default = timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now = True)
    comments = models.TextField("评论", default = '[]')

    def __str__(self):
        return str(self.msg_ID)
"""

class Message(models.Model):
    id = models.AutoField("信息唯一标识符", primary_key = True)
    pos_x = models.FloatField("信息位置经度", default = 0)
    pos_y = models.FloatField("信息位置纬度", default= = 0)
    title = models.CharField("信息标题", max_length = 62)
    content = models.TextField("信息内容")
    author = models.ManyToManyField(User, verbose_name = "该信息的作者")
    like = models.IntegerField("点赞数", default = 0)
    dislke = models.IntegerField("点踩数", default = 0)
    who_like = models.ManyToManyField(User, verbose_name = "点赞该信息的用户")
    who_dislike = models.ManyToManyField(User, verbose_name = "点踩该信息的用户")
    add_date = models.DateField("发布日期", default = timezone.now)
    mod_date = models.DateField("最后修改日期", auto_now = True)

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        #return reverse("Message_detail", kwargs={"pk": self.pk})
        pass

"""
class Comment(models.Model):
    comment_ID = models.AutoField("评论唯一标识符", primary_key = True)
    msg_ID = models.IntegerField("所评论信息唯一标识符", default = 0)
    user_ID = models.IntegerField("评论用户唯一标识符", default = 0)
    content = models.TextField("评论内容", default = 'Content')
    img = models.ImageField("评论图片", upload_to = "command_img", null = True)
    like = models.IntegerField("点赞数", default = 0)
    who_like = models.TextField("点赞用户", default = '[]')
    add_date = models.DateTimeField('保存日期',default = timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now = True)

    def __str__(self):
        return str(self.comment_ID)
"""

class Comment(models.Model):
    id = models.AutoField("评论唯一标识符", primary_key = True)
    msg = models.ForeignKey(Message, on_delete = models.CASCADE, verbose_name = "该评论所属信息")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "该评论所属用户")
    content = models.TextField("评论内容", default = "Hello")
    like = models.IntegerField("点赞数", default = 0)
    who_like = models.ManyToManyField(User, verbose_name = "点赞该评论的用户")
    add_date = models.DateTimeField('保存日期',default = timezone.now)
    mod_date = models.DateTimeField('最后修改日期', auto_now = True)
    

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Comment_detail", kwargs={"pk": self.pk})



class MessageImage(models.Model):
    id = models.AutoField("信息图片唯一标识符", primary_key = True)
    img = models.ImageField("存储图片", upload_to = "pic", null = False)
    message = models.ForeignKey(Message, on_delete = models.CASCADE, verbose_name = "该图片所属信息")

    class Meta:
        verbose_name = ("MessageImage")
        verbose_name_plural = ("MessageImages")

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        #return reverse("Image_detail", kwargs={"pk": self.pk})
        pass

class CommentImage(models.Model):
    id = models.AutoField("评论图片唯一标识符", primary_key = True)
    img = models.ImageField("存储图片", upload_to = "pic", null = False)
    message = models.ForeignKey(Comment, on_delete = models.CASCADE, verbose_name = "该图片所属评论")

    class Meta:
        verbose_name = ("CommentImage")
        verbose_name_plural = ("CommentImages")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        #return reverse("CommentImage_detail", kwargs={"pk": self.pk})
        pass
