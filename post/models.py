from django.contrib.auth.models import User
from django.db import models
from user.models import Theme


class Goal(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    inactive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    theme = models.ForeignKey(Theme)


class Post(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    user = models.ForeignKey(User)
    goal = models.ForeignKey(Goal)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
