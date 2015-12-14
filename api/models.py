from collections import Counter
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from post.models import Goal
from rest_framework.authtoken.models import Token
from user.models import Group


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Goal)
def create_group(sender, instance=None, created=False, **kwargs):
    if created:
        goal = instance.title
        goal = goal.split()
        same_goals = []
        for word in goal:
            for objects in Goal.objects.filter(title__icontains=word,
                                               theme=instance.theme):
                if 'not' not in objects.title and objects.id != instance.id:
                    same_goals.append(objects)
        if len(same_goals) > 0:
            goal_count = Counter(same_goals)
            goal_count = goal_count.most_common()
            for closest_goal in goal_count:
                goals = closest_goal[0]
                if closest_goal.theme == instance.theme:
                    groups = goals.user.group_set.filter(theme=instance.theme)[0]
                    if not groups.full:
                        instance.user.group_set.add(groups)
                        pass
        else:
            instance.user.group_set.create(theme=instance.theme)
