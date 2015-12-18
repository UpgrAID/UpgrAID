from api.permissions import IsOwnerOrReadOnly
from api.serializers import UserSerializer, PostSerializer, GoalSerializer, \
    CommentSerializer, ThemeSerializer, GroupSerializer, RankSerializer, \
    AchievementSerializer, ProfileSerializer, FriendshipSerializer, \
    EarnedSerializer, GroupMessageSerializer, UserMessageSerializer
from django.contrib.auth.models import User
from post.models import Post, Goal, Comment, UserMessage, GroupMessage
from rest_framework import generics, permissions
from user.models import Theme, Group, Rank, Achievement, Profile, Friendship, \
    Earned



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
            qs = qs.filter(from_friend__username=username)
        return qs


class DetailUpdateDestroyFriendship(generics.RetrieveUpdateDestroyAPIView):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer


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


class ListCreateUserMessage(generics.ListCreateAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer
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


class DetailUpdateDestroyUserMessage(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


class ListCreateGroupMessage(generics.ListCreateAPIView):
    queryset = GroupMessage.objects.all()
    serializer_class = GroupMessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        user = self.request.user
        channel = serializer.initial_data['channel']
        event = serializer.initial_data['event']
        group = serializer.initial_data['group']
        if not group.channel:
            group.channel = channel
            group.event = event
            group.save()
        serializer.save(user=user)

    def get_queryset(self):
        qs = super().get_queryset()
        username = self.request.query_params.get('username', None)
        if username:
            qs = qs.filter(user__username=username)
        return qs


class DetailUpdateDestroyGroupMessage(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupMessage.objects.all()
    serializer_class = GroupMessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)