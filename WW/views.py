"""
    本模块遵循Restful原则，使用不同的HTTP动词对应不同类型的操作
    POST: 增加
    GET: 获取
    PUT: 修改
    DELETE: 删除
    接口的具体功能见
    http://rap2.taobao.org/organization/repository/editor?id=224734&mod=313234
"""

import json
import os
from django.views import View
from django.http import JsonResponse, FileResponse
from . import models, sendEmail
from django.views.decorators.http import require_GET, require_http_methods, require_POST

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname('__file__')))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
PIC_ROOT = os.path.join(MEDIA_ROOT, 'pic')

# jhc work----------------------------------------------------------------


class UsersView(View):
    """
    本模块用于对用户信息进行增删改查
    """

    def post(self, request):
        # TO DO 用户注册
        result = {
            "state": {
                "msg": "existed"
            },
        }
        try:
            phone_number = request.POST.get("phone_number")
            password = request.POST.get("password")
            # veri_code = request.POST.get("veri_code")
            user = models.User.objects.filter(phonenumber=phone_number)
            if len(user) == 1:  # 已存在
                result['state']['msg'] = 'existed'
                return JsonResponse(result)
            elif len(user) == 0:  # 不存在，可以创建
                user = models.User.objects.create(
                    phonenumber=phone_number, password=password)
                user_id = user.id
                result['data'] = {'user_id': user_id}
                result['state']['msg'] = 'successful'
                return JsonResponse(result)
        except:
            result['state']['msg'] = 'failed'
            return JsonResponse(result)

    def get(self, request):
        # TO DO 获取用户信息
        pass

    def put(self, request):
        # TO DO 修改用户信息
        pass

    def delete(self, request):
        # TO DO 删除用户信息
        # 暂无需实现
        pass
# jhc work----------------------------------------------------------------


class MessagesView(View):
    """
    本模块用于对消息进行增删改查
    """

    def post(self, request):
        # TO DO 发送消息
        pass

    def get(self, request):
        # TO DO 获取消息
        pass

    def put(self, request):
        # TO DO 修改消息
        pass

    def delete(self, request):
        # TO DO 删除消息
        pass


class CommentsView(View):
    """
    本模块用于对评论进行增删改查
    """

    def post(self, request):
        # TO DO 发送评论
        pass

    def get(self, request):
        # TO DO 获取评论
        pass

    def put(self, request):
        # TO DO 修改评论
        pass

    def delete(self, request):
        # TO DO 删除评论
        pass


class ImagesView(View):
    """
    本模块用于上传下载图片
    """

    def post(self, request):
        # TO DO 上传图片
        pass

    def get(self, request):
        # TO DO 返回图片
        pass


def login(request):
    # TO DO 登陆
    pass


def vericode(request):
    # TO DO 向用户手机发送验证码，并将验证码存入数据库中
    # 目前打算仍用mysql进行存储验证码，也可考虑用redis等存储
    pass


"""
以下函数皆为废弃接口，仅用于参考
"""


def login_old(request):
    result = {
        'isSucceed': 0,
        'isNotExist': 0,
        'isWrong': 0,
        'userId': ''
    }
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = models.User.objects.filter(email=email)
    if len(user) == 0:
        result['isNotExist'] = 1
        result['userId'] = ""
        return JsonResponse(result)
    if user[0].password == password:
        result['isSucceed'] = 1
        result['userId'] = user[0].unique_ID
        return JsonResponse(result)
    result['isWrong'] = 1
    return JsonResponse(result)


def register(request):
    result = {
        'isSucceed': 0,
        'isExist': 0
    }
    email = request.POST.get('email')
    #username = request.POST.get('username')
    password = request.POST.get('password')
    user = models.User.objects.filter(email=email)
    print(len(user))
    if len(user) == 1:
        result['isExist'] = 1
        return JsonResponse(result)
    user = models.User.objects.create(email=email, password=password)
    result['isSucceed'] = 1
    return JsonResponse(result)


def getMessages(request):
    result = []
    x = float(request.POST.get('x'))
    y = float(request.POST.get('y'))
    zoom = float(request.POST.get('zoom'))
    width = float(request.POST.get('width'))
    height = float(request.POST.get('height'))
    messages = models.Message.objects.filter(
        pos_x__gte=x-width, pos_x__lte=x+width, pos_y__gte=y-height, pos_y__lte=y+height)
    for message in messages:
        one_result = {
            'title': '',
            'content': '',
            'img': {},
            'msgId': '',
            'x': '',
            'y': ''
        }
        one_result['title'] = message.title
        one_result['content'] = message.content
        one_result['img'] = message.img
        one_result['msgId'] = message.msg_ID
        one_result['x'] = message.pos_x
        one_result['y'] = message.pos_y
        result.append(one_result)
    return JsonResponse(result, safe=False)


def getMsgInfo(request):
    message = models.Message.objects.get(msg_ID=request.POST.get('msgID'))
    author = models.User.objects.get(unique_ID=message.author)
    result = {
        'name': author.user_name,
        'userID': author.unique_ID,
        'headerImgUrl': author.avatar_name.url,
        'like': message.like,
        'dislike': message.dislike,
        'time': message.add_date,
        'imgUrl': message.img,
        'comments': message.comments
    }
    return JsonResponse(result)


def getComtInfo(request):
    result = {
        'name': '',
        'headerImgUrl': '',
        'time': '',
        'content': '',
        'imgUrl': '',
        'like': ''
    }
    comment_ID = request.POST.get('commentsId')
    comment = models.Comment.objects.filter(comment_ID=comment_ID)
    user = models.User.objects.get(unique_ID=comment.user_ID)
    if len(comment_ID) != 1:
        return 0
    result['name'] = user.user_name
    result['headerImgUrl'] = user.avatar_name
    result['time'] = comment.add_date
    result['content'] = comment.content
    result['imgUrl'] = comment.img
    result['like'] = comment.like
    return JsonResponse(result)


def giveALike(request):
    message = models.Message.objects.get(msg_ID=request.POST.get('msgId'))
    user = models.User.objects.get(unique_ID=request.POST.get('userId'))
    message.like += 1
    who_like = json.loads(message.who_like)
    who_like.append(user.unique_ID)
    message.who_like = json.dumps(who_like)


def giveADisLike(request):
    message = models.Message.objects.get(msg_ID=request.POST.get('msgId'))
    user = models.User.objects.get(unique_ID=request.POST.get('userId'))
    message.dislike += 1
    who_dislike = json.loads(message.who_dislike)
    who_dislike.append(user.unique_ID)
    message.who_dislike = json.dumps(who_dislike)


def saveImg(image):
    if image is not None:
        print("++++++++++++++++++++++++++++")
        print(os.path.join(PIC_ROOT, image.name))
        with open(os.path.join(PIC_ROOT, image.name), 'wb') as f:
            for chunk in image.chunks(chunk_size=1024):
                f.write(chunk)
        return image.name
    else:
        return None


def postInfo(request):
    userID = request.POST.get('userID')
    content = request.POST.get('content')
    images = request.FILES.getlist('img')
    images_names = []
    print(type(images))
    for image in images:
        images_names.append('media/pic/' + saveImg(image))

    pos_x = request.POST.get('x')
    pos_y = request.POST.get('y')
    mention = request.POST.get('mention')
    models.Message.objects.create(
        pos_x=pos_x, pos_y=pos_y, content=content, author=userID, img=json.dumps(images_names))
    result = {
        'isSucceed': 1
    }
    return JsonResponse(result)


def postComt(request):
    try:
        msgId = request.POST.get('msgId')
        userID = request.POST.get('userID')
        content = request.POST.get('content')
        img = request.FILES.get('img')
        image_name = saveImg(img)

        user = models.User.objects.get(unique_ID=userID)
        msg = models.Message.objects.get(msg_ID=msgId)
        comment = models.Comment.objects.create(
            msg_ID=msgId, userID=userID, content=content, img=image_name)

        user_comments = json.loads(user.comments)
        user_comments.append(comment.comment_ID)
        user.comments = user_comments
        user.save()

        msg_comments = json.loads(msg.comments)
        msg_comments.append(comment.comment_ID)
        msg.comments = user_comments
        msg.save()
        return JsonResponse({'isSucceed': 1})
    except:
        return JsonResponse({'isSucceed': 0})


def appendTo(temp, key, added_one):
    temp_line = json.loads(temp)
    temp_line.append(added_one)

    temp = temp_line


def getPic(request):
    url = request.GET.get('image_url')
    url = os.path.join(PROJECT_ROOT, url)
    return FileResponse(open(url, 'rb'))


def userInfo(request):
    userID = request.POST.get('userID')
    user = models.User.get(unique_ID=userID)
    result = {
        'name': user.user_name,
        'summary': user.introduction,

    }
