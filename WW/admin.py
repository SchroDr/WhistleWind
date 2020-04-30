from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'avatar', 'password', 'introduction')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'pos_x', 'pos_y', 'title', 'author', 'like', 'dislike', 'add_date', 'mod_date')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'msg', 'author', 'like', 'add_date', 'mod_date')

class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'version', 'date')

class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'device')

class FollowshipAdmin(admin.ModelAdmin):
    list_display = ('followed_user', 'fan', 'date', 'deleted')

class CommentImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'img', 'thumbnail', 'message')

class MessageImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'img', 'thumbnail', 'message')

class MessageVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'message', 'deleted')

admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Version, VersionAdmin)
admin.site.register(UserDevice, UserDeviceAdmin)
admin.site.register(Followship, FollowshipAdmin)
admin.site.register(CommentImage, CommentImageAdmin)
admin.site.register(MessageImage, MessageImageAdmin)
admin.site.register(MessageVideo, MessageVideoAdmin)
