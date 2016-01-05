from django.contrib import admin
from user.models import Theme, Group, Rank, Achievement, Friendship, Profile, \
    Earned, BadgeGift


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'theme', 'user_limit', 'full')


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'exp_required')


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'point', 'badge_amount',
                    'date_create')


@admin.register(Earned)
class EarnedAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'achievement')


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'to_friend', 'from_friend')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'last_active')


@admin.register(BadgeGift)
class BadgeGiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver')