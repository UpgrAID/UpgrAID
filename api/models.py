from collections import Counter
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from post.models import Goal
from rest_framework.authtoken.models import Token
from user.models import Group


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(pre_save, sender=Goal)
def create_group(sender, instance=None, **kwargs):
    common_words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have',
                    'I', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you',
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
    if instance:
        goal = instance.title
        goal = [word for word in goal.split() if word not in common_words]
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
                        new_group = instance.user.group_set.create(theme=instance.theme)
                        instance.group = new_group

        else:
            new_group = instance.user.group_set.create(theme=instance.theme)
            instance.group = new_group
