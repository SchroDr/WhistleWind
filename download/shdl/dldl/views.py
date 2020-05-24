from django.shortcuts import render
from django.http import HttpResponse
import os
# Create your views here.


def download_file(request):
    if request.method == 'POST':
        path = str(os.path.abspath('.'))+'/download/'
        file = open(path+'shunhu.apk', 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="shunhu.apk"'
        return response
    return render(request, 'index.html')


def mains(request):
    return HttpResponse(" ")
