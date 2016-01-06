from django.contrib.auth.models import User
from post.models import Goal, Comment, Post, UserMessage, GroupMessage, \
    CommentLike
from rest_framework import serializers


class ShortGoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = ('id', 'title', 'theme', 'completed', 'group')


class ShortCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ('id', 'description', 'user', 'commentlike_set')


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
        read_only_fields = ('group')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'post', 'description', 'user', 'commentlike_set')
        read_only_fields = ('user', 'commentlike_set')


class PostSerializer(serializers.ModelSerializer):
    comment_set = ShortCommentSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'comment_set', 'group', 'user',
                  'created_at')


class UserMessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = UserMessage
        fields = ('id', 'sender', 'receiver', 'message', 'sent_at')


class GroupMessageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = GroupMessage
        fields = ('id', 'user', 'group', 'message', 'sent_at')


class CommentLikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = CommentLike
        fields = ('id', 'comment', 'user')
