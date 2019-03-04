from django.shortcuts import render
from django.http import JsonResponse
from . import models

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
        result['isNotExit'] = 1
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
    user = models.User.objects.filter(email = email)
    if len(user) == 1:
        result['isExit'] = 1
        return JsonResponse(result)
    user = models.User.objects.create(email = email, user_name = username, password = password)
    result['isSucceed'] = 1
    return JsonResponse(result)


def getMessages(request):
    one_result = {
        'title': '',
        'content': '',
        'img': {},
        'msgId': '',
        'x': '',
        'y': ''
    }
    result = []
    x = request.POST.get('x')
    y = request.POST.get('y')
    zoom = request.POST.get('zoom')
    width = request.POST.get('width')
    height = request.POST.get('height')
    messages = models.Message.objects.filter(pos_x__gte = x-width, pos_x__lte = x+width, pos_y__gte = y-width, pos_y__lte = y+width)    
    for message in messages:
        one_result['title'] = message.title
        one_result['content'] = message.content 
        one_result['img'] = message.img 
        one_result['msgId'] = message.msg_ID
        one_result['x'] = message.pos_x
        one_result['y'] = message.pos_y
        result.append(one_result)
    return JsonResponse(result, safe = False)

def getMsgInfo(request):
    message = models.Message.objectes.get(msg_ID = request.POST.get('msgID'))
    author = models.User.objects.get(unique_ID = message.author)
    result = {
        'name': author.user_name,
        'userID': author.unique_ID,
        'headerImgUrl': author.avatar_name,
        'like': message.like,
        'dislike': message.dislike,
        'time': message.add_date,
        'imgUrl': message.img,
        'comments': message.comments        
    }

def giveALike(request):
    message = models.Message.objects.get(msg_ID = request.POST.get('msgId'))
    user = models.User.objects.get(unique_ID = request.POST.get('userId'))