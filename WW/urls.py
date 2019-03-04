from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.login, name = 'login'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^getMessages/$', views.getMessages, name = 'getMessages'),
    url(r'^getMsgInfo/$', views.getMsgInfo, name = 'getMsgInfo'),
     
]