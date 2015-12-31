from post.models import Goal, Comment, Post, UserMessage, GroupMessage, \
    CommentLike
from rest_framework import serializers


class ShortGoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = ('id', 'title', 'theme', 'completed')


class ShortCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'description')


class ShortPostSerializer(serializers.ModelSerializer):
    comment_set = ShortCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'comment_set', 'group')


class GoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = ('id', 'title', 'theme', 'created_at', 'group',
                  'completed')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'post', 'description')


class PostSerializer(serializers.ModelSerializer):
    comment_set = ShortCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'comment_set', 'group')


class UserMessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    receiver = serializers.ReadOnlyField(source='reciever.username')

    class Meta:
        model = UserMessage
        fields = ('id', 'sender', 'receiver', 'message', 'sent_at')


class GroupMessageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = GroupMessage
        fields = ('id', 'user', 'group', 'message', 'sent_at')


class CommentLikeSerializer(serializers.ModelSerializer):
    comment = ShortCommentSerializer()

    class Meta:
        model = CommentLike
        fields = ('id', 'comment')