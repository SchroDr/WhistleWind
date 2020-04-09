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
    url(r'^comments/child_comments/$', views.commentsChildComments, name='commentsChildComments'),

    url(r'^images/$', views.ImagesView.as_view(), name='images'),
    url(r'^static_resources/$', views.staticResources, name='staticResources')
]
