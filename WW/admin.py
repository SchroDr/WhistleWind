from django.contrib import admin
from .models import User, Message, Comment

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'avatar', 'password', 'introduction')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'pos_x', 'pos_y', 'title', 'author', 'like', 'dislike', 'add_date', 'mod_date')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'msg', 'author', 'like', 'add_date', 'mod_date')


admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Comment, CommentAdmin)
