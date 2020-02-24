from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.UsersView.as_view(), name='users'),
    url(r'^users/login/$', views.login, name='login'),
    url(r'^users/vericode/$', views.vericode, name='veiricode'),
    url(r'^messages/$', views.MessagesView.as_view(), name='messages'),
    url(r'^comments/$', views.CommentsView.as_view(), name='comments'),
    url(r'^images/$', views.ImagesView.as_view(), name='images'),

    # 以下接口均为废弃接口
    url(r'^login/$', views.login_old, name='login_old'),
    url(r'^register/$', views.register, name='register'),
    url(r'^getMessages/$', views.getMessages, name='getMessages'),
    url(r'^getMsgInfo/$', views.getMsgInfo, name='getMsgInfo'),
    url(r'^getComtInfo/$', views.getComtInfo, name='getComtInfo'),
    url(r'^giveALike/$', views.giveALike, name='giveALike'),
    url(r'^giveADisLike', views.giveADisLike, name='giveADisLike'),
    url(r'^postInfo/$', views.postInfo, name='postInfo'),
    url(r'^getPic/$', views.getPic, name='getPic'),
]
