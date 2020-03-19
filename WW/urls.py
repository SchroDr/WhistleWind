from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.UsersView.as_view(), name='users'),
    url(r'^users/login/$', views.login, name='login'),

    url(r'^request_vericode/$', views.requestVericode, name='requestVeiricode'),
    url(r'^test_vericode/$', views.testVericode, name='testVeiricode'),

    url(r'^messages/$', views.MessagesView.as_view(), name='messages'),
    url(r'^messages/set/$', views.messagesSet, name='messagesSet'),
    url(r'^messages/like/$', views.messagesLike, name='messagesLike'),
    url(r'^messages/dislike/$', views.messagesDislike, name='messagesDislike'),
    url(r'^messages/mentioned/$', views.messagesMentioned, name='messagesMentioned'),

    url(r'^comments/$', views.CommentsView.as_view(), name='comments'),
    url(r'^comments/like/$', views.commentsLike, name='commentsLike'),

    url(r'^images/$', views.ImagesView.as_view(), name='images'),
    url(r'^static_resources/$', views.staticResources, name='staticResources'),

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
