from django.contrib import admin
from .models import User, Message, Comment

class UserAdmin(admin.ModelAdmin):
    list_display = ('unique_ID', 'email', 'user_name', 'avatar_name')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('msg_ID', 'pos_x', 'pos_y', 'title', 'author')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_ID', 'msg_ID', 'user_ID')


admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Comment, CommentAdmin)
