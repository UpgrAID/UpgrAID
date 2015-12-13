from django.contrib.auth.models import User
from post.models import Post, Goal, Comment
from rest_framework import serializers
from user.models import Theme, Achievement, Rank, Group, Profile, Friendship


class GoalSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Goal
        fields = ('id', 'title', 'user', 'theme', 'created_at')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'theme', 'user_limit', 'user')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ('id', 'post', 'description', 'user')


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'user', 'goal', 'comment_set')


class UserFriendSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name')


class UserSerializer(serializers.ModelSerializer):
    goal_set = GoalSerializer(many=True, read_only=True)
    post_set = PostSerializer(many=True, read_only=True)
    comment_set = CommentSerializer(many=True, read_only=True)
    group_set = GroupSerializer(many=True, read_only=True)


    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name',
                  'goal_set', 'post_set', 'comment_set', 'group_set',
                  'friend_set', 'to_friend_set')
        read_only_fields = ('friend_set', 'to_friend_set')

    def create(self, validated_data):

        user = User.objects.create_user(email=validated_data['email'],
                                        username=validated_data['username'],
                                        password=validated_data['password'],
                                        first_name=validated_data['first_name'])
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'last_active')
        read_only_fields = ('last_active',)



class ThemeSerializer(serializers.ModelSerializer):
    group_set = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = Theme
        fields = ('id', 'title', 'group_set')


class RankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rank
        fields = ('id', 'title', 'exp_required')


class AchievementSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Achievement
        fields = ('id', 'name', 'description', 'point', 'badge_amount', 'user')


class FriendshipSerializer(serializers.ModelSerializer):
    friend_set = UserFriendSerializer(many=True, read_only=True)
    to_friend_set = UserFriendSerializer(many=True, read_only=True)

    class Meta:
        model = Friendship
        fields = ('id', 'from_friend', 'to_friend')
