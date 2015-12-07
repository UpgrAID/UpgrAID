from django.contrib.auth.models import User
from django.db import models


class Theme(models.Model):
    title = models.CharField(max_length=20)


class Group(models.Model):
    theme = models.ForeignKey(Theme)
    user_limit = models.IntegerField(default=20)
    user = models.ManyToManyField(User)


class Rank(models.Model):
    title = models.CharField(max_length=15)
    exp_required = models.IntegerField()


class Achievement(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField (max_length=50)
    point = models.IntegerField(default=10)
    badge_amount = models.IntegerField(default=3)
    user = models.ForeignKey(User, blank=False, null=True)


class Profile(models.Model):
    user = models.OneToOneField(User)
    exp = models.IntegerField()
    rank = models.ForeignKey(Rank)

