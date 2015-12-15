from django.contrib.auth.models import User
from django.db import models
from user.models import Theme, Group


class Goal(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    inactive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    theme = models.ForeignKey(Theme)
    group = models.ForeignKey(Group, blank=True)
    completed = models.BooleanField(default=False)

    def remove_group(self):
        if self.completed:
            self.group.user.remove(self.user)

    def __str__(self):
        return "{}, {}: {}".format(self.user, self.id, self.inactive)


class Post(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
