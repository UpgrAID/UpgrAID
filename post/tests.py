import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from post.models import Goal, Post, Comment, GroupMessage, UserMessage, \
    CommentLike
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from user.models import Theme, Rank, Achievement


class PostTests(APITestCase):

    def setUp(self):
        self.rank = Rank.objects.create(title='Novice 5', exp_required=15)
        self.user = User.objects.create_user('test', email='test@test.com',
                                            password='testpassword')
        self.user2 = User.objects.create_user('test2', email='test2@test.com',
                                            password='test2password')
        self.theme = Theme.objects.create(title='Test Theme')
        self.goal = Goal.objects.create(title='test goal', user=self.user, theme=self.theme)
        self.post = Post.objects.create(title='test post',
                                        description='test description',
                                        user=self.user, group=self.goal.group)
        self.comment = Comment.objects.create(post=self.post,
                                              description='test comment',
                                              user=self.user)

    def test_goal_list(self):
        url = reverse('api_goal_list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url_username = reverse('api_goal_list') + "?username={}".format(self.user.username)
        response = self.client.get(url_username, {}, format='json')
        self.assertEqual(response.data[0]['user'], self.user.id)
        url_completed_false = reverse('api_goal_list') + "?completed=false"
        response = self.client.get(url_completed_false, {}, format='json')
        self.assertEqual(response.data[0]["completed"], False)
        completed_goal = Goal.objects.create(title='test goal', user=self.user,
                                             theme=self.theme, completed=True,
                                             group=self.goal.group)
        url_completed_true = reverse('api_goal_list') + "?completed=true"
        response = self.client.get(url_completed_true, {}, format='json')
        self.assertEqual(response.data[0]["completed"], True)

    def test_goal_create(self):
        url = reverse('api_goal_list')
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(url, {"title": "test goal 2", "theme": self.theme.pk},
                                    format='json')
        self.client.force_authenticate(user=self.user)
        response2 = self.client.post(url, {"title": "I want to dance",
                                           "theme": self.theme.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Goal.objects.count(), 3)
        goal = Goal.objects.get(title=response.data['title'])
        goal2 = Goal.objects.get(title=response2.data['title'])
        self.assertEqual(goal.user, self.user2)
        self.assertNotEqual(goal.group, goal2.group)
        self.assertEqual(goal.group,self.goal.group)
        self.assertEqual(len(goal.similar_goal_list()), 5)
        self.assertEqual((len(goal.closest_goal(goal.similar_goal_list()))), 2)
        self.assertEqual(goal.closest_goal(goal.similar_goal_list())[1][0], self.goal)
        self.user.profile.last_active = datetime.date.today() - datetime.timedelta(days=22)
        self.user.profile.activity()
        self.user.profile.save()
        self.assertEqual(goal2.inactive, True)

    def test_post_list(self):
        url = reverse('api_post_list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url_username = reverse('api_goal_list') + "?username={}".format(self.user.username)
        response = self.client.get(url_username, {}, format='json')
        self.assertEqual(response.data[0]['user'], self.user.id)
        url_user = reverse('api_goal_list') + "?user={}".format(self.user.id)
        response = self.client.get(url_user, {}, format='json')
        self.assertEqual(response.data[0]['user'], self.user.id)
        url_group = reverse('api_goal_list') + "?group={}".format(self.goal.group)
        response = self.client.get(url_group, {}, format='json')
        self.assertEqual(response.data[0]['group'], self.goal.group.id)

    def test_post_create(self):
        post_achievement = Achievement.objects.create(name='test achievement',
                                                      type='Post',
                                                      required_amount=1)
        url = reverse('api_post_list')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {"title": "test post 2",
                                         "description": "test description 2",
                                         "group": self.goal.group.pk},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        post = Post.objects.get(title='test post 2',
                                description='test description 2')
        self.assertEqual(post.user.achievement_set.count(), 1)
        self.assertEqual(post.user.achievement_set.all()[0], post_achievement)

    def test_comment_list(self):
        url = reverse('api_comment_list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_create(self):
        url = reverse('api_comment_list')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {"post": self.post.pk,
                                         "description": "test comment 2"},
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        comment = Comment.objects.get(description="test comment 2", post=self.post)
        self.assertEqual(comment.user, self.user)

    def test_user_message_list(self):
        url = reverse('api_user_message_list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url_username = reverse('api_goal_list') + "?username={}".format(self.user.username)
        response = self.client.get(url_username, {}, format='json')
        self.assertEqual(response.data[0]['user'], self.user.id)

    def test_user_message_create(self):
        url = reverse('api_user_message_list')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {"receiver": self.user2.pk,
                                          "message": "test user message"},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserMessage.objects.count(), 1)
        u_message = UserMessage.objects.all()[0]
        self.assertEqual(u_message.sender, self.user)

    def test_comment_like_list(self):
        url = reverse('api_comment_likes_list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_like_create(self):
        url = reverse('api_comment_likes_list')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {"comment": self.comment.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CommentLike.objects.count(), 1)
        comment_like = CommentLike.objects.all()[0]
        self.assertEqual(comment_like.user, self.user)
