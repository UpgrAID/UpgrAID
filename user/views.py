from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, permissions
from user.models import Theme, Group, Rank, Achievement, Profile, Friendship, \
    Earned, BadgeGift
from user.permissions import IsFromFriendOrReadOnly, IsToFriendOrReadOnly
from user.serializers import UserSerializer, ThemeSerializer, GroupSerializer, \
    RankSerializer, AchievementSerializer, ProfileSerializer, \
    FriendshipSerializer, EarnedSerializer, BadgeGiftSerializer


class ListCreateUsers(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


class DetailUsers(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListTheme(generics.ListAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer


class DetailTheme(generics.RetrieveAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer


class ListGroup(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        goal = self.request.query_params.get('goal', None)
        if goal:
            qs = qs.filter(goal__id=goal)
        username = self.request.query_params.get('username', None)
        if username:
            qs = qs.filter(user__username=username)
        return qs


class DetailGroup(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def perform_create(self, serializer):
        serializer.save()


class ListRank(generics.ListAPIView):
    queryset = Rank.objects.all()
    serializer_class = RankSerializer


class DetailRank(generics.RetrieveAPIView):
    queryset = Rank.objects.all()
    serializer_class = RankSerializer


class ListAchievement(generics.ListAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer


class DetailAchievement(generics.RetrieveAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer


class ListProfile(generics.ListAPIView):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.request.query_params.get('username', None)
        if username:
            qs = qs.filter(user__username=username)
        user = self.request.query_params.get('user', None)
        if user:
            qs = qs.filter(user=user)
        return qs


class DetailUpdateProfile(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ListCreateFriendship(generics.ListCreateAPIView):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.request.query_params.get('username', None)
        if username:
            qs = qs.filter(Q(from_friend__username=username) |
                           Q(to_friend__username=username))
        return qs


class DetailUpdateDestroyFriendship(generics.RetrieveUpdateDestroyAPIView):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsFromFriendOrReadOnly, IsToFriendOrReadOnly)


class ListEarned(generics.ListAPIView):
    queryset = Earned.objects.all()
    serializer_class = EarnedSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.request.query_params.get('username', None)
        if username:
            qs = qs.filter(user__username=username)
        return qs


class DetailEarned(generics.RetrieveAPIView):
    queryset = Earned.objects.all()
    serializer_class = EarnedSerializer


class ListCreateBadgeGift(generics.ListCreateAPIView):
    queryset = BadgeGift.objects.all()
    serializer_class = BadgeGiftSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(sender=user)

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.request.query_params.get('username', None)
        if username:
            qs = qs.filter(sender__username=username)
        return qs


class DetailBadgeGift(generics.RetrieveAPIView):
    queryset = BadgeGift.objects.all()
    serializer_class = BadgeGiftSerializer