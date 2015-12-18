from django.contrib.auth.models import User
from post.models import Post, Goal, Comment, UserMessage, GroupMessage
from rest_framework import serializers
from user.models import Theme, Achievement, Rank, Group, Profile, Friendship, \
    Earned


class ShortUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name')


class ShortGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'theme')


class ShortGoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = ('id', 'title', 'completed')


class ShortCommentSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'description', 'user')


class ShortPostSerializer(serializers.ModelSerializer):
    comment_set = ShortCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'comment_set', 'group')


class UserFriendSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name')


class FriendsAddedSerializer(serializers.ModelSerializer):
    to_friend = UserFriendSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ('id', 'to_friend')


class FriendsAddedMeSerializer(serializers.ModelSerializer):
    from_friend = UserFriendSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ('id', 'from_friend')


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


class GroupSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer(many=True, read_only=True)
    post_set = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'theme', 'user_limit', 'user', 'goal_set', 'post_set')


class FriendshipSerializer(serializers.ModelSerializer):
    from_friend = serializers.ReadOnlyField(source='from_friend.username')
    to_friend = serializers.ReadOnlyField(source='to_friend.username')

    class Meta:
        model = Friendship
        fields = ('id', 'from_friend', 'to_friend', 'accepted')


class UserSerializer(serializers.ModelSerializer):
    goal_set = ShortGoalSerializer(many=True, read_only=True)
    post_set = ShortPostSerializer(many=True, read_only=True)
    group_set = ShortGroupSerializer(many=True, read_only=True)
    friend_set = FriendsAddedSerializer(many=True, read_only=True)
    to_friend_set = FriendsAddedMeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name',
                  'goal_set', 'post_set', 'comment_set', 'group_set',
                  'friend_set', 'to_friend_set')
        read_only_fields = ('friend_set', 'to_friend_set', 'comment_set')

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
        fields = ('id', 'user', 'rank', 'exp', 'last_active')
        read_only_fields = ('last_active', 'exp', 'rank')


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
        fields = ('id', 'name', 'type', 'point', 'badge_amount', 'user')


class EarnedSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    achievement = AchievementSerializer()

    class Meta:
        model = Earned
        fields = ('id', 'user', 'achievement')


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