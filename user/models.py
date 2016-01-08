import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


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


@receiver(post_save, sender=Earned)
def rank(sender, instance=None, created=False, **kwargs):
    if created:
        instance.user.profile.exp = instance.user.profile.exp + instance.achievement.point
        instance.user.profile.rank_up()
        instance.user.profile.badges = instance.user.profile.badges + instance.achievement.badge_amount
        instance.user.profile.save()


@receiver(post_save, sender=Earned)
def earned_achievements(sender, instance=None, created=False, **kwargs):
    if created:
        achievements = Achievement.objects.filter(type='Earned')
        if len(achievements) > 0:
            for achievement in achievements:
                if instance.user.achievement_set.count() >= achievement.required_amount\
                        and achievement not in instance.user.achievement_set.all():
                    Earned.objects.create(user=instance.user, achievement=achievement)


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


@receiver(post_save, sender=Friendship)
def friend_request(sender, instance=None, **kwargs):
    if instance:
        instance.denied_friend_request()


class Profile(models.Model):
    user = models.OneToOneField(User)
    exp = models.IntegerField(default=0)
    rank = models.ForeignKey(Rank, blank=True)
    last_active = models.DateField(null=True, blank=True)
    badges = models.IntegerField(default=0)
    avatar = models.IntegerField(default=1)

    @property
    def friends_count(self):
        count = len(self.friend_set.all())+len(self.to_friend_set.all())
        return count

    def activity(self):
        """
        checks activity, if last active is greater the 21 days mark inactive
        for all goals
        """
        today = datetime.datetime.now()
        diff = today - datetime.datetime.strptime(str(self.last_active),
                                                  '%Y-%m-%d')
        if self.last_active is None:
            return
        elif diff.days >= 21:
            for goal in self.user.goal_set.all():
                goal.inactive = True
                goal.save()
            return
        return

    def rank_up(self):
        if self.exp >= self.rank.exp_required:
            new_rank = Rank.objects.get(pk=(1+self.rank.id))
            self.rank = new_rank

    def __str__(self):
        return '{}: Last Active: {}'.format(self.user, self.last_active)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_save, sender=Profile)
def default_rank(sender, instance=None, **kwargs):
    if not instance.id:
        instance.rank = Rank.objects.get(title='Novice 5')


class BadgeGift(models.Model):
    sender = models.ForeignKey(User, related_name='badge_sender')
    receiver = models.ForeignKey(User, related_name='badge_receiver')
    amount = models.IntegerField()

    def gift_sent(self):
        self.sender.profile.badges -= self.amount
        self.sender.profile.save()

    def gift_received(self):
        self.receiver.profile.badges += self.amount
        self.receiver.profile.save()


@receiver(post_save, sender=BadgeGift)
def badge_gift(sender, instance=None, created=False, **kwargs):
    if created:
        instance.gift_sent()
        instance.gift_received()