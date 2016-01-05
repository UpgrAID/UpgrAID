from django.contrib import admin
from post.models import Goal, Post, Comment, CommentLike, GroupMessage, \
    UserMessage


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'inactive', 'created_at', 'theme')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'user', 'group', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'description', 'user', 'created_at')


@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'group', 'message', 'sent_at')


@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'message', 'sent_at')


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'user')
