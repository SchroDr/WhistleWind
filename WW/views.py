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
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = models.User.objects.filter(user_name = username)
    if len(user) == 0:
        result['isNotExit'] = 1
        result['userId'] = username
        return JsonResponse(result)
    if user[0].password == password:
        result['isSucceed'] = 1
        result['userId'] = username
        return JsonResponse(result)
    result['isWrong'] = 1
    return JsonResponse(result)

def register(request):
    result = {
        'isSucceed': 0,
        'isExist': 0
    }
    userId = request.POST.get('userId')
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = models.User.objects.filter(user_name = username)
    if len(user) == 1:
        result['isExit'] = 1
        return JsonResponse(result)
    user = models.User.objects.create(user_Id)


def post(request):
    pass
    pass

