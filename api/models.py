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


# @receiver(post_save, sender=Goal)
# def create_group(sender, instance=None, created=False, **kwargs):
#     if created:
#         goal = instance.title
#         goal = goal.split()
#         same_goals = []
#         for word in goal:
#             for objects in Goal.objects.filter(title__icontains=word,
#                                                theme=instance.theme):
#                 if 'not' not in objects.title:
#                     same_goals.append(object)
#         if same_goals.count() > 0:
#             goal_count = Counter(same_goals)
#             closest_goal = goal_count.most_common(1)[0][0]
#             Group.objects.create(theme=instance.theme, user=instance.user)
#         else:
#             Group.objects.create()
