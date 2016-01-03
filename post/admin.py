from django.contrib import admin
from post.models import Goal, Post, Comment, CommentLike


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'inactive', 'created_at', 'theme')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'user', 'group', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'description', 'user', 'created_at')


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'user')
