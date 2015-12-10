import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


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
    date_create = models.DateTimeField(auto_now_add=True)


class FriendsList(models.Model):
    user = models.ForeignKey(User)
    friend = models.ForeignKey(User)


class Profile(models.Model):
    user = models.OneToOneField(User)
    # exp = models.IntegerField()
    # rank = models.ForeignKey(Rank)
    last_active = models.DateField(null=True, blank=True)
    friends = models.ManyToManyField(User, through=FriendsList)

    @property
    def friends_count(self):
        count = self.friends.all().count()
        return count

    def activity(self):
        # checks activity, if last active is greater the 21 days mark inactive for all goals
        today = datetime.date.today()
        diff = today - self.last_active
        if self.last_active is None:
            return 'New User'
        elif diff >= 21:
            for goal in self.user.goal_set.all():
                goal.inactive = True
            return 'All goals are inactive'
        else:
            return '{} has been inactive for {} days'.format(self.user, diff)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)