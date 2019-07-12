from django.contrib import admin
from .models import User, Message, Comment

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'avatar')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'pos_x', 'pos_y', 'title', 'author')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'msg', 'author')


admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Comment, CommentAdmin)
