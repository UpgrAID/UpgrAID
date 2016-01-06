from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from post.models import Goal, Post, Comment
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from user.models import Theme, Rank


class PostTests(APITestCase):

    def setUp(self):
        self.rank = Rank.objects.create(title='Novice 5', exp_required=15)
        self.user = User.objects.create_user('test', email='test@test.com',
                                            password='testpassword')
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

    def test_goal_create(self):
        url = reverse('api_goal_list')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, {"title": "test goal", "theme": 1},
                                   format='json')
        response2 = self.client.post(url, {"title": "I want to dance",
                                           "theme": 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Goal.objects.count(), 3)
        self.assertEqual(self.user.id, response.data['user'])
        self.assertNotEqual(response.data['group'], response2.data['group'])
        self.assertEqual(response.data['group'], self.goal.group)
        goal = Goal.objects.get(pk=response.data['id'])
        self.assertEqual(len(goal.similar_goal_list()), 2)
        self.assertEqual((goal.closest_goal(goal.similar_goal_list())), self.goal)


    # def test_post_list(self):
    #     url = reverse('api_post_list_create')
    #     response = self.client.get(url, {}, format='json')
    #
    # def test_comment_list(self):
    #     url = reverse('api_comment_list_create')
    #     response = self.client.get(url, {}, format='json')
    #
    # def test_group_message_list(self):
    #     url = reverse('api_group_message_list_create')
    #     response = self.client.get(url, {}, format='json')
    #
    # def test_user_message_list(self):
    #     url = reverse('api_user_message_list_create')
    #     response = self.client.get(url, {}, format='json')
    #
    # def test_comment_like_list(self):
    #     url = reverse('api_comment_like_list_create')
    #     response = self.client.get(url, {}, format='json')