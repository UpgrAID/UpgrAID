from post.models import Goal, Comment, Post, UserMessage, GroupMessage
from rest_framework import serializers
from user.serializers import ShortUserSerializer, ShortCommentSerializer


class GoalSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = ('id', 'title', 'user', 'theme', 'created_at', 'group',
                  'completed')


class CommentSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'description', 'user')


class PostSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer(read_only=True)
    comment_set = ShortCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'user', 'comment_set', 'group')


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