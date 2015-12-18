import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save


class Theme(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Group(models.Model):
    theme = models.ForeignKey(Theme)
    user_limit = models.IntegerField(default=20)
    user = models.ManyToManyField(User)
    channel = models.CharField(max_length=20, blank=True, null=True)
    event = models.CharField(max_length=20, blank=True, null=True)

    @property
    def full(self):
        if len(self.user.all()) == self.user_limit:
            return True
        else:
            return False
        
    def __str__(self):
        return '{} group #{}'.format(self.theme, self.id)


class Rank(models.Model):
    title = models.CharField(max_length=15)
    exp_required = models.IntegerField()

    def __str__(self):
        return '{}: exp required {}'.format(self.title, self.exp_required)


class Achievement(models.Model):
    MODEL_FOR_ACHIEVEMENT = (
        ('Goal', 'Goal'),
        ('Post', 'Post'),
        ('Earned', 'Earned')
    )
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=4, choices=MODEL_FOR_ACHIEVEMENT)
    point = models.IntegerField(default=2)
    user = models.ManyToManyField(User, through='Earned', related_name='achievement_set')
    badge_amount = models.IntegerField(default=3)
    date_create = models.DateTimeField(auto_now_add=True)
    required_amount = models.IntegerField()

    def __str__(self):
        return 'Achievement {} {}: points: {}, badge amount: {} earned by: {}'\
            .format(self.name, self.required_amount, self.point,
                    self.badge_amount, self.user)


class Earned(models.Model):
    user = models.ForeignKey(User)
    achievement = models.ForeignKey(Achievement)


class Friendship(models.Model):
    from_friend = models.ForeignKey(User, related_name='friend_set')
    to_friend = models.ForeignKey(User, related_name='to_friend_set')
    accepted = models.NullBooleanField()

    def denied_friend_request(self):
        if not self.accepted and self.accepted is not None:
            self.delete()

    def __str__(self):
        return '{} and {} are Friends'.format(self.from_friend, self.to_friend)

    class Meta:
        unique_together = (('to_friend', 'from_friend'), )


class Profile(models.Model):
    user = models.OneToOneField(User)
    exp = models.IntegerField(default=0)
    rank = models.ForeignKey(Rank)
    last_active = models.DateField(null=True, blank=True)

    @property
    def friends_count(self):
        count = len(self.friend_set.all())+len(self.to_friend_set.all())
        return count

    def activity(self):
        # checks activity, if last active is greater the 21 days mark inactive
        # for all goals
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

    def rank_check(self):
        if self.exp >= self.rank.exp_required:
            new_rank = Rank.objects.get(pk=(1+self.rank.id))
            self.rank = new_rank

    def __str__(self):
        return '{}: Last Active: {}'.format(self.user, self.last_active)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
