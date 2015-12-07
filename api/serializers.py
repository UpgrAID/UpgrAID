from django.contrib.auth.models import User
from post.models import Post, Goal, Comment
from rest_framework import serializers
from user.models import Theme, Achievement, Rank, Group


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'goal_set')

    def create(self, validated_data):

        user = User.objects.create_user(email=validated_data['email'],
                                        username=validated_data['username'],
                                        password=validated_data['password'],
                                        first_name=validated_data['first_name'])
        return user


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title', 'description', 'user', 'goal', 'comment_set')


class GoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = ('title', 'user')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('post', 'description', 'user')


class ThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Theme
        fields = ('title', 'group_set')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('theme', 'user_limit', 'user')


class RankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rank
        fields = ('title', 'exp_required')


class AchievementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Achievement
        fields = ('name', 'description', 'point', 'badge_amount', 'user')