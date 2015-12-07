from django.contrib.auth.models import User
from django.db import models


class Goal(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User)


class Post(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    user = models.ForeignKey(User)
    goal = models.ForeignKey(Goal)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User)

