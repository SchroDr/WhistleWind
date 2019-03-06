import json
import os
from . import models
from django.shortcuts import render
from django.http import JsonResponse

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname('__file__')))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
PIC_ROOT = os.path.join(MEDIA_ROOT, 'pic')


def login(request):
    result = {
        'isSucceed': 0,
        'isNotExist': 0,
        'isWrong': 0,
        'userId': ''
    }
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = models.User.objects.filter(email = email)
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
    print(request)
    email = request.POST.get('email')
    print(email)
    #username = request.POST.get('username')
    password = request.POST.get('password')
    user = models.User.objects.filter(email = email)
    print(len(user))
    if len(user) == 1:
        result['isExist'] = 1
        return JsonResponse(result)
    user = models.User.objects.create(email = email, password = password)
    result['isSucceed'] = 1
    return JsonResponse(result)


def getMessages(request):
    result = []
    x = int(request.POST.get('x'))
    y = int(request.POST.get('y'))
    zoom = int(request.POST.get('zoom'))
    width = int(request.POST.get('width'))
    height = int(request.POST.get('height'))
    messages = models.Message.objects.filter(pos_x__gte = x-width, pos_x__lte = x+width, pos_y__gte = y-height, pos_y__lte = y+height)    
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
    return JsonResponse(result, safe = False)


def getMsgInfo(request):
    message = models.Message.objects.get(msg_ID = request.POST.get('msgID'))
    author = models.User.objects.get(unique_ID = message.author)
    result = {
        'name': author.user_name,
        'userID': author.unique_ID,
        'headerImgUrl': author.avatar_name,
        'like': message.like,
        'dislike': message.dislike,
        'time': message.add_date,
        'imgUrl': message.img.url,
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
    comment = models.Comment.objects.filter(comment_ID = comment_ID)
    user = models.User.objects.get(unique_ID = comment.user_ID)
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
    message = models.Message.objects.get(msg_ID = request.POST.get('msgId'))
    user = models.User.objects.get(unique_ID = request.POST.get('userId'))
    message.like += 1
    who_like = json.loads(message.who_like)
    who_like.append(user.unique_ID)
    message.who_like = json.dumps(who_like)

def giveADisLike(request):
    message = models.Message.objects.get(msg_ID = request.POST.get('msgId'))
    user = models.User.objects.get(unique_ID = request.POST.get('userId'))
    message.dislike += 1
    who_dislike = json.loads(message.who_dislike)
    who_dislike.append(user.unique_ID)
    message.who_dislike = json.dumps(who_dislike)

def saveImg(image):
    if image is not None:
        with open(os.path.join(PIC_ROOT, image.name), 'wb') as f:
            for chunk in image.chunks(chunk_size = 1024):
                f.write(chunk)
        return image.name
    else:
        return None

def postInfo(request):
    userID = request.POST.get('userID')
    content = request.POST.get('content')
    images = request.FILES.get('img')
    images_names = []
    if images is not None:
        with open(os.path.join(PIC_ROOT, images.name), 'wb') as f:
            for chunk in images.chunks(chunk_size = 1024):
                f.write(chunk)
            images_names.append(images.name)
            print(f.name)

    """
    for f in images:
        destination = open(os.path.join(PIC_ROOT, f.name), 'wb')
        for chunk in f.chuncks():
            destination.write(chunk)
        destination.close()
        images_names.append(f.name)
    """

    pos_x = request.POST.get('x')
    pos_y = request.POST.get('y')
    mention = request.POST.get('mention')
    models.Message.objects.create(pos_x = pos_x, pos_y = pos_y, content = content, author = userID, img = json.dumps(images_names))
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

        user = models.User.objects.get(unique_ID = userID)
        msg = models.Message.objects.get(msg_ID = msgId)
        comment = models.Comment.objects.create(msg_ID = msgId, userID = userID, content = content, img = image_name)

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
