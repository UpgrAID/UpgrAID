from collections import Counter
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from post.models import Goal, Post, GroupMessage
from rest_framework.authtoken.models import Token
from upgraid.settings import PUSHER_ID, PUSHER_KEY, PUSHER_SECRET
from user.models import Group, Achievement, Earned, Friendship
from pusher import Pusher


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


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
        goal = [word for word in instance.title.split() if word.lower() not in common_words]
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
                        break
                    else:
                        new_group = instance.user.group_set.create(
                            theme=instance.theme)
                        instance.group = new_group
                        break
        else:
            new_group = instance.user.group_set.create(theme=instance.theme)
            instance.group = new_group
    else:
        if instance.completed:
            instance.remove_group()
            completed_count = len(instance.user.goal_set.filter(completed=True))
            achievements = Achievement.objects.filter(type='Goal')
            if len(achievements) > 0:
                for achievement in achievements:
                    if achievement.required_amount == completed_count:
                        Earned.objects.create(user=instance.user,
                                              achievement=achievement)


@receiver(post_save, sender=Post)
def post_achievements(sender, instance=None, created=False, **kwargs):
    if created:
        achievements = Achievement.objects.filter(type='Post')
        if len(achievements) > 0:
            for achievement in achievements:
                if len(instance.user.post_set.all()) == achievement.required_amount:
                    Earned.objects.create(user=instance.user, achievement=achievement)


@receiver(post_save, sender=Earned)
def earned_achievements(sender, instance=None, created=False, **kwargs):
    if created:
        achievements = Achievement.objects.filter(type='Earned')
        if len(achievements) > 0:
            for achievement in achievements:
                if len(instance.user.achievement_set.all()) == achievement.required_amount:
                    Earned.objects.create(user=instance.user, achievement=achievement)


@receiver(post_save, sender=Earned)
def rank(sender, instance=None, created=False, **kwargs):
    if created:
        instance.user.profile.exp = instance.user.profile.exp + instance.achievement.point
        instance.user.profile.rank_check()
        instance.user.profile.save()


@receiver(post_save, sender=Friendship)
def friend_request(sender, instance=None, **kwargs):
    if instance:
        instance.denied_friend_request()


@receiver(pre_save, sender=GroupMessage)
def pusher_info(sender, instance=None, **kwargs):
    pusher = Pusher(app_id=PUSHER_ID, key=PUSHER_KEY, secret=PUSHER_SECRET,
                    ssl=True)
    if instance.group.channel:
        pusher.trigger(instance.group.channel, instance.event, {'message': instance.message})
    else:
        pusher.trigger(instance.group.channel, instance.group.event, {'message': instance.message})