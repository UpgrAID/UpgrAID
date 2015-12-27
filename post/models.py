from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from pusher import Pusher
from rest_framework.authtoken.models import Token
from upgraid.settings import PUSHER_ID, PUSHER_KEY, PUSHER_SECRET
from user.models import Theme, Group
from django.conf import settings


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


@receiver(pre_save, sender=Goal)
def create_group(sender, instance=None, **kwargs):
    common_words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have',
                    'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you',
                    'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they',
                    'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one',
                    'all', 'would', 'there', 'their', 'what', 'so', 'up',
                    'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
                    'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him',
                    'know', 'take', 'person', 'into', 'year', 'your', 'good',
                    'some', 'could', 'them', 'see', 'other', 'than', 'then',
                    'now', 'look', 'only', 'come', 'its', 'over', 'think',
                    'also', 'back', 'after', 'use', 'two', 'how', 'our',
                    'work', 'first', 'well', 'way', 'even', 'new', 'want',
                    'because', 'any', 'these', 'give', 'day', 'most', 'us']
    if not instance.id:
        goal = [word
                for word in instance.title.split()
                if word.lower() not in common_words
                ]
        same_goal = []
        for word in goal:
            for object in Goal.objects.filter(title__icontains=word,
                                              theme=instance.theme):
                same_goal.append(object)
        if len(same_goal) > 0:
            goal_count = Counter(same_goal)
            goal_count = goal_count.most_common()
            for closest_goal in goal_count:
                goals = closest_goal[0]
                if goals.user != instance.user:
                    groups = goals.group
                    if not groups.full:
                        instance.group = groups
                        instance.user.group_set.add(groups)
                        instance.user.save()
                        break
                    # else:
                    #     new_group = instance.user.group_set.create(
                    #         theme=instance.theme)
                    #     instance.user.save()
                    #     instance.group = new_group
                    #     break
                if goals.user == instance.user and goals.completed:
                    groups = goals.group
                    if not groups.full:
                        instance.group = groups
                        instance.user.group_set.add(groups)
                        instance.user.save()
                        goals.delete()
                        break

        else:
            new_group = instance.user.group_set.create(theme=instance.theme)
            instance.user.save()
            instance.group = new_group
    else:
        if instance.completed:
            instance.group.user.remove(instance.user)
            completed_count = len(instance.user.goal_set.filter(completed=True))
            achievements = Achievement.objects.filter(type='Goal')
            if len(achievements) > 0:
                for achievement in achievements:
                    if achievement.required_amount == completed_count:
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
                if len(instance.user.post_set.all()) == achievement.required_amount:
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
    sender = models.ForeignKey(User, related_name='group_sender')
    receiver = models.ForeignKey(User, related_name='group_receiver')
    sent_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)