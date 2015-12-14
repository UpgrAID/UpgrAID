from api.permissions import IsOwnerOrReadOnly
from api.serializers import UserSerializer, PostSerializer, GoalSerializer, \
    CommentSerializer, ThemeSerializer, GroupSerializer, RankSerializer, \
    AchievementSerializer, ProfileSerializer, FriendshipSerializer
from django.contrib.auth.models import User
from post.models import Post, Goal, Comment
from rest_framework import generics, permissions
from user.models import Theme, Group, Rank, Achievement, Profile, Friendship


class ListCreateUsers(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


class DetailUsers(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListCreatePost(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.request.query_params.get('username', None)
        if username:
            qs = qs.filter(user__username=username)
        user = self.request.query_params.get('user', None)
        if user:
            qs = qs.filter(user__id=user)
        group = self.request.query_params.get('group', None)
        if group:
            qs = qs.filter(group__id=group)
        return qs


class DetailUpdatePost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


class ListCreateGoal(generics.ListCreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.request.query_params.get('username', None)
        if username:
            qs = qs.filter(user__username=username)
        return qs


class DetailUpdateGoal(generics.RetrieveUpdateDestroyAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


class ListCreateComment(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.request.query_params.get('username', None)
        if username:
            qs = qs.filter(user__username=username)
        return qs


class DetailUpdateComment(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


class ListTheme(generics.ListAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer


class DetailTheme(generics.RetrieveAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer


class ListGroup(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        goal = self.request.query_params.get('goal', None)
        if goal:
            qs = qs.filter(goal__id=goal)
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
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.request.query_params.get('username', None)
        if username:
            qs = qs.filter(user__username=username)
        return qs


class DetailProfile(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ListCreateFriendship(generics.ListCreateAPIView):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.request.query_params.get('username', None)
        if username:
            qs = qs.filter(to_friend__username=username)
        return qs


class DetailDestroyFriendship(generics.RetrieveDestroyAPIView):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
