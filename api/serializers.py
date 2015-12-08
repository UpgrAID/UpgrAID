from django.contrib.auth.models import User
from post.models import Post, Goal, Comment
from rest_framework import serializers
from user.models import Theme, Achievement, Rank, Group


class UserSerializer(serializers.ModelSerializer):
    goal_set = serializers.HyperlinkedRelatedField(many=True,
                                                    queryset=Goal.objects.all(),
                                                    view_name='api_goal_detail_update')

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
    user = serializers.ReadOnlyField(source='user.id')
    comment_set = serializers.HyperlinkedRelatedField(many=True,
                                                    queryset=Comment.objects.all(),
                                                    view_name='api_comment_detail_update')

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'user', 'goal', 'comment_set')


class GoalSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Goal
        fields = ('id', 'title', 'user')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ('id', 'post', 'description',)


class ThemeSerializer(serializers.ModelSerializer):
    group_set = serializers.HyperlinkedRelatedField(many=True,
                                                    queryset=Group.objects.all(),
                                                    view_name='api_group_detail_update')

    class Meta:
        model = Theme
        fields = ('id', 'title', 'group_set')


class GroupSerializer(serializers.ModelSerializer):
    user_set = serializers.HyperlinkedRelatedField(many=True,
                                                    queryset=User.objects.all(),
                                                    view_name='api_user_detail_update')

    class Meta:
        model = Group
        fields = ('id', 'theme', 'user_limit', 'user_set')


class RankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rank
        fields = ('id', 'title', 'exp_required')


class AchievementSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Achievement
        fields = ('id', 'name', 'description', 'point', 'badge_amount', 'user')