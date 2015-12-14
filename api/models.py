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
def create_group(sender, instance=None, created=False, **kwargs):
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
    if created:
        goal = instance.title
        goal = goal.split()
        same_goals = []
        for word in goal:
            for objects in Goal.objects.filter(title__icontains=word,
                                               theme=instance.theme):
                if word not in common_words:
                    if word in objects.title:
                        if objects.id != instance.id:
                            same_goals.append(objects)
        if len(same_goals) > 0:
            goal_count = Counter(same_goals)
            goal_count = goal_count.most_common()
            for closest_goal in goal_count:
                goals = closest_goal[0]
                if goals.user != instance.user:
                    if goals.theme == instance.theme:
                        groups = goals.user.group_set.filter(theme=instance.theme)[0]
                        if not groups.full:
                            instance.user.group_set.add(groups)
                            pass
        else:
            instance.user.group_set.create(theme=instance.theme)
