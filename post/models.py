from collections import Counter
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from pusher import Pusher
from rest_framework.authtoken.models import Token
from upgraid.settings import PUSHER_ID, PUSHER_KEY, PUSHER_SECRET
from user.models import Theme, Group, Achievement, Earned
from django.conf import settings


class Goal(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    inactive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    theme = models.ForeignKey(Theme)
    group = models.ForeignKey(Group, blank=True)
    completed = models.BooleanField(default=False)

    def similar_goal_list(self):
        """
        Goes through every goal and returns a list of goals that are
        close to this goal
        """
        goal = [word for word in self.title.split() if word.lower() not in open('common_words.txt').read()]
        same_goal = []
        for word in goal:
            for object in Goal.objects.filter(title__icontains=word,
                                              theme=self.theme):
                same_goal.append(object)
        return same_goal

    def closest_goal(self, same_goals):
        """
        With a given list of similar goals, gives each goal a number based on how
        similar they are and returns a list of tuples containing the goal and
        their respective numbers in order based off that number
        """
        goal_count = Counter(same_goals)
        goal_count = goal_count.most_common()
        return goal_count

    def assign_existing_group(self, group):
        if not group.full:
            self.group = group
            self.user.group_set.add(group)
            self.user.save()

    def assign_new_group(self):
        new_group = self.user.group_set.create(theme=self.theme)
        self.user.save()
        self.group = new_group

    def __str__(self):
        return "{}, {}: {}".format(self.user, self.id, self.inactive)


@receiver(pre_save, sender=Goal)
def create_group(sender, instance=None, **kwargs):
    if not instance.id:
        same_goal = instance.similar_goal_list()
        if len(same_goal) > 0:
            closest_goals = instance.closest_goal(same_goal)
            for closest_goal in closest_goals:
                goals = closest_goal[0]
                group = goals.group
                if goals.user != instance.user:
                    instance.assign_existing_group(group)
                if goals.user == instance.user and goals.completed:
                    instance.assign_existing_group(group)
                    goals.delete()
        else:
            instance.assign_new_group()


@receiver(post_save, sender=Goal)
def goal_achievements(sender, instance=None, **kwargs):
    """
    Checks to see if goal is completed. Then chekcs how many goals the user
    has completed and compares that to achievements for completed goals
    """
    if instance.completed:
        instance.group.user.remove(instance.user)
        completed_count = instance.user.goal_set.filter(completed=True).count()
        achievements = Achievement.objects.filter(type='Goal')
        if achievements.count() > 0:
            for achievement in achievements:
                if achievement.required_amount >= completed_count\
                        and achievement not in instance.user.achievement_set.all():
                    Earned.objects.create(user=instance.user,
                                          achievement=achievement)


class Post(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Post)
def post_achievements(sender, instance=None, created=False, **kwargs):
    if created:
        achievements = Achievement.objects.filter(type='Post')
        if len(achievements) > 0:
            for achievement in achievements:
                if instance.user.post_set.count() >= achievement.required_amount \
                        and achievement not in instance.user.achievement_set.all():
                    Earned.objects.create(user=instance.user, achievement=achievement)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class GroupMessage(models.Model):
    user = models.ForeignKey(User, related_name='sender')
    group = models.ForeignKey(Group, related_name='group')
    sent_at = models.TimeField(auto_now_add=True)
    message = models.TextField()


@receiver(post_save, sender=GroupMessage)
def pusher_info(sender, instance=None, created=False, **kwargs):
    pusher = Pusher(app_id=PUSHER_ID, key=PUSHER_KEY, secret=PUSHER_SECRET,
                    ssl=True)
    if created:
        if instance.group.channel:
            pusher.trigger(instance.group.channel, instance.group.event, {'message': instance.message})
        else:
            pusher.trigger(instance.group.channel, instance.group.event, {'message': instance.message})


class UserMessage(models.Model):
    sender = models.ForeignKey(User, related_name='user_sender')
    receiver = models.ForeignKey(User, related_name='receiver')
    sent_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ('comment', 'user')
