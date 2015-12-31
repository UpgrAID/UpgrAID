from post.models import Post, Goal, Comment, UserMessage, GroupMessage, \
    CommentLike
from post.permissions import IsOwnerOrReadOnly
from post.serializers import PostSerializer, GoalSerializer, CommentSerializer, \
    UserMessageSerializer, GroupMessageSerializer, CommentLikeSerializer
from rest_framework import generics, permissions
from user.models import Group


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
        completed = self.request.query_params.get('completed', None)
        if completed == 'true':
            qs = qs.filter(completed=completed)
        elif completed == 'false':
            qs = qs.filter(completed=False)
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
        group = Group.objects.get(pk=serializer.initial_data['group'])
        if not group.channel:
            group.channel = channel
            group.event = event
            group.save()
        serializer.save(user=user)

    def get_queryset(self):
        qs = super().get_queryset()
        group = self.request.query_params.get('group', None)
        if group:
            qs = qs.filter(group__id=group)
        return qs


class DetailUpdateDestroyGroupMessage(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupMessage.objects.all()
    serializer_class = GroupMessageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


class ListCreateCommentLike(generics.ListCreateAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
